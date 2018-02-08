#!/usr/bin/env python3

# Peter Sun
# hs859@cornell.edu

"""setup for the main window
"""

import os
import json
from functools import partial

from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QMainWindow, QAction, QDesktopWidget, QFrame

from tupelo_utils.shortcodes import _href_link_path 
from tupelo_gui.htmlview import TupeloWebView

class TupeloWindow(QMainWindow):

	def __init__(self):
		super().__init__()

	def move_center(self): # show window in the middle
		self.qtRectangle = self.frameGeometry()
		centerPoint = QDesktopWidget().availableGeometry().center()
		self.qtRectangle.moveCenter(centerPoint)
		self.move(self.qtRectangle.topLeft())

	def set_basics(self):
		self.set_menus()
		self.resize(1200, 750)
		self.setWindowTitle('Tupelo')

	def set_style(self, tupelo_dir):
		with open(os.path.join(tupelo_dir, 'css', 'qt_dark.css'), 'r') as qt_style:
			self.style = qt_style.read()
		self.setStyleSheet(self.style)

		# background image requries backslash (without 'file:///'')
		image_style = """
			background-image: url('{}') 100px 100px stretch stretch; 
			background-repeat: no-repeat; 
			background-position: center center;
			""".format(_href_link_path(os.path.join(tupelo_dir, 'images', 'tupelo.png')))

		self.background_image = QFrame(self)
		self.background_image.setGeometry(350, 100, 500, 550)
		self.background_image.setStyleSheet(image_style)

	def import_settings(self, user_dir_tupelo):
		## Import Settings
		try:
			with open(os.path.join(user_dir_tupelo, 'User_Settings.json'), 'r') as uset:
				self.view_settings = json.load(uset)
		except:
			print("Use default setting")
			self.view_settings = {
					'ScaleFactor': '1.2',
					'DefaultIndex': None,
					'Theme': 'Dark',
			}
			with open(os.path.join(user_dir_tupelo, 'User_Settings.json'), 'w+') as uset:
				json.dump(self.view_settings, uset)

	def set_menus(self):
		self.setup_trigger = QAction('New Notebook', self)
		self.setup_trigger.triggered.connect(self.new_nb_setup)

		main_menu = self.menuBar()
		main_menu.setNativeMenuBar(False)

		self.backAct = QAction('Back', self)	
		self.editAct = QAction('Edit', self)
		self.homeAct = QAction('Home', self)
		self.zoomOut = QAction('Zoom Out', self)
		self.zoomIn = QAction('Zoom In', self)
		self.setting = QAction('Setting', self)
		
		self.setting.triggered.connect(self.tupelo_settings)

		for action in [self.backAct, self.homeAct, self.editAct]:
			main_menu.addAction(action)
			action.setDisabled(True)

		self.view_menu = main_menu.addMenu('View')
		for view_option in [self.zoomIn, self.zoomOut]:
			self.view_menu.addAction(view_option)

		self.view_menu.setDisabled(True)
		self.note_menu = main_menu.addMenu('Notebooks')
		self.note_menu.addAction(self.setup_trigger)

		main_menu.addAction(self.setting)
		self.browser_action_lst = [self.backAct, self.editAct, self.homeAct, self.view_menu]

	def connect_browser_actions(self):
		# only activate when the browser is on
		self.backAct.triggered.connect(self.browser.back)
		self.editAct.triggered.connect(partial(self.browser.doc_edit, self.file_dict))
		self.homeAct.triggered.connect(self.browser.go_home)
		self.zoomOut.triggered.connect(self.browser.zoomOut)
		self.zoomIn.triggered.connect(self.browser.zoomIn)
		
		for action in self.browser_action_lst:
			action.setEnabled(True)

	def add_browser(self, url):
		self.browser = TupeloWebView(url)
		self.connect_browser_actions()
		self.setCentralWidget(self.browser)
		self.browser.setZoomFactor(float(self.view_settings['ScaleFactor']))