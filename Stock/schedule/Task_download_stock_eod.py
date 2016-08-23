#!/usr/bin/python2.7

import subprocess,os

from taskflow import task
from Sys_paths import Sys_paths
from Task import Task

BIN_DIR = Sys_paths.BIN_DIR
SEP = Sys_paths.SEP

class Task_download_stock_eod(Task):

    def set_command(self):
        self.cmd = 'python ' + BIN_DIR + SEP + 'download_stock_eod.py -o sina'
        #self.cmd = 'python ' + BIN_DIR + SEP + 'download_stock_eod.py'

        