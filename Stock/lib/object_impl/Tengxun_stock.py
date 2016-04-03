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
			try: 
				obj = Tengxun_stock_object(code, re.findall('\"(.+)\"', self.get_stock_content()[code])[0].split("~"))
			except:
				raise RuntimeError("Unknow stock. [" + code + "]") 
			out_object[code][obj.date] = obj
		return out_object
	
	@staticmethod
	def get_stock_object_from_str(str):
	# This method reads a str to create a stock object
	# This method is for backload trades from a pre-stored file which contains stock info with the same format as calling from url
#v_sz300244="51~迪安诊断~300244~49.64~49.79~49.55~48132~23854~24278~49.63~15~49.62~43~49.61~9~49.60~34~49.59~20~49.64~60~49.65~9~49.66~41~49.67~174~49.68~2~15:00:27/49.64/247/S/1226108/25462|14:56:57/49.64/5/S/24820/25252|14:56:54/49.64/2/S/9928/25246|14:56:45/49.67/35/B/173825/25232|14:56:39/49.67/12/B/59599/25220|14:56:36/49.67/4/B/19867/25214~20160303150133~-0.15~-0.30~52.00~48.80~49.64/47885/239706343~48132~24093~2.65~93.82~~52.00~48.80~6.43~90.07~150.74~15.26~54.77~44.81~";
		out_object = {}
		r_code = re.search(r'(?P<code>\d+)', str.split('=')[0])
		code = r_code.group('code')
		out_object[code] = {}
		#try: 
		obj = Tengxun_stock_object(code, re.findall('\"(.+)\"', str)[0].split("~"))
		#except:
		#	raise RuntimeError("Unknow stock. [" + code + "]") 
		out_object[code][obj.date] = obj
		return out_object
	
	
if __name__ == "__main__":
	#s = Tengxun_stock("600110")
	#print s.get_stock_content()
	
	#objs = s.get_stock_object()
	#for code in objs:
	#	for date in objs[code]:
	#		print code, date, objs[code][date].date, objs[code][date].top_price, objs[code][date].floor_price, objs[code][date].high_limit, objs[code][date].low_limit
	#		
	
	obj = Tengxun_stock.get_stock_object_from_str('v_sz300244="51~迪安诊断~300244~49.64~49.79~49.55~48132~23854~24278~49.63~15~49.62~43~49.61~9~49.60~34~49.59~20~49.64~60~49.65~9~49.66~41~49.67~174~49.68~2~15:00:27/49.64/247/S/1226108/25462|14:56:57/49.64/5/S/24820/25252|14:56:54/49.64/2/S/9928/25246|14:56:45/49.67/35/B/173825/25232|14:56:39/49.67/12/B/59599/25220|14:56:36/49.67/4/B/19867/25214~20160303150133~-0.15~-0.30~52.00~48.80~49.64/47885/239706343~48132~24093~2.65~93.82~~52.00~48.80~6.43~90.07~150.74~15.26~54.77~44.81~";')
	
	for code in obj:
		for date in obj[code]:
			print code, date, obj[code][date].date, obj[code][date].top_price, obj[code][date].floor_price, obj[code][date].high_limit, obj[code][date].low_limit
	
	
	