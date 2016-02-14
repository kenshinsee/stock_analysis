#!/usr/local/bin/python2.7
#coding:utf-8

import sys,os,re,datetime,yaml,csv
from common_tool import replace_vars, print_log, warn_log, error_log, get_date, get_yaml
from psql import get_conn, get_cur

def load_into_bankuai(db_conn, file, parent_bankuai_ids ):
	#-- load CSV
	csvf = open(file)
	csvr = csv.DictReader(csvf)
	bankuais = {}
	invalid_bankuai_ids = []

	#---- get parent_bankuai_id, bankuai_name from csv
	for row in csvr:
		bankuai = row[u'板块名称'.encode("gbk")].decode("gbk")
		parent_bankuai = row[u'子版块'.encode("gbk")].decode("gbk")
		parent_bankuai_id = parent_bankuai_ids[parent_bankuai]
		bankuais[bankuai] = {}
		bankuais[bankuai]["parent_bankuai_id"] = parent_bankuai_id
		#bankuais[bankuai].setdefault("parent_bankuai_id", parent_bankuai_id)
	csvf.close()
	print_log("%(num)s records have been read from %(fname)s." % {"num": len(bankuais.keys()), "fname": file})
	
	#---- get parent_bankuai_id, bankuai_name from db, seach the combination in csv dict, if it doesn't exist, add to invalid_bankuai_ids
	select_sql = "select t.parent_bankuai_id, t.name, t.id from dw.dim_bankuai t where t.is_valid = 'Y'"
	cur = get_cur(db_conn)
	cur.execute(select_sql)
	db_rows = list(cur)

	for db_row in db_rows:
		db_bankuai = db_row["name"].decode("utf-8")
		db_parent_bankuai_id = db_row["parent_bankuai_id"]
		db_id = db_row["id"]
		
		if db_bankuai in bankuais:
			if db_parent_bankuai_id == bankuais[db_bankuai]["parent_bankuai_id"]:
				#delete from bankuais if it's already in the table and is_valid=Y
				del bankuais[db_bankuai]
			else: 
				invalid_bankuai_ids.append(str(db_id))
		else:
			invalid_bankuai_ids.append(str(db_id))

	#---- mark bankuais is_valid=N
	if len(invalid_bankuai_ids) > 0:
		invalid_bankuai_ids_str = ",".join(invalid_bankuai_ids)
		print_log("Invalid bankuai ids: " + invalid_bankuai_ids_str)
		upd_sql = "update dw.dim_bankuai t set is_valid = 'N', upd_time = now() where t.id in (%(ids)s)" % {"ids": invalid_bankuai_ids_str}
		cur.execute(upd_sql)
		db_conn.commit()
	else:
		print_log("No invalid bankuai ids.")
		
	#---- insert bankuais into dim_bankuai
	if len(bankuais.keys()) > 0:
		values = []
		print_log("There are %(num)s bankuais will be inserted." % {"num": len(bankuais.keys())})
		for b in bankuais:
			values.append("('%(name)s', '%(parent_bankuai_id)s', now(), 'Y')" % {"name": b, "parent_bankuai_id": bankuais[b]["parent_bankuai_id"]} )
		values_str = ",".join(values)
		ins_sql = "insert into dw.dim_bankuai(name, parent_bankuai_id, upd_time, is_valid) values %(values)s" % {"values": values_str}
		cur.execute(ins_sql)
		db_conn.commit()
	else:
		print_log("No new bankuai ids.")
	
	print_log("dw.dim_bankuai has been refreshed successfully.")

if __name__ == "__main__":
	def return_parent_bankuai_ids(db_conn):
		query = "SELECT ID, NAME FROM DW.DIM_PARENT_BANKUAI"
		cur = get_cur(db_conn)
		cur.execute(query)
		rows = list(cur)
		return_dict = {}
		for row in rows:
			return_dict[row["name"].decode("utf-8")] = row["id"]
		cur.close()
		return return_dict

	db_dict = get_yaml('D:\\workspace\\Stock\\bin\\..\\etc\\db.yml')
	conn = get_conn(db_dict["DB"], db_dict["Username"], db_dict["Password"], db_dict["Host"], db_dict["Port"])
	
	parent_bankuai_ids = return_parent_bankuai_ids(conn)
	load_into_bankuai(conn, 'D:\\workspace\\Stock\\bin\\..\\log\\bankuai_20160205.csv', parent_bankuai_ids)
	conn.close()
