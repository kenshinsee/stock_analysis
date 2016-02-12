#!/usr/local/bin/python2.7
#coding:utf-8

import sys,os,re,datetime

from optparse import OptionParser
from common_tool import replace_vars, print_log, get_date


#-- sys var
FILE_PATH = os.getcwd()
FILE_BASE_NAME = __file__
FILE_NAME = FILE_PATH + "/" + FILE_BASE_NAME
today = get_date("today")
yesterday = get_date("yesterday")
start_date = ""
end_date = ""

#-- opts
parser = OptionParser()
parser.add_option("--start_date", "-s", dest="start_date", action="store", type="string", default=yesterday, help="Start date of the date range, e.g. 20150101, ignored if --all_hist|-a assigned")
parser.add_option("--end_date", "-e", dest="end_date", action="store", type="string", default=yesterday, help="End date of the date range, e.g. 20150101, ignored if --all_hist|-a assigned")
(options, args) = parser.parse_args()

#-- var assignment
vars_for_none_check = ["stock_code"]
if options.real_time:
	mode = "real_time"
	start_date = today
	end_date = today
elif options.all_hist:
	mode = "all_hist"
	start_date = "19000101"
	end_date = "99991231"
else:
	mode = "normal"
	start_date = options.start_date
	end_date = options.end_date
	
stock_object = {
	"real_time": {"object_class": "Sina_stock"},
	"all_hist": {"object_class": "Yahoo_stock"},
	"normal": {"object_class": "Yahoo_stock"},
}
	
#-- function
def exit_process():
	os.system("python " + FILE_NAME + " -h")
	sys.exit()
	
def exit_for_none_var(var):
	if eval("options." + var) is None:
		print_log(var + " must be assigned!")
		exit_process()

		
