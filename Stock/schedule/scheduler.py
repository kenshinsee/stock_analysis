#!/usr/bin/python2.7
from datetime import *
import taskflow.engines
from taskflow.patterns import linear_flow
from taskflow import task
from tooling.common_tool import replace_vars, print_log, error_log, warn_log, get_date, recent_working_day, get_yaml, return_new_name_for_existing_file
from tooling.psql import get_conn, get_cur
from tooling.db_func import get_query_result
from Sys_paths import Sys_paths

from Task_download_stock_bankuai import Task_download_stock_bankuai
from Task_recon_stock_bankuai import Task_recon_stock_bankuai
from Task_download_stock_eod import Task_download_stock_eod
from Task_download_stock_transaction import Task_download_stock_transaction

YML_DIR = Sys_paths.YML_DIR
SEP = Sys_paths.SEP
DB_YML = YML_DIR + SEP + "db.yml"
#-- fetch DB info
db_dict = get_yaml(DB_YML)
#-- open db connection
conn = get_conn(db_dict["DB"], db_dict["Username"], db_dict["Password"], db_dict["Host"], db_dict["Port"])


def flow_watch(state, details):
    print('Flow State: {}'.format(state))
    print('Flow Details: {}'.format(details))

def task_watch(state, details):
    print('Task State: {}'.format(state))
    print('Task Details: {}'.format(details))

def check_job_status(conn, name):
    query_status_for_last_run = '''
    select t.is_success
    from (
        select is_success, 
            row_number() over(partition by name order by start_time desc) rk 
        from dw.job 
        where name = '{0}' and date(start_time) = '{1}' 
    ) t where t.rk = 1
    '''.format(name, date.today())
    rows = get_query_result(conn, query_status_for_last_run)
    if len(rows) == 0:
        status = 'N'
    else:
        status = rows[0]['is_success']
    return status if not status is None else 'N'
    
jobs = {
    'download_stock_bankuai': Task_download_stock_bankuai('download_stock_bankuai'),
    'recon_stock_bankuai': Task_recon_stock_bankuai('recon_stock_bankuai'),
    'download_stock_eod': Task_download_stock_eod('download_stock_eod'),
    'download_stock_transaction': Task_download_stock_transaction('download_stock_transaction'),
}

#job_run_seq = ['download_stock_bankuai', 'recon_stock_bankuai', 'download_stock_eod', 'download_stock_transaction']
job_run_seq = ['download_stock_bankuai', 'recon_stock_bankuai', 'download_stock_eod']
job_to_run = []

# determine which jobs need to run
for i, job in enumerate(job_run_seq):
    status = check_job_status(conn, job)
    print_log(job + ' ====> ' + status)
    if status == 'N': # one job failed, itself and the jobs depend on it will be added to to-run list
        job_to_run = job_run_seq[i:]
        break

# add to flow
flow = linear_flow.Flow('Eod loading')
for job in job_to_run:
    flow.add(jobs[job])

engine  = taskflow.engines.load(flow)
engine.notifier.register('*', flow_watch)
engine.task_notifier.register('*', task_watch)
try:
    engine.run()
except Exception as ex:
    error_log(ex.message)
    
