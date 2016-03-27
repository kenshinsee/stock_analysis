#!/usr/local/bin/python2.7
#coding:utf-8
import sys,threading,Queue,time,random

def walk(sec):
    func_name = sys._getframe().f_code.co_name
    for i in range(2):
        print '\n{func} for iterator {num}... now it\'s {time}' . format(func=func_name, sec=sec, num=i, time=time.ctime())
        time.sleep(sec)
    
def run(sec):
    func_name = sys._getframe().f_code.co_name
    for i in range(2):
        print '\n{func} for iterator {num}... now it\'s {time}' . format(func=func_name, sec=sec, num=i, time=time.ctime())
        time.sleep(sec)
    
if __name__ == '__main__':
    walker1 = threading.Thread(target=walk, args=(2,))
    runner1 = threading.Thread(target=run, args=(5,))
    threads = [walker1, runner1]
    for t in threads:
        t.setDaemon(True)
        t.start()
    for t in threads:
        t.join()
    print '\nIt\'s the end ' + time.ctime()