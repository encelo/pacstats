## monthly_transactions.py
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


from matplotlib.font_manager import FontProperties

try:
        import numpy as np
except ImportError:
        print('NumPy is missing!')
        exit(-1)

from datetime import datetime
from matplotlib.dates import DateFormatter
from matplotlib.font_manager import FontProperties

from PacStats.basechart import BaseChart
import PacStats.logparser as logparser


class Chart(BaseChart):
	"""A derived chart"""
	def __init__(self, database):
		BaseChart.__init__(self, database)

		self._name = _('Monthly Transactions')
		self._description = _('Stacked transactions per month in the last twelve')
		self._version = '0.1'


	def generate(self):
		"""Generate the chart"""
	
		QUERY = """SELECT strftime('%%Y-%%m', date) AS month, action, count(action) AS count FROM %s
			WHERE date >= date('now', '-12 month') GROUP BY action, month ORDER BY month"""

		data = self._database.query_all(QUERY % self._transactions.name)

		dict = {}
		for t in data:
			dt = datetime.strptime(t['month'], "%Y-%m")
			if dt not in dict.keys():
				dict[dt] = [0, 0, 0, 0, 0]
			dict[dt][t['action']] = t['count']

		dates = dict.keys()
		dates.sort()

		h_sync = [dict[date][logparser.SYNC] for date in dates]
		h_sysup = [dict[date][logparser.SYSUP] for date in dates]
		h_install = [dict[date][logparser.INSTALL] for date in dates]
		h_remove = [dict[date][logparser.REMOVE] for date in dates]
		h_upgrade = [dict[date][logparser.UPGRADE] for date in dates]

		self._axes = self._canvas.figure.add_subplot(111)
		self._axes.grid(True)
		formatter = DateFormatter('%b %Y')
		self._canvas.figure.autofmt_xdate()

		self._axes.bar(dates, h_sync, width=12, color = 'r', align='center', label=_('Synchronizations'))
		bottoms = np.array(h_sync)
		self._axes.bar(dates, h_sysup, width=12, bottom=bottoms, color = 'g', align='center', label= _('System Upgrades'))
		bottoms += np.array(h_sysup)
		self._axes.bar(dates, h_install, width=12, bottom=bottoms, color = 'b', align='center', label= _('Installations'))
		bottoms += np.array(h_install)
		self._axes.bar(dates, h_remove, width=12, bottom=bottoms, color = 'y', align='center', label=_('Removals'))
		bottoms += np.array(h_remove)
		self._axes.bar(dates, h_upgrade, width=12, bottom=bottoms, color = 'm', align='center', label=_('Upgrades'))
		bottoms += np.array(h_upgrade)

		if len(data) > 0:
			self._axes.set_ylim(0, max(bottoms)*1.05)
			self._axes.xaxis.set_major_formatter(formatter)
			self._axes.legend(prop=FontProperties(size=8))
