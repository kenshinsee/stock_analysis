#!/usr/bin/python2.7

import subprocess,os

from taskflow import task
from Sys_paths import Sys_paths
from Task import Task

BIN_DIR = Sys_paths.BIN_DIR
SEP = Sys_paths.SEP

class Task_download_stock_bankuai(Task):

    def set_command(self):
        self.cmd = 'python ' + BIN_DIR + SEP + 'download_stock_bankuai.py'

        
        
        
        
        
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
        Task_download_stock_bankuai('download_stock_bankuai')
    )

    engine = taskflow.engines.load(flow)
    engine.notifier.register('*', flow_watch)
    engine.task_notifier.register('*', task_watch)
    engine.run()