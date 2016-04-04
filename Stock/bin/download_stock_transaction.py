#!/usr/local/bin/python2.7
#coding:utf-8
# This script is used to download transaction data to flat file and load data from flat file to db


import sys,os,re,datetime,time

from optparse import OptionParser
from urllib2 import HTTPError
from Queue import Queue
from tooling.common_tool import replace_vars, print_log, error_log, warn_log, get_date, recent_working_day, get_yaml, return_new_name_for_existing_file
from Sys_paths import Sys_paths
from tooling.psql import get_conn, get_cur
from tooling.db_func import insert_into_table
from downloader.Stock_trans_downloader import Stock_trans_downloader

#from object_impl.Tengxun_stock_transaction import Tengxun_stock_transaction
#from object_impl.Netease_stock_transaction import Netease_stock_transaction
#from object_impl.Sina_stock_transaction import Sina_stock_transaction

#-- sys var
SEP = os.path.sep
FILE_PATH = sys.path[0]
FILE_BASE_NAME = __file__
FILE_NAME = FILE_PATH + SEP + FILE_BASE_NAME
data_dir = Sys_paths.DATA_STOCK_TRANSACTION
YML_DIR = Sys_paths.YML_DIR
LOG_DIR = Sys_paths.LOG_DIR
DB_YML = YML_DIR + SEP + "db.yml"
STOCK_YML = YML_DIR + SEP + "table" + SEP + "dw.stock_transaction.yml"
now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
qsize = 3

#-- fetch DB info
db_dict = get_yaml(DB_YML)
#-- open db connection
conn = get_conn(db_dict["DB"], db_dict["Username"], db_dict["Password"], db_dict["Host"], db_dict["Port"])

recent_working_day = recent_working_day(is_skip_holiday=True, conn=conn)

#-- opts
parser = OptionParser()
parser.add_option("--mode", "-m", dest="mode", action="store", default='download', help="download|load|downloadAndLoad")
parser.add_option("--file", "-f", dest="file", action="store", help="--file|-f is required for load mode")
parser.add_option("--start_date", "-s", dest="start_date", action="store", default=recent_working_day, help="The default value is " + recent_working_day + ", the format is YYYYMMDD")
parser.add_option("--end_date", "-e", dest="end_date", action="store", default=recent_working_day, help="The default value is " + recent_working_day + ", the format is YYYYMMDD")
parser.add_option("--stock_id", "-i", dest="stock_id", action="store", help="--stock_id|-i is optional")
(options, args) = parser.parse_args()

#-- function
def exit_process():
    os.system("python " + FILE_NAME + " -h")
    sys.exit()
    
def exit_error(msg):
    error_log(msg)
    sys.exit()

def get_stock_list(conn,biz_date):
    # get stock list from db
    stocks = []
    sel_query = '''
        select id from dw.dim_stock where id <> '000000' and is_valid = 'Y'
        except 
        select stock_id from dw.log_stock_transaction where biz_date = '{biz_date}' and is_download_success = 'Y' '''.format(biz_date=biz_date)
    cur = get_cur(conn)
    cur.execute(sel_query)
    rows = list(cur)
    for row in rows:
        stocks.append(row['id'])
    return stocks


    
# check validation of mode and input file
if not (options.mode in ['download', 'load', 'downloadAndLoad']):
    exit_error(mode + ' is not recognized, it could be download|load|downloadAndLoad.')
elif options.mode == 'load' and options.file is None:
    exit_error('--file|-f is required when in load mode.')
elif options.mode == 'load' and not options.file is None and not os.path.exists(options.file):
    exit_error(options.file + ' doesn\'t exist.')
    
# check validation of start_date and end_date
if not (re.match("^\d{8}$", options.start_date) and re.match("^\d{8}$", options.end_date)):
    exit_error("Not valid start_date or end_date! [" + options.start_date + "][" + options.end_date + "]")
elif options.start_date > options.end_date:
    exit_error("Start date is greater then end date! [" + options.start_date + "][" + options.end_date + "]")


#-- download stock info from internet
if options.mode == 'download' or options.mode == 'downloadAndLoad':
    #-- create queue
    queue = Queue(qsize)
    
    #-- object list
    stock_objects = ['Tengxun_stock_transaction', 'Netease_stock_transaction', 'Sina_stock_transaction']
    iter = 3
    
    cur_date_dt = datetime.datetime.strptime(options.start_date,'%Y%m%d')
    end_date_dt = datetime.datetime.strptime(options.end_date,'%Y%m%d')
    while cur_date_dt <= end_date_dt:  
        #-- stock list
        if not options.stock_id is None:
            stocks = [options.stock_id]
        else:
            stocks = get_stock_list(conn, cur_date_dt)
        
        for stock in stocks:
            cur_date_str = cur_date_dt.strftime('%Y%m%d')
            cur_stock_object = stock_objects[iter%len(stock_objects)] # choose stock object
            #print stock, cur_date_str, cur_stock_object, iter

            while queue.full():
                print_log('-------> queue is full, wait for 1 second...')
                time.sleep(1)

            s = Stock_trans_downloader(queue, conn, cur_stock_object, stock, cur_date_str)
            s.start()
            s.join()
            iter += 1

        cur_date_dt = cur_date_dt + datetime.timedelta(1)

#-- load stock info into database
if options.mode == 'load' or options.mode == 'downloadAndLoad':
    pass


#-- close connection
conn.commit()
conn.close()


