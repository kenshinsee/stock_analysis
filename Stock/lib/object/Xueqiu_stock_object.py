#coding:utf-8
#成交时间	成交价格	价格变动	成交量(手)	成交额(元)	性质
#9:25:00	50.34		0.15		141			709794		买盘


class Xueqiu_stock_object:
	
	def __init__(self, code, date, attrs=[]):
		self.__code = code
		self.__date = date
		self.__attrs = attrs
		self.__source = 'Xueqiu'
	
	@property
	def code(self):
		return self.__code

	@property
	def date(self):
		return self.__date
	
	@property
	def attrs(self):
		return self.__attrs
	
	@property
	def attrs_in_dict(self):
		attrs_list = []
		for attr in self.__attrs:
			attr_dict = {}
			attr_dict['time'] = attr[0]
			attr_dict['trans_price'] = attr[1]
			attr_dict['price_change'] = attr[2]
			attr_dict['volume'] = attr[3]
			attr_dict['amount'] = attr[4]
			attr_dict['buy_sell'] = attr[5]
			attrs_list.append(attr_dict)
		return attrs_list
	
	@property
	def source(self):
		return self.__source
	
if __name__ == "__main__":
	s = Xueqiu_stock_object(600101, 20130501, [])
	print s.date
