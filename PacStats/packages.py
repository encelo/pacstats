## packages.py
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


class Packages(Table):
	"""Packages table managing class"""

	def __init__(self, database):
		"""Try to create the packages table"""

		Table.__init__(self, database, 'packages')


	def create(self):
		"""Create the packages table"""

		CREATE = """CREATE TABLE %s (
			id INTEGER PRIMARY KEY,
			name VARCHAR(128) UNIQUE NOT NULL,
			version VARCHAR(32) NOT NULL,
			description VARCHAR(256),
			url VARCHAR(256),
			license VARCHAR(128),
			arch VARCHAR(16) NOT NULL,
			builddate DATE,
			buildtime TIME,
			installdate DATE,
			installtime TIME,
			packager VARCHAR(128),
			size INTEGER NOT NULL,
			reason INTEGER NOT NULL,
			repository VARCHAR(32)
			);""" % self.name
	
		self._database.execute(CREATE)
		self._database.commit()


	def insert(self, name, version, description, url, license, arch, 
			   buildepoch, installepoch, packager, size, reason, repository):
		"""Insert a new transaction into the database"""

		INSERT = """INSERT INTO %s VALUES (NULL, ?, ?, ?, ?, ?, ?,
			date(?, 'unixepoch', 'localtime'), time(?, 'unixepoch', 'localtime'), 
			date(?, 'unixepoch', 'localtime'), time(?, 'unixepoch', 'localtime'), ?, ?, ?, ?)""" % self.name
		tuple = (name, version, description, url, license, arch, buildepoch, buildepoch,
			installepoch, installepoch, packager, size, reason, repository)

		self._database.execute(INSERT, tuple)
		

	def insert_many(self, tuples):
		"""Insert many new transactions into the database"""

		INSERT = """INSERT INTO %s VALUES (NULL, ?, ?, ?, ?, ?, ?,
			date(?, 'unixepoch', 'localtime'), time(?, 'unixepoch', 'localtime'), 
			date(?, 'unixepoch', 'localtime'), time(?, 'unixepoch', 'localtime'), ?, ?, ?, ?)""" % self.name

		self._database.execute_many(INSERT, tuples)


	def remove(self, id):
		"""Remove the package with the given id from the database"""

		DELETE = """DELETE FROM %s WHERE id = ?""" % self.name

		self._database.execute(DELETE, (id, ))
		self._database.commit()


	def remove_name(self, name):
		"""Remove the package with the given n ame from the database"""

		DELETE = """DELETE FROM %s WHERE name = ?""" % self.name

		self._database.execute(DELETE, (name, ))
		self._database.commit()
