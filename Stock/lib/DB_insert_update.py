#!/usr/local/bin/python2.7
#coding:utf-8


import sys,os,re,datetime,yaml,csv
from common_tool import replace_vars, print_log, warn_log, error_log, get_date, get_yaml
from psql import get_conn, get_cur

class DB_insert_update():
	# __csv_dict = {pk1: {main:{{f1: {value: a, type: int}}, {f2: {value: a, type: int}}, ...}, action: xxx}, ...}
	__csv_dict = {}
	# __db_dict = {pk1: {main:{{f1: {value: a}}, {f2: {value: a}}, ...}, action: xxx}, ...}
	__db_dict = {}
	def __init__(self, csv_file, csv_pk, csv_ins, db_conn, db_tab, db_pk, db_ins, is_valid_enable='Y', upd_time_enable='Y', csv_upd=[], field_conversion={}, db_upd=[]):
		# csv_file: full name of csv file 
		# csv_pk: [ pk1, pk2 ] pk in csv
		# csv_upd: [ f1, f2 ] fields in csv used to compare with corresponding fields in db (db_upd)
		# csv_ins: {f1:type, f2:type} all the fields in csv which will be inserted into db, type could be char|int|decimal
		# field_conversion: {csv_field: {csv_value:db_value}, ...} field in csv needs to convert to another value, then inserted into table
		# db_tab: db table name
		# db_pk: [ pk1, pk2 ] 
		# db_upd: [ f1, f2 ] 
		# db_ins: [ f1, f2, ...] fields used in INSERT statement, e.g. INSERT INTO XXX(f1, f2, ...)
		# is_valid_enable: Y|N, is is_valid used in the table
		# upd_time_enable: Y|N, is upd_time used in the table
		#==================================================================================
		#== read data from csv
		__csvf = open(csv_file)
		__csvr = csv.DictReader(__csvf)
		
		for row in __csvr:
			pk = []
			pv = ''
			pv_converted = ''
			for p in csv_pk: # unicode
				pv = row[p.encode('gbk')].decode('gbk')
				if p in field_conversion: # if it needs to be converted
					pv_converted = field_conversion[p][pv]
				else:
					pv_converted = pv
				pk.append(pv_converted)
			pk_concatenated = '|'.join(pk)
			
			# building __csv_dict for the row
			for f in csv_ins: # unicode
				self.__csv_dict[pk_concatenated] = {}
				self.__csv_dict[pk_concatenated]["main"] = {}
				self.__csv_dict[pk_concatenated]["main"][f] = {}
				pv = row[f.encode('gbk')].decode('gbk')
				if f in field_conversion: # if it needs to be converted
					pv_converted = field_conversion[f][pv]
				else:
					pv_converted = pv
				
				self.__csv_dict[pk_concatenated]["main"][f]['value'] = pv_converted
				self.__csv_dict[pk_concatenated]["main"][f]['type'] = csv_ins[f]
				#print pk_concatenated, f, self.__csv_dict[pk_concatenated]["main"][f]['value'], self.__csv_dict[pk_concatenated]["main"][f]['type']
		__csvf.close()
		print_log('%(num)s records have been read from %(fname)s.' % {'num': len(self.__csv_dict.keys()), 'fname': csv_file})
	
		#==================================================================================
		#== read data from db
		self.__db_conn = db_conn
		cur = get_cur(self.__db_conn)
		select_sql = "select * from %(tabname)s t" % {"tabname": db_tab}
		cur.execute(select_sql)
		db_rows = list(cur)

		for db_row in db_rows:
			pk = []
			pv = ''
			for p in db_pk: # unicode
				pv = str(db_row[p.encode('utf-8')]).decode('utf-8')
				pk.append(pv)
			pk_concatenated = '|'.join(pk)

			# building __db_dict for the row
			for f in db_ins: # unicode
				self.__db_dict[pk_concatenated] = {}
				self.__db_dict[pk_concatenated]["main"] = {}
				self.__db_dict[pk_concatenated]["main"][f] = {}
				pv = str(db_row[f.encode('utf-8')]).decode('utf-8')
				self.__db_dict[pk_concatenated]["main"][f]['value'] = pv
				#print pk_concatenated, f, self.__db_dict[pk_concatenated]["main"][f]['value']
		print_log('%(num)s records have been read from %(fname)s.' % {'num': len(self.__db_dict.keys()), 'fname': db_tab})

	def get_csv_dict(self):
		return self.__csv_dict
		
	def get_db_dict(self):
		return self.__db_dict
		
	def determine_action(self):
	# csv	db	is_valid	field_updated	action
	# 1		1	1			1				update db fields
	# 1		1	1			0				none
	# 1		1	0			1				is_valid->Y and update db fields
	# 1		1	0			0				is_valid->Y
	# 1		0	X			X				insert
	# 0		1	1			X				is_valid->N
	# 0		1	0			X				none
		cloned_csv_dict = self.__csv_dict.deepcopy() # deep copy csv dict used to iterate values, because the original csv dict may be updated 
		for r in cloned_csv_dict:
			actions = [] # UPD, INS, IS_VALID_TO_Y, IS_VALID_TO_N, or blank
			if r in self.__db_dict: # exists in db
				#-- check fields update
				if len(csv_upd) >0 and len(csv_upd) == len(db_upd): # need to check fields if they're updated
					csv_upd_value = []
					db_upd_value = []
					for c in csv_upd:
						csv_upd_value.append(self.__csv_dict[r]['main'][c]['value'])
					for d in db_upd:
						db_upd_value.append(self.__db_dict[r]['main'][c]['value'])
					if '|'.join(csv_upd_value) != '|'.join(db_upd_value):
						actions.append('UPD')
				elif len(csv_upd) != len(db_upd): # if length of csv_upd and db_upd are not same, raise error
					raise RuntimeError("The length of csv_upd and db_upd are not same. [" + ', '.join(csv_upd) + "], [" + ', '.join(db_upd) + "]) 
					
				#-- check is_valid flag
				if is_valid_enable = 'Y': # need to check is_valid flag
					if self.__db_dict[r]['main']['is_valid']['value'] == 'N':
						actions.append('IS_VALID_TO_Y') # if is_valid=N in db, mark it Y
					elif self.__db_dict[r]['main']['is_valid']['value'] == 'Y' and (not 'UPD' in actions): # if is_valid=Y in db and no field update, no action required, delete key from both dict
						del self.__csv_dict[r]
						del self.__db_dict[r]
			else: # not exists in db
				actions.append('INS')
			
			# r may be delete from process above, so check existence first
			if r in self.__csv_dict:
				self.__csv_dict[r]['action'] == actions
			
		cloned_db_dict = self.__db_dict.deepcopy()
		for r in cloned_db_dict:
			if not r in self.__csv_dict:
				if 'is_valid' in self.__db_dict[r]['main'] and self.__db_dict[r]['main']['is_valid']['value'] == 'Y'：
					actions.append('IS_VALID_TO_N')
				else:
					del self.__db_dict[r]
					
			# r may be delete from process above, so check existence first
			if r in self.__db_dict:
				self.__db_dict[r]['action'] == actions
				
if __name__ == '__main__':
	db_dict = get_yaml('D:\\workspace\\Stock\\etc\\db.yml')
	conn = get_conn(db_dict["DB"], db_dict["Username"], db_dict["Password"], db_dict["Host"], db_dict["Port"])
	
	d = DB_insert_update(
		csv_file='D:\\workspace\\Stock\\data\\bankuai_20160219.csv', 
		csv_pk=[u'板块名称'], 
		csv_ins={u'子版块': 'char', u'板块名称': 'char', u'涨跌幅': 'char', u'总市值(亿)': 'decimal', u'换手率': 'decimal', u'上涨家数': 'int', u'下跌家数': 'int', u'领涨股票代码': 'char', u'领涨股票涨跌幅': 'decimal'}, 
		field_conversion={u'子版块': {u'概念板块': 1, u'地域板块': 2, u'行业板块': 3}},
		db_conn=conn,
		db_tab=u'dw.dim_bankuai', 
		db_pk=[u'id'], 
		db_ins=[u'id', u'name', u'parent_bankuai_id']
	)

	

