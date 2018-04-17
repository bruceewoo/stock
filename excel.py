#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import re
import urllib
import os
import codecs

# "http://basic.10jqka.com.cn/601766/xls/mainreport.xls",
# "http://basic.10jqka.com.cn/601766/xls/mainyear.xls",
# "http://basic.10jqka.com.cn/601766/xls/mainsimple.xls",

# "http://basic.10jqka.com.cn/601766/xls/debtreport.xls",
# "http://basic.10jqka.com.cn/601766/xls/debtyear.xls",
# "http://basic.10jqka.com.cn/601766/xls/debtsimple.xls"

NEW_LINE = "\n"
root = "excel/"
validate_url = "http://basic.10jqka.com.cn/"
filenames = ["mainreport.xls", "mainyear.xls", "mainsimple.xls",
             "debtreport.xls", "debtyear.xls", "debtsimple.xls",
             "benefitreport.xls", "benefityear.xls", "benefitsimple.xls",
             "cashreport.xls", "cashyear.xls", "cashsimple.xls", ]

code_file = "code.txt"
stock_file = "stock.csv"
stock_url = "http://hq.sinajs.cn/list="
stock_column = " 股票代码, 股票名字, 今日开盘价, 昨日收盘价, 当前价格, 今日最高价, 今日最低价, 竞买价, 竞卖价," \
               + " 成交股票数, 成交金额, 买一, 买一报价, 买二, 买二报价, 买三, 买三报价, 买四, 买四报价, 买五, 买五报价, " \
               + " 卖一, 卖一报价, 卖二, 卖二报价,卖三, 卖三报价,卖四, 卖四报价, 卖五, 卖五报价,日期, 时间, 其他\n"


def is_valid_code(code):
    r = requests.get(validate_url + code)

    if "sub_page_bg.png" not in str(r.text.encode('utf-8')):
        return True
    return False


def get_prefix_code(code):
    if str(code).startswith('000'):
        return "sz" + str(code)
    return "sh" + str(code)


def add_code(code, code_list):
    if (get_prefix_code(code) not in code_list) and is_valid_code(code):
        with open(root + code_file, 'a') as f:
            print 'adding code %s ...' % (code,)
            f.write(get_prefix_code(code) + NEW_LINE)


def get_code_list():
    code_list = []
    if os.path.exists(root + code_file):
        with open(root + code_file, 'r') as f:
            for line in f.readlines():
                code_list.append(line.strip())
    return code_list


def get_finance(code):
    for filename in filenames:
        report_url = validate_url + "/xls/" + filename
        report_name = code + "_" + filename

        report_path = root + code + "/"
        if not os.path.exists(report_path):
            os.makedirs(report_path)

        if not os.path.exists(report_path + report_name):
            print "Downloading file %s..." % (report_name,)
            urllib.urlretrieve(report_url, report_path + report_name)


def add_stock_info(code_list):
    print "start to get stock information..."
    codes = []

    with open(root + stock_file, 'w+') as f:
        f.write(codecs.BOM_UTF8)
        f.write(stock_column)

    for index in xrange(len(code_list)):
        codes.append(code_list[index])

        if index % 10 == 0:
            request_url = stock_url + ",".join(codes)
            r = requests.get(request_url)
            codes = []
            print request_url

            with open(root + stock_file, 'a') as f:
                f.write(codecs.BOM_UTF8)
                stock_list = r.text.split(';')
                for stock in stock_list:
                    if '"' in stock:
                        name = stock.split('"')[0]
                        content = stock.split('"')[1]
                        if len(name) > 0 and len(content) > 0:
                            code = name[name.index('hq_str_') + 9: name.index('=')]
                            info = code.zfill(6) + "," + content + "\n"
                            print 'writing code %s ...' % (code,)
                            f.write(info.encode('utf-8'))


if __name__ == '__main__':
    code_list = get_code_list()

    '''
	for code in xrange(0, 1000):
		add_code(str(code).zfill(6), code_list)
	
	for code in xrange(600000, 602000):
		add_code(str(code), code_list)
    '''	
    for code in xrange(603000, 604000):
	add_code(str(code), code_list)
	

    code_list = get_code_list()
    add_stock_info(code_list)

    print 'END'
