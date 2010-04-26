## monthly_old_packages.py
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

from datetime import datetime
from matplotlib.dates import DateFormatter

from PacStats.basechart import BaseChart


class Chart(BaseChart):
	"""A derived chart"""
	def __init__(self, database):
		BaseChart.__init__(self, database)

		self._name = _('Monthly Old Packages')
		self._description = _('Packages no more updated since a certain month in the last twelve')
		self._version = '0.1'


	def generate(self):
		"""Generate the chart"""
	
		QUERY = """SELECT strftime('%%Y-%%m', installdate) AS month, COUNT(*) FROM %s 
			WHERE installdate >= date('now', '-12 month') GROUP BY month ORDER BY month"""

		data = self._database.query_all(QUERY % self._packages.name)
		dates = [datetime.strptime(x[0], "%Y-%m") for x in data]
		heights = [x[1] for x in data]

		self._axes = self._canvas.figure.add_subplot(111)
		self._axes.grid(True)
		formatter = DateFormatter('%b %Y')
		self._axes.xaxis.set_major_formatter(formatter)
		self._canvas.figure.autofmt_xdate()
		self._axes.bar(dates, heights, width=15, align='center')
		if len(data) > 0:
			self._axes.set_ylim(0, max(heights)*1.05)
