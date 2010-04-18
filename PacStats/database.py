## database.py
##
## PacStats: Statistical charts about Archlinux pacman activity
## Copyright (C) 2010 Angelo "Encelo" Theodorou <encelo@gmail.com>
##
## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this program; if not, write to the Free Software
## Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
##


import sys
import os
if sys.version_info[:2] >= (2, 5):
	from sqlite3 import dbapi2 as sqlite
else:
	from pysqlite2 import dbapi2 as sqlite

from transactions import Transactions
from packages import Packages


class Database:
	"""General database managing class"""
	def __init__(self, fname):
		"""Connect to the specified database"""

		self.error = sqlite.Error 
		if os.path.exists(fname) == False:
			print('Creating \"%s\"' % fname)
		self._con = sqlite.connect(fname)
		
		if sys.version_info[:2] >= (2, 5):
			self._con.row_factory = sqlite.Row
			self._con.text_factory = sqlite.OptimizedUnicode
			
		self._cur = self._con.cursor()

		self.table = None


	def __del__(self):
		"""Commit and close the connection"""

		self._con.commit()
		self._con.close()


	def commit(self):
		"""Commit the transaction"""

		self._con.commit()


	def rollback(self):
		"""Cancel the last transaction"""

		self._con.rollback()

	
	def get_cursor(self):
		"""Return the database cursor"""

		return self._cur

	cursor = property(get_cursor)


	def drop(self, name):
		"""Drop the specified table"""
		
		DROP = """DROP TABLE %s""" % name

		self._cur.execute(DROP)
		self._con.commit()


	def execute(self, string, tuple=()):
		"""Execute an arbitrary string"""

		self._cur.execute(string, tuple)
			
			
	def execute_many(self, string, tuples = [()]):
		"""Execute an arbitrary string multiple times"""

		self._cur.executemany(string, tuples)


	def query_one(self, string, tuple=()):
		"""Execute an arbitrary query, returning a single result"""

		self._cur.execute(string, tuple)
		return self._cur.fetchone()


	def query_many(self, string, tuple=(), size=-1):
		"""Execute an arbitrary query, returning a specified amount of results"""

		if size == -1:
			size = self._cur.arraysize

		self._cur.execute(string, tuple)
		return self._cur.fetchmany(size)


	def query_all(self, string, tuple=()):
		"""Execute an arbitrary query, returning all the results"""

		self._cur.execute(string, tuple)
		return self._cur.fetchall()


	def vacuum(self):
		"""Optimize the whole database defragmenting it"""

		self._cur.execute("VACUUM")


class ConcreteDB(Database):
	"""The concrete database actually used by the application"""

	def __init__(self, fname = 'pacstats.db'):
		"""Connect and try to create the tables"""

		Database.__init__(self, fname)
		self.transactions = Transactions(self)
		self.packages = Packages(self)
