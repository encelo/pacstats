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
	def __init__(self, ui_file, packages, transactions):
		self._packages = packages
		self._transactions = transactions

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
		self.setup_entries()

		self.window.show()


	def setup_entries(self):
		"""Setup information labels"""

		packages = self._packages.query("SELECT COUNT(*) FROM packages;")[0][0]
		transactions = self._transactions.query("SELECT COUNT(*) FROM transactions;")[0][0]
		if transactions == 0:
			first = ['', '']
			last = ['', '']
		else:
			first = self._transactions.query("SELECT date, time FROM transactions ORDER BY date ASC LIMIT 1;")[0]
			last = self._transactions.query("SELECT date, time FROM transactions ORDER BY date DESC LIMIT 1;")[0]
		sync = self._transactions.query("SELECT COUNT(*) FROM transactions WHERE action=%s;" % logparser.SYNC)[0][0]
		sysup = self._transactions.query("SELECT COUNT(*) FROM transactions WHERE action=%s;" % logparser.SYSUP)[0][0]
		install = self._transactions.query("SELECT COUNT(*) FROM transactions WHERE action=%s;" % logparser.INSTALL)[0][0]
		remove = self._transactions.query("SELECT COUNT(*) FROM transactions WHERE action=%s;" % logparser.REMOVE)[0][0]
		upgrade = self._transactions.query("SELECT COUNT(*) FROM transactions WHERE action=%s;" % logparser.UPGRADE)[0][0]

		self._packages_label.set_text(str(packages))
		self._transactions_label.set_text(str(transactions))
		self._first_label.set_text(first[1] + ' ' + first[0])
		self._last_label.set_text(last[1] + ' ' + last[0])
		self._synchronizations_label.set_text(str(sync))
		self._sysupgrades_label.set_text(str(sysup))
		self._installations_label.set_text(str(install))
		self._removals_label.set_text(str(remove))
		self._upgrades_label.set_text(str(upgrade))
