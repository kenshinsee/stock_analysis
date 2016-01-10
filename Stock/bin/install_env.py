#!/usr/local/bin/python2.7
#coding:utf-8
import os
from distutils.sysconfig import get_python_lib

lib_dir = get_python_lib()
stock_pth = lib_dir + '/stock.pth'

# The lib dir below should be updated to the correct path based on the env
lib_dir_for_stock_workspace = 'd:/workspace/Stock/lib'

# Install python pth file
if not os.path.exists(stock_pth):
    print "Start to install " + stock_pth
    try:
        fh = open(stock_pth,'w')
        fh.write(lib_dir_for_stock_workspace + '\n')
        print ">>" + lib_dir_for_stock_workspace
        print stock_pth + " has been installed successfully."
    except:
        print 'Can\'t open ' + stock_pth
    finally:
        fh.close()
else:
    print stock_pth + " already exists."