#!/usr/local/bin/python2.7
#coding:utf-8

import sys,os,re,datetime,yaml,csv
from common_tool import replace_vars, print_log, warn_log, error_log, get_date, get_yaml
from psql import get_conn, get_cur

def load_into_dim_stock_bankuai(db_conn, file ):
	#-- load CSV
	csvf = open(file)
	csvr = csv.DictReader(csvf)
	bk_st_pairs = []
	bk_st_pairs_dict = {}
	bk_id_dict = {}
	
	codes_to_valid = []
	codes_to_invalid = []
	
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
	
	#---- convert to dict 
	for i in range(len(bk_st_pairs)):
		bk_st_pairs[i][0] = bk_id_dict[bk_st_pairs[i][0]]
		bk_st_pairs[i].append(str(bk_st_pairs[i][0]) + "-" + str(bk_st_pairs[i][1])) # as PK
		bk_st_pairs_dict[bk_st_pairs[i][2]] = {"bk": bk_st_pairs[i][0], "st": bk_st_pairs[i][1]}
		
	#---- get bk_id, st_id from db, seach the combination in csv dict
	select_sql = "select t.stock_id, t.bankuai_id, t.is_valid from dw.dim_stock_bankuai t"
	cur.execute(select_sql)
	db_rows = list(cur)
	for db_row in db_rows:
		db_bk_id = db_row["bankuai_id"]
		db_st_id = db_row["stock_id"]
		db_pk = str(db_bk_id) + "-" + db_st_id
		db_is_valid = db_row["is_valid"]
		
		if db_pk in bk_st_pairs_dict and db_is_valid == "Y":
			del bk_st_pairs_dict[db_pk]
		elif db_pk in bk_st_pairs_dict and db_is_valid == "N":
			codes_to_valid.append(" ( bankuai_id = " + str(db_bk_id) + " and stock_id = '" + str(db_st_id) + "' ) ")
			del bk_st_pairs_dict[db_pk]
		elif db_is_valid == "N":
			# not in csv file and it's already invalid in db, do nothing
			pass
		else:
			# not in csv, but in db it's valid, mark it to invalid
			codes_to_invalid.append(" ( bankuai_id = " + str(db_bk_id) + " and stock_id = '" + str(db_st_id) + "' ) ")
			
	#---- mark is_valid=N
	if len(codes_to_invalid) > 0:
		codes_to_invalid_str = " or ".join(codes_to_invalid)
		print_log("There are %(num)s stock bankuai combination will be marked invalid. %(combination)s" % {"num": len(codes_to_invalid), "combination": codes_to_invalid_str})
		upd_sql = "update dw.dim_stock_bankuai t set is_valid = 'N', upd_time = now() where %(combinations)s" % {"combinations": codes_to_invalid_str}
		cur.execute(upd_sql)
		db_conn.commit()
	else:
		print_log("No stock bankuai combinations need to be marked invalid.")			

	#---- mark is_valid=Y
	if len(codes_to_valid) > 0:
		codes_to_valid_str = " or ".join(codes_to_valid)
		print_log("There are %(num)s stock bankuai combination will be marked valid. %(combination)s" % {"num": len(codes_to_valid), "combination": codes_to_valid_str})
		upd_sql = "update dw.dim_stock_bankuai t set is_valid = 'Y', upd_time = now() where %(combinations)s" % {"combinations": codes_to_valid_str}
		cur.execute(upd_sql)
		db_conn.commit()
	else:
		print_log("No stock bankuai combinations need to be marked valid.")			

	#---- insert stocks into dim_stock_bankuai
	if len(bk_st_pairs_dict.keys()) > 0:
		values = []
		print_log("There are %(num)s stock bankuai combination will be inserted." % {"num": len(bk_st_pairs_dict.keys())})
		for pk in bk_st_pairs_dict:
			print_log(pk)
			values.append("('%(stock_id)s', '%(bankuai_id)s', now(), 'Y')" % {"stock_id": bk_st_pairs_dict[pk]["st"], "bankuai_id": bk_st_pairs_dict[pk]["bk"]} )
		values_str = ",".join(values)
		ins_sql = "insert into dw.dim_stock_bankuai(stock_id, bankuai_id, upd_time, is_valid) values %(values)s" % {"values": values_str}
		cur.execute(ins_sql)
		db_conn.commit()
	else:
		print_log("No new stock bankuai combination.")

	print_log("dw.dim_stock_bankuai has been refreshed successfully.")

		
if __name__ == "__main__":
	db_dict = get_yaml('D:\\workspace\\Stock\\bin\\..\\etc\\db.yml')
	conn = get_conn(db_dict["DB"], db_dict["Username"], db_dict["Password"], db_dict["Host"], db_dict["Port"])
	
	load_into_stock_bankuai(conn, 'D:\\workspace\\Stock\\bin\\..\\log\\bankuai_stock_20160104.csv')
	conn.close()
