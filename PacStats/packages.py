## packages.py
##
## PacStats: PacStats: ArchLinux' Pacman statistics
## Copyright (C) 2007 Angelo Theodorou <encelo@users.sourceforge.net>
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

class  Packages(Database):
	"""Packages table managing class"""
	def __init__(self, fname = 'pacstats.db'):
		"""Connect and try to create the packages table"""
		Database.__init__(self, fname)
		self.table = 'packages'

		try:
			self.create_table()
		except self.error:
			print _('%s table exists already') % self.table


	def create_table(self):
		"""Create the packagess table"""
		CREATE = """CREATE TABLE %s (
			name VARCHAR(128) PRIMARY KEY,
			version VARCHAR(32) NOT NULL,
			description VARCHAR(256),
			url VARCHAR(256),
			license VARCHAR(128),
			arch VARCHAR(16) NOT NULL,
			builddate TIMESTAMP,
			installdate TIMESTAMP,
			packager VARCHAR(128),
			size INTEGER,
			reason INTEGER
			);""" % self.table
	
		self.cur.execute(CREATE)
		self.con.commit()


	def insert(self, name, version, description, url, license, arch, builddate, installdate, packager, size, reason):
		"""Insert a new transaction into the database"""
		INSERT = """INSERT INTO %s VALUES ('%s', '%s', "%s", '%s', '%s', '%s', '%s', '%s', "%s", %d, %d)""" % \
				(self.table, name, version, description, url, license, arch, builddate, installdate, packager, size, reason)
		
		try:
			self.cur.execute(INSERT)
		except self.error:
			return
		self.con.commit()


	def remove(self, name):
		"""Remove the package with the given n ame from the database"""
		DELETE = """DELETE FROM %s WHERE name='%s'""" % (self.table, name)

		self.cur.execute(DELETE)
		self.con.commit()
