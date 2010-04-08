## about_dlg.py
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


import pygtk
pygtk.require('2.0')
import sys
import webbrowser
import gtk

import PacStats

class About_Dialog:
	"""Open the about dialog"""

	def __init__(self, ui_file, logo):
		gtk.about_dialog_set_url_hook(self._url_hook)

		ui = gtk.Builder()
		ui.add_from_file(ui_file)
		self._dialog = ui.get_object("about_dlg")

		self._dialog.set_version(PacStats.VERSION)
		self._dialog.set_logo(logo)
		self._dialog.run()
		self._dialog.destroy()
		return


	def _url_hook(dialog, link, user_data):
		"""Hook function called when a link in the about dialog is clicked"""
		if sys.version_info[:2] >= (2, 5):
			webbrowser.open_new_tab(user_data)
		else:
			webbrowser.Netscape('firefox').open(user_data) # priority given to Firefox

