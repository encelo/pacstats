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

from PacStats.basechart import BaseChart
import PacStats.logparser as logparser


class Chart(BaseChart):
	"""A derived chart"""
	def __init__(self, database):
		BaseChart.__init__(self, database)

		self._name = _('Monthly Transactions')
		self._description = _('Type splitted transactions per month in the last twelve')
		self._version = '0.1'


	def generate(self):
		"""Generate the chart"""
	
		QUERY = """SELECT strftime('%%Y-%%m', date) AS month, action, count(action) AS count FROM %s
			WHERE date >= date('now', '-12 month') GROUP BY action, month ORDER BY month"""

		data = self._database.query_all(QUERY % self._transactions.name)

		dict = {}
		for t in data:
			if t['month'] not in dict.keys():
				dict[t['month']] = [0, 0, 0, 0, 0]
			dict[t['month']][t['action']] = t['count']

		labels = dict.keys()
		labels.sort()

		h_sync = [dict[date][logparser.SYNC] for date in labels]
		h_sysup = [dict[date][logparser.SYSUP] for date in labels]
		h_install = [dict[date][logparser.INSTALL] for date in labels]
		h_remove = [dict[date][logparser.REMOVE] for date in labels]
		h_upgrade = [dict[date][logparser.UPGRADE] for date in labels]

		ind = np.arange(len(h_sync))
		width = 0.15

		self._axes = self._canvas.figure.add_subplot(111)
		self._axes.grid(True)
		if len(data) > 0:
			self._axes.set_ylim(0, max(h_sync)*1.1)
		self._axes.set_xticks(np.arange(len(labels)) + 2.5*width)
		self._axes.set_xticklabels(labels, fontsize=10)
		self._canvas.figure.autofmt_xdate()

		self._axes.bar(ind, h_sync, width, color = 'r', label=_('Synchronizations'))
		self._axes.bar(ind+width, h_sysup, width, color = 'g', label= _('System Upgrades'))
		self._axes.bar(ind+2*width, h_install, width, color = 'b', label= _('Installations'))
		self._axes.bar(ind+3*width, h_remove, width, color = 'y', label=_('Removals'))
		self._axes.bar(ind+4*width, h_upgrade, width, color = 'm', label=_('Upgrades'))

		self._axes.legend(prop=FontProperties(size=7))
