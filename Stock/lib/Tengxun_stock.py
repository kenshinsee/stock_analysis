#coding:utf-8
#------------------------------------
#-- tengxun stock api - real time
#------------------------------------
#sh: http://qt.gtimg.cn/q=sh600110
#sz: http://qt.gtimg.cn/q=sz000858
#

import urllib2,re,sys
from object.Tengxun_stock_object import Tengxun_stock_object

class Tengxun_stock:
	__url_prefix = "http://qt.gtimg.cn/q="
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
			try: 
				obj = Tengxun_stock_object(code, re.findall('\"(.+)\"', self.get_stock_content()[code])[0].split("~"))
			except:
				raise RuntimeError("Unknow stock. [" + code + "]") 
			out_object[code][obj.datetime[0:8]] = obj
		return out_object

if __name__ == "__main__":
	s = Tengxun_stock("600110")
	#print s.get_stock_content()
	
	objs = s.get_stock_object()
	for code in objs:
		for date in objs[code]:
			print code, date, objs[code][date].datetime, objs[code][date].high_price, objs[code][date].low_price, objs[code][date].high_limit, objs[code][date].low_limit
			
			
			