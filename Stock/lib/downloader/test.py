#!/usr/bin/python2.7
# coding:utf-8


import re,sys,pprint,copy,csv,os
reload(sys)
sys.setdefaultencoding("gbk")
from tooling.common_tool import print_log, warn_log, read_url, get_date, return_new_name_for_existing_file
from Sys_paths import Sys_paths


page_code = read_url('http://stock.jrj.com.cn/share,600225,jjcg_3.shtml')

print page_code

