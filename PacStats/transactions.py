## transactions.py
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

import os
from db import Database

class Transactions(Database):
	"""Transactions table managing class"""
	def __init__(self, fname = 'pacstats.db'):
		"""Connect and try to create the transactions table"""
		Database.__init__(self, fname)
		self.table = 'transactions'

		try:
			self.create_table()
		except self._error:
#			print('\"%s\" table exists already' % self.table)
			pass


	def create_table(self):
		"""Create the transactions table"""
		CREATE = """CREATE TABLE %s (
			id INTEGER PRIMARY KEY,
			date DATE NOT NULL,
			time TIME NOT NULL,
			action INTEGER NOT NULL,
			package VARCHAR(128),
			old_ver VARCHAR(32),
			new_ver VARCHAR(32)
			);""" % self.table
	
		self._cur.execute(CREATE)
		self._con.commit()


	def insert(self, date, time, action, package=None, old_ver=None, new_ver=None):
		"""Insert a new transaction into the database"""
		if package == None:
			INSERT = """INSERT INTO %s VALUES (NULL, '%s', '%s', %d, NULL, NULL, NULL)""" % (self.table, date, time, action)
		else:
			INSERT = """INSERT INTO %s VALUES (NULL, '%s', '%s', %d, '%s', '%s', '%s')""" % \
				(self.table, date, time, action, package, old_ver, new_ver)
	
		self._cur.execute(INSERT)
		self._con.commit()


	def remove(self, id):
		"""Remove the transaction with the given id from the database"""
		DELETE = """DELETE FROM %s WHERE rowid=%d""" % (self.table, id)

		self._cur.execute(DELETE)
		self._con.commit()
