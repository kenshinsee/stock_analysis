#coding:utf-8
#  0: 未知  
#  1: 名字  
#  2: 代码  
#  3: 当前价格  
#  4: 昨收  
#  5: 今开  
#  6: 成交量（手）  
#  7: 外盘（手）
#  8: 内盘（手）
#  9: 买一  
# 10: 买一量（手）  
# 11-18: 买二 买五  
# 19: 卖一  
# 20: 卖一量  
# 21-28: 卖二 卖五  
# 29: 最近逐笔成交  
# 30: 时间  
# 31: 涨跌  
# 32: 涨跌%  
# 33: 最高  
# 34: 最低  
# 35: 价格/成交量（手）/成交额  
# 36: 成交量（手）  
# 37: 成交额（万）  
# 38: 换手率% 
# 39: 市盈率  
# 40: unknown
# 41: 最高  
# 42: 最低  
# 43: 振幅%
# 44: 流通市值 (亿)
# 45: 总市值 (亿)
# 46: 市净率  
# 47: 涨停价  
# 48: 跌停价  

#v_sz300244="51~迪安诊断~300244~49.64~49.79~49.55~48132~23854~24278~49.63~15~49.62~43~49.61~9~49.60~34~49.59~20~49.64~60~49.65~9~49.66~41~49.67~174~49.68~2~15:00:27/49.64/247/S/1226108/25462|14:56:57/49.64/5/S/24820/25252|14:56:54/49.64/2/S/9928/25246|14:56:45/49.67/35/B/173825/25232|14:56:39/49.67/12/B/59599/25220|14:56:36/49.67/4/B/19867/25214~20160303150133~-0.15~-0.30~52.00~48.80~49.64/47885/239706343~48132~24093~2.65~93.82~~52.00~48.80~6.43~90.07~150.74~15.26~54.77~44.81~";

#v_sh600110="1~诺德股份~600110~6.25~6.30~6.25~344270~156404~187866~6.24~1144~6.23~1606~6.22~1339~6.21~1794~6.20~1609~6.25~173~6.26~862~6.27~444~6.28~315~6.29~895~15:00:02/6.25/53/B/33085/10757|14:59:57/6.24/107/S/66803/10753|14:59:52/6.25/66/B/41250/10748|14:59:47/6.25/148/B/92523/10744|14:59:42/6.25/106/M/66250/10740|14:59:37/6.26/1185/B/741677/10737~20160303150551~-0.05~-0.79~6.44~6.21~6.24/344217/216644131~344270~21668~2.99~~~6.44~6.21~3.65~71.89~71.89~6.42~6.93~5.67~";

class Tengxun_stock_object:
	def __init__(self, code, attr=[]):
		self.__code = code
		if len(attr) > 0:
			self.__name = attr[1]
			self.__current_price = attr[3]
			self.__yesterday_close_price = attr[4]
			self.__open_price = attr[5]
			self.__close_price = attr[3] # because it's an eod extract, the current price is the close price
			self.__volume = attr[6] # round-lot
			self.__outer_disc = attr[7] # round-lot
			self.__inner_disc = attr[8] # round-lot
			self.__buy_1_price = attr[9]
			self.__buy_1_roundlot = attr[10]
			self.__buy_2_price = attr[11]
			self.__buy_2_roundlot = attr[12]
			self.__buy_3_price = attr[13]
			self.__buy_3_roundlot = attr[14]
			self.__buy_4_price = attr[15]
			self.__buy_4_roundlot = attr[16]
			self.__buy_5_price = attr[17]
			self.__buy_5_roundlot = attr[18]
			self.__sell_1_price = attr[19]
			self.__sell_1_roundlot = attr[20]
			self.__sell_2_price = attr[21]
			self.__sell_2_roundlot = attr[22]
			self.__sell_3_price = attr[23]
			self.__sell_3_roundlot = attr[24]
			self.__sell_4_price = attr[25]
			self.__sell_4_roundlot = attr[26]
			self.__sell_5_price = attr[27]
			self.__sell_5_roundlot = attr[28]
			self.__trade_by_trade_deal = attr[29]
			self.__date = attr[30][0:4] + '-' + attr[30][4:6] + '-' + attr[30][6:8]
			self.__time = attr[30][8:10] + ':' + attr[30][10:12] + ':' + attr[30][12:14]
			self.__rise_price = attr[31]
			self.__rise = attr[32]
			self.__top_price = attr[33]
			self.__floor_price = attr[34]
			self.__unknown_1 = attr[35]
			self.__amount = attr[37] # 10 thousands
			self.__turnover_ratio = attr[38]
			self.__PE_ratio = attr[39]
			self.__amplitudes = attr[43]
			self.__circulation_market_value = attr[44]
			self.__total_market_value = attr[45]
			self.__PB_ratio = attr[46]
			self.__high_limit = attr[47]
			self.__low_limit = attr[48]
			self.__source = 'Tengxun'

	@property
	def code(self):
		return self.__code

	@property
	def name(self):
		return self.__name

	@name.setter
	def name(self, name):
		self.__name = name
		
	@property
	def current_price(self):
		return self.__current_price

	@current_price.setter
	def current_price(self, current_price):
		self.__current_price = current_price

	@property
	def yesterday_close_price(self):
		return self.__yesterday_close_price
	
	@yesterday_close_price.setter
	def yesterday_close_price(self, yesterday_close_price):
		self.__yesterday_close_price = yesterday_close_price
		
	@property
	def open_price(self):
		return self.__open_price
	
	@open_price.setter
	def open_price(self, open_price):
		self.__open_price = open_price

	@property
	def close_price(self):
		return self.__close_price
	
	@yesterday_close_price.setter
	def close_price(self, close_price):
		self.__close_price = close_price
				
	@property
	def volume(self):
		return self.__volume
	
	@volume.setter
	def volume(self, volume):
		self.__volume = volume

	@property
	def outer_disc(self):
		return self.__outer_disc
	
	@outer_disc.setter
	def outer_disc(self, outer_disc):
		self.__outer_disc = outer_disc

	@property
	def inner_disc(self):
		return self.__inner_disc
	
	@inner_disc.setter
	def inner_disc(self, inner_disc):
		self.__inner_disc = inner_disc
		
	@property
	def buy_1_price(self):
		return self.__buy_1_price
	
	@buy_1_price.setter
	def buy_1_price(self, buy_1_price):
		self.__buy_1_price = buy_1_price
		
	@property
	def buy_1_roundlot(self):
		return self.__buy_1_roundlot
	
	@buy_1_roundlot.setter
	def buy_1_roundlot(self, buy_1_roundlot):
		self.__buy_1_roundlot = buy_1_roundlot
		
	@property
	def buy_2_price(self):
		return self.__buy_2_price
	
	@buy_2_price.setter
	def buy_2_price(self, buy_2_price):
		self.__buy_2_price = buy_2_price
		
	@property
	def buy_2_roundlot(self):
		return self.__buy_2_roundlot
	
	@buy_2_roundlot.setter
	def buy_2_roundlot(self, buy_2_roundlot):
		self.__buy_2_roundlot = buy_2_roundlot
		
	@property
	def buy_3_price(self):
		return self.__buy_3_price
	
	@buy_3_price.setter
	def buy_3_price(self, buy_3_price):
		self.__buy_3_price = buy_3_price
		
	@property
	def buy_3_roundlot(self):
		return self.__buy_3_roundlot
	
	@buy_3_roundlot.setter
	def buy_3_roundlot(self, buy_3_roundlot):
		self.__buy_3_roundlot = buy_3_roundlot

	@property
	def buy_4_price(self):
		return self.__buy_4_price
	
	@buy_4_price.setter
	def buy_4_price(self, buy_4_price):
		self.__buy_4_price = buy_4_price
		
	@property
	def buy_4_roundlot(self):
		return self.__buy_4_roundlot
	
	@buy_4_roundlot.setter
	def buy_4_roundlot(self, buy_4_roundlot):
		self.__buy_4_roundlot = buy_4_roundlot
		
	@property
	def buy_5_price(self):
		return self.__buy_5_price
	
	@buy_5_price.setter
	def buy_5_price(self, buy_5_price):
		self.__buy_5_price = buy_5_price
		
	@property
	def buy_5_roundlot(self):
		return self.__buy_5_roundlot
	
	@buy_5_roundlot.setter
	def buy_5_roundlot(self, buy_5_roundlot):
		self.__buy_5_roundlot = buy_5_roundlot
		
	@property
	def sell_1_price(self):
		return self.__sell_1_price
	
	@sell_1_price.setter
	def sell_1_price(self, sell_1_price):
		self.__sell_1_price = sell_1_price
		
	@property
	def sell_1_roundlot(self):
		return self.__sell_1_roundlot
	
	@sell_1_roundlot.setter
	def sell_1_roundlot(self, sell_1_roundlot):
		self.__sell_1_roundlot = sell_1_roundlot
		
	@property
	def sell_2_price(self):
		return self.__sell_2_price
	
	@sell_2_price.setter
	def sell_2_price(self, sell_2_price):
		self.__sell_2_price = sell_2_price
		
	@property
	def sell_2_roundlot(self):
		return self.__sell_2_roundlot
	
	@sell_2_roundlot.setter
	def sell_2_roundlot(self, sell_2_roundlot):
		self.__sell_2_roundlot = sell_2_roundlot
		
	@property
	def sell_3_price(self):
		return self.__sell_3_price
	
	@sell_3_price.setter
	def sell_3_price(self, sell_3_price):
		self.__sell_3_price = sell_3_price
		
	@property
	def sell_3_roundlot(self):
		return self.__sell_3_roundlot
	
	@sell_3_roundlot.setter
	def sell_3_roundlot(self, sell_3_roundlot):
		self.__sell_3_roundlot = sell_3_roundlot

	@property
	def sell_4_price(self):
		return self.__sell_4_price
	
	@sell_4_price.setter
	def sell_4_price(self, sell_4_price):
		self.__sell_4_price = sell_4_price
		
	@property
	def sell_4_roundlot(self):
		return self.__sell_4_roundlot
	
	@sell_4_roundlot.setter
	def sell_4_roundlot(self, sell_4_roundlot):
		self.__sell_4_roundlot = sell_4_roundlot
		
	@property
	def sell_5_price(self):
		return self.__sell_5_price
	
	@sell_5_price.setter
	def sell_5_price(self, sell_5_price):
		self.__sell_5_price = sell_5_price
		
	@property
	def sell_5_roundlot(self):
		return self.__sell_5_roundlot
	
	@sell_5_roundlot.setter
	def sell_5_roundlot(self, sell_5_roundlot):
		self.__sell_5_roundlot = sell_5_roundlot
		
	@property
	def date(self):
		return self.__date

	@date.setter
	def date(self, date):
		self.__date = date

	@property
	def time(self):
		return self.__time

	@time.setter
	def time(self, time):
		self.__time = time

	@property
	def rise_price(self):
		return self.__rise_price

	@rise_price.setter
	def rise_price(self, rise_price):
		self.__rise_price = rise_price

	@property
	def rise(self):
		return self.__rise
	
	@rise.setter
	def rise(self, rise):
		self.__rise = rise
		
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
	def amount(self):
		return self.__amount
	
	@amount.setter
	def amount(self, amount):
		self.__amount = amount

	@property
	def turnover_ratio(self):
		return self.__turnover_ratio
	
	@turnover_ratio.setter
	def turnover_ratio(self, turnover_ratio):
		self.__turnover_ratio = turnover_ratio

	@property
	def PE_ratio(self):
		return self.__PE_ratio
	
	@PE_ratio.setter
	def PE_ratio(self, PE_ratio):
		self.__PE_ratio = PE_ratio

	@property
	def amplitudes(self):
		return self.__amplitudes
	
	@amplitudes.setter
	def amplitudes(self, amplitudes):
		self.__amplitudes = amplitudes

	@property
	def circulation_market_value(self):
		return self.__circulation_market_value
	
	@circulation_market_value.setter
	def circulation_market_value(self, circulation_market_value):
		self.__circulation_market_value = circulation_market_value

	@property
	def total_market_value(self):
		return self.__total_market_value
	
	@total_market_value.setter
	def total_market_value(self, total_market_value):
		self.__total_market_value = total_market_value

	@property
	def PB_ratio(self):
		return self.__PB_ratio
	
	@PB_ratio.setter
	def PB_ratio(self, PB_ratio):
		self.__PB_ratio = PB_ratio

	@property
	def high_limit(self):
		return self.__high_limit
	
	@high_limit.setter
	def high_limit(self, high_limit):
		self.__high_limit = high_limit

	@property
	def low_limit(self):
		return self.__low_limit
	
	@low_limit.setter
	def low_limit(self, low_limit):
		self.__low_limit = low_limit
	
	@property
	def source(self):
		return self.__source
	
	@source.setter
	def source(self, source):
		self.__source = source
	
if __name__ == "__main__":
	s = Tengxun_stock_object(600101)
	s.datetime = 20130501
	print s.datetime
	
	
	
	