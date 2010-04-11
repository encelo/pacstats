## db.py
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
import datetime
if sys.version_info[:2] >= (2, 5):
	from sqlite3 import dbapi2 as sqlite
else:
	from pysqlite2 import dbapi2 as sqlite

class Database:
	"""General database managing class"""
	def __init__(self, fname):
		"""Connect to the specified database"""
		self._error = sqlite.Error 
		if os.path.exists(fname) == False:
			print('Creating \"%s\"' % fname)
		self._con = sqlite.connect(fname)
		self._cur = self._con.cursor()

		self.table = None


	def __del__(self):
		"""Close the connection"""
		self._con.commit()
		self._con.close()


	def clear(self):
		"""Clear the whole specified table"""
		DELETE = """DELETE FROM %s;""" % self.table

		self._cur.execute(DELETE)
		self._con.commit()


	def drop_table(self):
		"""Drop the specified table"""
		DROP = """DROP TABLE %s;""" % self.table

		self._cur.execute(DROP)
		self._con.commit()


	def query(self, string):
		"""Execute an arbitrary query"""
		self._cur.execute(string)
		return self._cur.fetchall()


	def select(self, where=''):
		"""Return the rows selected by a WHERE clause"""
		SELECT = """SELECT * FROM %s WHERE %s;""" % (self.table, where)
		self._cur.execute(SELECT)
		return self._cur.fetchall()


	def show(self, where=''):
		"""Print the rows selected by a WHERE clause"""
		SELECT = """SELECT * FROM %s WHERE %s;""" % (self.table, where)

		self._cur.execute(SELECT)
		for row in self._cur:
			line = ''
			for i in range(len(row)-2):
				line = line + str(row[i]) + '|'
			line = line + str(row[len(row)-1])
			print(line)


	def save_as(self, fname):
		"""Save the database as a text file"""
		SELECT = """SELECT * FROM %s;""" % self.table
		
		self._cur.execute(SELECT)

		f = open(fname, 'w')

		for row in self._cur:
			line = ''
			for i in range(len(row)-2):
				line = line + str(row[i]) + '|'
			line = line + str(row[len(row)-1])
			f.write(line + '\n')
		
		f.close()


	def vacuum(self):
		"""Optimize the whole database defragmenting it"""

		self._cur.execute('VACUUM;')
		self._con.commit()
