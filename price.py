#!/usr/bin/env python
# -*- coding: utf-8 -*-

from db import db
from logger import logging
from enum import Enum
import requests
from constant import COMMA
from constant import SEMI
from constant import QUOT
from constant import EQUAL
from constant import SINGLE_QUOT
import sys


class Price(object):
    def __init__(self):
        self.INSERT_PRICE = "insert into stock_price_history (`code`,`open` ,`close` ,`price` ,`high`,`low`,`buy_price` ,`sell_price`,`deal_number`,`deal_money` ,`buy_one_number`,`buy_one_price`,`buy_two_number`,`buy_two_price`,`buy_three_number`,`buy_three_price`,`buy_four_number`,`buy_four_price`,`buy_five_number` ,`buy_five_price` ,`sell_one_number` ,`sell_one_price` ,`sell_two_number`,`sell_two_price` ,`sell_three_number` ,`sell_three_price` ,`sell_four_number`,`sell_four_price` ,`sell_five_number` ,`sell_five_price`,`date`,`time`,`other`) values (%s) on duplicate key update `other`='00'"
        self.INSERT_TODAY_PRICE = "insert into stock_price_newest (`code`,`open` ,`close` ,`price` ,`high`,`low`,`buy_price` ,`sell_price`,`deal_number`,`deal_money` ,`buy_one_number`,`buy_one_price`,`buy_two_number`,`buy_two_price`,`buy_three_number`,`buy_three_price`,`buy_four_number`,`buy_four_price`,`buy_five_number` ,`buy_five_price` ,`sell_one_number` ,`sell_one_price` ,`sell_two_number`,`sell_two_price` ,`sell_three_number` ,`sell_three_price` ,`sell_four_number`,`sell_four_price` ,`sell_five_number` ,`sell_five_price`,`date`,`time`,`other`) values (%s) on duplicate key update `other`='00'"
        self.TRUNCATE_TODAY_PRICE = "truncate table stock_price_newest"
        self.UPDATE_NAME = "update stock set name='%s' where code='%s'"
        self.stock_url = "http://hq.sinajs.cn/list="
        self.logger = logging.getLogger('price.py')
        reload(sys)
        sys.setdefaultencoding('utf-8')

    def get_code_list(self):
        code_list = []
        sql = "select code, code_type from stock"
        result = db.get(sql)
        for row in result:
            code_list.append(row[1].lower() + row[0])
        return code_list

    def get_stock_info(self, code_list):
        codes = []
        stocks = []
        for index in xrange(len(code_list)):
            codes.append(code_list[index])

            if index % 10 == 0:
                request_url = self.stock_url + COMMA.join(codes)
                r = requests.get(request_url)
                codes = []

                results = r.text.split(SEMI)
                for row in results:
                    if QUOT in row:
                        var = row.split(QUOT)[0]
                        content = row.split(QUOT)[1]
                        if len(var) > 0 and len(content) > 0:
                            code = var[var.index('hq_str_') + 9: var.index(EQUAL)]
                            stock = code.zfill(6) + COMMA + content
                            stocks.append(stock)
        return stocks

    def update_name(self, stock_list):
        for stock in stock_list:
            column = stock.split(COMMA)
            code = column[0]
            name = column[1]
            print name
            sql = self.UPDATE_NAME % (name, code,)
            db.execute(sql)

    def update_stock_history(self, stock_list):
        for stock in stock_list:
            column = stock.split(COMMA)
            row = column[0:1]
            info = column[2:]
            row[len(row): len(row)] = info
            value = ""
            for index in range(len(row)):
                if index == 0 or index == 30 or index == 31:
                    value += SINGLE_QUOT + str(row[index]) + SINGLE_QUOT + COMMA
                elif index == 32:
                    value += SINGLE_QUOT + str(row[index]) + SINGLE_QUOT
                else:
                    value += row[index] + COMMA
            sql = self.INSERT_PRICE % (value,)
            db.execute(sql)

    def update_stock_today(self, stock_list):
        sql = self.TRUNCATE_TODAY_PRICE
        db.execute(sql)
        for stock in stock_list:
            column = stock.split(COMMA)
            row = column[0:1]
            info = column[2:]
            row[len(row): len(row)] = info
            value = ""
            for index in range(len(row)):
                if index == 0 or index == 30 or index == 31:
                    value += SINGLE_QUOT + str(row[index]) + SINGLE_QUOT + COMMA
                elif index == 32:
                    value += SINGLE_QUOT + str(row[index]) + SINGLE_QUOT
                else:
                    value += row[index] + COMMA
            sql = self.INSERT_TODAY_PRICE % (value,)
            db.execute(sql)


if __name__ == '__main__':
    price = Price()
    code_list = price.get_code_list()
    stocks = price.get_stock_info(code_list)
    # price.update_name(stocks)
    # price.update_stock_history(stocks)
    price.update_stock_today(stocks)
