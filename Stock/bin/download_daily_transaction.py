#!/usr/local/bin/python2.7
#coding:utf-8
# This script is used to download the eod data to flat file and load data from flat file to db

import sys,os,re,datetime

from optparse import OptionParser
from urllib2 import HTTPError
from common_tool import replace_vars, print_log, error_log, warn_log, get_date, recent_working_day, get_yaml, return_new_name_for_existing_file
from Sys_paths import Sys_paths
from psql import get_conn, get_cur
from db_func import insert_into_table

from Xueqiu_stock import Xueqiu_stock
from Netease_stock import Netease_stock

#-- sys var
SEP = os.path.sep
FILE_PATH = sys.path[0]
FILE_BASE_NAME = __file__
FILE_NAME = FILE_PATH + SEP + FILE_BASE_NAME
recent_working_day = recent_working_day()
data_dir = Sys_paths.DATA_STOCK_TRANSACTION
YML_DIR = Sys_paths.YML_DIR
LOG_DIR = Sys_paths.LOG_DIR
DB_YML = YML_DIR + SEP + "db.yml"
STOCK_YML = YML_DIR + SEP + "table" + SEP + "dw.stock_transaction.yml"
now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

stock_object = {
    'xueqiu': 'Xueqiu_stock',
    'netease': 'Netease_stock',
}

#-- opts
parser = OptionParser()
parser.add_option("--object_class", "-o", dest="object_class", action="store", default='xueqiu', help="Stock object class overwrites the hardcoded objects, " + '|'.join(stock_object.keys()))
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

def get_stock_list(conn):
    # get stock list from db
    stocks = []
    sel_query = "select id from dw.dim_stock where id <> '000000'"
    cur = get_cur(conn)
    cur.execute(sel_query)
    rows = list(cur)
    for row in rows:
        stocks.append(row['id'])
    return stocks


def download_to_file(stocks, stock_obj_name, start_date, end_date, to_file, log_fh, warn_fh):
    #-- iterate stocks, download transaction data from webside
    fh = open(to_file, 'a')
    num = 0
    cur_date_dt = datetime.datetime.strptime(start_date,'%Y%m%d')
    end_date_dt = datetime.datetime.strptime(end_date,'%Y%m%d')
    for s in stocks:
        while cur_date_dt <= end_date_dt:
            cur_date = cur_date_dt.strftime("%Y%m%d")
            #-- call method of stock object to get content of url
            try:
                new_class = '%(object)s("%(stock)s", "%(date)s")' % {'object': stock_obj_name, 'stock': s, 'date':cur_date }
                print_log(new_class)
                obj = eval(new_class)
                if stock_obj_name == 'Netease_stock': # download xls file to local as the 1st step for netease
                    if os.path.exists(obj.download_file) and os.path.getsize(obj.download_file) > 1024*100: 
                        # if file exists and file size is greater than 100k, it's a valid file and no need to download again.
                        print_log(obj.download_file + ' is already downloaded, no need to download it again.')
                    else:
                        obj.download_to_local()
                    
                content = obj.get_stock_content()[s][cur_date]
                if stock_obj_name == 'Netease_stock': # encode data to gb2312 for netease, same coding as xueqiu
                    content = content.encode('gb2312')
                print_log('Writing %(code)s on %(date)s...' % {'code': s, 'date': cur_date}, log_fh )
                if content == u'暂无数据'.encode('gb2312'): 
                    warn_log('No content fetched for ' + new_class, warn_fh)
                else: 
                    fh.write(content + '\n')
                    num += 1
                cur_date_dt = cur_date_dt + datetime.timedelta(1)
            except KeyError:
                warn_log(s[0:2] + ' is not setup in ' + stock_obj_name, warn_fh)
                continue
            except HTTPError: # log and skip for stocks couldn't be returned from stock interface
                warn_log('Get content failed when ' + new_class, warn_fh)
                continue
    fh.close()
    print_log('{num} stocks have been written into {file}.'.format(num=num, file=to_file), log_fh)
    


#-- parse input parameter, var assignment
# check validation of object class
if not options.object_class in stock_object:
    exit_error('%(entered_object)s is not a valid object, it could be %(valid_objects)s' % {'entered_object': options.object_class, 'valid_objects': '|' . join(stock_object)})
else:
    print_log(options.object_class + ' selected.')

# check validation of mode and input file
if not (options.mode == 'download' or options.mode == 'load' or options.mode == 'downloadAndLoad'):
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
    
#-- data file name

if options.mode == 'load':
    file_full_name = options.file
    file_name = os.path.basename(file_full_name)
else:
    file_name = '{object_class}_{start_date}_{end_date}_{stock_id}.txt'.format(object_class = options.object_class, start_date = options.start_date, end_date = options.end_date, stock_id = 'all' if options.stock_id is None else options.stock_id)

    file_full_name = return_new_name_for_existing_file(data_dir + SEP + file_name)
    file_name = os.path.basename(file_full_name)

#-- open log files
log_file = LOG_DIR + SEP + file_name.replace('.txt', '.' + str(now) + '.log')
warn_file = LOG_DIR + SEP + file_name.replace('.txt', '.' + str(now) + '.warn')
error_file = LOG_DIR + SEP + file_name.replace('.txt', '.' + str(now) + '.err')

log_fh = open(log_file, 'a')
warn_fh = open(warn_file, 'a')
error_fh = open(error_file, 'a')

print_log('data file is ' + file_full_name, log_fh)

#-- fetch DB info
db_dict = get_yaml(DB_YML)
#-- open db connection
conn = get_conn(db_dict["DB"], db_dict["Username"], db_dict["Password"], db_dict["Host"], db_dict["Port"])

#-- download stock info from internet
if options.mode == 'download' or options.mode == 'downloadAndLoad':
    #-- stock list fetch from dw.dim_stock
    stocks = get_stock_list(conn)
    if ( not options.stock_id is None ) and options.stock_id in stocks:
        stocks = [options.stock_id]
    elif ( not options.stock_id is None ) and ( not options.stock_id in stocks ):
        exit_error('Invalid stock id ' + options.stock_id)
    
    download_to_file(stocks, stock_object[options.object_class], options.start_date, options.end_date, file_full_name, log_fh, warn_fh)
    
#-- load stock info into database
if options.mode == 'load' or options.mode == 'downloadAndLoad':
    insert_into_table(STOCK_YML, stock_object[options.object_class], file_full_name, conn, log_fh, warn_fh)


#-- close connection
conn.close()

#-- complete
print_log('log file: ' + log_file, log_fh)
print_log('warn file: ' + warn_file, log_fh)
print_log('error file: ' + error_file, log_fh)

log_fh.close()
warn_fh.close()
error_fh.close()

#-- parsing log file


