#!/usr/local/bin/python2.7
#coding:utf-8
import sys,threading,Queue,time,random

q = Queue.Queue()
def walk(sec):
    func_name = sys._getframe().f_code.co_name
    for i in range(1):
        print '\n{func} for iterator {num}... now it\'s {time}' . format(func=func_name, sec=sec, num=i, time=time.ctime())
        time.sleep(sec)
        q.put((func_name, time.ctime()))
        print 'queue size: walk ' + str(q.qsize())
def run(sec):
    func_name = sys._getframe().f_code.co_name
    for i in range(1):
        print '\n{func} for iterator {num}... now it\'s {time}' . format(func=func_name, sec=sec, num=i, time=time.ctime())
        time.sleep(sec)
        q.put((func_name, time.ctime()))
        print 'queue size: run ' + str(q.qsize())

if __name__ == '__main__':
    result = []
    walker1 = threading.Thread(target=walk, args=(5,))
    runner1 = threading.Thread(target=run, args=(5,))
    threads = [walker1, runner1]
    for t in threads:
        print '\n ------------------ before start: ' + time.ctime()
        t.setDaemon(True)
        t.start()
        print '\n ================== after start: ' + time.ctime()

    for t in threads:
        print '\n ****************** before join: ' + time.ctime()
        t.join()
        print '\n &&&&&&&&&&&&&&&&&& after join: ' + time.ctime()
    
    print 'QUEUE SIZE: ' + str(q.qsize())
    
    while not q.empty():
        result.append(q.get())
        print 'QUEUE SIZE: ' + str(q.qsize())
    print 'QUEUE SIZE: ' + str(q.qsize())

    print result
    print '\nIt\'s the end ' + time.ctime()