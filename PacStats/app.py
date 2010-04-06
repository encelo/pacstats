## app.py
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


import os
import pygtk
pygtk.require('2.0')
import gtk

import settings, transactions, logparser, packages, libparser, charts
import main_win

class Application:
	"""
	This is the main application class.
	Its role is to instantiate the singleton classes which compose the program.
	"""
	def __init__(self, share_dir='', charts_dir=''):
		#db_file = os.path.expanduser('~/.pacstats.db')
		db_file = 'pacstats.db'
		self.share_dir = share_dir
		self.glade_file = os.path.join(share_dir, 'pacstats.glade')
		
		# Singletons
		self.settings = settings.Settings(db_file)
		self.transactions = transactions.Transactions(db_file)
		self.logparser = logparser.LogParser(self.settings, self.transactions)
		self.packages = packages.Packages(db_file)
		self.libparser = libparser.LibParser(self.packages)
		self.charts = charts.Charts((os.path.join(charts_dir, 'charts')), self.transactions, self.packages)
		
		self.main_win = main_win.Main_Window(self)

	def run(self):
		"""Make the gtk main loop start."""
		gtk.main()
