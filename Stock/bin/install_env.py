#!/usr/bin/python2.7
#coding:utf-8
import os,re
from optparse import OptionParser
from distutils.sysconfig import get_python_lib

SEP = os.path.sep


parser = OptionParser()
parser.add_option("--base_dir", "-d", dest="base_dir", action="store", help="Base directory of the project")
parser.add_option("--user", "-u", dest="user", action="store", default='hong', help="By default, the user is hong")
(options, args) = parser.parse_args()

if options.base_dir is None:
    raise RuntimeError('Base dir must be specified!')
elif not os.path.exists(options.base_dir):
    raise RuntimeError(options.base_dir + ' doesn\'t exist!')

base_dir = options.base_dir

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
# create the directories marked as MANUALLY CREATE
data_dir = {'data': ['stock_bankuai_daily','stock_daily','stock_transaction']}
for k,v in data_dir.items():
    if not os.path.exists(base_dir + SEP + k):
        os.makedirs(base_dir + SEP + k)
        os.system('chgrp {who} {path}'.format(who=options.user, path=base_dir + SEP + k))
        os.system('chmod g+w {path}'.format(path=base_dir + SEP + k))
        print base_dir + SEP + k + ' has been created successfully.'
    else:
        print base_dir + SEP + k + ' is already exists.'
        
    for i in v:
        if not os.path.exists(base_dir + SEP + k + SEP + i):
            os.makedirs(base_dir + SEP + k + SEP + i)
            os.system('chgrp {who} {path}'.format(who=options.user, path=base_dir + SEP + k + SEP + i))
            os.system('chmod g+w {path}'.format(path=base_dir + SEP + k + SEP + i))
            print base_dir + SEP + k + SEP + i + ' has been created successfully.'
        else:
            print base_dir + SEP + k + SEP + i + ' is already exists.'

log_dir = 'log'
if not os.path.exists(base_dir + SEP + log_dir):
    os.makedirs(base_dir + SEP + log_dir)
    os.system('chgrp {who} {path}'.format(who=options.user, path=base_dir + SEP + log_dir))
    os.system('chmod g+w {path}'.format(path=base_dir + SEP + log_dir))
    print base_dir + SEP + log_dir + ' has been created successfully.'
else:
    print base_dir + SEP + log_dir + ' is already exists.'
    
    
print "-------------------------------------"
print "Update PROJ_BASE_DIR in Sys_paths.py"
print "-------------------------------------"
sys_paths_file = base_dir + SEP + 'lib' + SEP + 'Sys_paths.py'
tmp_sys_paths_file = base_dir + SEP + 'lib' + SEP + 'Sys_paths.py.tmp'
if os.path.exists(sys_paths_file):
    if os.path.exists(tmp_sys_paths_file):
        os.remove(tmp_sys_paths_file)
    fh = open(sys_paths_file, 'r')
    data = fh.read()
    new_data = re.sub(r'\s*PROJ_BASE_DIR = "(?P<value>.+)"',lambda m:'\n    PROJ_BASE_DIR = "' + base_dir + '"',data)
    new_fh = open(tmp_sys_paths_file,'w')
    new_fh.write(new_data)
    fh.close()
    new_fh.close()
    
    os.remove(sys_paths_file)
    os.rename(tmp_sys_paths_file, sys_paths_file)
    os.system('chown {who}:{who} {file}'.format(who=options.user, file=sys_paths_file))
    os.system('chmod g+w {file}'.format(file=sys_paths_file))
    print sys_paths_file + ' was updated with new project base directory.'
else:
    raise RuntimeError(base_dir + SEP + 'lib' + SEP + 'Sys_paths.py doesn\'t not exist, please check.')

    
    
    
    

