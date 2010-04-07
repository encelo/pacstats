## pie_letter.py
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
	"""Pie letter chart"""
	def __init__(self, transactions, packages):
		BaseChart.__init__(self, transactions, packages)

		self.name = 'Pie Letter'
		self.description = 'Initial package letter pie chart'
		self.version = '0.1'

		self.transactions = transactions
		self.letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o' , 'p', 'q', 'r', 's', 't', 'y', 'w', 'x', 'z']
		self.letters.reverse() # Clockwise pie chart
		self.data = []


	def attach(self, parent_box):
		"""Setup the Drawing Area class for the test chart"""
		self.parent = parent_box
		
		data = []
		QUERY = """SELECT COUNT(*) FROM %s WHERE name LIKE '%s%%';"""
		for l in self.letters:
			data.append(self.packages.query(QUERY % (self.packages.table, l))[0][0])

 		self.fig = f.Figure(figsize=(5,4), dpi=100, facecolor='w', edgecolor='k')
		self.fig.hold(False)
		self.axes = self.fig.add_subplot(111)
		self.pie = self.axes.pie(data, labels=self.letters, shadow=True)

		self.canvas = FigureCanvas(self.fig)  # a gtk.DrawingArea
		self.parent.pack_start(self.canvas, True, True)
		self.canvas.show()


	def update(self):
		"""Update the test chart"""

		self.canvas.draw()


	def detach(self):
		"""Delete the Drawing class for the test chart"""

		try:
			self.parent.remove(self.canvas)
			self.canvas.destroy()
		except AttributeError:
			pass

