## settings.py
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

import os
import ConfigParser
import cPickle


class PersistentInt():
	"""A class to persistently store an integer in a binary file"""
	def __init__(self, fname, default = 0):
		if os.path.isdir(os.path.dirname(fname)) == False:
			os.makedirs(os.path.dirname(fname))

		self._pfile = fname

		if os.path.isfile(fname):
			with open(self._pfile, 'rb') as pfile:
				self._value = cPickle.load(pfile)
#				print ('Read %s from \"%s\"' % (str(self._value), self._pfile))
			if type(self._value) != type(0L):
				self._value = default
		else:
			self._value = default


	def get(self):
		return self._value

	def set(self, value):
		self._value = value


	def write(self):
		with open(self._pfile, 'wb') as pfile:
			cPickle.dump(self._value, pfile, cPickle.HIGHEST_PROTOCOL)
#		print('Written %s to \"%s\"' % (str(self._value), self._pfile))


class Settings():
	"""A class to parse the configuration file"""
	def __init__(self, fname = ''):
		# Determining config file path
		if fname == '':
			cfg_home = os.environ.get('XDG_CONFIG_HOME')
			if cfg_home == None or cfg_home == '':
				cfg_home = os.path.expanduser('~/.config')

			cfg_home = os.path.join(cfg_home, 'pacstats')
			if os.path.isdir(cfg_home) == False:
				os.makedirs(cfg_home)
			fname = os.path.join(cfg_home, 'pacstats.cfg')

		self._cfg_file = fname

		# Determining default database path
		data_home = os.environ.get('XDG_DATA_HOME')
		if data_home == None or data_home == '':
			data_home = os.path.expanduser('~/.local/share')

		data_home = os.path.join(data_home, 'pacstats')
		if os.path.isdir(data_home) == False:
			os.makedirs(data_home)
		dbname = os.path.join(data_home, 'pacstats.db')

		# Setting defaults
		defaults = {}
		defaults['db'] = dbname
		defaults['log'] = '/var/log/pacman.log'
		defaults['lib'] = '/var/lib/pacman/local'
		defaults['abs'] = '/var/abs'

		self._cfg = ConfigParser.RawConfigParser()
		if os.path.isfile(fname):
			self._cfg.read(fname)
		else:
			self._cfg.add_section('pacstats')

		for key in defaults:
			if self._cfg.has_option('pacstats', key) == False:
				self._cfg.set('pacstats', key, defaults[key])

	
	def get_db(self):
	    return self._cfg.get('pacstats', 'db')

	def set_db(self, value):
		self._cfg.set('pacstats', 'db', value)

	db = property(get_db, set_db)


	def get_log(self):
	    return self._cfg.get('pacstats', 'log')

	def set_log(self, value):
		self._cfg.set('pacstats', 'log', value)

	log = property(get_log, set_log)


	def get_lib(self):
	    return self._cfg.get('pacstats', 'lib')

	def set_lib(self, value):
		self._cfg.set('pacstats', 'lib', value)

	lib = property(get_lib, set_lib)


	def get_abs(self):
	    return self._cfg.get('pacstats', 'abs')

	def set_abs(self, value):
		self._cfg.set('pacstats', 'abs', value)

	abs = property(get_abs, set_abs)


	def write(self):
		"""Save the configuration file on exit"""
	
		with open(self._cfg_file, 'w') as configfile:
		    self._cfg.write(configfile)
