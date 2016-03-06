#!/usr/local/bin/python2.7
#coding:utf-8
# This script is used to download the eod data to flat file

import sys,os,re,datetime

from optparse import OptionParser
from common_tool import replace_vars, print_log, error_log, warn_log, get_date, recent_working_day, get_yaml, return_new_name_for_existing_file
from Sys_paths import Sys_paths
from Sina_stock import Sina_stock
from Tengxun_stock import Tengxun_stock
from psql import get_conn, get_cur

#-- sys var
SEP = os.path.sep
FILE_PATH = sys.path[0]
FILE_BASE_NAME = __file__
FILE_NAME = FILE_PATH + SEP + FILE_BASE_NAME
recent_working_day = recent_working_day()
data_dir = Sys_paths.DATA_STOCK_DAILY
YML_DIR = Sys_paths.YML_DIR
LOG_DIR = Sys_paths.LOG_DIR
DB_YML = YML_DIR + SEP + "db.yml"
now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

#-- opts
parser = OptionParser()
parser.add_option("--object_class", "-o", dest="object_class", action="store", default='tengxun', help="Stock object class overwrites the hardcoded objects, Sina_stock|Tengxun_stock|Yahoo_stock")
(options, args) = parser.parse_args()

#-- function
def exit_process():
	os.system("python " + FILE_NAME + " -h")
	sys.exit()
	
def exit_error(msg):
	error_log(msg)
	sys.exit()

#-- creating folder
if not os.path.exists(data_dir):
	os.makedirs(data_dir)
	print_log(data_dir + ' created.')

#-- data file name
file_name = options.object_class + '_' + recent_working_day + '.txt'
file_full_name = return_new_name_for_existing_file(data_dir + SEP + file_name)
file_name = os.path.basename(file_full_name)

#-- open log files
log_file = LOG_DIR + SEP + file_name.replace('.txt', '.' + str(now) + '.log')
warn_file = LOG_DIR + SEP + file_name.replace('.txt', '.' + str(now) + '.warn')
error_file = LOG_DIR + SEP + file_name.replace('.txt', '.' + str(now) + '.err')

log_fh = open(log_file, 'a')
warn_fh = open(warn_file, 'a')
error_fh = open(error_file, 'a')

#-- var assignment
stock_object = {
	"tengxun": "Tengxun_stock",
	"sina": "Sina_stock",
}

if not options.object_class in stock_object:
	exit_error('%(entered_object)s is not a valid object, it could be %(valid_objects)s' % {'entered_object': options.object_class, 'valid_objects': '|' . join(stock_object)})
else:
	print_log(options.object_class + ' selected.', log_fh)

print_log('data directory is ' + data_dir, log_fh)
print_log('data file is ' + file_full_name, log_fh)

#-- fetch DB info
db_dict = get_yaml(DB_YML)
#-- open db connection
conn = get_conn(db_dict["DB"], db_dict["Username"], db_dict["Password"], db_dict["Host"], db_dict["Port"])

#-- stock list
stocks = []
sel_query = 'select id from dw.dim_stock where id<>\'000000\''
cur = get_cur(conn)
cur.execute(sel_query)
rows = list(cur)
for row in rows:
	stocks.append(row['id'])
conn.close()

#-- open file
fh = open(file_full_name, 'a')

#-- iterate stocks, download eod data from webside
for s in stocks:
	#-- call static method of stock object to get content of url
	print_log('%(object)s("%(stock)s", "dummy", "dummy")' % {'object': stock_object[options.object_class], 'stock': s})
	try:
		obj = eval('%(object)s("%(stock)s", "dummy", "dummy")' % {'object': stock_object[options.object_class], 'stock': s})
		for k,v in obj.get_stock_content().items():
			print_log('Writing %(code)s ...' % {'code': k} )
			fh.write(v + '\n')
			if re.match(r'pv_none_match', v) or re.match(r'.+"";$', v): # match empty from tengxun and sina
				warn_log('No content fetched for ' + k, warn_fh)
	except KeyError:
		warn_log(s[0:2] + ' is not setup in ' + stock_object[options.object_class], warn_fh)
		continue

#-- write file completed
fh.close()
log_fh.close()
warn_fh.close()
error_fh.close()


print_log('log file: ' + log_file)
print_log('warn file: ' + warn_file)
print_log('error file: ' + error_file)



