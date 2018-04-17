#!/usr/bin/env python
# -*- coding: utf-8 -*-

import MySQLdb
from config import config
from logger import logging

class DB(object):
	def __init__(self): 
		self.logger = logging.getLogger('db.py')
		self.con = MySQLdb.connect(config.get_db("host"), config.get_db("user"), 
			config.get_db("pass"), config.get_db("database"), charset="utf8")
		self.cursor = self.con.cursor()

	def get(self, sql):
		try:
			self.cursor.execute(sql)
			self.logger.debug('get sql:'+ sql)
			results = self.cursor.fetchall()
			return results
		except Exception as e:
			self.logger.error("unable to fetch data for "+ sql)

	def execute(self, sql):
		try:
			self.cursor.execute(sql)
			self.logger.info('execute sql:'+ sql)
			self.con.commit()
		except Exception as e:
			self.con.rollback()
			self.logger.error(e)

db = DB()

if __name__ == '__main__':
	sql = "update stock set code_type='%s' where code = '%s'" % ("SZ", "000001",)
	print sql
	db.execute(sql)

	sql = "select * from stock limit 1"
	result = db.get(sql)
	print result