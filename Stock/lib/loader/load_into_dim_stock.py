#!/usr/local/bin/python2.7
#coding:utf-8

import sys,os,re,datetime,yaml,csv
from common_tool import replace_vars, print_log, warn_log, error_log, get_date, get_yaml
from psql import get_conn, get_cur

def load_into_dim_stock(db_conn, file ):
	#-- load CSV
	csvf = open(file)
	csvr = csv.DictReader(csvf)
	codes = {}
	codes_to_update = {}
	codes_to_valid = []
	codes_to_invalid = []

	# 板块	子版块		板块名称	股票代码	股票名称
	# 板块	概念板块	送转预期	600587		新华医疗
	for row in csvr:
		code = row[u'股票代码'.encode("gbk")].decode("gbk")
		name = row[u'股票名称'.encode("gbk")].decode("gbk")
		codes[code] = name
	csvf.close()
	print_log("%(num)s records have been read from %(fname)s." % {"num": len(codes.keys()), "fname": file})
	
	
	#---- get id, name from db, seach the combination in csv dict
	# if id exists but different name, update
	# if id doesn't exist, mark is_valid=N
	select_sql = "select t.id, t.name, t.is_valid from dw.dim_stock t /*where t.is_valid = 'Y'*/"
	cur = get_cur(db_conn)
	cur.execute(select_sql)
	db_rows = list(cur)

	for db_row in db_rows:
		db_name = db_row["name"].decode("utf-8")
		db_id = db_row["id"]
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
			
	#---- mark stocks is_valid=N
	if len(codes_to_invalid) > 0:
		codes_to_invalid_str = ",".join(codes_to_invalid)
		#print_log("Mark stock ids to invalid: " + codes_to_invalid_str)
		print_log("There are %(num)s stocks will be marked invalid. %(stocks)s" % {"num": len(codes_to_invalid), "stocks": codes_to_invalid_str})
		upd_sql = "update dw.dim_stock t set is_valid = 'N', upd_time = now() where t.id in (%(ids)s)" % {"ids": codes_to_invalid_str}
		cur.execute(upd_sql)
		db_conn.commit()
	else:
		print_log("No stocks need to be marked invalid.")

	#---- mark stocks is_valid=Y
	if len(codes_to_valid) > 0:
		codes_to_valid_str = ",".join(codes_to_valid)
		print_log("There are %(num)s stocks will be marked valid. %(stocks)s" % {"num": len(codes_to_valid), "stocks": codes_to_valid_str})
		upd_sql = "update dw.dim_stock t set is_valid = 'Y', upd_time = now() where t.id in (%(ids)s)" % {"ids": codes_to_valid_str}
		cur.execute(upd_sql)
		db_conn.commit()
	else:
		print_log("No stocks need to be marked valid.")
		
	#---- update stock names in dim_stock
	if len(codes_to_update.keys()) > 0:
		print_log("There are %(num)s stocks will be updated." % {"num": len(codes_to_update.keys())})
		for id in codes_to_update:
			print_log(id)
			upd_sql = "update dw.dim_stock t set name = '%(name)s', upd_time = now() where t.id = '%(id)s'" % {"id": id, "name": codes_to_update[id]}
			cur.execute(upd_sql)
		db_conn.commit()
	else:
		print_log("No stocks need to be updated.")
	
	#---- insert stocks into dim_stock
	if len(codes.keys()) > 0:
		values = []
		print_log("There are %(num)s stocks will be inserted." % {"num": len(codes.keys())})
		for b in codes:
			print_log(b)
			values.append("('%(id)s', '%(name)s', now(), 'Y')" % {"id": b, "name": codes[b]} )
		values_str = ",".join(values)
		ins_sql = "insert into dw.dim_stock(id, name, upd_time, is_valid) values %(values)s" % {"values": values_str}
		cur.execute(ins_sql)
		db_conn.commit()
	else:
		print_log("No new stock ids.")
	
	print_log("dw.dim_stock has been refreshed successfully.")

if __name__ == "__main__":
	db_dict = get_yaml('D:\\workspace\\Stock\\bin\\..\\etc\\db.yml')
	conn = get_conn(db_dict["DB"], db_dict["Username"], db_dict["Password"], db_dict["Host"], db_dict["Port"])
	
	#load_into_stock(conn, 'D:\\workspace\\Stock\\bin\\..\\log\\bankuai_stock_20160104.csv')
	load_into_stock(conn, 'D:\\workspace\\Stock\\bin\\..\\log\\test.csv')
	conn.close()

