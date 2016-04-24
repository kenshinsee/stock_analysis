#!/usr/bin/python2.7

import subprocess,os

from taskflow import task
from Sys_paths import Sys_paths
from Task import Task

BIN_DIR = Sys_paths.BIN_DIR
SEP = Sys_paths.SEP

class Task_recon_stock_bankuai(Task):

    def set_command(self):
        self.cmd = 'python ' + BIN_DIR + SEP + 'recon_stock_bankuai.py'

        