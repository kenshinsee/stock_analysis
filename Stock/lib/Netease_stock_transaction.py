#coding:utf-8
#------------------------------------
#-- Netease stock transaction api 
#------------------------------------
# http://quotes.money.163.com/cjmx/2016/20160318/0600594.xls
# http://quotes.money.163.com/cjmx/2016/20160318/1000004.xls
# Netease provides the recent 4 days' transaction details

import urllib2,re,sys,datetime,xlrd,StringIO,os
from common_tool import save_file_from_url, print_log
from Sys_paths import Sys_paths
from object.Netease_stock_transaction_object import Netease_stock_transaction_object

class Netease_stock_transaction:
    __url_prefix = "http://quotes.money.163.com/cjmx"
    __code_symbol = "/%(year)s/%(date)s/%(code_loc)s%(code)s.xls"
    __code_loc_dict = {
        "60": "0", 
        "00": "1", 
        "30": "1", 
        "51": "0",
        "15": "1",
        "20": "1",
        "90": "0",
    }

    def __init__(self, code, date):
        self.__code = str(code)
        self.__date = str(date)
        self.__download_file_dir = Sys_paths.DATA_STOCK_TRANSACTION + Sys_paths.SEP + str(date)
        self.__download_file = self.__download_file_dir + Sys_paths.SEP + 'netease_' + self.__date + '_' + self.__code + '.xls'
        if not os.path.exists(self.__download_file_dir):
            os.mkdir(self.__download_file_dir)
        
    @property
    def download_file(self):
        return self.__download_file
        
    @download_file.setter
    def download_file(file):
        self.__download_file = file
        
    def get_url(self):
        return self.__url_prefix + self.__code_symbol % {"year": self.__date[0:4], "date": self.__date, "code": self.__code, "code_loc": self.__code_loc_dict[self.__code[0:2]]}

    def download_to_local(self):
        print_log('Reading data from ' + self.get_url())
        save_file_from_url(self.__download_file, self.get_url())
        print_log('Data saved to ' + self.__download_file)
        
    def get_stock_content(self):
        #read from xls file, save data as flat file seperate each column by \t and remove header
        workbook = xlrd.open_workbook(self.__download_file)
        sheet = workbook.sheets()[0]
        out_content = ''
        for row_idx in range(sheet.nrows):
            if row_idx == 0: continue
            out_content = out_content + self.__code + '\t' + self.__date + '\t' + sheet.cell(row_idx,0).value + '\t' + str(sheet.cell(row_idx,1).value) + '\t' + str(sheet.cell(row_idx,2).value) + '\t' + str(sheet.cell(row_idx,3).value) + '\t' + str(sheet.cell(row_idx,4).value) + '\t' + sheet.cell(row_idx,5).value + '\n'
        out_dict = {}
        out_dict[self.__code] = {}
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
                out_object[code][date] = Netease_stock_transaction_object(code, date, rows)
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
        out_object[code][date] = Netease_stock_transaction_transaction_object(code, date, rows)
        return out_object
    
        
        
if __name__ == "__main__":
    s = Netease_stock_transaction("300499", "20160325")
    #s.download_to_local()
    #c = s.get_stock_content()
    #print c['300499']['20160325']
    obj = s.get_stock_object()#['300499']['20160318']
    for code in obj:
        for date in obj[code]:
            print code, date, obj[code][date].attrs_in_dict[1]['buy_sell']
            
        
