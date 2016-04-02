#!/usr/local/bin/python2.7
#coding:utf8
import random,threading,time,os
from Queue import Queue
from Sys_paths import Sys_paths
from psql import get_conn, get_cur
from common_tool import replace_vars, print_log, error_log, warn_log, get_date, recent_working_day, get_yaml, return_new_name_for_existing_file
import traceback  

#-- sys var
SEP = os.path.sep
YML_DIR = Sys_paths.YML_DIR
DB_YML = YML_DIR + SEP + "db.yml"

class Stock_trans_downloader(threading.Thread):
    def __init__(self, queue, conn, stock_trans_obj_name, stock_id, date, in_out_file=None):
        threading.Thread.__init__(self,name=stock_id + '-' + date)
        self.queue = queue
        self.conn = conn
        self.stock_id = stock_id
        self.date = date
        exec('from {object} import {object}'.format(object = stock_trans_obj_name), globals())
        self.stock_trans_object = eval("{object}('{code}', '{date}')".format(object=stock_trans_obj_name, code=str(stock_id), date=date))
        #by default, store the out file into the same directory as download file
        self.out_file = ( os.path.dirname(self.stock_trans_object.download_file) + SEP + stock_id + '.txt' ) if in_out_file == None else in_out_file

    def get_row_id(self):
        row_id_sql = "select nextval('dw.seq_log_stock_trans_row_id') as row_id"
        cur = get_cur(conn)
        cur.execute(row_id_sql)
        db_rows = list(cur)
        self.row_id = db_rows[0]['row_id']
        return self.row_id
        
    def insert_log_table(self):
        ins_sql = '''insert into dw.log_stock_transaction ( row_id, biz_date, stock_id, download_start_time ) values ( {row_id}, '{date}', '{stock}', '{start_time}' )
        '''.format(row_id=self.row_id, date=self.date, stock=self.stock_id, start_time=time.ctime())
        cur = get_cur(conn)
        cur.execute(ins_sql)
        conn.commit()
    
    def update_log_table(self, is_success=True):
        ins_sql = '''update dw.log_stock_transaction 
        set download_end_time = '{end_time}', is_download_success = '{is_success}'
        where row_id = {row_id}
        '''.format(row_id=self.row_id, end_time=time.ctime(), is_success='Y' if is_success else 'N')
        cur = get_cur(conn)
        cur.execute(ins_sql)
        conn.commit()

    def download_to_local(self):
        # save raw data into local
        # if file already exists and size >= 5KB, it doesn't download again.
        if os.path.exists(self.stock_trans_object.download_file) and os.path.getsize(self.stock_trans_object.download_file) >= 1024 * 5:
            print_log(self.stock_trans_object.download_file + ' already exists.')
        else:
            self.stock_trans_object.download_to_local()
    
    def save_formatted_data(self):
        # save formatted data into file, \t as delimiter
        # 9:25:00    50.34   0.15    141 709794  买盘
        with open(self.out_file, 'w') as file:
            file.write(self.stock_trans_object.get_stock_content()[self.stock_id][self.date])
        print_log('Formatted data saved to ' + self.out_file)

    def run(self):
        self.queue.put(self.getName())
        print 'queue name: ' + self.getName() + ' joined.'
        print 'queue size at the moment: ' + str(self.queue.qsize())
        row_id = self.get_row_id()
        self.insert_log_table()
        try:
            self.download_to_local()
            self.update_log_table(is_success=True)
            self.save_formatted_data()
        except:
            traceback.print_exc()
            self.update_log_table(is_success=False)
            raise RuntimeError('Download {stock_id} for {date} failed.'.format(stock_id=self.stock_id, date=self.date))
        finally:
            queue_name = self.queue.get()
            print 'queue name: ' + queue_name + ' shifted out.'
    
    
if __name__ == '__main__':
    queue = Queue()
    #-- fetch DB info
    db_dict = get_yaml(DB_YML)
    #-- open db connection
    conn = get_conn(db_dict["DB"], db_dict["Username"], db_dict["Password"], db_dict["Host"], db_dict["Port"])
 
    s = Stock_trans_downloader(queue, conn, 'Netease_stock_transaction', '300244', '20160401')
    s1 = Stock_trans_downloader(queue, conn, 'Sina_stock_transaction', '000005', '20160401')
    s2 = Stock_trans_downloader(queue, conn, 'Tengxun_stock_transaction', '600100', '20160401')
    s.start()
    s1.start()
    s2.start()
    s.join()
    s1.join()
    s2.join()

    print 'queue size at the moment: ' + str(queue.qsize())
    print 'All done.'
