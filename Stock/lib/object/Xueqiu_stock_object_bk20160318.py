#coding:utf-8
#成交时间	成交价格	价格变动	成交量(手)	成交额(元)	性质
#9:25:00	50.34		0.15		141			709794		买盘


class Xueqiu_stock_object:
	
	def __init__(self, code, date, attrs=[]):
		self.__code = code
		self.__date = date

		if len(attr) > 0:
			self.__time = attr[0]
			self.__trans_price = attr[1]
			self.__price_change = attr[2]
			self.__volume = attr[3]
			self.__amount = attr[4]
			self.__buy_sell = attr[5]
			self.__source = 'Xueqiu'
	
	@property
	def code(self):
		return self.__code

	@property
	def date(self):
		return self.__date
		
	@property
	def time(self):
		return self.__time
	
	@time.setter
	def time(self, time):
		self.__time = time
	
	@property
	def trans_price(self):
		return self.__trans_price
	
	@trans_price.setter
	def trans_price(self, trans_price):
		self.__trans_price = trans_price
	
	@property
	def price_change(self):
		return self.__price_change
	
	@price_change.setter
	def price_change(self, price_change):
		self.__price_change = price_change

	@property
	def volume(self):
		return self.__volume
	
	@volume.setter
	def volume(self, volume):
		self.__volume = volume
	
	@property
	def amount(self):
		return self.__amount
	
	@amount.setter
	def amount(self, amount):
		self.__amount = amount

	@property
	def buy_sell(self):
		return self.__buy_sell
	
	@buy_sell.setter
	def buy_sell(self, buy_sell):
		self.__buy_sell = buy_sell

	@property
	def source(self):
		return self.__source
	
	@source.setter
	def source(self, source):
		self.__source = source
	
if __name__ == "__main__":
	s = Xueqiu_stock_object(600101, 20130501)
	print s.date
