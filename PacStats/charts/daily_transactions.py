## daily_transactions.py
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


import time
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

		self._name = _('Daily Transactions')
		self._description = _('Current month transactions per day')
		self._version = '0.1'


	def generate(self):
		"""Generate the chart"""
		
		QUERY = """SELECT COUNT(*) FROM %s WHERE date = date('now', '-%s day');"""

		today = int(time.strftime('%d'))

		data = []
		for d in range(today):
			data.append(self._database.query_one(QUERY % (self._transactions.name, d))[0])
		data.reverse()

		self._axes = self._fig.add_subplot(111)
		if len(data) > 0:
			self._axes.set_ylim(0, max(data)*1.1)
		self._axes.set_xlim(0, today)
		self._axes.set_xticks(n.arange(0.5, today))
		self._axes.set_xticklabels(range(1, today+1), fontsize=5)
		self._axes.bar(range(today), data)
