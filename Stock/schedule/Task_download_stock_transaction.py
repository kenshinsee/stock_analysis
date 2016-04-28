#!/usr/bin/python2.7

import subprocess,os

from taskflow import task
from Sys_paths import Sys_paths
from Task import Task

BIN_DIR = Sys_paths.BIN_DIR
SEP = Sys_paths.SEP

class Task_download_stock_transaction(Task):

    def set_command(self):
        self.cmd = 'python ' + BIN_DIR + SEP + 'download_stock_transaction.py -o "S|N"'

        