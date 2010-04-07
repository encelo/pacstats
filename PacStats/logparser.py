## logparser.py
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

from os import stat
from subject import Subject

SYNC = 0
SYSUP = 1
INSTALL = 2
REMOVE = 3
UPGRADE = 4

class LogParser(Subject):
	"""A parser for pacman.log"""
	def __init__(self, settings, transactions):

		Subject.__init__(self)

		self.settings = settings
		self.transactions = transactions


	def parse(self, logfile='/var/log/pacman.log'):
		"""Parse a logfile from the saved seek position"""

		try:
			f = open(logfile)
		except IOError:
			print('Cannot open %s!' % logfile)
			return

		size = stat(logfile).st_size
		seek_value = self.settings.get('log_seek')
		if seek_value:
			seek_value = int(seek_value)
			f.seek(seek_value)
		else:
			seek_value = 0

		for line in f:
			rawstamp = line[:line.find(']')+1]
			rawaction = line[line.find(']')+2:]

			# Timestamp
			rawstamp = rawstamp.strip('[')
			rawstamp = rawstamp.strip(']')
			rawstamp = rawstamp.split(' ')
			
			date = rawstamp[0]
			time = rawstamp[1]

			# Action performed
			if rawaction.find('synchronizing package lists') == 0:
				action = SYNC
			elif rawaction.find('starting full system upgrade') == 0:
				action = SYSUP
			else:
				rawaction = rawaction.split(' ')
				if rawaction[0] == 'installed':
					action = INSTALL
				elif rawaction[0] == 'removed':
					action = REMOVE
				elif rawaction[0] == 'upgraded':
					action = UPGRADE
				else:
					continue

				package = rawaction[1]
				version = []

				if action == UPGRADE:
					version.append(rawaction[2].strip('('))
					version.append(rawaction[4].strip(')\n'))
				else:
					version.append(None)
					version.append(rawaction[2].strip('(').strip(')\n'))

			if action in (0, 1):
				self.transactions.insert(date, time, action)
			else:
				self.transactions.insert(date, time, action, package, version[0], version[1])

			seek_value = f.tell()
			self.settings.set('log_seek', seek_value)
			self.notify(float(seek_value)/float(size))

		f.close()
