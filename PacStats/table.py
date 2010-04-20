## table.py
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


class Table:
	"""Generic table managing class"""

	def __init__(self, database, name):
		"""Try to create the packages table"""

		self._database = database
		self.name = name

		try:
			self.create()
		except self._database.error:
			print('\"%s\" table exists already' % self.name)
			pass


	def clear(self):
		"""Clear the table from data"""

		DELETE = """DELETE FROM %s""" % self.name
		
		self._database.execute(DELETE)
		self._database.commit()


	def drop(self):
		"""Drop the table"""
		
		DROP = """DROP TABLE %s""" % self.name

		self._database.execute(DROP)
		self._database.commit()


	def create(self):
		pass
	
	
	def insert(self):
		pass


	def save_as(self, fname=''):
		"""Save the table as a text file"""

		SELECT = """SELECT * FROM %s""" % self.name
		
		if fname == '':
			fname = self.name
		 
		# Using execute() instead of query_all() for cursor iteration
		self._database.execute(SELECT)
		 
		f = open(fname, 'w')
		for row in self._database.cursor:
			line = ''
			for i in range(len(row)-2):
				line = line + str(row[i]) + '|'
			line = line + str(row[len(row)-1])
			f.write(line + '\n')
		f.close()
