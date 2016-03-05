#!/usr/local/bin/python2.7
#coding:utf-8

import sys,os,re,datetime

from optparse import OptionParser
from common_tool import replace_vars, print_log, error_log, get_date
from Sina_stock import Sina_stock
from Tengxun_stock import Tengxun_stock

#-- sys var
FILE_PATH = os.getcwd()
FILE_BASE_NAME = __file__
FILE_NAME = FILE_PATH + "/" + FILE_BASE_NAME
today = get_date("today")
yesterday = get_date("yesterday")
mode = ""
start_date = ""
end_date = ""

#-- opts
parser = OptionParser()
parser.add_option("--start_date", "-s", dest="start_date", action="store", type="string", help="Start date of the date range, e.g. 20150101, applicable in hist mode only")
parser.add_option("--end_date", "-e", dest="end_date", action="store", type="string", help="End date of the date range, e.g. 20150101, applicable in hist mode only")
parser.add_option("--mode", "-m", dest="mode", action="store", default='eod', help="eod|hist")
parser.add_option("--object_class", "-o", dest="object_class", action="store", help="Stock object class overwrites the hardcoded objects, Sina_stock|Tengxun_stock|Yahoo_stock")
(options, args) = parser.parse_args()

#-- var assignment
if options.mode == 'hist':
	if options.start_date is None:
		start_date = "19000101"
	else:
		start_date = options.start_date
		
	if options.end_date is None:
		end_date = "99991231"
	else:
		end_date = options.end_date
elif options.mode == 'eod':
	start_date = today
	end_date = today
	
stock_object = {
	#"real_time": {"object_class": "Sina_stock"},
	"eod": {"object_class": "Tengxun_stock"},
	"hist": {"object_class": "Yahoo_stock"},
}
	
#-- function
def exit_process():
	os.system("python " + FILE_NAME + " -h")
	sys.exit()
	
def exit_error(msg):
	error_log(msg)
	sys.exit()

def exit_for_none_var(var):
	if eval("options." + var) is None:
		print_log(var + " must be assigned!")
		exit_process()

def new_stock_object(mode, stock_code, start_date, end_date):
	object_class = ''
	if options.object_class is None:
		object_class = stock_object[mode]["object_class"]
	else:
		object_class = options.object_class
		
	print_log('Creating stock object from '+ object_class)
	try:
		print_log(object_class + "('" + stock_code + "','" + start_date + "','" + end_date + "')" )
		return eval(object_class + "('" + stock_code + "','" + start_date + "','" + end_date + "')" )
	except:
		exit_error(object_class + ' is not valid.')
		
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
		print code, date, stock_objs[code][date].open_price, stock_objs[code][date].top_price, stock_objs[code][date].floor_price, stock_objs[code][date].date, stock_objs[code][date].volume#, stock_objs[code][date].circulation_market_value, stock_objs[code][date].total_market_value



