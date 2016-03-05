#coding:utf-8
#------------------------------------
#-- sina stock api - real time
#------------------------------------
#sh: http://hq.sinajs.cn/list=sh601006
#sz: http://hq.sinajs.cn/list=sz300374
#

import urllib2,re,sys
from object.Sina_stock_object import Sina_stock_object

class Sina_stock:
	__url_prefix = "http://hq.sinajs.cn/list="
	__code_symbol = "%(code_loc)s%(code)s"
	__code_loc_dict = {
		"60": "sh", 
		"00": "sz", 
		"30": "sz", 
	}

	def __init__(self, codes, start_date="dummy", end_date="dummy"):
		self.__codes = str(codes)
		
	def get_url(self):
		if "," in self.__codes:
			out_url = {}
			for code in self.__codes.split(","):
				out_url[code] = self.__url_prefix + self.__code_symbol % {"code": code, "code_loc": self.__code_loc_dict[code[0:2]]}
			return out_url
		else:
			return { self.__codes: self.__url_prefix + self.__code_symbol % {"code": self.__codes, "code_loc": self.__code_loc_dict[self.__codes[0:2]]} }

	def get_stock_content(self):
		out_content = {}
		for code in self.get_url():
			out_content[code] = urllib2.urlopen(self.get_url()[code]).read().strip()#.decode('gbk').encode('gb2312')
		return out_content
		
	def get_stock_object(self):
		out_object = {}
		for code in self.get_stock_content():
			out_object[code] = {}
			#try: 
			obj = Sina_stock_object(code, re.findall('\"(.+)\"', self.get_stock_content()[code])[0].split(","))
			#except:
			#	raise RuntimeError("Unknow stock. [" + code + "]") 
			out_object[code][obj.date] = obj
		return out_object

if __name__ == "__main__":
	#s = sina_stock("002708,002547")
	#s = Sina_stock("600101")
	s = Sina_stock(600101,'20160305','20160305')
	print s.get_stock_content()['600101']

	
	objs = s.get_stock_object()
	for code in objs:
		for date in objs[code]:
			print code, date, objs[code][date].open_price, objs[code][date].current_price, objs[code][date].date, objs[code][date].time
