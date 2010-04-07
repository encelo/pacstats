## charts.py
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

import os
import sys


class Charts():
	"""Charts manager class"""
	def __init__(self, transactions, packages):

		self.__charts = {}
		charts_dir = os.path.join(os.path.dirname(__file__), 'charts')
		sys.path.insert(0, charts_dir)

		charts_dir_list = os.listdir(charts_dir)
		for file in charts_dir_list:
			if file[0] == '.' or file.endswith('.py') == False: #exlude hidden and not .py files
				continue

			modname = file.replace('.py', '')
			module = __import__(modname)
			if 'Chart' in dir(module):
				self.__charts[modname] = module.Chart(transactions, packages)


	def __len__(self):
		"""Return the number of available charts"""
		return len(self.__charts)


	def get_names(self):
		"""Return chart names"""
		return self.__charts.keys()


	def get_chart(self, name):
		"""Return the given chart"""
		try:
			return self.__charts[name]
		except KeyError:
			return None

