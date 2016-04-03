#coding:utf-8
#------------------------------------
#-- Sina stock transaction api 
#------------------------------------
# http://market.finance.sina.com.cn/downxls.php?date=2016-03-25&symbol=sh600038
# Sina provides the recent 2 months transaction details

import urllib2,re,sys,datetime,os
import StringIO
from tooling.common_tool import save_file_from_url, print_log
from Sys_paths import Sys_paths
from object.Tengxun_stock_transaction_object import Tengxun_stock_transaction_object

class Tengxun_stock_transaction:
    __url_prefix = "http://stock.gtimg.cn/data/index.php?appn=detail&action=download"
    __code_symbol = "&c=%(code_loc)s%(code)s"
    __date_symbol = "&d=%(date)s"
    __code_loc_dict = {
        "60": "sh", 
        "00": "sz", 
        "30": "sz", 
        "51": "sh",
        "15": "sz",
        "20": "sz",
        "90": "sh",
    }

    def __init__(self, code, date):
        self.__code = str(code)
        self.__date = str(date)
        self.__download_file_dir = Sys_paths.DATA_STOCK_TRANSACTION + Sys_paths.SEP + str(date)
        self.__download_file = self.__download_file_dir + Sys_paths.SEP + 'tengxun_' + self.__date + '_' + self.__code + '.txt'
        if not os.path.exists(self.__download_file_dir):
            os.mkdir(self.__download_file_dir)
        
    @property
    def download_file(self):
        return self.__download_file
        
    @download_file.setter
    def download_file(file):
        self.__download_file = file
        
    def get_url(self):
            return self.__url_prefix + self.__code_symbol % {"code": self.__code, "code_loc": self.__code_loc_dict[self.__code[0:2]]} + self.__date_symbol % {"date": self.__date}
    
    def download_to_local(self):
        print_log('Reading data from ' + self.get_url())
        save_file_from_url(self.__download_file, self.get_url())
        print_log('Data saved to ' + self.__download_file)
        
    def get_stock_content(self):
        out_dict = {}
        out_dict[self.__code] = {}
        row_idx = 0
        out_content = ''
        with open(self.__download_file) as f:
            for row in f.readlines():
                row_idx += 1
                if row_idx == 1: continue
                row_add_stock_id_date =str(self.__code) + '\t' + self.__date + '\t' + row #+ '\n'
                out_content = out_content + row_add_stock_id_date
        out_dict[self.__code][self.__date] = out_content
        return out_dict
        
    def get_stock_object(self):
        out_object = {}
        for code in self.get_stock_content():
            out_object[code] = {}
            for date in self.get_stock_content()[code]:
                buf = StringIO.StringIO(self.get_stock_content()[code][date])
                rows = []
                for row in buf.readlines():
                    rows.append(row.split('\t')[2:])
                out_object[code][date] = Tengxun_stock_transaction_object(code, date, rows)
                buf.close()
        return out_object
        
    @staticmethod
    def get_stock_object_from_str(str):
    # This method reads a str to create a stock object
    # This method is for backload trades from a pre-stored file which contains stock info with the same format as calling from url
    # Different from the same function for other stock source, the [str] here is a full transaction of a day
        buf = StringIO.StringIO(str)
        rows = []
        code = ''
        date = ''
        for row in buf.readlines():
            if len(rows) == 0:
                code = row.split('\t')[0]
                date = row.split('\t')[1]
            rows.append(row.split('\t')[2:])
        
        out_object = {}
        out_object[code] = {}
        out_object[code][date] = Tengxun_stock_transaction_object(code, date, rows)
        return out_object
    
        
        
if __name__ == "__main__":
    s = Tengxun_stock_transaction("300499", "20160325")#Tengxun_stock_transaction("300499", "20160317")
    #s.download_to_local()
    #c = s.get_stock_content()
    #print c['300499']['20160325']

    obj = s.get_stock_object()#['300499']['20160317']
    for code in obj:
        for date in obj[code]:
            print code, date, obj[code][date].attrs_in_dict[1]['buy_sell']
            
        
