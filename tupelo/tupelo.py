#!/usr/bin/env python3

import sys
import os
from functools import partial

from PyQt5.QtWidgets import QApplication, QStyleFactory, QSplashScreen
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap

from tupelo_gui.tupelocore import TupeloCore
from tupelo_gui.pandoccheck import pandoc_install
from tupelo_utils.shortcodes import _except_record, _create_folder

from shutil import which

if __name__ == "__main__":

	USER_DIR = os.path.expanduser('~')

	if getattr(sys, 'frozen', False):
		TUPELO_DIR = os.path.dirname(sys.executable)
	else:
		TUPELO_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)))

	_create_folder(os.path.join(USER_DIR, '.tupelo'))
	sys.excepthook = partial(_except_record, user_dir = os.path.join(USER_DIR, '.tupelo'))

	if which('pandoc'): #Track if pandoc is executable
		print('Checked: Pandoc installed')
		app = QApplication(sys.argv)
		########## Add splash screen
		splash_pix = QPixmap(os.path.join(TUPELO_DIR, 'images', 'tupelo.png'))
		splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
		splash.show()
		##########################
		app.setWindowIcon(QIcon(os.path.join(TUPELO_DIR, 'images', 'logo.ico')))
		app.setAttribute(Qt.AA_EnableHighDpiScaling)
		tupelo = TupeloCore(TUPELO_DIR, USER_DIR)
		tupelo.show()
		splash.close()
		sys.exit(app.exec_())

	else: # if pandoc is not installed, prompt pandoc installation window
		pandoc_install()
		


