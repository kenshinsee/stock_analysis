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
from pprint import pprint

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
STOCK_YML = YML_DIR + SEP + "table" + SEP + "dw.stock.yml"
now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

#-- opts
parser = OptionParser()
parser.add_option("--object_class", "-o", dest="object_class", action="store", default='tengxun', help="Stock object class overwrites the hardcoded objects, sina|tengxun")
parser.add_option("--mode", "-m", dest="mode", action="store", default='download', help="download|load|downloadAndLoad")
parser.add_option("--file", "-f", dest="file", action="store", help="If mode is load, --file|-f is required")
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

def download_to_file(stocks, stock_obj_name, fh, log_fh, warn_fh):
	#-- iterate stocks, download eod data from webside
	for s in stocks:
		#-- call method of stock object to get content of url
		print_log('%(object)s("%(stock)s", "dummy", "dummy")' % {'object': stock_obj_name, 'stock': s})
		try:
			obj = eval('%(object)s("%(stock)s", "dummy", "dummy")' % {'object': stock_obj_name, 'stock': s})
			for k,v in obj.get_stock_content().items():
				print_log('Writing %(code)s ...' % {'code': k}, log_fh )
				fh.write(v + '\n')
				if re.match(r'pv_none_match', v) or re.match(r'.+"";$', v): # match empty from tengxun and sina
					warn_log('No content fetched for ' + k, warn_fh)
		except KeyError:
			warn_log(s[0:2] + ' is not setup in ' + stock_obj_name, warn_fh)
			continue

#-- parse input parameter, var assignment
stock_object = {
	"tengxun": 'Tengxun_stock',
	"sina": 'Sina_stock',
}

if not options.object_class in stock_object:
	exit_error('%(entered_object)s is not a valid object, it could be %(valid_objects)s' % {'entered_object': options.object_class, 'valid_objects': '|' . join(stock_object)})
else:
	print_log(options.object_class + ' selected.')

if not (options.mode == 'download' or options.mode == 'load' or options.mode == 'downloadAndLoad'):
	exit_error(mode + ' is not recognized, it could be download|load|downloadAndLoad.')
elif options.mode == 'load' and options.file is None:
	exit_error('--file|-f is required when in load mode.')
elif options.mode == 'load' and not options.file is None and not os.path.exists(options.file):
	exit_error(options.file + ' doesn\'t exist.')
	
	
#-- data file name
file_name = options.object_class + '_' + recent_working_day + '.txt'
file_full_name = return_new_name_for_existing_file(data_dir + SEP + file_name)
file_name = os.path.basename(file_full_name)
if options.mode == 'load':
	file_full_name = options.file
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
	#-- stock list
	stocks = get_stock_list(conn)
	#-- open file
	fh = open(file_full_name, 'a')
	download_to_file(stocks, stock_object[options.object_class], fh, log_fh, warn_fh)
	fh.close()

#-- load stock info into database
if options.mode == 'load' or options.mode == 'downloadAndLoad':
	# python download_stock_eod.py -m load -f D:\\workspace\\Stock\\data\\stock_daily\\tengxun_20160304.txt
	db_field_mapping = get_yaml(STOCK_YML)
	tab_name = os.path.basename(STOCK_YML).replace('.yml', '') # yml file name as table name
	tab_fields = [] # table field names
	tab_types = [] # table field types
	obj_attrs = [] # attribute names in stock object
	for k,v in db_field_mapping.items():
		tab_type = v['type']
		obj_attr = v['stock_object'][stock_object[options.object_class]]
		if obj_attr != None: # If None|Null is set for fields in yml, remove the fields from insertion
			tab_fields.append(k)
			tab_types.append(tab_type)
			obj_attrs.append(obj_attr)
	
	print_log('Start to load data into {tab_name}...'.format(tab_name=tab_name), log_fh)
	ins_sql = 'insert into {tab_name}({fields}) '.format(tab_name=tab_name, fields=','.join(tab_fields))

	with open(file_full_name) as f:
		for row in f.readlines():
			# get_stock_object_from_str is a function should be available in all the stock objects
			# this function accepts the string returned from website and generate a dict for stock object
			# the dict is like {stock: {date: object}}
			stock_dict = eval('{object}.get_stock_object_from_str(row)'.format(object=stock_object[options.object_class], row=row))
			for stock in stock_dict: # for Tengxun or sina interface, there is just one stock in one stock dict
				for date in stock_dict[stock]: # for Tengxun or sina interface, there is just one date in one stock dict
					stock_obj = stock_dict[stock][date] # this object is stock implementation object
					value_sql = reduce(lambda x, y: ( x if re.match(r'stock_obj', x) else 'stock_obj.' + x + ', ' ) + "stock_obj.{attr_name}, ".format(attr_name=y), obj_attrs)
					value_sql = value_sql[0:-2] # remove the last comma and the blankspace next to it
					value_sql = eval(value_sql) # tupe returned
					final_value_sql = ''
					for i, v in enumerate(value_sql):
						final_value_sql = final_value_sql + ( "'" + v + "', " if tab_types[i] == 'date' or tab_types[i] == 'varchar' else 'Null, ' if len(str(v)) == 0 else str(v) + ', ' ) # date and varchar quoted by single quote, otherwise no quote or null(if length of value is 0)
					final_value_sql = final_value_sql[0:-2]
					ins_complete_sql = ins_sql + ' values( ' + final_value_sql + ')'
					print ins_complete_sql
					cur = get_cur(conn)
					cur.execute(ins_complete_sql)
					conn.commit()
					sys.exit()
conn.close()

#-- complete
print_log('log file: ' + log_file, log_fh)
print_log('warn file: ' + warn_file, log_fh)
print_log('error file: ' + error_file, log_fh)

log_fh.close()
warn_fh.close()
error_fh.close()

#-- parsing log file


