import sys,os,re,datetime,cookielib,urllib,urllib2,yaml
from psql import get_conn, get_cur
from urllib2 import HTTPError
from common_tool import replace_vars, print_log, error_log, warn_log, get_date, recent_working_day, get_yaml, return_new_name_for_existing_file

#the script will dynamically load module, no need to load class modules at the beginning
#from Sina_stock import Sina_stock
#from Tengxun_stock import Tengxun_stock
#from Yahoo_stock import Yahoo_stock

def insert_into_table(db_field_yaml, stock_obj_name, in_file, conn, log_fh, warn_fh):
	# based on the fields mapping between db and object, db type defined in yaml, generate delete sql and insert sql, and fire to db
	# this function could be used for any db insert, if yaml and object are setup properly
	# Yaml example
	# biz_date: 
	#   type: date
	#   is_pk: Y
	#   stock_object: 
	# 		Tengxun_stock: date
	db_field_mapping = get_yaml(db_field_yaml)
	tab_name = os.path.basename(db_field_yaml).replace('.yml', '') # yml file name as table name
	tab_fields = [] # table field names
	tab_pk = [] # table pk
	tab_types = [] # table field types
	obj_attrs = [] # attribute names in stock object
	for k,v in db_field_mapping.items():
		tab_type = v['type']
		obj_attr = v['stock_object'][stock_obj_name]
		if obj_attr != None: # If None|Null is set for fields in yml, remove the fields from insertion
			tab_fields.append(k)
			if v['is_pk'] == 'Y': tab_pk.append(k) # pk, delete before insert
			tab_types.append(tab_type)
			obj_attrs.append(obj_attr)
	del_sql = 'delete from {tab_name} where 1=1 '.format(tab_name=tab_name)
	ins_sql = 'insert into {tab_name}({fields}) '.format(tab_name=tab_name, fields=','.join(tab_fields))
	# iterate each row in the file, insert into table
	num = 0
	with open(in_file) as f:
		for row in f.readlines():
			# get_stock_object_from_str is a function should be available in all the stock objects
			# this function accepts the string returned from website and generate a dict for stock object
			# the dict is like {stock: {date: object}}
			###if re.match(r'pv_none_match', row) or re.match(r'.+"";$', row): # match empty from tengxun and sina
			###	warn_log('No content fetched for ' + k, warn_fh)
			###	continue
			# dynamically import object module, class name and file name should be identical
			exec('from {object} import {object}'.format(object = stock_obj_name), globals())
			stock_dict = eval('{object}.get_stock_object_from_str(row)'.format(object=stock_obj_name, row=row))
			for stock in stock_dict: # for Tengxun or sina interface, there is just one stock in one stock dict
				for date in stock_dict[stock]: # for Tengxun or sina interface, there is just one date in one stock dict
					stock_obj = stock_dict[stock][date] # this object is stock implementation object
					value_sql = reduce(lambda x, y: ( x if re.match(r'stock_obj', x) else 'stock_obj.' + x + ', ' ) + "stock_obj.{attr_name}, ".format(attr_name=y), obj_attrs) # add 'stock_obj.' to the first attr, and concatenate attrs to a string
					value_sql = value_sql[0:-2] # remove the last comma and the blankspace next to it
					value_sql = eval(value_sql) # tupe returned
					final_value_sql = ''
					del_where = ''
					for i, v in enumerate(value_sql):
						value = "'" + v + "'" if tab_types[i] == 'date' or tab_types[i] == 'varchar' else 'Null' if len(str(v)) == 0 else str(v) # date and varchar quoted by single quote, otherwise no quote or null(if length of value is 0)
						final_value_sql = final_value_sql + value + ', '
						if tab_fields[i] in tab_pk: 
							del_where = del_where + ' and {field}={value}'.format(field=tab_fields[i], value=value)
					final_value_sql = final_value_sql[0:-2]
					del_complete_sql = del_sql + del_where
					ins_complete_sql = ins_sql + ' values( ' + final_value_sql + ')'
					#print_log('Deleting [{stock},{date}] from {tab_name}...\n {sql}'.format(stock=stock,date=date,tab_name=tab_name,sql=del_complete_sql), log_fh)
					cur = get_cur(conn)
					cur.execute(del_complete_sql)
					cur.execute(ins_complete_sql)
					print_log('Inserted [{stock},{date}] into {tab_name}.'.format(stock=stock,date=date,tab_name=tab_name), log_fh)
					num += 1
					if num % 1000 == 0: conn.commit()
	conn.commit()
	print_log('{num} records have been written into {tab_name}.'.format(num=num, tab_name=tab_name), log_fh)

