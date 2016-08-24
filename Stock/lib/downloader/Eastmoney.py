#!/usr/bin/python2.7
# coding:utf-8
# This class is to grab data from www.eastmoney.com
#
# Four main methods
#
# return_stock_in_bankuai
#   input parameter: <bankuai> 
#   return: all the stocks belonging to <bankuai>
#
# return_bankuai_in_bankuai
#    input parameter: <bankuai>, <sort_direction>
#    return: based on <sort_direction>, return bankuais in descending or ascending order
#
# export_bankuai_status
#    input parameter: full path of out file
#    out file header: [u'板块',u'子版块',u'板块名称',u'涨跌幅',u'总市值(亿)',u'换手率',u'上涨家数',u'下跌家数',u'领涨股票代码',u'领涨股票',u'领涨股票涨跌幅']
#
# export_bankuai_stock
#    input parameter: full path of out file
#    out file header: [u'板块',u'子版块',u'板块名称',u'股票代码',u'股票名称']
#

import re,sys,pprint,copy,csv,os
reload(sys)
sys.setdefaultencoding("gbk")
from tooling.common_tool import print_log, warn_log, read_url, get_date, return_new_name_for_existing_file
from Sys_paths import Sys_paths

class Eastmoney:

    __base_url = "http://quote.eastmoney.com/center"
    __bankuai_ext = "BanKuai.html"
    
    def __init__(self):
        def return_bankuai_tree(bankuai_url = self.__base_url + "/" + self.__bankuai_ext):
        # The bankuai in html is like
        # AAA
        # BBB->GGG
        # BBB->CCC
        # DDD->EEE->FFF
        # 
        # to match AAA, we use r_return_category_no_sub_category
        # to match BBB and its children, we use r_return_first_lvl_with_sub_category and r_return_detail_lvl
        # to match DDD and its children (2nd lvl), we use r_return_first_lvl_with_sub_category, r_return_second_lvl_with_sub_category and r_return_detail_lvl
        #
        # *The code for Chinese character is gb2312*
            bankuai_page = read_url(bankuai_url)

            d_code_url = {}
            #{name: url=...
            #        children={name: url=...
            #                        children={name: url=...}
            #                 },
            # name: url=...,}
            r_return_category_no_sub_category = r'<dd class="node-item" data-key="\w+"><a href="(?P<url>[0-9a-zA-Z_,#\.]+)"><span class="text">(?P<name>[^<]+)</span></a></dd>'
            r_return_first_lvl_with_sub_category = r'<dd class="js-sub" data-id="\w+"><span class="node-item" data-key="\w*"><b class="icon-sub-title"></b><a href="(?P<url>[0-9a-zA-Z_,#\.]+)"[^>]*><span class="text">(?P<name>[^<]+)</span>(?P<content>.*?)(?=</ul>)</ul></dd>'
            r_return_second_lvl_with_sub_category = r'<li class="node-sub-sub"><a href="(?P<url>[^"]+)" class="[^>]+"><span class="text">(?P<name>[^<]+)</span></a><b class="icon-right"></b><div class="[^>]+">(?P<content>.*?)(?=</div>)</div><div class="hover-mask"></div></li>'
            r_return_detail_lvl = r'<a href="(?P<url>[^"]+)"[^>]*><span class="text">(?P<name>[^<]+)</span></a>'
            
            r_no_sub_cat = re.compile(r_return_category_no_sub_category)
            r_first_lvl = re.compile(r_return_first_lvl_with_sub_category)
            r_second_lvl = re.compile(r_return_second_lvl_with_sub_category)
            r_detail_lvl = re.compile(r_return_detail_lvl)
            
            for m in r_no_sub_cat.finditer(bankuai_page):
                if m.group("name").decode("gb2312") not in d_code_url: 
                    d_code_url[m.group("name").decode("gb2312")] = {"url": m.group("url")}
                    
            for m in r_first_lvl.finditer(bankuai_page):
                first_lvl_group_name = m.group("name").decode("gb2312")
                d_code_url[first_lvl_group_name] = {"url": m.group("url")}
                d_code_url[first_lvl_group_name].setdefault("children", {})
                if m.group("content").find("class=\"node-sub-sub\"") == -1:
                # one sub-branches
                    for m1 in r_detail_lvl.finditer(m.group("content")):
                        d_code_url[first_lvl_group_name]["children"][m1.group("name").decode("gb2312")] = {"url": m1.group("url")}
                else:
                # two sub-branches
                    for m1 in r_second_lvl.finditer(m.group("content")):
                        second_lvl_group_name = m1.group("name").decode("gb2312")
                        d_code_url[first_lvl_group_name]["children"][second_lvl_group_name] = {"url": m1.group("url")}
                        d_code_url[first_lvl_group_name]["children"][second_lvl_group_name].setdefault("children", {})
                        for m2 in r_detail_lvl.finditer(m1.group("content")):
                            d_code_url[first_lvl_group_name]["children"][second_lvl_group_name]["children"][m2.group("name").decode("gb2312")] = {"url": m2.group("url")}
            return d_code_url
        
        self.__bankuai_tree = return_bankuai_tree()
    
    @property
    def bankuai_tree(self):
        return self.__bankuai_tree

    @bankuai_tree.setter
    def bankuai_tree(tree):
        self.__bankuai_tree = tree
    

    def return_url_for_bankuai_stock(self, bankuai, page=1, page_size=10000):
        bankuai_tree = self.__bankuai_tree
        def return_bankuai_code(bankuai_tree, bankuai):
            # bankuai parameter is a list from the top bankuai to the bottom bankuai in the format below
            # ['板块','概念板块','AB股票']
            # Parse the url of bankuai, for the url of bankuai under [概念板块, 地域板块, 行业板块], the numbers before the first underscore is the key to get the stocks belonging to that bankuai
            # e.g. For 板块->概念板块->AB股, the url is list.html#28003498_0_2, 28003498 is the key to get the stocks belonging to AB股
            def drill_to_sub_bankuai(bankuai_dict,sub_bankuai):
                if sub_bankuai in bankuai_dict:
                    return bankuai_dict[sub_bankuai]
                elif "children" in bankuai_dict and sub_bankuai in bankuai_dict["children"]:
                    return bankuai_dict["children"][sub_bankuai]
                else:
                    # This error should not be captured by the except block below
                    raise RuntimeError(sub_bankuai + " is not found.", "in Eastmoney.py") 
                    
            try:
                bankuai_code = re.search(r'#(?P<bankuai_code>\d+)', reduce(drill_to_sub_bankuai, bankuai, bankuai_tree)["url"]).group("bankuai_code")
            except AttributeError:
                # The exception block only captures AttributeError: 'NoneType' object has no attribute 'group'
                print_log("The url of [" + ",".join(bankuai) + "] doesn't contain digits.")
                bankuai_code = "-99"
                
            return bankuai_code
                
        base_url = "http://hqdigi2.eastmoney.com/EM_Quote2010NumericApplication/index.aspx?type=s&sortType=C&sortRule=-1&jsName=quote_123"
        p_page_size = "&pageSize=%(page_size)s"
        p_page = "&page=%(page)s"
        p_bankuai_code = "&style=%(bankuai_code)s" 
        bankuai_url = ( base_url + p_page_size + p_page + p_bankuai_code ) % {"page_size": page_size, "page": page, "bankuai_code": return_bankuai_code(bankuai_tree, bankuai)}
        print_log(bankuai_url) 
        return bankuai_url

    
    def return_url_for_bankuai_bankuai(self, bankuai):
        # This method handles the lvl2 bankuai
        bankuai_bankuai_url = {u"板块": 
            {u"概念板块": "http://quote.eastmoney.com/hq2data/bk/data/notion.js?v=1",
             u"地域板块": "http://quote.eastmoney.com/hq2data/bk/data/area.js?v=1",
             u"行业板块": "http://quote.eastmoney.com/hq2data/bk/data/trade.js?v=1",
            }
        }
        if bankuai[0] in bankuai_bankuai_url and bankuai[1] in bankuai_bankuai_url[bankuai[0]]:
            return bankuai_bankuai_url[bankuai[0]][bankuai[1]]
        else:
            raise RuntimeError("The url of [" + ",".join(bankuai) + "] is not configured.","in Eastmoney.py")

            
    def return_stock_in_bankuai(self, bankuai):
        # bankuai parameter is a list from the top bankuai to the bottom bankuai in the format below
        # ['板块','概念板块','AB股票']
        #
        # return ['板块','概念板块','AB股票',[[code,name],[code,name],...]]
        bankuai_tree = self.__bankuai_tree

        if not bankuai[2] in bankuai_tree[bankuai[0]]["children"][bankuai[1]]["children"]:
            raise RuntimeError,("The url of [" + ",".join(bankuai) + "] is not correct.","in Eastmoney.py")
        
        bankuai_detail_url = self.return_url_for_bankuai_stock(bankuai)
        while True: # Infinite loop unitl stock download completes successfully
            try:
                bankuai_detail_page = read_url(bankuai_detail_url)
                break
            except:
                warn_log('Connection lost, retry in 10 seconds ...')
                time.sleep(10)                
                
        r_return_code_detail_grp = r'\[(?P<code_detail_grp>.*)\]'
        code_detail_grp = re.search(r_return_code_detail_grp, bankuai_detail_page).group("code_detail_grp")

        r_return_code_detail = r'"(?P<code_detail>[^"]*)"'
        r_code_detail = re.compile(r_return_code_detail)
        
        stocks = []
        for m in r_code_detail.finditer(code_detail_grp):
            match_group_into_list = m.group("code_detail").split(",")
            stocks.append([match_group_into_list[1],match_group_into_list[2].decode("utf-8")])
        
        out_list = copy.copy(bankuai)
        out_list.append(stocks)
        return out_list

        
    def return_bankuai_in_bankuai(self, bankuai, sort_direction="desc"):
        # bankuai parameter is a list from the top bankuai to the bottom bankuai in the format below
        # ['板块','概念板块']
        # return 
        # ['板块','概念板块',[
        #                    [bankuai_name,increase,amount(in 0.1billion),change_ratio,rising_count,falling_count,leading_stock_code,leading_stock_name,increase],
        #                    [bankuai_name,increase,amount(in 0.1billion),change_ratio,rising_count,falling_count,leading_stock_code,leading_stock_name,increase],
        #                    ...
        #                    ]
        if not sort_direction.lower() in ["desc","asc"]:
            raise RuntimeError,("Incorrect parameter [%(direction)s]" % {"direction": sort_direction},"in Eastmoney.py")
            
        bankuai_url = self.return_url_for_bankuai_bankuai(bankuai)
        while True: # Infinite loop unitl stock download completes successfully
            try:
                bankuai_page = read_url(bankuai_url)
                break
            except:
                warn_log('Connection lost, retry in 10 seconds ...')
                time.sleep(10)
                
        r_return_bankuai_detail_grp = r'\[\[(?P<bankuai_detail_group_desc>[^\]]+)\],\[(?P<bankuai_detail_group_asc>[^\]]+)\]\]'
        match_objs = re.search(r_return_bankuai_detail_grp, bankuai_page)
        bankuai_detail_grp = match_objs.group("bankuai_detail_group_" + sort_direction)
        
        r_return_code_detail = r'"(?P<code_detail>[^"]*)"'
        r_code_detail = re.compile(r_return_code_detail)
        
        bankuais = []
        for m in r_code_detail.finditer(bankuai_detail_grp):
            match_group_into_list = m.group("code_detail").split(",")
            bankuais.append([match_group_into_list[0],match_group_into_list[1],match_group_into_list[2],match_group_into_list[3],match_group_into_list[4],match_group_into_list[5],match_group_into_list[6],match_group_into_list[7],match_group_into_list[8]])
        
        out_list = copy.copy(bankuai)
        out_list.append(bankuais)
        return out_list
    
        
    def export_bankuai_status(self, out_file, in_bk=[]):
        # If in_bk parameter is not assigned, export all the bankuais
        # in_bk could be [行业板块]
        bkbk_exception = []
        out_file = return_new_name_for_existing_file(out_file)
        bkbkfile = open(out_file, 'wb') # open in wb is used to remove the blank lines
        bkbkfile_writer = csv.writer(bkbkfile,quoting=csv.QUOTE_NONNUMERIC)
        bkbk_head = [u'板块',u'子版块',u'板块名称',u'涨跌幅',u'总市值(亿)',u'换手率',u'上涨家数',u'下跌家数',u'领涨股票代码',u'领涨股票',u'领涨股票涨跌幅']
        bkbkfile_writer.writerow(bkbk_head)
        for bk in self.__bankuai_tree[u'板块']["children"]:
            if len(in_bk)>0 and bk != in_bk[0]: continue
            print_log("Start to process -->" + bk + "...")
            parent_bk = []
            for i in self.return_bankuai_in_bankuai([u'板块',bk]):
                bkbk = []
                if not isinstance(i, list):
                    parent_bk.append(i)
                else:
                    for j in i:
                        bkbk = parent_bk + j
                        try:
                            bkbkfile_writer.writerow(bkbk)
                        except:
                            if j[0] not in bkbk_exception: bkbk_exception.append(j[0])
        bkbkfile.close()
        if len(bkbk_exception)>0: 
            print_log("There are " + len(bkbk_exception) + " exceptions!")
            for i in bkbk_exception:
                print i
        else:
            print_log("Completed successfully.")
        return bkbk_exception

    def export_bankuai_stock(self, out_file, in_bk=[]):
        # If in_bk parameter is not assigned, export all the bankuai stocks
        # in_bk could be [行业板块, 浙江板块] or [行业板块] 
        bkst_exception = {}
        out_file = return_new_name_for_existing_file(out_file)
        bkstfile = open(out_file, 'wb') # open in wb is used to remove the blank lines
        bkstfile_writer = csv.writer(bkstfile,quoting=csv.QUOTE_NONNUMERIC)
        bkst_head = [u'板块',u'子版块',u'板块名称',u'股票代码',u'股票名称']
        bkstfile_writer.writerow(bkst_head)
        for sub_bk in self.__bankuai_tree[u'板块']["children"]:
            if len(in_bk)>0 and sub_bk != in_bk[0]: continue
            print_log("Start to process -->" + sub_bk + "...")
            for dtl_bk in self.__bankuai_tree[u'板块']["children"][sub_bk]["children"]:
                if len(in_bk)>1 and dtl_bk != in_bk[1]: continue
                print_log("Start to process -->" + sub_bk + "-->" + dtl_bk + "...")
                parent_bk = []
                for i in self.return_stock_in_bankuai([u'板块', sub_bk, dtl_bk]):
                    bkst = []
                    if not isinstance(i, list):
                        parent_bk.append(i)
                    else:
                        for j in i:
                            bkst = parent_bk + j
                            try:
                                bkstfile_writer.writerow(bkst)
                            except:
                                if not j[0] in bkst_exception: bkst_exception[j[0]] = j[1]
        bkstfile.close()
        if len(bkst_exception.keys())>0: 
            print_log("There are " + str(len(bkst_exception.keys())) + " exceptions!")
            for i in bkst_exception:
                print i + bkst_exception[i]
        else:
            print_log("Completed successfully.")
        return bkst_exception
    
if __name__ == "__main__":

    e = Eastmoney()
    #print e.bankuai_tree
    print e.return_url_for_bankuai_stock([u'板块',u'概念板块',u'AB股票'])
    
    #today = get_date('today')
    #
    #bkbkfile_name = 'bankuai_' + today + '.csv'
    #return_list = e.export_bankuai_status( Sys_paths.DATA_STOCK_BANKUAI_DAILY + Sys_paths.SEP + bkbkfile_name)
	#
    #bkstfile_name = 'bankuai_stock_' + today + '.csv'
    #return_dict = e.export_bankuai_stock( Sys_paths.DATA_STOCK_BANKUAI_DAILY + Sys_paths.SEP + bkstfile_name)
    