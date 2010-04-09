## setup.py
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

import sys
import os
from distutils.core import setup
from distutils.command import install 


def compile_po(path):
	for lang in os.listdir(path):
		if os.path.isdir(os.path.join(path, lang)) == False:
			continue

		po_file = os.path.join(path, lang, lang + '.po')
		lc_path = os.path.join(path, lang, 'LC_MESSAGES')
		if os.path.isdir(lc_path) == False:
			os.mkdir(lc_path)

		if os.path.isfile(po_file):
			mo_file = os.path.join(lc_path, 'pacstats.mo')
			args = ['msgfmt', '-c', '-o', mo_file, po_file]
			return os.spawnvp(os.P_WAIT, 'msgfmt', args)

def replace_paths_exe(fname):
	lines_p = []

	file = open(fname)
	for line in file:
		if line.find('share_dir =') != -1:
			line = 'share_dir = ' + "'" + os.path.join(prefix, 'share/pacstats') + "'" + '\n'
		elif line.find('locale_dir =') != -1:
			line = 'locale_dir = ' + "'" + os.path.join(prefix, 'share/locale') + "'" + '\n'
		lines_p.append(line)
	file.close()

	# Writing patched file
	file = open(fname, 'w')
	file.writelines(lines_p)
	file.close()

def replace_paths_desktop(fname):
	lines_p = []

	file = open(fname)
	for line in file:
		if line.find('Icon=') != -1:
			line = 'Icon=' + os.path.join(prefix, 'share/pacstats/pixmaps', 'icon.png') + '\n'
		lines_p.append(line)
	file.close()

	# Writing patched file
	file = open(fname, 'w')
	file.writelines(lines_p)
	file.close()


prefix = ''
if 'install' in sys.argv:
	prefix = sys.prefix # default
	for arg in sys.argv:
		if arg.find('--prefix') == 0:
			prefix = arg.split('=')[1]

print 'Compiling i18n files'
compile_po('po')
print 'Replacing data paths'
replace_paths_exe('pacstats')
replace_paths_desktop('pacstats.desktop')


setup(name='pacstats',
	version='0.1',
	description='ArchLinux\' Pacman statistical charts application',
	author='Angelo "Encelo" Theodorou',
	author_email='encelo@gmail.com',
	url='http://pacstats.googlecode.com',
	download_url='http://code.google.com/p/pacstats/downloads/list',
	license = 'GNU GENERAL PUBLIC LICENSE',
	classifiers=[
          'Development Status :: 3 - Alpha',
          'Environment :: X11 Applications :: GTK',
          'Intended Audience :: End Users/Desktop',
          'Intended Audience :: System Administrators',
          'License :: OSI Approved :: GNU General Public License (GPL)',
          'Operating System :: POSIX :: Linux',
          'Programming Language :: Python',
		  'Topic :: System',
          'Topic :: Utilities',
          ],
	requires=['pygtk', 'matplotlib', 'numpy'],
	packages=['PacStats', 'PacStats/charts'],
	scripts=['pacstats'],
	data_files=[('share/pacstats/ui', ['ui/about_dlg.ui', 'ui/main_win.ui']),
				('share/locale/it/LC_MESSAGES', ['po/it/LC_MESSAGES/pacstats.mo']),
				('share/pacstats/pixmaps', ['pixmaps/icon.png', 'pixmaps/logo.png']),
				('share/applications', ['pacstats.desktop'])]
	)
