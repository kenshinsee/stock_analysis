#!/usr/local/bin/python2.7
#coding:utf-8

import sys,os,re,datetime,yaml,csv

from optparse import OptionParser
from common_tool import replace_vars, print_log, get_date
from psql import get_conn, get_cur

#-- sys var
SEP = os.path.sep
FILE_PATH = os.getcwd()
FILE_BASE_NAME = __file__
FILE_NAME = FILE_PATH + SEP + FILE_BASE_NAME
YML_DIR = FILE_PATH + SEP + ".." + SEP + "etc"
DB_YML = YML_DIR + SEP + "db.yml"

today = get_date("today")
yesterday = get_date("yesterday")
type = ""
start_date = ""
end_date = ""
in_file = ""

#-- opts
parser = OptionParser()
parser.add_option("--type", "-t", dest="type", action="store", type="string", help="Bankuai|Stock_Bankuai")
parser.add_option("--start_date", "-s", dest="start_date", action="store", type="string", default=yesterday, help="Start date of the date range, e.g. 20150101")
parser.add_option("--end_date", "-e", dest="end_date", action="store", type="string", default=yesterday, help="End date of the date range, e.g. 20150101")
parser.add_option("--in_file", "-f", dest="in_file", action="store", type="string", help="Load a specific file, $DATE would be replaced from --start_date and --end_date")
(options, args) = parser.parse_args()

#-- var assignment
vars_for_none_check = ["type"]
start_date = options.start_date
end_date = options.end_date

#-- function
def exit_process():
	os.system("python " + FILE_NAME + " -h")
	sys.exit()
	
def exit_for_none_var(var):
	if eval("options." + var) is None:
		print_log(var + " must be assigned!")
		exit_process()
	
#-- iterate vars for none check
[exit_for_none_var(var) for var in vars_for_none_check]

#-- Load DB info
dbf = open(DB_YML)
db_dict = yaml.load(dbf)
dbf.close()


conn = get_conn(db_dict["DB"], db_dict["Username"], db_dict["Password"], db_dict["Host"], db_dict["Port"])
cur = get_cur(conn)
cur.execute("SELECT * FROM DW.DIM_PARENT_BANKUAI")
result = cur.fetchall()
print result[0]["name"].decode("utf-8")
cur.close()
conn.close()

# -- bankuai table
# create table dw.dim_bankuai(
#   id serial primary key,
#   name varchar(16) not null,
#   parent_bankuai_id integer not null,
#   upd_time timestamp,
#   is_valid varchar(1) --Y/N
# );



