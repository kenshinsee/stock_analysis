#coding:utf-8
#------------------------------------
#-- yahoo stock api 
#------------------------------------
#-- historical
#http://table.finance.yahoo.com/table.csv?s=600629.SS&a=8&b=1&c=2015&d=8&e=9&f=2015&g=d
#http://table.finance.yahoo.com/table.csv?s=600629.SS&a=8&b=1&c=2015&d=9&e=9&f=2015&g=w
#http://table.finance.yahoo.com/table.csv?s=600629.SS&a=8&b=1&c=2015&d=9&e=9&f=2015&g=m
#http://table.finance.yahoo.com/table.csv?s=600629.ss
#http://table.finance.yahoo.com/table.csv?s=600629.SS&a=8&b=1&c=2015&d=8&e=9&f=2015&g=d&ignore=.csv
#
#-- real time
#http://finance.yahoo.com/d/quotes.csv?s=300193.sz&f=l1c1va2xj1b4j4dyekjm3m4rr5p5p6s7
#

import urllib2,re,sys,datetime
from object.Yahoo_stock_object import Yahoo_stock_object
from common_tool import replace_vars
import StringIO

class Yahoo_stock:
	__url_prefix = "http://table.finance.yahoo.com/table.csv?s="
	__code_symbol = "%(code)s.%(code_loc)s"
	__date_range = "&a={sm}&b={sd}&c={sy}&d={em}&e={ed}&f={ey}&g=d&ignore=.csv"
	__code_loc_dict = {
		"60": "ss", 
		"00": "sz", 
		"30": "sz", 
	}

	def __init__(self, code, start_date="19000101", end_date="99991231"):
		self.__code = str(code)
		
		self.__start_dt = start_date
		self.__start_dt_dt = datetime.datetime.strptime(self.__start_dt,'%Y%m%d')
		self.__start_dt_iso = self.__start_dt_dt.strftime("%Y-%m-%d")
		self.__end_dt = end_date
		self.__end_dt_dt = datetime.datetime.strptime(self.__end_dt,'%Y%m%d')
		self.__end_dt_iso = self.__end_dt_dt.strftime("%Y-%m-%d")

		self.__day_slice = {
			"{sy}": str(self.__start_dt_dt.year),
			"{sm}": str(self.__start_dt_dt.month - 1),
			"{sd}": str(self.__start_dt_dt.day),
			"{ey}": str(self.__end_dt_dt.year),
			"{em}": str(self.__end_dt_dt.month - 1),
			"{ed}": str(self.__end_dt_dt.day),
		}
		
	def get_url(self):
			return self.__url_prefix + self.__code_symbol % {"code": self.__code, "code_loc": self.__code_loc_dict[self.__code[0:2]]} + replace_vars(self.__date_range, self.__day_slice)

	def get_stock_content(self):
		return urllib2.urlopen(self.get_url()).read().strip()
		
	def get_stock_object(self):
		# one row for one day
		out_object = {self.__code: {}}
		buf = StringIO.StringIO(self.get_stock_content())
		try: 
			buf.readline() # remove header
			for row in buf.readlines():
				out_object[self.__code][row.strip().split(",")[0]] = Yahoo_stock_object(self.__code, row.strip().split(","))
		except: 
			#info=sys.exc_info()  
			#print info[0],":",info[1]
			raise RuntimeError("Unknow stock. [" + self.__code + "]") 
		finally:
			buf.close()
			
		return out_object

		
if __name__ == "__main__":
	s = Yahoo_stock("002547", "20151110", "20151121")
	objs = s.get_stock_object()
	for code in objs:
		for date in objs[code]:
			print code, date, objs[code][date].open_price
		
