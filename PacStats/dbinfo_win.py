## dbinfo_win.py
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

import logparser


class DBInfo_Window:
	"""Open the database information window"""
	def __init__(self, ui_file, database):
		self._database = database
		self._packages = database.packages
		self._transactions = database.transactions

		ui = gtk.Builder()
		ui.add_from_file(ui_file)

		# Getting widgets
		self.window = ui.get_object("dbinfo_win")
		self._packages_label = ui.get_object("packages_label")
		self._transactions_label = ui.get_object("transactions_label")
		self._first_label = ui.get_object("first_label")
		self._last_label = ui.get_object("last_label")
		self._synchronizations_label = ui.get_object("synchronizations_label")
		self._sysupgrades_label = ui.get_object("sysupgrades_label")
		self._installations_label = ui.get_object("installations_label")
		self._removals_label = ui.get_object("removals_label")
		self._upgrades_label = ui.get_object("upgrades_label")

		# Init methods
		self.setup_labels()

		self.window.show()


	def setup_labels(self):
		"""Setup information labels"""

		packages = self._database.query_one("SELECT COUNT(*) FROM %s;" % self._packages.name)[0]
		transactions = self._database.query_one("SELECT COUNT(*) FROM %s;" % self._transactions.name)[0]
		if transactions > 0:
			first = self._database.query_one("SELECT date, time FROM %s ORDER BY date ASC LIMIT 1;" % self._transactions.name)
			last = self._database.query_one("SELECT date, time FROM %s ORDER BY date DESC LIMIT 1;" % self._transactions.name)
		sync = self._database.query_one("SELECT COUNT(*) FROM %s WHERE action = ?;" % self._transactions.name, (logparser.SYNC, ))[0]
		sysup = self._database.query_one("SELECT COUNT(*) FROM %s WHERE action = ?;" % self._transactions.name, (logparser.SYSUP, ))[0]
		install = self._database.query_one("SELECT COUNT(*) FROM %s WHERE action = ?;" % self._transactions.name, (logparser.INSTALL, ))[0]
		remove = self._database.query_one("SELECT COUNT(*) FROM %s WHERE action = ?;" % self._transactions.name, (logparser.REMOVE, ))[0]
		upgrade = self._database.query_one("SELECT COUNT(*) FROM %s WHERE action = ?;" % self._transactions.name, (logparser.UPGRADE, ))[0]

		self._packages_label.set_text(str(packages))
		self._transactions_label.set_text(str(transactions))
		if transactions == 0:
			self._first_label.set_text(_('N/A'))
			self._last_label.set_text(_('N/A'))
		else:
			self._first_label.set_text(first[1] + ' ' + first[0])
			self._last_label.set_text(last[1] + ' ' + last[0])
		self._synchronizations_label.set_text(str(sync))
		self._sysupgrades_label.set_text(str(sysup))
		self._installations_label.set_text(str(install))
		self._removals_label.set_text(str(remove))
		self._upgrades_label.set_text(str(upgrade))
