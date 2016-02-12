#!/usr/local/bin/python2.7
# coding:utf-8

import sys, os, re, datetime
import psycopg2, psycopg2.extras

def get_conn(dbname, uname, passwd, host, port):
	return psycopg2.connect(database=dbname, user=uname, password=passwd, host=host, port=port)
	
def get_cur(conn, cursor_factory=psycopg2.extras.RealDictCursor):
	return conn.cursor(cursor_factory=cursor_factory)
	
	
	
if __name__ == "__main__":
	now = datetime.datetime.now()
	print now

	conn = get_conn("StockDb", "hong", "hong", "192.168.119.128", "5432")
	dict_cur = get_cur(conn)
	dict_cur.execute("SELECT * FROM DW.DIM_PARENT_BANKUAI")
	result = dict_cur.fetchall()
	print result[0]["name"].decode("utf-8")
	dict_cur.execute("""INSERT INTO DW.DIM_PARENT_BANKUAI(ID, NAME, UPD_TIME) VALUES (%(id)s, %(name)s, %(upd_time)s)""",  
     {'id': 10, 'name': "test", 'upd_time': now} )
	conn.commit()
	dict_cur.close()
	conn.close()