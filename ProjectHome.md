## News ##
13 May 2010: Version 0.1 released!

## Description ##
[PacStats](http://pacstats.googlecode.com) is able to analyze the log and the lib directory of the [ArchLinux](http://www.archlinux.org) package manager ([pacman](http://www.archlinux.org/pacman/)) and generate statistical charts.
The GUI is programmed in [Python](http://www.python.org) with [PyGTK](http://www.pygtk.org), the internal database is based on [SQLite](http://www.sqlite.org/) and the charts are made with [Matplotlib](http://matplotlib.sourceforge.net/).
The application is currently in Beta stage, but the user is encouraged to try it and [report](http://code.google.com/p/pacstats/issues/list) any issue found.

## Screenshots ##
| ![http://lh5.ggpht.com/_GAUVUW68ti4/S9iE6zfljRI/AAAAAAAAAVM/Gt-HCfxfHgk/s576/monthly_transactions.png](http://lh5.ggpht.com/_GAUVUW68ti4/S9iE6zfljRI/AAAAAAAAAVM/Gt-HCfxfHgk/s576/monthly_transactions.png) | ![http://lh4.ggpht.com/_GAUVUW68ti4/S9YTev4XJmI/AAAAAAAAAUU/o6vy6etyLNA/s576/pie_repositories.png](http://lh4.ggpht.com/_GAUVUW68ti4/S9YTev4XJmI/AAAAAAAAAUU/o6vy6etyLNA/s576/pie_repositories.png) |
|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| ![http://lh5.ggpht.com/_GAUVUW68ti4/S8uHmCvFvXI/AAAAAAAAAQE/rFbb1YbtYuE/prefs_win.png](http://lh5.ggpht.com/_GAUVUW68ti4/S8uHmCvFvXI/AAAAAAAAAQE/rFbb1YbtYuE/prefs_win.png) | ![http://lh4.ggpht.com/_GAUVUW68ti4/S9CK4hnBhDI/AAAAAAAAASc/Tez_dKwqAbo/dbinfo_win.png](http://lh4.ggpht.com/_GAUVUW68ti4/S9CK4hnBhDI/AAAAAAAAASc/Tez_dKwqAbo/dbinfo_win.png) |

Screenshots from the remaining charts are on this [Picasa Album](http://picasaweb.google.it/encelo/PacStats#).

## Requirements ##
  * Python (Program)
  * GTK2, PyGTK (GUI)
  * SQLite, PySQLite if Python <= 2.4 (DB)
  * MatplotLib, NumPy (Statistical charts)
  * Epydoc and Graphviz (Docs generation)
### Package requirements ###
On ArchLinux most of the users should only need to type:
```
pacman -S python-matplotlib
```
to get also python-numpy.

If you haven't it already, install the pygtk package for the GUI to work.

Most of the users should already have a python>=2.5 package installed on their systems, which is enough for SQLite inclusion.

If you want to automatically generate the docs, issue the following command:
```
pacman -S epydoc graphviz
```

## Installation ##
This is intended as an application for ArchLinux users only, so the usual way of installing through pacman is the preferred one.

Download the PKGBUILD from AUR: [pacstats](http://aur.archlinux.org/packages.php?ID=37160) [pacstats-hg](http://aur.archlinux.org/packages.php?ID=36293)

### Direct installation ###
If you want to manually install the the program, type:
```
$ python setup.py install [ --root=path --prefix=path ]
```
You can specify a prefix (e.g. _/usr_) and an alternative root (e.g. _/mnt/hdb1_).

## Docs generation ##
To generate automatic documentation type:
```
$ epydoc -o epydoc --name=pacstats --url=http://pacstats.googlecode.com --graph=all PacStats/*.py PacStats/Charts/*.py
```

## Configuration ##
You can change the configuration through the preferences window, or manually, editing the configuration file.

The program creates a directory called "pacstats" inside $XDG\_CONFIG\_HOME (usually ~/.config) and then a pacstats.cfg file.

The default content looks like this:
```
[pacstats]
db = ~/.local/share/pacstats/pacstats.sqlite
log = /var/log/pacman.log
lib = /var/lib/pacman
```
The db key allows the user to choose the sqlite database.
The log and lib keys specify the log and lib directory of pacman, they are best left to their default values.