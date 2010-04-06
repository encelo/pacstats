## main_win.py
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


import pygtk
pygtk.require('2.0')
import gtk.glade

import about_dlg


class Main_Window:
	def __init__(self, app_cls):
		"""Handle the main window"""
		# Getting instances of "singleton" classes

		self.settings = app_cls.settings
		self.transactions = app_cls.transactions
		self.logparser = app_cls.logparser
		self.packages = app_cls.packages
		self.libparser = app_cls.libparser
		self.charts = app_cls.charts

		self.glade_file = 'pacstats.glade'
		self.xml = gtk.glade.XML(self.glade_file, root="main_win")

		app_signals = {
			"on_main_win_destroy": self.on_main_win_destroy,
			"on_quit_activate": self.on_quit_activate,
			"on_clear_db_activate": self.on_clear_db_activate,
			"on_update_db_activate": self.on_update_db_activate,
			"on_dump_db_activate": self.on_dump_db_activate,
			"on_about_activate": self.on_about_activate,
			"on_charts_list_button_press_event": self.on_charts_list_button_press_event,
			"on_charts_list_row_activated": self.on_charts_list_row_activated
		}
		self.xml.signal_autoconnect(app_signals)

		# Getting widgets
		self.window = self.xml.get_widget("main_win")
		self.charts_list = self.xml.get_widget("charts_list")
		self.chart_vbox = self.xml.get_widget("chart_vbox")
		self.statusbar = self.xml.get_widget("statusbar")

		# Setting initial attributes
		#pix = gtk.gdk.pixbuf_new_from_file(os.path.join(self.share_dir, 'pixmaps/globs.png'))
		#gtk.window_set_default_icon(pix)
		#self.window.set_icon(pix)

		# Init methods
		self.setup_charts_list()
		self.populate_charts_list()

		# parsing
		self.pb = gtk.ProgressBar()
		self.statusbar.pack_start(self.pb)
		self.logparser.attach(self)
		self.libparser.attach(self)

		self.pb.show()
		self.window.set_sensitive(False)
		self.statusbar.push(1, _('Parsing the log file...'))
		self.logparser.parse()
		self.statusbar.pop(1)
		self.statusbar.push(1, _('Parsing the library...'))
		self.libparser.parse()
 		self.statusbar.pop(1)
		self.pb.hide()

		self.setup_dbstatus()
		self.window.set_sensitive(True)


		self.active_chart = None


	def setup_dbstatus(self):
		"""Setup DB info in the statusbar"""

		packages = self.packages.query("SELECT COUNT(*) FROM packages;")[0]

		transactions = self.transactions.query("SELECT COUNT(*) FROM transactions;")[0]
		if transactions[0] == 0:
			first = ['', '']
			last = ['', '']
		else:
			first = self.transactions.query("SELECT date, time FROM transactions ORDER BY date ASC LIMIT 1;")[0]
			last = self.transactions.query("SELECT date, time FROM transactions ORDER BY date DESC LIMIT 1;")[0]

		string = _('Packages: %d   | Transactions: %d   first: %s %s   last: %s %s') % (packages[0], transactions[0], first[0], first[1], last[0], last[1])

		self.statusbar.push(1, string)


	def setup_charts_list(self):
		"""Setup the treeview for charts list"""
		cell = gtk.CellRendererText()

		# Columns
		column = gtk.TreeViewColumn(_('Name'))
		column.pack_start(cell, True)
		column.add_attribute(cell, 'text', 0)
		column.set_resizable(True)
		column.set_sort_column_id(0)
		self.charts_list.append_column(column)

		column = gtk.TreeViewColumn(_('Description'))
		column.pack_start(cell, True)
		column.add_attribute(cell, 'text', 1)
		column.set_resizable(True)
		column.set_sort_column_id(1)
		self.charts_list.append_column(column)

		column = gtk.TreeViewColumn(_('Version'))
		column.pack_start(cell, True)
		column.add_attribute(cell, 'text', 2)
		column.set_resizable(True)
		column.set_sort_column_id(2)
		self.charts_list.append_column(column)

		# Model
		self.liststore = gtk.ListStore(str, str, str)
		self.charts_list.set_model(self.liststore)


	def populate_charts_list(self):
		"""Populate the treeview with charts"""
		for name in self.charts.get_names():
			chart = self.charts.get_chart(name)
			self.liststore.append([chart.get_name(), chart.get_description(), chart.get_version()])


	def attach_chart(self, chart):
		"""The given chart become the active one"""

		if self.active_chart:
			self.detach_chart()

		self.active_chart = chart
		chart.attach(self.chart_vbox)


	def detach_chart(self):
		"""The active chart got detached"""

		if self.active_chart:
			self.active_chart.detach()
			self.active_chart = None


	def notify(self, arg):
		"""Drive the ProgressBar"""

		self.pb.set_fraction(arg)
		self.pb.set_text('%d%%' % (arg*100))
		while gtk.events_pending():
			gtk.main_iteration()


	# Callbacks
	def on_main_win_destroy(self, widget, data=None):
		"""Quit the application"""
		return gtk.main_quit()


	def on_quit_activate(self, event):
		"""Quit the application"""
		return gtk.main_quit()


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
			self.statusbar.push(1, _('Clearing the database...'))
			self.transactions.clear()
			self.settings.set('log_seek', 0)
			self.packages.clear()
			self.statusbar.pop(1)
			self.setup_dbstatus()


	def on_update_db_activate(self, event):
		"""Update the database"""

		self.pb.show()
		self.window.set_sensitive(False)
		self.statusbar.push(1, _('Parsing the log file...'))
		self.logparser.parse()
		self.statusbar.pop(1)
		self.statusbar.push(1, _('Parsing the library...'))
		self.libparser.parse()
		self.statusbar.pop(1)
		self.pb.hide()

		self.setup_dbstatus()
		self.window.set_sensitive(True)


	def on_dump_db_activate(self, event):
		"""Dump the database in a text file"""

		dlg = gtk.FileChooserDialog(_('DB Dump'), self.window, gtk.FILE_CHOOSER_ACTION_SAVE,
			(gtk.STOCK_OK, gtk.RESPONSE_ACCEPT, gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT))
		dlg.set_default_response(gtk.RESPONSE_ACCEPT)
		response = dlg.run()

		if response == gtk.RESPONSE_ACCEPT:
			file = dlg.get_filename()
		else:
			dlg.destroy()
			return
			
		dlg.destroy()
		self.statusbar.push(1, _('Saving the transactions table as ') + file + '_transactions.db')
		self.transactions.save_as(file + '_transactions.db')
		self.statusbar.pop(1)
		self.statusbar.push(1, _('Saving the packages table as ') + file + '_packages.db')
		self.packages.save_as(file + '_packages.db')
		self.statusbar.pop(1)


	def on_about_activate(self, event):
		"""Open the about dialog"""

		about_dlg.About_Dialog(self.glade_file)
		return


	def on_charts_list_button_press_event(self, widget, event, data=None):
		"""A treeview element was clicked once"""

		try:
			(path, column, x, y) = self.charts_list.get_path_at_pos(
				int(event.x),
				int(event.y),
			)
		except TypeError: # Returned None, no path at that position
			return

		self.charts_list.row_activated(path, self.charts_list.get_column(0))


	def on_charts_list_row_activated(self, treeview, path, view_column):
		"""A treeview element was activated"""
		iter = self.liststore.get_iter(path)
		(selname, ) = self.liststore.get(iter, 0)

		for modname in self.charts.get_names():
			chart = self.charts.get_chart(modname)
			if chart.get_name() == selname:
				self.detach_chart()
				self.attach_chart(chart)
