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
	__top_price = ""
	__floor_price = ""
	__bidding = ""
	__auction = ""
	__volume = ""
	__amount = ""
	__buy_1_roundlot = ""
	__buy_1_price = ""
	__buy_2_roundlot = ""
	__buy_2_price = ""
	__buy_3_roundlot = ""
	__buy_3_price = ""
	__buy_4_roundlot = ""
	__buy_4_price = ""
	__buy_5_roundlot = ""
	__buy_5_price = ""
	__sell_1_roundlot = ""
	__sell_1_price = ""
	__sell_2_roundlot = ""
	__sell_2_price = ""
	__sell_3_roundlot = ""
	__sell_3_price = ""
	__sell_4_roundlot = ""
	__sell_4_price = ""
	__sell_5_roundlot = ""
	__sell_5_price = ""
	__date = ""
	__time = ""

# var hq_str_sz300374="��ͨ�Ƽ�,18.760,18.800,19.200,20.650,17.500,19.200,19.220,2724272,51598032.370,34200,19.200,2100,19.190,200,19.180,5300,19.150,1300,19.100,600,19.220,18700,19.230,2200,19.250,1200,19.290,3100,19.300,2016-03-04,15:05:56,00";

	def __init__(self, code, attr=[]):
		self.__code = code
		if len(attr) > 0:
			self.__open_price = attr[1]
			self.__yesterday_close_price = attr[2]
			self.__current_price = attr[3]
			self.__top_price = attr[4]
			self.__floor_price = attr[5]
			self.__bidding = attr[6]
			self.__auction = attr[7]
			self.__volume = round(float(attr[8]) / 100, 2) # share to round-lot
			self.__amount = round(float(attr[9]) / 10000, 2) # 10 thousands
			self.__buy_1_roundlot = attr[10]
			self.__buy_1_price = attr[11]
			self.__buy_2_roundlot = attr[12]
			self.__buy_2_price = attr[13]
			self.__buy_3_roundlot = attr[14]
			self.__buy_3_price = attr[15]
			self.__buy_4_roundlot = attr[16]
			self.__buy_4_price = attr[17]
			self.__buy_5_roundlot = attr[18]
			self.__buy_5_price = attr[19]
			self.__sell_1_roundlot = attr[20]
			self.__sell_1_price = attr[21]
			self.__sell_2_roundlot = attr[22]
			self.__sell_2_price = attr[23]
			self.__sell_3_roundlot = attr[24]
			self.__sell_3_price = attr[25]
			self.__sell_4_roundlot = attr[26]
			self.__sell_4_price = attr[27]
			self.__sell_5_roundlot = attr[28]
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
