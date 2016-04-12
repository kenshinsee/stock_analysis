#!/usr/local/bin/python2.7
#coding:utf-8
import os
from distutils.sysconfig import get_python_lib
from Sys_paths import Sys_paths

SEP = os.path.sep
base_dir = Sys_paths.PROJ_BASE_DIR

print "-------------------------------------"
print "Installing stock.pth"
print "-------------------------------------"
lib_dir = get_python_lib()
stock_pth = lib_dir + SEP + 'stock.pth'

# The lib dir below should be updated to the correct path based on the env
lib_dir_for_stock_workspace = base_dir + SEP + 'lib'

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
    print stock_pth + " is already exists."
    
    
print "-------------------------------------"
print "Creating direcotories"
print "-------------------------------------"
"""
Stock
  --bin [git sync]
  --data  [***MANUALLY CREATE***]
    --stock_bankuai_daily
    --stock_daily
    --stock_transaction
  --db  [git sync]
    --ddl
      --tables
  --etc  [git sync]
    --table
  --lib  [git sync]
    --downloader
    --loader
    --object
    --object_impl
    --tooling
  --log  [***MANUALLY CREATE***]
"""

data_dir = {'data': ['stock_bankuai_daily','stock_daily','stock_transaction']}
for k,v in data_dir.items():
    if not os.path.exists(base_dir + SEP + k):
        os.makedirs(base_dir + SEP + k)
        print base_dir + SEP + k + ' has been created successfully.'
    else:
        print base_dir + SEP + k + ' is already exists.'
    for i in v:
        if not os.path.exists(base_dir + SEP + k + SEP + i):
            os.makedirs(base_dir + SEP + k + SEP + i)
            print base_dir + SEP + k + SEP + i + ' has been created successfully.'
        else:
            print base_dir + SEP + k + SEP + i + ' is already exists.'

log_dir = 'log'
if not os.path.exists(base_dir + SEP + log_dir):
    os.makedirs(base_dir + SEP + log_dir)
    print base_dir + SEP + log_dir + ' has been created successfully.'
else:
    print base_dir + SEP + log_dir + ' is already exists.'
    
    
