import sys,os

class Sys_paths:
    SEP = os.path.sep
    PROJ_BASE_DIR = "D:\workspace\Stock"
    YML_DIR = PROJ_BASE_DIR + SEP + "etc"
    DATA_DIR = PROJ_BASE_DIR + SEP + "data"
    LOG_DIR = PROJ_BASE_DIR + SEP + "log"
    LIB_DIR = PROJ_BASE_DIR + SEP + "lib"
    BIN_DIR = PROJ_BASE_DIR + SEP + "bin"
    DATA_STOCK_DAILY = DATA_DIR + SEP + "stock_daily"
    DATA_STOCK_BANKUAI_DAILY = DATA_DIR + SEP + "stock_bankuai_daily"
    DATA_STOCK_TRANSACTION = DATA_DIR + SEP + "stock_transaction"