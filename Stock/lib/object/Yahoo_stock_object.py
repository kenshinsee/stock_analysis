#
# Date,Open,High,Low,Close,Volume,Adj Close(复权收盘价)
# 2015-11-13,12.08,13.28,12.03,13.28,31383100,13.28
#

class Yahoo_stock_object:
	__code = ""
	__date = ""
	__open_price = ""
	__high_price = ""
	__low_price = ""
	__close_price = ""
	__volume = ""
	__adj_close_price = ""
	
	def __init__(self, code, attr=[]):
		self.__code = code
		if len(attr) > 0:
			self.__date = attr[0]
			self.__open_price = attr[1]
			self.__high_price = attr[2]
			self.__low_price = attr[3]
			self.__close_price = attr[4]
			self.__volume = attr[5]
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
	def high_price(self):
		return self.__high_price
	
	@high_price.setter
	def high_price(self, high_price):
		self.__high_price = high_price
	
	@property
	def low_price(self):
		return self.__low_price
	
	@low_price.setter
	def low_price(self, low_price):
		self.__low_price = low_price
	
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
