## libparser.py
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
from subject import Subject

class LibParser(Subject):
	"""A parser for the pacman lib"""
	def __init__(self, packages, libdir):

		Subject.__init__(self)
		self._packages = packages
		self._libdir = os.path.join(libdir, 'local')


	def parse(self):
		"""Parse the lib directory"""

		try:
			lib_listdir = os.listdir(self._libdir)
		except OSError:
			print('Cannot list \"%s\"!' % self._libdir)
			return
		print('Parsing the lib \"%s\"' % self._libdir)

		pkg_count = 0
		for pkg in lib_listdir:
			pkgdesc = os.path.join(self._libdir, pkg, 'desc')

			list = pkg.split('-')
			pkgname = '-'.join(list[:len(list)-2])
			pkgver = '-'.join(list[len(list)-2:])
			try:
				stored_pkg = self._packages.query("SELECT name, version FROM %s WHERE name='%s'" % \
					(self._packages.table, pkgname))[0]
			except IndexError:
				pass
			else:
				if stored_pkg[1] == pkgver:
					pkg_count += 1
					self.notify(float(pkg_count)/float(len(lib_listdir)))
					continue
				else:
					self._packages.query("DELETE FROM %s WHERE name='%s'" % (self._packages.table, pkgname))

			reas = 0 # Default value for packages missing this field

			f = open(pkgdesc)
			line = f.readline()
			while line:
				if line.find('%NAME%') == 0:
					name = f.readline().replace('\n', '')
				elif line.find('%VERSION%') == 0:
					ver = f.readline().replace('\n', '')
				elif line.find('%DESC%') == 0:
					desc = f.readline().replace('\n', '')
				elif line.find('%URL%') == 0:
					url = f.readline().replace('\n', '')
				elif line.find('%LICENSE%') == 0:
					lic = f.readline().replace('\n', '')
				elif line.find('%ARCH%') == 0:
					arch = f.readline().replace('\n', '')
				elif line.find('%BUILDDATE%') == 0:
					bepoch = f.readline().replace('\n', '')
				elif line.find('%INSTALLDATE%') == 0:
					iepoch = f.readline().replace('\n', '')
				elif line.find('%PACKAGER%') == 0:
					pack = f.readline().replace('\n', '')
				elif line.find('%SIZE%') == 0:
					size = int(f.readline())
				elif line.find('%REASON%') == 0:
					reas = int(f.readline())
				line = f.readline()
			f.close()
			pkg_count += 1

			self._packages.insert(name, ver, desc, url, lic, arch, bepoch, iepoch, pack, size, reas)
			self.notify(float(pkg_count)/float(len(lib_listdir)))
