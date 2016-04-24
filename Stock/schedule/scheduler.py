#!/usr/bin/python2.7

import taskflow.engines
from taskflow.patterns import linear_flow
from taskflow import task
from tooling.common_tool import replace_vars, print_log, error_log, warn_log, get_date, recent_working_day, get_yaml, return_new_name_for_existing_file
from tooling.psql import get_conn, get_cur
from tooling.db_func import get_query_result

from Task_download_stock_bankuai import Task_download_stock_bankuai
from Task_recon_stock_bankuai import Task_recon_stock_bankuai
from Task_download_stock_eod import Task_download_stock_eod
from Task_download_stock_transaction import Task_download_stock_transaction

def flow_watch(state, details):
    print('Flow State: {}'.format(state))
    print('Flow Details: {}'.format(details))

def task_watch(state, details):
    print('Task State: {}'.format(state))
    print('Task Details: {}'.format(details))


flow = linear_flow.Flow('Eod loading').add(
    Task_download_stock_bankuai('download_stock_bankuai'),
    Task_recon_stock_bankuai('recon_stock_bankuai'),
    Task_download_stock_eod('download_stock_eod'),
    #Task_download_stock_transaction('download_stock_transaction')
)
    
engine  = taskflow.engines.load(flow)
engine.notifier.register('*', flow_watch)
engine.task_notifier.register('*', task_watch)
engine.run()
    
