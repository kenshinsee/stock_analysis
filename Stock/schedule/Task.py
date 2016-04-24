#!/usr/bin/python2.7

import subprocess,os,time

from taskflow import task
from Sys_paths import Sys_paths
from tooling.common_tool import replace_vars, print_log, error_log, warn_log, get_date, recent_working_day, get_yaml, return_new_name_for_existing_file
from tooling.psql import get_conn, get_cur
from tooling.db_func import get_query_result

BIN_DIR = Sys_paths.BIN_DIR
YML_DIR = Sys_paths.YML_DIR
SEP = Sys_paths.SEP
DB_YML = YML_DIR + SEP + "db.yml"

class Task(task.Task):
    
    def __init__(self, name):
        task.Task.__init__(self, name)
        self.name = name
        #-- fetch DB info
        db_dict = get_yaml(DB_YML)
        #-- open db connection
        self.conn = get_conn(db_dict["DB"], db_dict["Username"], db_dict["Password"], db_dict["Host"], db_dict["Port"])

    def set_command(self):
        self.cmd = None
    
    def pre_execute(self):
        self.set_command()
        if not self.cmd is None and len(self.cmd) > 0:
            #-- get row_id
            self.row_id = get_query_result(self.conn, "select nextval('dw.seq_job_row_id') as row_id")[0]["row_id"]
            ins_sql = "insert into dw.job(row_id, name, start_time) values({0}, '{1}', '{2}')".format(self.row_id, self.name, time.ctime())
            get_query_result(self.conn, ins_sql)
            self.conn.commit()
        else:
            raise RuntimeError('No command needs to be executed.')
    
    def execute(self):
        p = subprocess.Popen(self.cmd, shell=True)
        return_code = p.wait()
        
        if return_code == 0:
            get_query_result(self.conn, "update dw.job set end_time = '{0}', is_success = 'Y' where row_id = {1}".format(time.ctime(), self.row_id))
        else:
            get_query_result(self.conn, "update dw.job set end_time = '{0}', is_success = 'N' where row_id = {1}".format(time.ctime(), self.row_id))

    def post_execute(self):
        self.conn.commit()

        
        
if __name__ == "__main__":
    import taskflow.engines
    from taskflow.patterns import linear_flow
    
    def flow_watch(state, details):
        print('Flow State: {}'.format(state))
        print('Flow Details: {}'.format(details))

    def task_watch(state, details):
        print('Task State: {}'.format(state))
        print('Task Details: {}'.format(details))

    flow = linear_flow.Flow('simple-linear').add(
        Task('test')
    )

    #engine = taskflow.engines.load(flow, store=dict(cmd='echo hello'))
    engine = taskflow.engines.load(flow)
    #engine.notifier.register('*', flow_watch)
    #engine.task_notifier.register('*', task_watch)
    #engine.notifier.register('SUCCESS', flow_watch)
    engine.run()