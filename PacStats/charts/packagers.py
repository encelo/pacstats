## packagers.py
##
## PacStats: ArchLinux' Pacman statistical charts application
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
	import matplotlib.figure as f
	import matplotlib.pylab as p
	from matplotlib.backends.backend_gtkcairo import FigureCanvasGTKCairo as FigureCanvas
except ImportError:
	print('MatPlotLib is missing!')
	exit(-1)


class Chart(BaseChart):
	"""Packagers chart"""
	def __init__(self, transactions, packages):
		BaseChart.__init__(self, transactions, packages)

		self._name = 'Packagers'
		self._description = 'Top ten for number of packages delivered'
		self._version = '0.1'


	def attach(self, parent_box):
		"""Setup the Drawing Area class for the test chart"""
		self._parent = parent_box
		
		QUERY = """SELECT packager, COUNT(*) AS total FROM %s GROUP BY packager ORDER BY total DESC LIMIT 10;"""
		data = self._packages.query(QUERY % (self._packages.table))
		data.reverse()
		widths = []
		labels = []
		for tuple in data:
			name = tuple[0][:tuple[0].find('<')].rstrip() # stripping email
			labels.append(name)
			widths.append(tuple[1])
	
 		self._fig = f.Figure(figsize=(5,4), dpi=100, facecolor='w', edgecolor='k')
		self._fig.hold(False)
		self._axes = self._fig.add_subplot(111)
		self._axes.set_ylim(0, len(widths))
		if len(widths) > 0:
			self._axes.set_xlim(0, max(widths)+max(widths)*0.05)
		self._axes.set_yticks(n.arange(0.5, len(widths)))
		self._axes.set_yticklabels(labels, fontsize=5)
		self._axes.barh(range(len(widths)), widths)

		self._canvas = FigureCanvas(self._fig)  # a gtk.DrawingArea
		self._parent.pack_start(self._canvas, True, True)
		self._canvas.show()


	def update(self):
		"""Update the test chart"""

		self._canvas.draw()


	def detach(self):
		"""Delete the Drawing class for the test chart"""
	
		try:
			self._parent.remove(self._canvas)
			self._canvas.destroy()
		except AttributeError:
			pass

