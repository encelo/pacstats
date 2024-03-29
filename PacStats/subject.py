## subject.py
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


class Subject():
	"""A subject in the observer pattern"""
	def __init__(self):

		self._observers = []

	def attach(self, cls):

		if isinstance(cls, object) and cls not in self._observers:
			self._observers.append(cls)


	def detach(self, cls):

		if cls in self._observers:
			self._observers.remove(cls)


	def notify(self, arg):

		for cls in self._observers:
			cls.notify(arg)
