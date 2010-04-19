## packagers.py
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

		self._name = _('Packagers')
		self._description = _('Top ten for number of packages created')
		self._version = '0.1'


	def generate(self):
		"""Generate the chart"""
		
		QUERY = """SELECT packager, COUNT(*) AS total FROM %s GROUP BY packager ORDER BY total DESC LIMIT 10"""

		data = self._database.query_all(QUERY % self._packages.name)
		data.reverse()
		widths = []
		labels = []
		for tuple in data:
			name = tuple[0][:tuple[0].find('<')].rstrip() # stripping email
			labels.append(name)
			widths.append(tuple[1])
	
		self._axes = self._canvas.figure.add_subplot(111)
		self._axes.grid(True)
		self._axes.set_ylim(0, len(widths))
		if len(widths) > 0:
			self._axes.set_xlim(0, max(widths)*1.1)
		self._axes.set_yticks(range(len(widths)))
		self._axes.set_yticklabels(labels, fontsize=5)
		self._axes.barh(range(len(widths)), widths, align='center')

