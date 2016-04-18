#!/usr/local/bin/python2.7
#coding:utf8
# This module is to call object impl classes to download stock transaction data
# It downloads raw data from internet and convert it into a standard format
# It is an implementation of threading, and it put a spaceholder into queue when it gets started and remove it from queue when it is finished, so the outer caller could count on the queue size to see how many threads are running.


import random,threading,time,os,traceback,datetime
from Queue import Queue
from Sys_paths import Sys_paths
from tooling.psql import get_conn, get_cur
from tooling.common_tool import replace_vars, print_log, error_log, warn_log, get_date, recent_working_day, get_yaml, return_new_name_for_existing_file
from tooling.db_func import inserter, get_query_result, psql_copy_from

#-- sys var
SEP = Sys_paths.SEP
DB_YML = Sys_paths.YML_DIR + SEP + "db.yml"
DATA_DIR = Sys_paths.DATA_STOCK_TRANSACTION
TABLE = 'dw.stock_transaction'
COLS = 'stock_id,biz_date,time,trans_price,price_change,volume,amount,buy_sell,source'
DB_NAME = get_yaml(DB_YML)["DB"]

class Stock_trans_loader(threading.Thread):
    def __init__(self, queue, conn, log_row_id, stock_id, date, file=None, enable_copy=False):
        threading.Thread.__init__(self, name=stock_id + '-' + date)
        self.queue = queue
        self.conn = conn
        self.log_row_id = log_row_id
        self.stock_id = stock_id
        self.date = date
        self.file = DATA_DIR + SEP + date + SEP + stock_id + '.txt' if file is None else file
        self.enable_copy = enable_copy
        
    def check_row_id_existance(self):
        sel_sql = '''
        select count(*) as count from dw.log_stock_transaction where row_id = {0} and stock_id = '{1}' and biz_date = '{2}'
        '''.format(self.log_row_id, self.stock_id, self.date)
        row_count = get_query_result(self.conn, sel_sql)[0]['count']
        if row_count == 0: raise RuntimeError('Row id {0} is not found for {1}:{2}'.format(self.log_row_id, self.stock_id, self.date))
    
    def log_load_start(self):
        upd_sql = '''
        update dw.log_stock_transaction
        set load_start_time = '{0}'
        where row_id = {1} and stock_id = '{2}' and biz_date = '{3}'
        '''.format(time.ctime(), self.log_row_id, self.stock_id, self.date)
        get_query_result(self.conn, upd_sql)
        self.conn.commit()
        
    def log_load_end(self, is_success=True):
        upd_sql = '''
        update dw.log_stock_transaction
        set load_end_time = '{0}', is_load_success = '{1}'
        where row_id = {2} and stock_id = '{3}' and biz_date = '{4}'
        '''.format(time.ctime(), 'Y' if is_success else 'N', self.log_row_id, self.stock_id, self.date)
        get_query_result(self.conn, upd_sql)
        self.conn.commit()
    
    def delete_existing_records(self):
        del_sql = '''
        delete from dw.stock_transaction where stock_id = '{0}' and biz_date = '{1}'
        '''.format(self.stock_id, datetime.datetime.strptime(self.date,'%Y%m%d'))
        get_query_result(self.conn, del_sql)
        print_log('Deletion for {0} {1} completed successfully.'.format(self.stock_id, self.date))
        
    def run(self):
        self.check_row_id_existance()
        self.queue.put(self.getName())
        self.log_load_start()
        self.delete_existing_records()
        try:
            if self.enable_copy:
                print_log('psql copy...')
                psql_copy_from(DB_NAME, 'dw.stock_transaction', self.file, args=' with (encoding \'GBK\')')
            else:
                print_log('psql insert...')
                inserter(self.conn, TABLE, COLS, 'file', self.file, '\t')
            self.log_load_end(is_success=True)
            print_log('Loading {stock_id} for {date} completes successfully.'.format(stock_id=self.stock_id, date=self.date))
        except:
            traceback.print_exc()
            self.log_load_end(is_success=False)
            raise RuntimeError('Loading {stock_id} for {date} failed.'.format(stock_id=self.stock_id, date=self.date))
        finally:
            queue_name = self.queue.get()
    
    
if __name__ == '__main__':
    queue = Queue()
    #-- fetch DB info
    db_dict = get_yaml(DB_YML)
    #-- open db connection
    conn = get_conn(db_dict["DB"], db_dict["Username"], db_dict["Password"], db_dict["Host"], db_dict["Port"])

    s = Stock_trans_loader(queue, conn, '57', '300250', "20160401", enable_copy=True)
    s.start()
    s.join()
    
    print 'All done.'
