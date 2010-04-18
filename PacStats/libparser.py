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


from time import clock
import os
from subject import Subject


class LibParser(Subject):
	"""A parser for the pacman lib"""
	def __init__(self, database, libdir):

		Subject.__init__(self)
		self._database = database
		self._packages = database.packages
		self._libdir = os.path.join(libdir, 'local')


	def parse(self):
		"""Parse the lib directory"""

		start = clock()
		
		try:
			lib_listdir = os.listdir(self._libdir)
		except OSError:
			print('Cannot list \"%s\"!' % self._libdir)
			return
		print('Parsing the lib \"%s\"' % self._libdir)

		tuples = []
		pkg_count = 0
		for pkg in lib_listdir:
			pkgdesc = os.path.join(self._libdir, pkg, 'desc')

			list = pkg.split('-')
			pkgname = '-'.join(list[:len(list)-2])
			pkgver = '-'.join(list[len(list)-2:])
			
			SELECT = """SELECT name, version FROM %s WHERE name = ?""" % self._packages.name
			stored_pkg = self._database.query_one(SELECT, (pkgname, ))
			
			if stored_pkg != None:
				if stored_pkg[1] == pkgver:
					# Skipping the not updated package
					pkg_count += 1
					self.notify(float(pkg_count)/float(len(lib_listdir)))
					continue
				else:
					DELETE = """DELETE FROM %s WHERE name = ?""" % self._packages.name
					self._database.execute(DELETE, (pkgname, ))

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

#			self._packages.insert(name, ver, desc, url, lic, arch, bepoch, iepoch, pack, size, reas)
			tuples.append((name, ver, desc, url, lic, arch, bepoch, bepoch, iepoch, iepoch, pack, size, reas))
			self.notify(float(pkg_count)/float(len(lib_listdir)))
			
		self._packages.insert_many(tuples)
		self._database.commit() # committing one time at the end
		
		end = clock()
		print('Parsed in %f seconds' % (end-start))
