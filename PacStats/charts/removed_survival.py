## removed_survival.py
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


class Chart(BaseChart):
	"""A derived chart"""
	def __init__(self, database):
		BaseChart.__init__(self, database)

		self._name = _('Removed survival')
		self._description = _('Top ten for days of survival of removed packages')
		self._version = '0.1'


	def generate(self):
		"""Generate the chart"""
		
		QUERY = """SELECT t1.package, julianday(t2.date, t2.time) - julianday(t1.date, t1.time) AS survival 
			FROM %s AS t1 INNER JOIN transactions AS t2 
			ON t1.package = t2.package 
			WHERE t1.date <= t2.date AND 
				t1.time < t2.time AND 
				t1.action = 2 AND t2.action = 3
			ORDER BY survival DESC LIMIT 10"""

		data = self._database.query_all(QUERY % self._transactions.name)
		data.reverse()
		widths = []
		labels = []
		for tuple in data:
			labels.append(tuple[0])
			widths.append(tuple[1])
	
		self._axes = self._canvas.figure.add_subplot(111)
		self._axes.grid(True)
		self._axes.set_ylim(0, len(widths))
		if len(widths) > 0:
			self._axes.set_xlim(0, max(widths)*1.1)
		self._axes.set_yticks(range(len(widths)))
		self._axes.set_yticklabels(labels, fontsize=8)
		self._axes.barh(range(len(widths)), widths, align='center')
