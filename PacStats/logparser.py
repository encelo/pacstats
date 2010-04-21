## logparser.py
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


from os import stat
from time import clock, strftime, strptime
from subject import Subject


SYNC = 0
SYSUP = 1
INSTALL = 2
REMOVE = 3
UPGRADE = 4

class LogParser(Subject):
	"""A parser for pacman.log"""
	def __init__(self, database, logfile, seek):

		Subject.__init__(self)
		self._database = database
		self._transactions = database.transactions
		self._logfile = logfile
		self._seek = seek

	
	def get_seek(self):
		"""Get the seek value"""

		return self._seek.get()


	def reset_seek(self):
		"""Reset the seek value to zero"""

		self._seek.set(0)
		self._seek.write()


	def parse(self):
		"""Parse a logfile from the saved seek position"""

		start = clock()

		try:
			f = open(self._logfile)
		except IOError:
			print('Cannot open \"%s\"!' % self._logfile)
			return

		print('Parsing the log \"%s\"' % self._logfile)

		size = stat(self._logfile).st_size
		seek_value = self._seek.get()
		f.seek(seek_value)

		tuples = []
		line_no = 0
		for line in f:
			line_no += 1

			open_box = line.find('[')
			close_box = line.find(']')
			if open_box == -1 or close_box == -1:
#				print('No matching brackets at line %s: \"%s\"' % (line_no, line.rstrip('\n')))
				continue

			rawstamp = line[open_box:close_box+1]
			rawaction = line[close_box+1:].lstrip()

			# Timestamp
			rawstamp = rawstamp.strip('[')
			rawstamp = rawstamp.strip(']')
			rawstamp = rawstamp.split(' ')

			date = rawstamp[0]
			time = rawstamp[1]

			# parsing the old format
			splitted = date.split('/')
			if len(splitted) > 1:
				date = '20'+splitted[2] + '-' + splitted[0] + '-' + splitted[1]

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
#					print('Unknown action at line  %s: \"%s\"' % (line_no, line.rstrip('\n')))
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
#				self._transactions.insert(date, time, action)
				tuples.append((date, time, action, None, None, None))
			else:
#				self._transactions.insert(date, time, action, package, version[0], version[1])
				tuples.append((date, time, action, package, version[0], version[1]))

			seek_value = f.tell()
			if line_no % 250 == 0: # updating the progress bar every 250 lines
				self.notify(float(seek_value)/float(size))

		f.close()
		self._transactions.insert_many(tuples)
		self._database.commit() # committing one time at the end
		self._seek.set(size)
		self._seek.write()
		
		end = clock()
		print('Parsed %d lines in %f seconds' % (line_no, end-start))
