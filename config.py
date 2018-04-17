#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ConfigParser
import os

class Config(object):
	def __init__(self):
		self.cf = ConfigParser.ConfigParser()
		self.cf.read("config/default.conf")

	def get_db(self, key):
		return self.cf.get('db', key)

config = Config()

if __name__ == '__main__':
	config = Config()
	print config.get_db("host")