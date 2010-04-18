## histo_letter.py
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


from PacStats.basechart import BaseChart

try:
	import numpy as n
except ImportError:
	print('NumPy is missing!')
	exit(-1)


class Chart(BaseChart):
	"""A derived chart"""
	def __init__(self, database):
		BaseChart.__init__(self, database)

		self._name = _('Histo Letter')
		self._description = _('Initial package letter histogram')
		self._version = '0.1'

		self._letters = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o' , 'p', 'q', 'r', 's', 't', 'y', 'w', 'x', 'z')


	def generate(self):
		"""Generate the chart"""

		data = []
		QUERY = """SELECT COUNT(*) FROM %s WHERE name LIKE '%s%%';"""
		for l in self._letters:
			data.append(self._database.query_one(QUERY % (self._packages.name, l))[0])
	 
		self._axes = self._fig.add_subplot(111)
		self._axes.set_xlim(0, len(self._letters))
		self._axes.set_ylim(0, max(data)*1.1)
		self._axes.set_xticks(n.arange(0.5, len(self._letters)))
		self._axes.set_xticklabels(self._letters)
		self._axes.bar(range(len(self._letters)), data)
