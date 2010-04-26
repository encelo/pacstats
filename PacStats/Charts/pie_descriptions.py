## pie_descriptions.py
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


from math import ceil
from PacStats.basechart import BaseChart


class Chart(BaseChart):
	"""A derived chart"""
	def __init__(self, database):
		BaseChart.__init__(self, database)

		self._name = _('Pie Descriptions')
		self._description = _('Description lengths pie chart')
		self._version = '0.1'


	def generate(self):
		"""Genrate the chart"""
	
		MAX = """SELECT MAX(length(description)) FROM %s"""
		MIN = """SELECT MIN(length(description)) FROM %s"""
		QUERY = """SELECT COUNT(*) FROM %s WHERE length(description) BETWEEN ? AND ?"""

		max = self._database.query_one(MAX % self._packages.name)[0]
		min = self._database.query_one(MIN % self._packages.name)[0]

		labels = []
		fracts = []

		fractions = 6
		lrange = int(ceil((max - min)/float(fractions)))
		low = min
		high = min + lrange
		for i in range(fractions):
			labels.append(str(low) + '-' + str(high) + ' ' + _('characters'))
			fracts.append(self._database.query_one(QUERY % self._packages.name, (low, high))[0])
			low += lrange
			high = low + lrange

		self._axes = self._canvas.figure.add_subplot(111)
		self._pie = self._axes.pie(fracts, labels=labels, shadow=True)
