#coding:utf-8
# 0����������·������Ʊ���֣�
# 1����27.55�壬���տ��̼ۣ�
# 2����27.25�壬�������̼ۣ�
# 3����26.91�壬��ǰ�۸�
# 4����27.55�壬������߼ۣ�
# 5����26.20�壬������ͼۣ�
# 6����26.91�壬����ۣ�������һ�����ۣ�
# 7����26.92�壬�����ۣ�������һ�����ۣ�
# 8����22114263�壬�ɽ��Ĺ�Ʊ�������ڹ�Ʊ������һ�ٹ�Ϊ������λ��������ʹ��ʱ��ͨ���Ѹ�ֵ����һ�٣�
# 9����589824680�壬�ɽ�����λΪ��Ԫ����Ϊ��һĿ��Ȼ��ͨ���ԡ���Ԫ��Ϊ�ɽ����ĵ�λ������ͨ���Ѹ�ֵ����һ��
# 10����4695�壬����һ������4695�ɣ���47�֣�
# 11����26.91�壬����һ�����ۣ�
# 12����57590�壬�������
# 13����26.90�壬�������
# 14����14700�壬��������
# 15����26.89�壬��������
# 16����14300�壬�����ġ�
# 17����26.88�壬�����ġ�
# 18����15100�壬�����塱
# 19����26.87�壬�����塱
# 20����3100�壬����һ���걨3100�ɣ���31�֣�
# 21����26.92�壬����һ������
# (22, 23), (24, 25), (26,27), (28, 29)�ֱ�Ϊ����������������������
# 30����2008-01-11�壬���ڣ�
# 31����15:05:32�壬ʱ�䣻
#

class Sina_stock_object:
	__code = ""
	__open_price = ""
	__yesterday_close_price = ""
	__current_price = ""
	__high_price = ""
	__low_price = ""
	__bidding = ""
	__auction = ""
	__volume = ""
	__amount = ""
	__buy_1_handes = ""
	__buy_1_price = ""
	__buy_2_handes = ""
	__buy_2_price = ""
	__buy_3_handes = ""
	__buy_3_price = ""
	__buy_4_handes = ""
	__buy_4_price = ""
	__buy_5_handes = ""
	__buy_5_price = ""
	__sell_1_handes = ""
	__sell_1_price = ""
	__sell_2_handes = ""
	__sell_2_price = ""
	__sell_3_handes = ""
	__sell_3_price = ""
	__sell_4_handes = ""
	__sell_4_price = ""
	__sell_5_handes = ""
	__sell_5_price = ""
	__date = ""
	__time = ""

	def __init__(self, code, attr=[]):
		self.__code = code
		if len(attr) > 0:
			self.__open_price = attr[1]
			self.__yesterday_close_price = attr[2]
			self.__current_price = attr[3]
			self.__high_price = attr[4]
			self.__low_price = attr[5]
			self.__bidding = attr[6]
			self.__auction = attr[7]
			self.__volume = attr[8]
			self.__amount = attr[9]
			self.__buy_1_handes = attr[10]
			self.__buy_1_price = attr[11]
			self.__buy_2_handes = attr[12]
			self.__buy_2_price = attr[13]
			self.__buy_3_handes = attr[14]
			self.__buy_3_price = attr[15]
			self.__buy_4_handes = attr[16]
			self.__buy_4_price = attr[17]
			self.__buy_5_handes = attr[18]
			self.__buy_5_price = attr[19]
			self.__sell_1_handes = attr[20]
			self.__sell_1_price = attr[21]
			self.__sell_2_handes = attr[22]
			self.__sell_2_price = attr[23]
			self.__sell_3_handes = attr[24]
			self.__sell_3_price = attr[25]
			self.__sell_4_handes = attr[26]
			self.__sell_4_price = attr[27]
			self.__sell_5_handes = attr[28]
			self.__sell_5_price = attr[29]
			self.__date = attr[30]
			self.__time = attr[31]

	@property
	def code(self):
		return self.__code
	
	@property
	def open_price(self):
		return self.__open_price
	
	@open_price.setter
	def open_price(self, open_price):
		self.__open_price = open_price

	@property
	def yesterday_close_price(self):
		return self.__yesterday_close_price
	
	@yesterday_close_price.setter
	def yesterday_close_price(self, close_price):
		self.__yesterday_close_price = close_price

	@property
	def current_price(self):
		return self.__current_price

	@current_price.setter
	def current_price(self, current_price):
		self.__current_price = current_price

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
	def bidding(self):
		return self.__bidding
	
	@bidding.setter
	def bidding(self, bidding):
		self.__bidding = bidding

	@property
	def auction(self):
		return self.__auction

	@auction.setter
	def auction(self, auction):
		self.__auction = auction
	
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
	

if __name__ == "__main__":
	s = Sina_stock_object(600101)
	s.date = 20130501
	print s.date
