#coding:utf-8
#  0: 未知  
#  1: 名字  
#  2: 代码  
#  3: 当前价格  
#  4: 昨收  
#  5: 今开  
#  6: 成交量（手）  
#  7: 外盘  
#  8: 内盘  
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
# 38: 换手率  
# 39: 市盈率  
# 40: 最高  
# 41: 最低  
# 42: 振幅  
# 43: 流通市值  
# 44: 总市值  
# 45: 市净率  
# 46: 涨停价  
# 47: 跌停价  

#v_sz000858="51~五 粮 液~000858~22.83~22.46~22.55~113281~64133~49148~22.83~766~22.82~551~22.81~40~22.80~143~22.79~132~22.84~4~22.85~42~22.86~10~22.87~20~22.88~68~15:00:17/22.83/906/S/2068261/31759|14:56:59/22.82/76/S/172679/31535|14:56:53/22.82/8/S/18256/31519|14:56:47/22.83/5/B/11415/31512|14:56:41/22.82/1/S/2282/31493|14:56:35/22.82/12/B/28130/31484~20160301150459~0.37~1.65~23.04~22.42~22.82/112375/254869761~113281~25694~0.30~15.12~~23.04~22.42~2.76~866.55~866.62~2.08~24.71~20.21~";

class Tengxun_stock_object:
	def __init__(self, code, attr=[]):
		self.__code = code
		if len(attr) > 0:
			self.__name = attr[1]
			self.__current_price = attr[3]
			self.__yesterday_close_price = attr[4]
			self.__open_price = attr[5]
			self.__volume_hands = attr[6]
			self.__outer_disc = attr[7]
			self.__inner_disc = attr[8]
			self.__buy_1_price = attr[9]
			self.__buy_1_handes = attr[10]
			self.__buy_2_price = attr[11]
			self.__buy_2_handes = attr[12]
			self.__buy_3_price = attr[13]
			self.__buy_3_handes = attr[14]
			self.__buy_4_price = attr[15]
			self.__buy_4_handes = attr[16]
			self.__buy_5_price = attr[17]
			self.__buy_5_handes = attr[18]
			self.__sell_1_price = attr[19]
			self.__sell_1_handes = attr[20]
			self.__sell_2_price = attr[21]
			self.__sell_2_handes = attr[22]
			self.__sell_3_price = attr[23]
			self.__sell_3_handes = attr[24]
			self.__sell_4_price = attr[25]
			self.__sell_4_handes = attr[26]
			self.__sell_5_price = attr[27]
			self.__sell_5_handes = attr[28]
			self.__trade_by_trade_deal = attr[29]
			self.__datetime = attr[30]
			self.__rise_price = attr[31]
			self.__rise = attr[32]
			self.__high_price = attr[33]
			self.__low_price = attr[34]
			self.__unknown_1 = attr[35]
			self.__volume_money_in_ten_thousand = attr[37]
			self.__turnover_ratio = attr[38]
			self.__PE_ratio = attr[39]
			self.__amplitudes = attr[42]
			self.__circulation_market_value = attr[43]
			self.__total_market_value = attr[44]
			self.__PB_ratio = attr[45]
			self.__high_limit = attr[46]
			self.__low_limit = attr[47]

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
	def yesterday_close_price(self, close_price):
		self.__yesterday_close_price = close_price
		
	@property
	def open_price(self):
		return self.__open_price
	
	@open_price.setter
	def open_price(self, open_price):
		self.__open_price = open_price

	@property
	def volume_hands(self):
		return self.__volume_hands
	
	@volume_hands.setter
	def volume_hands(self, volume_hands):
		self.__volume_hands = volume_hands

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
	def buy_1_handes(self):
		return self.__buy_1_handes
	
	@buy_1_handes.setter
	def buy_1_handes(self, buy_1_handes):
		self.__buy_1_handes = buy_1_handes
		
	@property
	def buy_2_price(self):
		return self.__buy_2_price
	
	@buy_2_price.setter
	def buy_2_price(self, buy_2_price):
		self.__buy_2_price = buy_2_price
		
	@property
	def buy_2_handes(self):
		return self.__buy_2_handes
	
	@buy_2_handes.setter
	def buy_2_handes(self, buy_2_handes):
		self.__buy_2_handes = buy_2_handes
		
	@property
	def buy_3_price(self):
		return self.__buy_3_price
	
	@buy_3_price.setter
	def buy_3_price(self, buy_3_price):
		self.__buy_3_price = buy_3_price
		
	@property
	def buy_3_handes(self):
		return self.__buy_3_handes
	
	@buy_3_handes.setter
	def buy_3_handes(self, buy_3_handes):
		self.__buy_3_handes = buy_3_handes

	@property
	def buy_4_price(self):
		return self.__buy_4_price
	
	@buy_4_price.setter
	def buy_4_price(self, buy_4_price):
		self.__buy_4_price = buy_4_price
		
	@property
	def buy_4_handes(self):
		return self.__buy_4_handes
	
	@buy_4_handes.setter
	def buy_4_handes(self, buy_4_handes):
		self.__buy_4_handes = buy_4_handes
		
	@property
	def buy_5_price(self):
		return self.__buy_5_price
	
	@buy_5_price.setter
	def buy_5_price(self, buy_5_price):
		self.__buy_5_price = buy_5_price
		
	@property
	def buy_5_handes(self):
		return self.__buy_5_handes
	
	@buy_5_handes.setter
	def buy_5_handes(self, buy_5_handes):
		self.__buy_5_handes = buy_5_handes
		
	@property
	def sell_1_price(self):
		return self.__sell_1_price
	
	@sell_1_price.setter
	def sell_1_price(self, sell_1_price):
		self.__sell_1_price = sell_1_price
		
	@property
	def sell_1_handes(self):
		return self.__sell_1_handes
	
	@sell_1_handes.setter
	def sell_1_handes(self, sell_1_handes):
		self.__sell_1_handes = sell_1_handes
		
	@property
	def sell_2_price(self):
		return self.__sell_2_price
	
	@sell_2_price.setter
	def sell_2_price(self, sell_2_price):
		self.__sell_2_price = sell_2_price
		
	@property
	def sell_2_handes(self):
		return self.__sell_2_handes
	
	@sell_2_handes.setter
	def sell_2_handes(self, sell_2_handes):
		self.__sell_2_handes = sell_2_handes
		
	@property
	def sell_3_price(self):
		return self.__sell_3_price
	
	@sell_3_price.setter
	def sell_3_price(self, sell_3_price):
		self.__sell_3_price = sell_3_price
		
	@property
	def sell_3_handes(self):
		return self.__sell_3_handes
	
	@sell_3_handes.setter
	def sell_3_handes(self, sell_3_handes):
		self.__sell_3_handes = sell_3_handes

	@property
	def sell_4_price(self):
		return self.__sell_4_price
	
	@sell_4_price.setter
	def sell_4_price(self, sell_4_price):
		self.__sell_4_price = sell_4_price
		
	@property
	def sell_4_handes(self):
		return self.__sell_4_handes
	
	@sell_4_handes.setter
	def sell_4_handes(self, sell_4_handes):
		self.__sell_4_handes = sell_4_handes
		
	@property
	def sell_5_price(self):
		return self.__sell_5_price
	
	@sell_5_price.setter
	def sell_5_price(self, sell_5_price):
		self.__sell_5_price = sell_5_price
		
	@property
	def sell_5_handes(self):
		return self.__sell_5_handes
	
	@sell_5_handes.setter
	def sell_5_handes(self, sell_5_handes):
		self.__sell_5_handes = sell_5_handes
		
	@property
	def datetime(self):
		return self.__datetime

	@datetime.setter
	def datetime(self, datetime):
		self.__datetime = datetime
	
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
	def volume_money_in_ten_thousand(self):
		return self.__volume_money_in_ten_thousand
	
	@volume_money_in_ten_thousand.setter
	def volume_money_in_ten_thousand(self, volume_money_in_ten_thousand):
		self.__volume_money_in_ten_thousand = volume_money_in_ten_thousand

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
	
	@low_price.setter
	def low_limit(self, low_limit):
		self.__low_limit = low_limit
	
	
if __name__ == "__main__":
	s = Tengxun_stock_object(600101)
	s.datetime = 20130501
	print s.datetime
	
	
	
	