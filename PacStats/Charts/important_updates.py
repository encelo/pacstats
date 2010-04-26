## important_updates.py
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
from matplotlib.font_manager import FontProperties
from matplotlib.ticker import NullLocator

from PacStats.basechart import BaseChart


class Chart(BaseChart):
	"""A derived chart"""
	def __init__(self, database):
		BaseChart.__init__(self, database)

		self._name = _('Important Updates')
		self._description = _('Update dates chart of some important packages in the last twelve months')
		self._version = '0.1'


	def generate(self):
		"""Generate the chart"""

		QUERY = """SELECT date, time, new_ver FROM %s WHERE date > date('now', '-12 month') AND package = ?"""

		self._axes = self._canvas.figure.add_subplot(111)
		self._axes.yaxis.set_major_locator(NullLocator())
		self._axes.yaxis.set_minor_locator(NullLocator())
		self._axes.grid(True)
		self._canvas.figure.autofmt_xdate()

		colors = ('r', 'g', 'b', 'y', 'm', 'c')
		pkgs = ('kernel26', 'glibc', 'gcc', 'xorg-server', 'python', 'gtk2')
		height = 0.0
		for pkg in pkgs:
			height += 1.0 / len(pkgs)
			data = self._database.query_all(QUERY % self._transactions.name, (pkg, ))
			dates = [datetime.strptime(x[0] + ' ' + x[1], "%Y-%m-%d %H:%M") for x in data]
			labels = [x[2] for x in data]
			heights = [height for x in data]

			self._axes.plot_date(dates, heights, color=colors[pkgs.index(pkg)], label=pkg)

		self._axes.set_ylim(0, 1 + (1.0/len(pkgs)))
		self._axes.legend(prop=FontProperties(size=8))
