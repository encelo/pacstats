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


from table import Table


class Transactions(Table):
	"""Transactions table managing class"""

	def __init__(self, database):
		"""Try to create the transactions table"""

		Table.__init__(self, database, 'transactions')


	def create(self):
		"""Create the transactions table"""
		
		CREATE = """CREATE TABLE %s (
			id INTEGER PRIMARY KEY,
			date DATE NOT NULL,
			time TIME NOT NULL,
			action INTEGER NOT NULL,
			package VARCHAR(128),
			old_ver VARCHAR(32),
			new_ver VARCHAR(32)
			);""" % self.name
	
		self._database.execute(CREATE)
		self._database.commit()


	def insert(self, date, time, action, package=None, old_ver=None, new_ver=None):
		"""Insert a new transaction into the database"""
		
		if package == None:
			INSERT = """INSERT INTO %s VALUES (NULL, ?, ?, ?, NULL, NULL, NULL)""" % self.name
			tuple = (date, time, action)
		else:
			INSERT = """INSERT INTO %s VALUES (NULL, ?, ?, ?, ?, ?, ?)""" % self.name
			tuple = (date, time, action, package, old_ver, new_ver)
	
		self._database.execute(INSERT, tuple)
		
		
	def insert_many(self, tuples):
		"""Insert many new transactions into the database"""
		
		INSERT = """INSERT INTO %s VALUES (NULL, ?, ?, ?, ?, ?, ?)""" % self.name
		
		self._database.execute_many(INSERT, tuples)


	def remove(self, id):
		"""Remove the transaction with the given id from the database"""
		
		DELETE = """DELETE FROM %s WHERE id = ?""" % self.name

		self._database.execute(DELETE, (id, ))
		self._database.commit()
