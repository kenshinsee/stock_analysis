#coding:utf-8
# Date,Open,High,Low,Close,Volume(股),Adj Close(复权收盘价)
# 2015-11-13,12.08,13.28,12.03,13.28,31383100,13.28
#

class Yahoo_stock_object:
	__code = ""
	__date = ""
	__open_price = ""
	__top_price = ""
	__floor_price = ""
	__close_price = ""
	__volume = ""
	__adj_close_price = ""
	
	def __init__(self, code, attr=[]):
		self.__code = code
		if len(attr) > 0:
			self.__date = attr[0]
			self.__open_price = attr[1]
			self.__top_price = attr[2]
			self.__floor_price = attr[3]
			self.__close_price = attr[4]
			self.__volume = round(float(attr[5]) / 100, 2) # share to round-lot
			self.__adj_close_price = attr[6]
	
	@property
	def code(self):
		return self.__code

	@property
	def date(self):
		return self.__date
	
	@date.setter
	def date(self, date):
		self.__date = date
	
	@property
	def open_price(self):
		return self.__open_price
	
	@open_price.setter
	def open_price(self, open_price):
		self.__open_price = open_price
		
	@property
	def top_price(self):
		return self.__top_price
	
	@top_price.setter
	def top_price(self, top_price):
		self.__top_price = top_price
	
	@property
	def floor_price(self):
		return self.__floor_price
	
	@floor_price.setter
	def floor_price(self, floor_price):
		self.__floor_price = floor_price
	
	@property
	def close_price(self):
		return self.__close_price
	
	@close_price.setter
	def close_price(self, close_price):
		self.__close_price = close_price
	
	@property
	def volume(self):
		return self.__volume
	
	@volume.setter
	def volume(self, volume):
		self.__volume = volume
	
	@property
	def adj_close_price(self):
		return self.__adj_close_price
	
	@adj_close_price.setter
	def adj_close_price(self, adj_close_price):
		self.__adj_close_price = adj_close_price


if __name__ == "__main__":
	s = Yahoo_stock_object(600101)
	s.date = 20130501
	print s.date
