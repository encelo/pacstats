## basechart.py
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


class BaseChart:
	"""A skeleton class for a chart to inherit from"""
	def __init__(self, transactions, packages):
		self.transactions = transactions
		self.packages = packages

		self.name = ''
		self.description = ''
		self.version = ''


	def get_name(self):
		return self.name

	def get_description(self):
		return self.description

	def get_version(self):
		return self.version


	def attach(self, parent_box):
		"""Setup the Drawing Area class for the chart"""
		self.parent = parent_box
		

	def update(self):
		"""Update the chart"""
		pass


	def detach(self):
		"""Erase the Drawing Area class of the chart"""
		self.parent = None
