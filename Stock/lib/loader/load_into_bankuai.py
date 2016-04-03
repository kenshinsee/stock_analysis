#!/usr/local/bin/python2.7
#coding:utf-8

import sys,os,re,datetime,yaml,csv
from tooling.common_tool import replace_vars, print_log, warn_log, error_log, get_date, get_yaml
from tooling.psql import get_conn, get_cur

def load_into_bankuai(db_conn, file, biz_date=None ):

# 板块	子版块		板块名称	涨跌幅	总市值(亿)	换手率	上涨家数	下跌家数	领涨股票代码	领涨股票	领涨股票涨跌幅
# 板块	概念板块	全息技术	3.95%	365.12		11.65	7			1			600288			大恒科技	10.03
# 板块	概念板块	网络安全	2.95%	818.79		25.61	19			1			002308			威创股份	10.01

# biz_date date not null,
# bankuai_id integer not null,
# rise varchar(16),
# market_value_in_million decimal(12,2),
# turnover_rate decimal(5,2),
# num_of_rise integer,
# num_of_drop integer,
# leading_stock_id varchar(6),
# rise_of_leading_stock decimal(10,2),
# primary key(biz_date, bankuai_id)
	
	bk_id_dict = {}
	csv_data = []
	v_biz_date = ""
	
	#-- build dict for bankuai name and bankuai id from db
	select_sql = 'select t.name, t.id from dw.dim_bankuai t'
	cur = get_cur(db_conn)
	cur.execute(select_sql)
	db_rows = list(cur)
	for db_row in db_rows:
		db_name = db_row["name"].decode("utf-8")
		db_id = db_row["id"]
		bk_id_dict[db_name] = db_id
	
	print_log("There are %(num)s records read from %(name)s" % {"num": len(bk_id_dict.keys()), "name": 'dw.dim_bankuai'})

	#-- load CSV
	csvf = open(file)
	csvr = csv.DictReader(csvf)
	for row in csvr:
		bk_name = row[u'板块名称'.encode("gbk")].decode("gbk")
		bk_id = bk_id_dict[bk_name]
		row_dict = {}
		row_dict[bk_id] = {}
		row_dict[bk_id]["rise"] = row[u'涨跌幅'.encode("gbk")].decode("gbk")
		row_dict[bk_id]["market_value_in_million"] = row[u'总市值(亿)'.encode("gbk")]
		row_dict[bk_id]["turnover_rate"] = row[u'换手率'.encode("gbk")]
		row_dict[bk_id]["num_of_rise"] = row[u'上涨家数'.encode("gbk")]
		row_dict[bk_id]["num_of_drop"] = row[u'下跌家数'.encode("gbk")]
		row_dict[bk_id]["leading_stock_id"] = row[u'领涨股票代码'.encode("gbk")]
		row_dict[bk_id]["rise_of_leading_stock"] = row[u'领涨股票涨跌幅'.encode("gbk")]
		
		csv_data.append(row_dict)
		
	csvf.close()
	print_log("%(num)s records have been read from %(name)s." % {"num": len(csv_data), "name": file})

	#-- determine biz_date
	if not biz_date is None: 
		if re.search(r'\d{8}', biz_date):
			v_biz_date = biz_date
		else:
			raise RuntimeError(biz_date + " is not a valid date format, the date should be like YYYYMMDD.") 
	elif re.search(r'.*(?P<date>\d{8})\.csv', file):
		v_biz_date = re.search(r'.*(?P<date>\d{8})\.csv', file).group("date")
	else:
		raise RuntimeError('Can not determine biz_date, please check if file name has date included or pass biz_date when calling the function.')
	v_biz_date_dt = datetime.datetime.strptime(v_biz_date,'%Y%m%d')
	
	#-- delete biz_date from dw.bankuai
	del_sql = 'delete from dw.bankuai where biz_date = \'%(date)s \'' % {'date': v_biz_date_dt}
	cur.execute(del_sql)
	db_conn.commit()
	print_log("Deleted records from dw.bankuai where biz_date = '%(biz_date)s'." % {"biz_date": v_biz_date})

	#-- insert into dw.bankuai
	iter = 0
	for r in csv_data:
		k = r.keys()[0]
		iter += 1
		ins_sql = '''insert into dw.bankuai(
			biz_date, 
			bankuai_id, 
			rise, 
			market_value_in_million, 
			turnover_rate, 
			num_of_rise, 
			num_of_drop, 
			leading_stock_id, 
			rise_of_leading_stock) values(
			'%(biz_date)s',
			%(bankuai_id)s, 
			'%(rise)s', 
			%(market_value_in_million)s, 
			%(turnover_rate)s, 
			%(num_of_rise)s, 
			%(num_of_drop)s, 
			'%(leading_stock_id)s', 
			%(rise_of_leading_stock)s
			)''' % {
			'biz_date': v_biz_date_dt, 
			'bankuai_id': k, 
			'rise': r[k]['rise'], 
			'market_value_in_million': r[k]['market_value_in_million'], 
			'turnover_rate': r[k]['turnover_rate'], 
			'num_of_rise': r[k]['num_of_rise'], 
			'num_of_drop': r[k]['num_of_drop'], 
			'leading_stock_id': r[k]['leading_stock_id'] if r[k]['leading_stock_id'] != '-' else '000000', # sometimes eastmoney doesn't return valid leading stock id, but '-', for this case, '000000' would replace it as an unknown stock id
			'rise_of_leading_stock': r[k]['rise_of_leading_stock']
			}
		cur.execute(ins_sql)
		
	db_conn.commit()
	print_log( str(iter) + " inserted into dw.bankuai.")
	print_log("dw.bankuai has been refreshed successfully.")


if __name__ == "__main__":
	db_dict = get_yaml('D:\\workspace\\Stock\\bin\\..\\etc\\db.yml')
	conn = get_conn(db_dict["DB"], db_dict["Username"], db_dict["Password"], db_dict["Host"], db_dict["Port"])
	
	load_into_bankuai(conn, 'D:\\workspace\\Stock\\bin\\..\\data\\bankuai_20160104.csv')
	conn.close()
