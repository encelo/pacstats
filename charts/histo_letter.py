## histo_letter.py
##
## PacStats: ArchLinux' Pacman statistics
## Copyright (C) 2007 Angelo Theodorou <encelo@users.sourceforge.net>
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
	import matplotlib.figure as f
	import matplotlib.pylab as p
	import matplotlib.numerix as n
	import matplotlib.backends.backend_gtkcairo as cairo
except ImportError:
	print 'MatPlotLib is missing!'
	exit(-1)


class Chart(BaseChart):
	"""Histo letter chart"""
	def __init__(self, transactions, packages):
		BaseChart.__init__(self, transactions, packages)

		self.name = 'Histo Letter'
		self.description = 'Initial package letter histogram'
		self.version = '0.1'

		self.letters = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o' , 'p', 'q', 'r', 's', 't', 'y', 'w', 'x', 'z')
		self.data = []


	def attach(self, parent_box):
		"""Setup the Drawing Area class for the test chart"""
		self.parent = parent_box
		
		data = []
		QUERY = """SELECT COUNT(*) FROM %s WHERE name LIKE '%s%%';"""
		for l in self.letters:
			data.append(self.packages.query(QUERY % (self.packages.table, l))[0])
	
 		self.fig = f.Figure(figsize=(5,4), dpi=100, facecolor='w', edgecolor='k')
		self.fig.hold(False)
		self.axes = self.fig.add_subplot(111)
		self.axes.set_xlim(0, len(self.letters))
		self.axes.set_ylim(0, max(data)[0])
		self.axes.set_xticks(n.arange(0.5, len(self.letters)))
		self.axes.set_xticklabels(self.letters)

		self.axes.bar(range(len(self.letters)), data)

		self.canvas = cairo.FigureCanvasGTKCairo(self.fig)  # a gtk.DrawingArea
		self.parent.pack_start(self.canvas, True, True)
		self.canvas.show()


	def update(self):
		"""Update the test chart"""

		self.canvas.destroy()
		self.canvas = cairo.FigureCanvasGTKCairo(self.fig)  # a gtk.DrawingArea
		self.parent.pack_start(self.canvas, True, True)
		self.canvas.show()


	def detach(self):
		"""Delete the Drawing class for the test chart"""
	
		try:
			self.parent.remove(self.canvas)
			self.canvas.destroy()
		except AttributeError:
			pass

