#!/usr/bin/env python3

import sys
import os
from PyQt5.QtWidgets import QApplication, QStyleFactory
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

from tupelo_gui.main import Tupelo

if __name__ == "__main__":

	USER_DIR_BASE = os.path.expanduser('~')

	if getattr(sys, 'frozen', False):
		TUPELO_DIR = os.path.dirname(sys.executable)
	else:
		TUPELO_DIR = os.path.dirname(os.path.abspath(__file__))

	app = QApplication(sys.argv)
	app.setWindowIcon(QIcon(os.path.join(TUPELO_DIR, 'images', 'logo.ico')))
	app.setAttribute(Qt.AA_EnableHighDpiScaling)

	tupelo_window = Tupelo(TUPELO_DIR, USER_DIR_BASE)
	tupelo_window.show()

	sys.exit(app.exec_())

