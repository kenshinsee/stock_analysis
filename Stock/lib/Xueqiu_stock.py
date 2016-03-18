#coding:utf-8
#------------------------------------
#-- Xueqiu stock api 
#------------------------------------
# http://stock.gtimg.cn/data/index.php?appn=detail&action=download&c=sz002444&d=20160314
# Xueqiu provides the recent 2 months transaction details

import urllib2,re,sys,datetime
import StringIO
from object.Xueqiu_stock_object import Xueqiu_stock_object

class Xueqiu_stock:
	__url_prefix = "http://stock.gtimg.cn/data/index.php?appn=detail&action=download"
	__code_symbol = "&c=%(code_loc)s%(code)s"
	__date_symbol = "&d=%(date)s"
	__code_loc_dict = {
		"60": "sh", 
		"00": "sz", 
		"30": "sz", 
		"51": "sh",
		"15": "sz",
		"20": "sz",
		"90": "sh",
	}

	def __init__(self, code, date):
		self.__code = str(code)
		self.__date = str(date)
		
	def get_url(self):
			return self.__url_prefix + self.__code_symbol % {"code": self.__code, "code_loc": self.__code_loc_dict[self.__code[0:2]]} + self.__date_symbol % {"date": self.__date}

	def get_stock_content(self):
		content = urllib2.urlopen(self.get_url()).read().strip()
		out_dict = {}
		out_dict[self.__code] = {}
		content_add_stock_id_date = re.subn(r'\n', '\n' + str(self.__code) + '\t' + self.__date + '\t', content)[0] # the data return from Yahoo doesn't contain stock id and date, manually add stock id at first column
		content_no_header = re.subn(r'^.+\n', '', content_add_stock_id_date)[0] # remove header
		out_dict[self.__code][self.__date] = content_no_header
		return out_dict
		
	def get_stock_object(self):
		out_object = {}
		for code in self.get_stock_content():
			out_object[code] = {}
			for date in self.get_stock_content()[code]:
				buf = StringIO.StringIO(self.get_stock_content()[code][date])
				rows = []
				for row in buf.readlines():
					rows.append(row.split('\t')[2:])
				out_object[code][date] = Xueqiu_stock_object(code, date, rows)
				buf.close()
		return out_object
		
	@staticmethod
	def get_stock_object_from_str(str):
	# This method reads a str to create a stock object
	# This method is for backload trades from a pre-stored file which contains stock info with the same format as calling from url
	# Different from the same function for other stock source, the [str] here is a full transaction of a day
		buf = StringIO.StringIO(str)
		rows = []
		code = ''
		date = ''
		for row in buf.readlines():
			if len(rows) == 0:
				code = row.split('\t')[0]
				date = row.split('\t')[1]
			rows.append(row.split('\t')[2:])
		
		out_object = {}
		out_object[code] = {}
		out_object[code][date] = Xueqiu_stock_object(code, date, rows)
		return out_object
	
		
		
if __name__ == "__main__":
	s = Xueqiu_stock("300499", "20160317")
	#print s.get_url()
	#print s.get_stock_content()['300499']['20160317']

	obj = s.get_stock_object()#['300499']['20160317']
	for code in obj:
		for date in obj[code]:
			print code, date, obj[code][date].attrs_in_dict[1]['buy_sell']
		
