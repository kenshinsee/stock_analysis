#!/usr/local/bin/python2.7
#coding:utf-8

import sys,os,re,datetime,yaml,csv
from common_tool import replace_vars, print_log, warn_log, error_log, get_date, get_yaml
from psql import get_conn, get_cur

def load_into_stock_bankuai(db_conn, file ):
	#-- load CSV
	csvf = open(file)
	csvr = csv.DictReader(csvf)
	bk_st_pairs = []
	bk_id_dict = {}
	
	# 板块	子版块		板块名称	股票代码	股票名称
	# 板块	概念板块	送转预期	600587		新华医疗
	for row in csvr:
		bk_name = row[u'板块名称'.encode("gbk")].decode("gbk")
		st_id = row[u'股票代码'.encode("gbk")].decode("gbk")
		bk_st_pairs.append([bk_name, st_id])
	csvf.close()
	print_log("%(num)s records have been read from %(fname)s." % {"num": len(bk_st_pairs), "fname": file})
	
	#---- get bankuai_id from dim_bankuai
	select_sql = "select t.id, t.name from dw.dim_bankuai t"
	cur = get_cur(db_conn)
	cur.execute(select_sql)
	db_rows = list(cur)
	for db_row in db_rows:
		db_name = db_row["name"].decode("utf-8")
		db_id = db_row["id"]
		bk_id_dict[db_name] = db_id
	
	#---- get bk_id, st_id from db, seach the combination in csv dict
	select_sql = "select t.stock_id, t.bankuai_id, t.is_valid from dw.dim_stock_bankuai t"
	cur.execute(select_sql)
	db_rows = list(cur)
	for db_row in db_rows:
		db_bk_id = db_row["bankuai_id"]
		db_st_id = db_row["stock_id"]
		db_is_valid = db_row["is_valid"]
		
		
		
		
		if db_id in codes and db_is_valid == "Y":
			if db_name == codes[db_id]:
				#delete from codes if it's already in the table and name is not changed.
				del codes[db_id]
			else: 
				#delete from codes, we will use codes_to_update dict to update the name 
				codes_to_update[db_id] = codes[db_id]
				del codes[db_id]
		elif db_id in codes and db_is_valid == "N":
			codes_to_valid.append("'" + str(db_id) + "'")
			del codes[db_id]
		elif db_is_valid == "N":
			# not in csv file and it's already invalid in db, do nothing
			pass
		else:
			# not in csv, but in db it's valid, mark it to invalid
			codes_to_invalid.append("'" + str(db_id) + "'")
			

if __name__ == "__main__":
	pass