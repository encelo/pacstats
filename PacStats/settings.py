## settings.py
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

import os
from db import Database

class Settings(Database):
	"""A class to store key/value pairs in a database table"""
	def __init__(self, fname = 'pacstats.db'):
		"""Connect and try to create the settings table"""
		Database.__init__(self, fname)
		self.table = 'settings'

		try:
			self.create_table()
		except self.error:
			print(_('%s table exists already') % self.table)


	def create_table(self):
		"""Create the settings table"""
		CREATE = """CREATE TABLE %s (
			key VARCHAR(128) PRIMARY KEY,
			value VARCHAR(128)
			);""" % self.table
	
		self.cur.execute(CREATE)
		self.con.commit()


	def set(self, key, value):
		"""Insert or update a key/value pair into the database"""
		INSERT = """INSERT INTO %s VALUES ('%s', '%s');""" % (self.table, str(key), str(value))
		UPDATE = """UPDATE %s SET value='%s' WHERE key='%s';""" % (self.table, str(value), str(key))
	
		try:
			self.cur.execute(INSERT)
		except self.error:
			self.cur.execute(UPDATE)
		self.con.commit()


	def get(self, key):
		"""Retrieve the value associated with the given key"""
		SELECT = """SELECT value FROM %s WHERE key='%s';""" % (self.table, key)
		
		self.cur.execute(SELECT)

		try:
			return self.cur.fetchall()[0][0]
		except IndexError:
			return None


	def remove(self, key):
		"""Remove a key/value pair from the database"""
		DELETE = """DELETE FROM %s WHERE key='%s';""" % (self.table, key)

		self.cur.execute(DELETE)
		self.con.commit()
