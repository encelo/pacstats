## prefs_win.py
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
import gtk


class Preferences_Window:
	"""Open the preferences window"""
	def __init__(self, ui_file, settings):
		self._settings = settings

		ui = gtk.Builder()
		ui.add_from_file(ui_file)

		app_signals = {
			"on_cancel_button_clicked": self.on_cancel_button_clicked,
			"on_apply_button_clicked": self.on_apply_button_clicked,
			"on_db_entry_activate": self.on_db_entry_activate,
			"on_db_entry_icon_press": self.on_db_entry_icon_press,
			"on_log_entry_activate": self.on_log_entry_activate,
			"on_log_entry_icon_press": self.on_log_entry_icon_press,
			"on_lib_entry_activate": self.on_lib_entry_activate,
			"on_lib_entry_icon_press": self.on_lib_entry_icon_press,
		}
		ui.connect_signals(app_signals)

		# Getting widgets
		self.window = ui.get_object("prefs_win")
		self._db_entry = ui.get_object("db_entry")
		self._log_entry = ui.get_object("log_entry")
		self._lib_entry = ui.get_object("lib_entry")

		# Init methods
		self.setup_entries()
		self.check_entries()

		self.window.show()


	def setup_entries(self):
		"""Setup configuration entrie"""

		self._db_entry.set_text(self._settings.db)
		self._log_entry.set_text(self._settings.log)
		self._lib_entry.set_text(self._settings.lib)

		self._valid_db = self._settings.default_db
		self._valid_log = self._settings.default_log
		self._valid_lib = self._settings.default_lib


	def check_entries(self):
		"""Check entries validity to setup the stock icon"""

		self.check_db_entry()
		self.check_log_entry()
		self.check_lib_entry()


	def check_db_entry(self):
		db = self._db_entry.get_text()

		if self._settings.check_db(db) == True:
			self._db_entry.props.primary_icon_stock = gtk.STOCK_YES
			self._valid_db = db
		else:
			self._db_entry.props.primary_icon_stock = gtk.STOCK_NO

	def check_log_entry(self):
		log = self._log_entry.get_text()

		if self._settings.check_log(log) == True:
			self._log_entry.props.primary_icon_stock = gtk.STOCK_YES
			self._valid_log = log
		else:
			self._log_entry.props.primary_icon_stock = gtk.STOCK_NO
		
	def check_lib_entry(self):
		lib = self._lib_entry.get_text()

		if self._settings.check_lib(lib) == True:
			self._lib_entry.props.primary_icon_stock = gtk.STOCK_YES
			self._valid_lib = lib
		else:
			self._lib_entry.props.primary_icon_stock = gtk.STOCK_NO


	#Callbacks
	def on_cancel_button_clicked(self, event):
		"""Close the preferences window"""
		self.window.destroy()


	def on_apply_button_clicked(self, event):
		"""Save the configurations and close the window"""

		self._settings.set_db(self._db_entry.get_text())
		self._settings.set_log(self._log_entry.get_text())
		self._settings.set_lib(self._lib_entry.get_text())
		self._settings.write()

		self.window.destroy()


	def on_db_entry_activate(self, event):
		self.check_db_entry()

	def on_db_entry_icon_press(self, entry, icon_pos, event):
		self._db_entry.set_text(self._valid_db)
		self.check_db_entry()

	def on_log_entry_activate(self, event):
		self.check_log_entry()

	def on_log_entry_icon_press(self, entry, icon_pos, event):
		self._log_entry.set_text(self._valid_log)
		self.check_log_entry()

	def on_lib_entry_activate(self, event):
		self.check_lib_entry()

	def on_lib_entry_icon_press(self, entry, icon_pos, event):
		self._lib_entry.set_text(self._valid_lib)
		self.check_lib_entry()
