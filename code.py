#!/usr/bin/env python
# -*- coding: utf-8 -*-

from db import db
from logger import logging
from enum import Enum
import requests


class Code(object):
    def __init__(self):
        self.validate_url = "http://basic.10jqka.com.cn/"
        self.logger = logging.getLogger('code.py')

    def is_valid_code(self, code, code_type):
        flag = False
        if code_type == 'HK':
            code = code_type + code[1:]
        r = requests.get(self.validate_url + code)

        if code_type == 'HK':
            if code in str(r.text.encode('utf-8')):
                flag = True
        else:
            if "sub_page_bg.png" not in str(r.text.encode('utf-8')):
                flag = True

        return flag

    def get_code_type(self, code):
        if str(code).startswith('000'):
            return "SZ"
        return "SH"

    def add_or_update_code(self, code, code_type='SH'):
        if self.is_valid_code(code, code_type):
            sql = "insert into stock (code, code_type) values('%s','%s') on duplicate key update code_type='%s'" % (
            code, code_type, code_type,)
            self.logger.info(sql)
            db.execute(sql)


code = Code()

# 港股
for index in xrange(3740, 4000):
    code.add_or_update_code(str(index).zfill(5), 'HK')
'''
for index in xrange(0, 1000, 'SZ'):
	code.add_or_update_code(str(index).zfill(6))

for index in xrange(600000, 602000):
	code.add_or_update_code(str(index))

for index in xrange(603000, 604000):
	code.add_or_update_code(str(index))
'''
