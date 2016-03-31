#!/usr/local/bin/python2.7
#coding:utf8
import random,threading,time,os
from Queue import Queue
from Sys_paths import Sys_paths
from psql import get_conn, get_cur
from common_tool import replace_vars, print_log, error_log, warn_log, get_date, recent_working_day, get_yaml, return_new_name_for_existing_file

#-- sys var
SEP = os.path.sep
YML_DIR = Sys_paths.YML_DIR
DB_YML = YML_DIR + SEP + "db.yml"

class Stock_trans_downloader(threading.Thread):
    def __init__(self, queue, conn, stock_trans_obj_name, stock_id, date):
        threading.Thread.__init__(self,name=stock_id + ':' + date)
        self.queue = queue
        self.conn = conn
        self.stock_id = stock_id
        self.date = date
        exec('from {object} import {object}'.format(object = stock_trans_obj_name), globals())
        self.stock_trans_object = eval('{object}({code}, {date})'.format(object=stock_trans_obj_name, code=stock_id, date=date))

    def insert_log_table(self):
      ins_sql = '''insert into dw.log_stock_transaction ( biz_date, stock_id, download_start_time ) values ( '{date}', '{stock}', '{start_time}' )
      '''.format(date=self.date, stock=self.stock_id, start_time=time.ctime())
      cur = get_cur(conn)
      cur.execute(ins_sql)
      conn.commit()
    
    def update_log_table(self, is_success=True):
      ins_sql = '''update dw.log_stock_transaction 
      set download_start_time = '{end_time}', is_download_success = '{is_success}'
      where biz_date = '{date}' and stock_id = '{stock}'
      '''.format(date=self.date, stock=self.stock_id, end_time=time.ctime(), is_success='Y' if is_success else 'N')
      cur = get_cur(conn)
      cur.execute(ins_sql)
      conn.commit()
    
    def run(self):
      self.queue.put(self.getName())
      # save data into local
      self.stock_trans_object.download_to_local()
      content = self.stock_trans_object.get_stock_content()
      for code in content:
          for date in content[code]:
              print content[code][date]
      time.sleep(1)
      self.queue.get()

##Consumer thread
#class Consumer_even(threading.Thread):
#  def __init__(self,thread_name,queue):
#    threading.Thread.__init__(self,name=thread_name)
#    self.data=queue
#  def run(self):
#    while 1:
#      try:
#        val_even = self.data.get(1,5) #get(self, block=True, timeout=None) ,1就是阻塞等待,5是超时5秒
#        if val_even%2==0:
#          print "%s: %s is consuming. %d in the queue is consumed!" % (time.ctime(),self.getName(),val_even)
#          time.sleep(2)
#        else:
#          self.data.put(val_even)
#          time.sleep(2)
#      except:   #等待输入，超过5秒 就报异常
#        print "%s: %s finished!" %(time.ctime(),self.getName())
#        break
#class Consumer_odd(threading.Thread):
#  def __init__(self,thread_name,queue):
#    threading.Thread.__init__(self, name=thread_name)
#    self.data=queue
#  def run(self):
#    while 1:
#      try:
#        val_odd = self.data.get(1,5)
#        if val_odd%2!=0:
#          print "%s: %s is consuming. %d in the queue is consumed!" % (time.ctime(), self.getName(), val_odd)
#          time.sleep(2)
#        else:
#          self.data.put(val_odd)
#          time.sleep(2)
#      except:
#        print "%s: %s finished!" % (time.ctime(), self.getName())
#        break
##Main thread
#def main():
#  queue = Queue()
#  producer = Producer('Pro.', queue)
#  consumer_even = Consumer_even('Con_even.', queue)
#  consumer_odd = Consumer_odd('Con_odd.',queue)
#  producer.start()
#  consumer_even.start()
#  consumer_odd.start()
#  producer.join()
#  consumer_even.join()
#  consumer_odd.join()
#  print 'All threads terminate!'

if __name__ == '__main__':
    queue = Queue()
    #-- fetch DB info
    db_dict = get_yaml(DB_YML)
    #-- open db connection
    conn = get_conn(db_dict["DB"], db_dict["Username"], db_dict["Password"], db_dict["Host"], db_dict["Port"])

    s = Stock_trans_downloader(queue, conn, 'Netease_stock_transaction', '300244', '20160331')
    s.start()
    s.join()
    print 'All done.'
    