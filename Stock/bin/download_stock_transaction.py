#!/usr/bin/python2.7
#coding:utf-8
# This script is used to download transaction data to flat file and load data from flat file to db


import sys,os,re,datetime,time,platform,fnmatch,shutil

from optparse import OptionParser
from urllib2 import HTTPError
from Queue import Queue
from tooling.common_tool import replace_vars, print_log, error_log, warn_log, get_date, recent_working_day, get_yaml, return_new_name_for_existing_file
from Sys_paths import Sys_paths
from tooling.psql import get_conn, get_cur
from downloader.Stock_trans_downloader import Stock_trans_downloader
from loader.Stock_trans_loader import Stock_trans_loader
from tooling.db_func import inserter, get_query_result, psql_copy_from


#-- sys var
SEP = os.path.sep
FILE_PATH = sys.path[0]
FILE_BASE_NAME = __file__
FILE_NAME = FILE_PATH + SEP + FILE_BASE_NAME
data_dir = Sys_paths.DATA_STOCK_TRANSACTION
YML_DIR = Sys_paths.YML_DIR
LOG_DIR = Sys_paths.LOG_DIR
DB_YML = YML_DIR + SEP + "db.yml"
now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
QUEUE_DOWNLOAD_MAX_SIZE = 3
QUEUE_LOAD_MAX_SIZE = 2

#-- fetch DB info
db_dict = get_yaml(DB_YML)
DB_NAME = db_dict["DB"]
DB_HOST = db_dict["Host"]
DB_PORT = db_dict["Port"]
DB_UNAME = db_dict["Username"]
DB_PWD = db_dict["Password"]

#-- open db connection
conn = get_conn(db_dict["DB"], db_dict["Username"], db_dict["Password"], db_dict["Host"], db_dict["Port"])

recent_working_day = recent_working_day(is_skip_holiday=True, conn=conn)


#-- opts
parser = OptionParser()
parser.add_option("--mode", "-m", dest="mode", action="store", default='downloadAndLoad', help="download|load|downloadAndLoad")
parser.add_option("--start_date", "-s", dest="start_date", action="store", default=recent_working_day, help="The default value is " + recent_working_day + ", the format is YYYYMMDD")
parser.add_option("--end_date", "-e", dest="end_date", action="store", default=recent_working_day, help="The default value is " + recent_working_day + ", the format is YYYYMMDD")
parser.add_option("--stock_id", "-i", dest="stock_id", action="store", help="--stock_id|-i is optional")
parser.add_option("--obj_selection", "-o", dest="obj_selection", action="store", help="--obj_selection|-o can indicate which object interface you want to use, T:Tengxun, S:Sina, N:Netease, e.g. -o \"T|S\"")
parser.add_option("--merge_before_copy", "-g", dest="merge_before_copy", action="store_true", default=True, help="Merge all the files in the data directory into one file and load it into table")
#parser.add_option("--enable_copy", "-c", dest="enable_copy", action="store_true", default=True if platform.system() == 'Linux' else False, help="Enable postgres copy when loading data into table")
parser.add_option("--enable_copy", "-c", dest="enable_copy", action="store_true", default=True, help="Enable postgres copy when loading data into table")
(options, args) = parser.parse_args()

#-- function
def exit_error(msg):
    error_log(msg)
    raise RuntimeError(msg)

def get_stock_list(conn, biz_date, stock_id):
    # get stock list from db
    stocks = []
    if not stock_id is None:
        sel_query = '''
            select id from dw.dim_stock where id <> '000000' and is_valid = 'Y' and id = '{stock_id}'
            except 
            select stock_id from dw.log_stock_transaction where biz_date = '{biz_date}' and is_download_success = 'Y' and stock_id = '{stock_id}'
            '''.format(stock_id=stock_id, biz_date=biz_date)
    else:
        sel_query = '''
            select id from dw.dim_stock where id <> '000000' and is_valid = 'Y'
            except 
            select stock_id from dw.log_stock_transaction where biz_date = '{biz_date}' and is_download_success = 'Y' 
            '''.format(biz_date=biz_date)
    cur = get_cur(conn)
    cur.execute(sel_query)
    rows = list(cur)
    for row in rows:
        stocks.append(row['id'])
    return stocks

def downloader(queue, conn, start_date=options.start_date, end_date=options.end_date, stock_id=options.stock_id, obj_selection=options.obj_selection):
    #-- object list
    obj_mapping = {
        'T': 'Tengxun_stock_transaction',
        'N': 'Netease_stock_transaction',
        'S': 'Sina_stock_transaction',
    }
    if obj_selection is None:
        stock_objects = ['Tengxun_stock_transaction', 'Netease_stock_transaction', 'Sina_stock_transaction']
    else:
        stock_objects = [ obj_mapping[o] for o in obj_selection.split('|') if o in obj_mapping ]
    
    print_log('|'.join(stock_objects) + ' selected.')
    
    iter = len(stock_objects)
    
    cur_date_dt = datetime.datetime.strptime(start_date,'%Y%m%d')
    end_date_dt = datetime.datetime.strptime(end_date,'%Y%m%d')
    while cur_date_dt <= end_date_dt:  
        #-- stock list
        stocks = get_stock_list(conn, cur_date_dt, stock_id)
        for stock in stocks:
            cur_date_str = cur_date_dt.strftime('%Y%m%d')
            cur_stock_object = stock_objects[iter%len(stock_objects)] # choose stock object
            while queue.full():
                print_log('=================> queue is full, wait for 1 second...')
                time.sleep(1)
            s = Stock_trans_downloader(queue, conn, cur_stock_object, stock, cur_date_str)
            s.start()
            #s.join()
            print_log('-----> queue size: ' + str(queue.qsize()))
            iter += 1
        cur_date_dt = cur_date_dt + datetime.timedelta(1)
        
    while not queue.empty():
        print_log('=================> queue is not empty yet, wait for 1 second...')
        time.sleep(1)

        
def download_log_checker(conn, start_date=options.start_date, end_date=options.end_date, stock_id=options.stock_id):
    start_date_dt = datetime.datetime.strptime(start_date,'%Y%m%d')
    end_date_dt = datetime.datetime.strptime(end_date,'%Y%m%d')
    
    # get stock ids which is_download_success=N
    chk_sql = '''
    select t.biz_date, 
      t.stock_id
    from (
    select 
      biz_date, 
      stock_id, 
      is_download_success, 
      row_number() over(partition by biz_date, stock_id order by download_end_time desc nulls last) rankid
    from dw.log_stock_transaction
    where biz_date between '{start_date}' and '{end_date}' 
    ) t where t.rankid = 1
    and t.is_download_success = 'N' '''.format(start_date=start_date_dt, end_date=end_date_dt)
    if not stock_id is None: chk_sql = chk_sql + ' and t.stock_id = \'' + stock_id + '\''

    cur = get_cur(conn)
    cur.execute(chk_sql)
    rows = list(cur)
    if len(rows) == 0:
        print_log('All the stocks have been downloaded successfully.')
    else:
        for row in rows:
            error_log(str(row['biz_date']) + ':' + row['stock_id'] + ' failed to download.')
    return len(rows)


def load_log_checker(conn, start_date=options.start_date, end_date=options.end_date, stock_id=options.stock_id):
    start_date_dt = datetime.datetime.strptime(start_date,'%Y%m%d')
    end_date_dt = datetime.datetime.strptime(end_date,'%Y%m%d')

    chk_sql = '''
    select biz_date, stock_id
    from dw.log_stock_transaction
    where biz_date between '{start_date}' and '{end_date}'
    and is_download_success = 'Y'
    and (is_load_success = 'N' or is_load_success is null)
    '''.format(start_date=start_date_dt, end_date=end_date_dt)
    if not stock_id is None: chk_sql = chk_sql + ' and stock_id = \'' + stock_id + '\''

    cur = get_cur(conn)
    cur.execute(chk_sql)
    rows = list(cur)
    if len(rows) == 0:
        print_log('All the stocks have been loaded successfully.')
    else:
        for row in rows:
            error_log(str(row['biz_date']) + ':' + row['stock_id'] + ' failed to load.')
    return len(rows)

    
def loader(queue, conn, start_date=options.start_date, end_date=options.end_date, stock_id=options.stock_id, merge_before_copy=options.merge_before_copy, enable_copy=options.enable_copy):

    cur_date_dt = datetime.datetime.strptime(start_date,'%Y%m%d')
    end_date_dt = datetime.datetime.strptime(end_date,'%Y%m%d')
    
    stock_list_sql = '''
    select row_id, biz_date, stock_id
    from dw.log_stock_transaction
    where biz_date = '{biz_date}'
    and is_download_success = 'Y'
    and (is_load_success = 'N' or is_load_success is null)
    '''
    if not stock_id is None: stock_list_sql = stock_list_sql + ' and stock_id = \'' + stock_id + '\''
    
    cur = get_cur(conn)
    while cur_date_dt <= end_date_dt:  
        if merge_before_copy:
        # since load files one by one into table is taking too much time, the solution to boost the procedure is to merge all the pieces of files into one file and load the merge file into table, this takes less than 5 mins to complete.
            cur_date_str = cur_date_dt.strftime('%Y%m%d')
            working_dir = data_dir + SEP + cur_date_str
            file_merged = os.path.join(working_dir, "file_merged.csv")
            if os.path.exists(file_merged):
                warn_log('Removing old file: ' + file_merged)
                os.remove(file_merged)
            #-- Starting to merge files
            with open(file_merged, "a") as dest:
                i=0
                for _, _, filenames in os.walk(working_dir):
                    for filename in fnmatch.filter(filenames, "[0-9]*.txt"):
                        with open(os.path.join(working_dir, filename)) as src:
                            shutil.copyfileobj(src, dest)
                        i+=1
                        print_log('Merged ' + str(i) + ' files.')
            #-- Deleting records from db
            del_sql = '''delete from dw.stock_transaction where biz_date = '{}' '''.format(cur_date_str)
            get_query_result(conn, del_sql)
            conn.commit()
            print_log('Deletion for biz_date {} completed successfully.'.format(cur_date_str))
            #-- Updating is_load_success to N in log table
            upd_sql = '''update dw.log_stock_transaction set is_load_success = 'N' where biz_date = '{}' and is_download_success = 'Y' '''.format(cur_date_str)
            get_query_result(conn, upd_sql)
            conn.commit()
            print_log('is_load_success is updated to N')

            #++++++++ Starting to load the merged file into table
            psql_copy_from(DB_HOST, DB_NAME, DB_UNAME, 'dw.stock_transaction', file_merged, DB_PORT, args=' with (encoding \'GBK\')')
            print_log('Successfully loaded {} into table.'.format(file_merged))
            
            #-- Updating is_load_success to Y in log table
            upd_sql = '''update dw.log_stock_transaction set is_load_success = 'Y' where biz_date = '{}' and is_download_success = 'Y' '''.format(cur_date_str)
            get_query_result(conn, upd_sql)
            conn.commit()
            print_log('is_load_success is updated to Y')

            #-- Cleaning up working dir
            os.remove(file_merged)
            
            cur_date_dt = cur_date_dt + datetime.timedelta(1)
            
        else:
            stock_list_sql_var_replaced = stock_list_sql.format(biz_date=cur_date_dt)
            cur.execute(stock_list_sql_var_replaced)
            rows = list(cur)
            for row in rows:
                row_id = row['row_id']
                biz_date = str(row['biz_date']).replace('-','')
                stock_id = row['stock_id']
                while queue.full():
                    print_log('=================> queue is full, wait for 1 second...')
                    time.sleep(1)
                s = Stock_trans_loader(queue, conn, row_id, stock_id, biz_date, enable_copy=enable_copy )
                s.start()
                print_log('-----> queue size: ' + str(queue.qsize()))
                conn.commit()
                    
            cur_date_dt = cur_date_dt + datetime.timedelta(1)

    while not queue.empty():
        print_log('=================> queue is not empty yet, wait for 1 second...')
        time.sleep(1)
            
        
# check validation of mode
if not (options.mode in ['download', 'load', 'downloadAndLoad']):
    exit_error(mode + ' is not recognized, it could be download|load|downloadAndLoad.')
    
# check validation of start_date and end_date
if not (re.match("^\d{8}$", options.start_date) and re.match("^\d{8}$", options.end_date)):
    exit_error("Not valid start_date or end_date! [" + options.start_date + "][" + options.end_date + "]")
elif options.start_date > options.end_date:
    exit_error("Start date is greater then end date! [" + options.start_date + "][" + options.end_date + "]")

#-- create queue
queue = Queue(QUEUE_DOWNLOAD_MAX_SIZE)
#-- download stock info from internet
if options.mode == 'download' or options.mode == 'downloadAndLoad':
    #-- at most run 3 times, just in case some stocks failed to download
    for i in ['1st', '2nd', '3rd']:
        print_log('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        print_log('downloader running for the {n} time...' . format(n=i))
        print_log('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        downloader(queue, conn)
        error_num = download_log_checker(conn)
        if error_num == 0: break
        print_log('=================> waiting for 10 seconds to start the next round run...')
        time.sleep(10)
    #-- retry 3 times, still failed, raise runtime error
    if error_num > 0: exit_error('There are {num} stocks failed to download, please check.' . format(num=error_num))
    #queue.task_done()

#-- upsize queue size to speed up data loading 
queue = Queue(QUEUE_LOAD_MAX_SIZE)
#-- load stock info into database
if options.mode == 'load' or options.mode == 'downloadAndLoad':
    #-- at most run 3 times, just in case some stocks failed to download
    for i in ['1st', '2nd', '3rd']:
        print_log('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        print_log('loader running for the {n} time...' . format(n=i))
        print_log('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        loader(queue, conn)
        error_num = load_log_checker(conn)
        if error_num == 0: break
        print_log('=================> waiting for 10 seconds to start the next round run...')
        time.sleep(10)
    #-- retry 3 times, still failed, raise runtime error
    if error_num > 0: exit_error('There are {num} stocks failed to load, please check.' . format(num=error_num))
    #queue.task_done()

#-- close connection
conn.commit()
conn.close()


