## main_win.py
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
from os import stat
import pygtk
pygtk.require('2.0')
import gtk

import about_dlg, dbinfo_win, prefs_win


class Main_Window:
	def __init__(self, app_cls):
		"""Handle the main window"""
		# Getting instances of "singleton" classes

		self._settings = app_cls.settings
		self._transactions = app_cls.transactions
		self._logparser = app_cls.logparser
		self._packages = app_cls.packages
		self._libparser = app_cls.libparser
		self._charts = app_cls.charts

		self._share_dir = app_cls.share_dir
		self._ui_dir = app_cls.ui_dir

		ui = gtk.Builder()
		ui.add_from_file(os.path.join(self._ui_dir, 'main_win.ui'))

		app_signals = {
			"on_main_win_destroy": self.on_main_win_destroy,
			"on_prefs_activate": self.on_prefs_activate,
			"on_quit_activate": self.on_quit_activate,
			"on_info_db_activate": self.on_info_db_activate,
			"on_optimize_db_activate": self.on_optimize_db_activate,
			"on_update_db_activate": self.on_update_db_activate,
			"on_clear_db_activate": self.on_clear_db_activate,
			"on_dump_db_activate": self.on_dump_db_activate,
			"on_about_activate": self.on_about_activate,
			"on_charts_list_button_press_event": self.on_charts_list_button_press_event,
			"on_charts_list_row_activated": self.on_charts_list_row_activated
		}
		ui.connect_signals(app_signals)

		# Getting widgets
		self._window = ui.get_object("main_win")
		self._vpaned = ui.get_object("vpaned")
		self._charts_list = ui.get_object("charts_list")
		self._liststore = ui.get_object("liststore")
		self._chart_vbox = ui.get_object("chart_vbox")
		self._statusbar = ui.get_object("statusbar")
		
		# Open/close window flags
		self._prefs_win = None
		self._dbinfo_win = None

		# Init
		self._logo = gtk.gdk.pixbuf_new_from_file(os.path.join(self._share_dir, 'pixmaps/logo.png'))
		pix = gtk.gdk.pixbuf_new_from_file(os.path.join(self._share_dir, 'pixmaps/icon.png'))
		gtk.window_set_default_icon(pix)
		self._window.set_icon(pix)

		self.populate_charts_list()
		self._active_chart = None
		self._window.show()

		# Parsing
		self._pb = gtk.ProgressBar()
		self._statusbar.pack_start(self._pb)
		self._logparser.attach(self)
		self._libparser.attach(self)

#		on_update_db_activate()


	def setup_dbstatus(self):
		"""Setup DB info in the statusbar"""

		packages = self._packages.query("SELECT COUNT(*) FROM packages;")[0][0]
		transactions = self._transactions.query("SELECT COUNT(*) FROM transactions;")[0][0]
		string = _('Packages: %d Transactions: %d') % (packages, transactions)

		self._statusbar.push(1, string)


	def populate_charts_list(self):
		"""Populate the treeview with charts"""
		for name in self._charts.get_names():
			chart = self._charts.get_chart(name)
			self._liststore.append([chart.get_name(), chart.get_description(), chart.get_version()])


	def attach_chart(self, chart):
		"""The given chart become the active one"""

		if self._active_chart:
			self.detach_chart()

		self._active_chart = chart
		chart.attach(self._chart_vbox)


	def detach_chart(self):
		"""The active chart got detached"""

		if self._active_chart:
			self._active_chart.detach()
			self._active_chart = None


	def notify(self, arg):
		"""Drive the ProgressBar"""

		self._pb.set_fraction(arg)
		self._pb.set_text('%d%%' % (arg*100))
		while gtk.events_pending():
			gtk.main_iteration()


	# Callbacks
	def on_main_win_destroy(self, widget, data=None):
		"""Quit the application"""
		return gtk.main_quit()


	def on_prefs_activate(self, event):
		"""Open the preferences window"""

		if self._prefs_win:
			self._prefs_win.window.present()
		else:
			ui_file = os.path.join(self._ui_dir, 'prefs_win.ui')
			self._prefs_win = prefs_win.Preferences_Window(ui_file, self._settings)
			self._prefs_win.window.connect('destroy', self.on_prefs_destroy)


	def on_prefs_destroy(self, event):
		"""Close the preferences window"""
		self._prefs_win = None


	def on_quit_activate(self, event):
		"""Quit the application"""
		return gtk.main_quit()


	def on_info_db_activate(self, event):
		"""Open the database Information window"""

		if self._dbinfo_win:
			self._dbinfo_win.window.present()
		else:
			ui_file = os.path.join(self._ui_dir, 'dbinfo_win.ui')
			self._dbinfo_win = dbinfo_win.DBInfo_Window(ui_file, self._packages, self._transactions)
			self._dbinfo_win.window.connect('destroy', self.on_info_db_destroy)


	def on_info_db_destroy(self, event):
		"""Close the database information window"""
		self._dbinfo_win = None


	def on_update_db_activate(self, event):
		"""Update the database"""

		self._pb.show()
		self._vpaned.set_sensitive(False)
		self._statusbar.push(1, _('Parsing the log file...'))
		self._logparser.parse()
		self._statusbar.pop(1)
		self._statusbar.push(1, _('Parsing the library...'))
		self._libparser.parse()
		self._statusbar.pop(1)
		self._pb.hide()

		self.setup_dbstatus()
		self._vpaned.set_sensitive(True)


	def on_optimize_db_activate(self, event):
		"""Optimize the database and open an informative dialog"""

		old_size = stat(self._settings.db).st_size
		self._packages.vacuum() # this call is enough for the whole DB
		new_size = stat(self._settings.db).st_size

		dlg = gtk.MessageDialog(type=gtk.MESSAGE_INFO, buttons=gtk.BUTTONS_OK,
			message_format=_('Database optimized. The new file size is %s bytes (%s bytes less).' % (new_size, old_size-new_size)))
		dlg.run()
		dlg.destroy()


	def on_clear_db_activate(self, event):
		"""Clear the whole database"""

		dlg = gtk.MessageDialog(type=gtk.MESSAGE_QUESTION, buttons=gtk.BUTTONS_YES_NO,
			message_format=_('Do you really want to clear the database?'))
		dlg.set_default_response(gtk.RESPONSE_NO)
		response = dlg.run()
		dlg.destroy()

		if response == gtk.RESPONSE_NO:
			return
		else:
			self._statusbar.push(1, _('Clearing the database...'))
			self._transactions.clear()
			self._logparser.reset_seek()
			self._packages.clear()
			self._statusbar.pop(1)
			self.setup_dbstatus()


	def on_dump_db_activate(self, event):
		"""Dump the database in a text file"""

		dlg = gtk.FileChooserDialog(_('DB Dump'), self._window, gtk.FILE_CHOOSER_ACTION_SAVE,
			(gtk.STOCK_OK, gtk.RESPONSE_ACCEPT, gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT))
		dlg.set_default_response(gtk.RESPONSE_ACCEPT)
		response = dlg.run()

		if response == gtk.RESPONSE_ACCEPT:
			file = dlg.get_filename()
		else:
			dlg.destroy()
			return
			
		dlg.destroy()
		self._statusbar.push(1, _('Saving the transactions table as ') + file + '_transactions.db')
		self._transactions.save_as(file + '_transactions.txt')
		self._statusbar.pop(1)
		self._statusbar.push(1, _('Saving the packages table as ') + file + '_packages.db')
		self._packages.save_as(file + '_packages.txt')
		self._statusbar.pop(1)


	def on_about_activate(self, event):
		"""Open the about dialog"""

		ui_file = os.path.join(self._ui_dir, 'about_dlg.ui')
		about_dlg.About_Dialog(ui_file, self._logo)


	def on_charts_list_button_press_event(self, widget, event, data=None):
		"""A treeview element was clicked once"""

		try:
			(path, column, x, y) = self._charts_list.get_path_at_pos(
				int(event.x),
				int(event.y),
			)
		except TypeError: # Returned None, no path at that position
			return

		self._charts_list.row_activated(path, self._charts_list.get_column(0))


	def on_charts_list_row_activated(self, treeview, path, view_column):
		"""A treeview element was activated"""
		iter = self._liststore.get_iter(path)
		(selname, ) = self._liststore.get(iter, 0)

		chart = self._charts.get_chart(selname)
		if chart != None:
			self.detach_chart()
			self.attach_chart(chart)
