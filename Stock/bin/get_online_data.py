#coding:utf-8

import sys,os,re,datetime
sys.path.append("..\\")

from optparse import OptionParser
from lib.common_tool import replace_vars, print_log, get_date
from lib.Sina_stock import Sina_stock
from lib.Yahoo_stock import Yahoo_stock

#-- sys var
FILE_PATH = os.getcwd()
FILE_BASE_NAME = __file__
FILE_NAME = FILE_PATH + "\\" + FILE_BASE_NAME
today = get_date("today")
yesterday = get_date("yesterday")
mode = ""
start_date = ""
end_date = ""

#-- opts
parser = OptionParser()
parser.add_option("--stock_code", "-c", dest="stock_code", action="store", type="string", help="Stock code, e.g. 601006")
parser.add_option("--start_date", "-s", dest="start_date", action="store", type="string", default=yesterday, help="Start date of the date range, e.g. 20150101, ignored if --all_hist|-a assigned")
parser.add_option("--end_date", "-e", dest="end_date", action="store", type="string", default=yesterday, help="End date of the date range, e.g. 20150101, ignored if --all_hist|-a assigned")
parser.add_option("--all_hist", "-a", dest="all_hist", action="store_true", default=False, help="All the historical data, ignoring start_date/end_date argments")
parser.add_option("--real_time", "-r", dest="real_time", action="store_true", default=False, help="Realtime data, ignoring start_date/end_date/all_hist argments")
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

def new_stock_object(mode, stock_code, start_date, end_date):
	return eval(stock_object[mode]["object_class"] + "(" + stock_code + ",'" + start_date + "','" + end_date + "')" )
			
#-- iterate vars for none check
[exit_for_none_var(var) for var in vars_for_none_check]

#-- verify param
if not re.match("^\d{6}$", options.stock_code):
	print_log("stock code error! [" + options.stock_code + "]")
	exit_process()

if mode == "normal": 
	if not (re.match("^\d{8}$", start_date) and re.match("^\d{8}$", end_date)):
		print_log("start_date or end_date error! [" + start_date + "][" + end_date + "]")
		exit_process()
	elif start_date > end_date:
		print_log("start_date must be smaller than end_date! [" + start_date + "][" + end_date + "]")
		exit_process()

obj = new_stock_object(mode, options.stock_code, start_date, end_date)

stock_objs = obj.get_stock_object()
for code in stock_objs:
	for date in stock_objs[code]:
		print code, date, stock_objs[code][date].open_price, stock_objs[code][date].high_price, stock_objs[code][date].low_price




