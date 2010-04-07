## db.py
##
## PacStats: ArchLinux' Pacman statistical charts application
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
		self.error = sqlite.Error 
		if os.path.exists(fname) == False:
			print('Creating' + ' ' + fname)
		self.con = sqlite.connect(fname)
		self.cur = self.con.cursor()

		self.table = None


	def __del__(self):
		"""Close the connection"""
		self.con.commit()
		self.con.close()


	def clear(self):
		"""Clear the whole specified table"""
		DELETE = """DELETE FROM %s;""" % self.table

		self.cur.execute(DELETE)
		self.con.commit()


	def drop_table(self):
		"""Drop the specified table"""
		DROP = """DROP TABLE %s;""" % self.table

		self.cur.execute(DROP)
		self.con.commit()


	def query(self, string):
		"""Execute an arbitrary query"""
		self.cur.execute(string)
		return self.cur.fetchall()


	def select(self, where=''):
		"""Return the rows selected by a WHERE clause"""
		SELECT = """SELECT * FROM  %s %s;""" % (self.table, where)
		self.cur.execute(SELECT)
		return self.cur.fetchall()


	def show(self, where=''):
		"""Print the rows selected by a WHERE clause"""
		SELECT = """SELECT * FROM %s %s;""" % (self.table, where)

		self.cur.execute(SELECT)
		for row in self.cur:
			line = ''
			for i in range(len(row)-2):
				line = line + str(row[i]) + '|'
			line = line + str(row[len(row)-1])
			print(line)


	def save_as(self, fname):
		"""Save the database as a text file"""
		SELECT = """SELECT * FROM %s;""" % self.table
		
		self.cur.execute(SELECT)

		f = open(fname, 'w')

		for row in self.cur:
			line = ''
			for i in range(len(row)-2):
				line = line + str(row[i]) + '|'
			line = line + str(row[len(row)-1])
			f.write(line + '\n')
		
		f.close()
