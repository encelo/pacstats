## libparser.py
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
from subject import Subject

class LibParser(Subject):
	"""A parser for the pacman lib"""
	def __init__(self, packages):

		Subject.__init__(self)

		self.packages = packages


	def parse(self, libdir='/var/lib/pacman/local'):
		"""Parse the lib directory"""

		try:
			lib_listdir = os.listdir(libdir)
		except OSError:
			print _('Cannot list %s!') % libdir
			return

		pkg_count = 0
		for pkg in lib_listdir:
			pkgdesc = os.path.join(libdir, pkg, 'desc')

			list = pkg.split('-')
			pkgname = '-'.join(list[:len(list)-2])
			pkgver = '-'.join(list[len(list)-2:])
			try:
				stored_pkg = self.packages.query("SELECT name, version FROM %s WHERE name='%s'" % \
					(self.packages.table, pkgname))[0]
			except IndexError:
				pass
			else:
				if stored_pkg[1] == pkgver:
					pkg_count += 1
					self.notify(float(pkg_count)/float(len(lib_listdir)))
					continue
				else:
					self.packages.query("DELETE FROM %s WHERE name='%s'" % (self.packages.table, pkgname))

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
					bdate = f.readline().replace('\n', '')
				elif line.find('%INSTALLDATE%') == 0:
					idate = f.readline().replace('\n', '')
				elif line.find('%PACKAGER%') == 0:
					pack = f.readline().replace('\n', '')
				elif line.find('%SIZE%') == 0:
					size = int(f.readline())
				elif line.find('%REASON%') == 0:
					reas = int(f.readline())
				line = f.readline()
			f.close()
			pkg_count += 1

			self.packages.insert(name, ver, desc, url, lic, arch, bdate, idate, pack, size, reas)
			self.notify(float(pkg_count)/float(len(lib_listdir)))
