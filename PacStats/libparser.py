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
		self._libdir = libdir


	def parse(self):
		"""Parse the lib directory"""

		start = clock()

		localdir = os.path.join(self._libdir, 'local')
		syncdir = os.path.join(self._libdir, 'sync')
		
		try:
			local_listdir = os.listdir(localdir)
		except OSError:
			print('Cannot list \"%s\"!' % localdir)
			return
		print('Parsing the lib \"%s\"' % localdir)

		try:
			sync_listdir = os.listdir(syncdir)
		except OSError:
			print('Cannot list \"%s\"!' % syncdir)
			sync_listdir = None

		# The packages table is always cleared before parsing.
		# This ensures a correct synchronization even if the pacman 
		# library misses some package already in the database.
		self._packages.clear()

		tuples = []
		pkg_count = 0
		for pkgdir in local_listdir:
			pkgdesc = os.path.join(localdir, pkgdir, 'desc')

			list = pkgdir.split('-')
			pkgname = '-'.join(list[:len(list)-2])
			pkgver = '-'.join(list[len(list)-2:])

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

			repo = None
			for repodir in sync_listdir:
				if os.path.isdir(os.path.join(syncdir, repodir, pkgdir)):
					repo = repodir
					break

#			self._packages.insert(name, ver, desc, url, lic, arch, bepoch, iepoch, pack, size, reas, repo)
			tuples.append((name, ver, desc, url, lic, arch, bepoch, bepoch, iepoch, iepoch, pack, size, reas, repo))
			self.notify(float(pkg_count)/float(len(local_listdir)))
			
		self._packages.insert_many(tuples)
		self._database.commit() # committing one time at the end
		
		end = clock()
		print('Parsed in %f seconds' % (end-start))
