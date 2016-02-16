#!/usr/local/bin/python2.7
#coding:utf-8

import sys,os,re,datetime,csv

from optparse import OptionParser
from common_tool import replace_vars, print_log, warn_log, error_log, get_date, get_yaml
from psql import get_conn, get_cur
from loader.load_into_bankuai import load_into_bankuai
from loader.load_into_stock import load_into_stock
from loader.load_into_stock_bankuai import load_into_stock_bankuai

#-- sys var
SEP = os.path.sep
FILE_PATH = os.getcwd()
FILE_BASE_NAME = __file__
FILE_NAME = FILE_PATH + SEP + FILE_BASE_NAME
PROJ_BASE_DIR = FILE_PATH + SEP + ".."
YML_DIR = PROJ_BASE_DIR + SEP + "etc"
DATA_DIR = PROJ_BASE_DIR + SEP + "data"
LOG_DIR = PROJ_BASE_DIR + SEP + "log"
DB_YML = YML_DIR + SEP + "db.yml"

file_to_recon = ""
csv_dict = {}
dbsql_dict = {}

file_db_recon = {
	"bankuai": {
		"file": DATA_DIR + SEP + "bankuai_$DATE.csv", 
		"recon_fields_in_file": [u'子版块', u'板块名称'],
		"sql": '''
SELECT PB.NAME AS PB_NAME, B.NAME AS BK_NAME
FROM DW.DIM_BANKUAI B 
INNER JOIN DW.DIM_PARENT_BANKUAI PB ON B.PARENT_BANKUAI_ID = PB.ID
WHERE B.IS_VALID = 'Y' 
		''',
		"recon_fields_in_db": ["pb_name", "bk_name"]
	},
	"stock_bankuai": {
		"file": DATA_DIR + SEP + "bankuai_stock_$DATE.csv", 
		"recon_fields_in_file": [u'子版块', u'板块名称', u'股票代码'],
		"sql": '''
SELECT PB.NAME AS PB_NAME, B.NAME AS BK_NAME, S.ID AS STOCK_ID
FROM DW.DIM_STOCK S
INNER JOIN DW.DIM_STOCK_BANKUAI SB ON S.ID = SB.STOCK_ID
INNER JOIN DW.DIM_BANKUAI B ON SB.BANKUAI_ID = B.ID
INNER JOIN DW.DIM_PARENT_BANKUAI PB ON B.PARENT_BANKUAI_ID = PB.ID
WHERE S.IS_VALID = 'Y'
AND SB.IS_VALID = 'Y'
AND B.IS_VALID = 'Y'
		''',
		"recon_fields_in_db": ["pb_name", "bk_name", "stock_id"]
	}
}


#-- opts
parser = OptionParser()
parser.add_option("--type", "-t", dest="type", action="store", type="string", help="bankuai|stock_bankuai")
parser.add_option("--in_file", "-f", dest="in_file", action="store", type="string", help="To recon a specific file")
(options, args) = parser.parse_args()


#-- function
def exit_process():
	os.system("python " + FILE_NAME + " -h")
	sys.exit()
	

#-- verify param
if options.type is None:
	error_log("--type|-t must be specified!")
	exit_process()
elif not options.type in file_db_recon:
	error_log("type is not correct! [" + options.type + "]")
	exit_process()

#-- determine the file name for reconcilation
max_date = ""
if options.in_file is None:
	# to fetch the latest file for reconcilation 
	for root, dirs, files in os.walk(DATA_DIR):
		for f in files:
			matcher = re.compile(r'' + os.path.basename(file_db_recon[options.type]["file"]).replace("$DATE", "(?P<date>\d{8})") + '')
			for m in matcher.finditer(f):
				if m.group("date") > max_date:
					max_date = m.group("date")
	file_to_recon = file_db_recon[options.type]["file"].replace("$DATE", max_date)
else:
	if not os.path.isfile(options.in_file):
		error_log("file can't be found! [" + options.in_file + "]")
		exit_process()
	else:
		file_to_recon = options.in_file
		
#-- fetch DB info
db_dict = get_yaml(DB_YML)

#-- open db connection
conn = get_conn(db_dict["DB"], db_dict["Username"], db_dict["Password"], db_dict["Host"], db_dict["Port"])

#-- building dict for csv and db
csvf = open(file_to_recon)
csvr = csv.DictReader(csvf)

if options.type == "bankuai":
	# csv
	print_log("Start to read csv...")
	for row in csvr:
		pb_name = row[u'子版块'.encode("gbk")].decode("gbk")
		bk_name = row[u'板块名称'.encode("gbk")].decode("gbk")
		csv_dict[pb_name + "-" + bk_name] = ""
	print_log("dict for csv done.")
	
	# db
	print_log("Start to read db...")
	select_sql = file_db_recon[options.type]["sql"]
	cur = get_cur(conn)
	cur.execute(select_sql)
	db_rows = list(cur)
	for db_row in db_rows:
		db_pb_name = db_row["pb_name"].decode("utf-8")
		db_bk_name = db_row["bk_name"].decode("utf-8")
		dbsql_dict[db_pb_name + "-" + db_bk_name] = ""
	print_log("dict for db done.")
	
elif options.type == "stock_bankuai":
	# csv
	print_log("Start to read csv...")
	for row in csvr:
		pb_name = row[u'子版块'.encode("gbk")].decode("gbk")
		bk_name = row[u'板块名称'.encode("gbk")].decode("gbk")
		st_id = row[u'股票代码'.encode("gbk")].decode("gbk")
		csv_dict[pb_name + "-" + bk_name + "-" + st_id] = ""
	print_log("dict for csv done.")
	
	# db
	print_log("Start to read db...")
	select_sql = file_db_recon[options.type]["sql"]
	cur = get_cur(conn)
	cur.execute(select_sql)
	db_rows = list(cur)
	for db_row in db_rows:
		db_pb_name = db_row["pb_name"].decode("utf-8")
		db_bk_name = db_row["bk_name"].decode("utf-8")
		db_st_id = db_row["stock_id"].decode("utf-8")
		dbsql_dict[db_pb_name + "-" + db_bk_name + "-" + db_st_id ] = ""
	print_log("dict for db done.")


csvf.close()
conn.close()





#------------------------------------------- RECONing
copy_csv_dict = csv_dict.copy()
for csv_key in copy_csv_dict:
	if csv_key in dbsql_dict:
		del csv_dict[csv_key]
		del dbsql_dict[csv_key]
	
if len(csv_dict.keys()) > 0:
	error_log("There are %(num)s records missing from db" % {"num": len(csv_dict.keys())})
	error_log("-".join(file_db_recon[options.type]["recon_fields_in_file"]))
	for key in csv_dict.keys():
		error_log(key)
else:
	print_log("csv data is all in db")

	
if len(dbsql_dict.keys()) > 0:
	error_log("There are %(num)s records missing from csv" % {"num": len(dbsql_dict.keys())})
	error_log("-".join(file_db_recon[options.type]["recon_fields_in_db"]))
	for key in dbsql_dict.keys():
		error_log(key)
else:
	print_log("db data is all in csv")
	
	
	