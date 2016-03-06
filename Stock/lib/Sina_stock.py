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
		"51": "sh",
		"15": "sz",
		"20": "sz",
		"90": "sh",
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

	@staticmethod
	def get_stock_object_from_str(str):
	# This method reads a str to create a stock object
	# This method is for backload trades from a pre-stored file which contains stock info with the same format as calling from url
# var hq_str_sz300374="恒通科技,18.760,18.800,19.200,20.650,17.500,19.200,19.220,2724272,51598032.370,34200,19.200,2100,19.190,200,19.180,5300,19.150,1300,19.100,600,19.220,18700,19.230,2200,19.250,1200,19.290,3100,19.300,2016-03-04,15:05:56,00";

		out_object = {}
		r_code = re.search(r'(?P<code>\d+)', str.split('=')[0])
		code = r_code.group('code')
		out_object[code] = {}
		#try: 
		obj = Sina_stock_object(code, re.findall('\"(.+)\"', str)[0].split(","))
		#except:
		#	raise RuntimeError("Unknow stock. [" + code + "]") 
		out_object[code][obj.date] = obj
		return out_object
	
		
		
if __name__ == "__main__":
	#s = sina_stock("002708,002547")
	#s = Sina_stock("600101")
	#s = Sina_stock(600101,'20160305','20160305')
	#print s.get_stock_content()['600101']
    #
	#
	#objs = s.get_stock_object()
	#for code in objs:
	#	for date in objs[code]:
	#		print code, date, objs[code][date].open_price, objs[code][date].current_price, objs[code][date].date, objs[code][date].time
	
	obj = Sina_stock.get_stock_object_from_str('var hq_str_sz300374="恒通科技,18.760,18.800,19.200,20.650,17.500,19.200,19.220,2724272,51598032.370,34200,19.200,2100,19.190,200,19.180,5300,19.150,1300,19.100,600,19.220,18700,19.230,2200,19.250,1200,19.290,3100,19.300,2016-03-04,15:05:56,00";')
	
	for code in obj:
		for date in obj[code]:
			print code, date, obj[code][date].date, obj[code][date].top_price, obj[code][date].floor_price#, obj[code][date].high_limit, obj[code][date].low_limit
	