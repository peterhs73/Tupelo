#!/usr/bin/env python3

import os
import sys
import time
import json
import shutil
from functools import partial

from PyQt5.QtCore import QUrl, pyqtSignal, pyqtSlot, QThreadPool, QThread
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QAction, QApplication, QDesktopWidget, QFrame

from tupelo_utils.shortcodes import _create_folder, _file_dict
from tupelo_utils.notebook import tupelo_update
from tupelo_gui.threads import TupeloThread
from tupelo_gui.watcher import LiveEdit
from tupelo_gui.htmlview import TupeloWebView
from tupelo_gui.setnotebook import NotebookInfo

class Tupelo(QMainWindow):

	thread_abort = pyqtSignal()

	def __init__(self, tupelo_dir, user_dir_base):
		super().__init__()
		self.thread_pool = QThreadPool()
		self.notebooks = []
		self.__threads = []

		# File Location Setup
		self.tupelo_dir = tupelo_dir
		self.user_dir_base = user_dir_base
		self.user_dir_desktop = os.path.join(user_dir_base, 'Desktop')
		self.user_info_path = os.path.join(user_dir_base, 'Documents', '.tupelo', 'user', 'user_info.json')
		_create_folder(os.path.join(user_dir_base, 'Documents', '.tupelo', 'user'))

		self.file_dict = {}
		with open(os.path.join(self.tupelo_dir, 'css', 'qt_dark.css'), 'r') as qt_style:
			self.style = qt_style.read()
		self.initUI()
		self.show()
		print('shown, start live edit')
		self.start_live_edit_threads(self.notebooks)
		for notebook_info in self.notebooks:
			self.file_dict.update(_file_dict(notebook_info['dst_folder']))

	def initUI(self):
		self.setStyleSheet(self.style)
		self.set_menus()
		self.resize(1100, 750)
		self.move_center() 
		self.setWindowTitle('Tupelo')
		self.background()
		self.notebook_menu() ## start another thread of this 

		# self.setWindowIcon(QIcon(os.path.normcase('tupelo_gui/gui_files/logo.png')))

	def background(self):
		image_style = """
			background-image: url('images/logo.png') 100px 100px stretch stretch; 
			background-repeat: no-repeat; 
			background-position: center center;
			"""
		self.background_image = QFrame(self)
		self.background_image.setGeometry(300, 125, 500, 500)
		self.background_image.setStyleSheet(image_style)

	def move_center(self): # show window in the middle
		self.qtRectangle = self.frameGeometry()
		centerPoint = QDesktopWidget().availableGeometry().center()
		self.qtRectangle.moveCenter(centerPoint)
		self.move(self.qtRectangle.topLeft())

	def set_menus(self):
		self.setup_trigger = QAction('new notebook', self)
		self.setup_trigger.triggered.connect(self.setup_page)

		main_menu = self.menuBar()
		main_menu.setNativeMenuBar(False)

		self.backAct = QAction('Back', self)	
		self.editAct = QAction('Edit', self)
		self.homeAct = QAction('Home', self)

		for action in [self.backAct, self.editAct, self.homeAct]:
			main_menu.addAction(action)
			action.setDisabled(True)

		self.note_menu = main_menu.addMenu('Notebooks')
		self.note_menu.addAction(self.setup_trigger)

	def browser_actions(self):
		self.backAct.triggered.connect(self.browser.back)
		self.editAct.triggered.connect(partial(self.browser.doc_edit, self.file_dict))
		self.homeAct.triggered.connect(self.browser.go_home)

		for action in [self.backAct, self.editAct, self.homeAct]:
			action.setEnabled(True)

	@pyqtSlot()
	def add_browser(self, url):
		self.browser = TupeloWebView(url)
		self.browser_actions()
		self.setCentralWidget(self.browser)

	# This part takes care of notebook setups when startup 
	def notebook_menu(self):
		"""this part is to design to auto add the menu when startup. 
		"""
		try:
			print('started')
			notebooks_list_new = []
			with open(self.user_info_path, 'r') as user_info:
				self.notebooks = json.load(user_info)
			for notebook_info in self.notebooks:
				if os.path.isdir(notebook_info['src_folder']): # check if dir still exsit
					notebooks_list_new.append(notebook_info)
					action = self.note_menu.addAction(notebook_info['nickname'])
					action.triggered.connect(partial(self.add_browser, notebook_info['index_url']))
					self.notebook_update_thread(notebook_info)
				elif os.path.isdir(notebook_info['dst_folder']):
					print('{} is deleted, deleted folder {}'.format(notebook_info['src_folder'], notebook_info['nickname']))
					shutil.rmtree(notebook_info['dst_folder'])

			with open(self.user_info_path, 'w+') as user_info:
				json.dump(notebooks_list_new, user_info)

			self.notebooks = notebooks_list_new  #clean up the notebook list
		except:
			print('No notebook stored')
			self.notebooks = []

		print('Tupelo Statup Check completed, now show the GUI')

	def notebook_update_thread(self, notebook_info):
		# Thread for updating notebooks
		notebook_update = TupeloThread(tupelo_update, notebook_info['filetypes'], notebook_info['src_folder'], notebook_info['dst_folder'], self.tupelo_dir)
		notebook_update.signals.finished.connect(self.thread_complete)
		self.thread_pool.start(notebook_update)

	# This part starts the setup pages for the notebooks (new notebook action)

	@pyqtSlot()
	def setup_page(self):
		for action in [self.backAct, self.editAct, self.homeAct]:
			action.setDisabled(True)
		try:
			self.background_image.close()
			self.browser.close()
		except:
			pass 
			print('nothing to close')

		self.user_info = NotebookInfo(self.notebooks, self.user_dir_base, parent = self)
		self.user_info.setGeometry(350, 250, 400, 170) # set for the resize (1100 - 350 /2, 750 - 150 /2)
		self.user_info.show()

		self.user_info.setup_sig.connect(self.notebook_gen_thread) # collect the signal from NotebookInfo, which is a notebook dictionary

	def notebook_gen(self, notebook_info): 
		# need to turn off the live edit first
		tupelo_update(notebook_info['filetypes'], notebook_info['src_folder'], notebook_info['dst_folder'], self.tupelo_dir)
		print('adding {} to live edit thread'.format(notebook_info['src_folder']))
		self.start_live_edit_threads([notebook_info])
		print('current live edit folders are {}'.format(self.__threads))

	def notebook_gen_complete(self, notebook_info):

		print('notebook setup finished')

		self.add_browser(notebook_info['index_url'])
		action = self.note_menu.addAction(notebook_info['nickname'])
		action.triggered.connect(partial(self.add_browser, notebook_info['index_url']))
		
		self.notebooks.append(notebook_info)

		with open(self.user_info_path, 'w+') as user_info:
			json.dump(self.notebooks, user_info)
		self.file_dict.update(_file_dict(notebook_info['dst_folder']))

	@pyqtSlot(dict)
	def notebook_gen_thread(self, notebook_info):

		notebook_gen = TupeloThread(self.notebook_gen, notebook_info)
		notebook_gen.signals.finished.connect(partial(self.notebook_gen_complete, notebook_info))
		self.thread_pool.start(notebook_gen)

	def thread_complete(self):
		print("notebook updated")
		
	def start_live_edit_threads(self, notebooks_list):

		for notebook in notebooks_list:
			LiveEditEvent = LiveEdit(notebook, self.tupelo_dir)
			thread = QThread()
			# thread.setObjectName('watch folder' + notebook['src_folder'])
			self.__threads.append((thread, LiveEditEvent))
			LiveEditEvent.moveToThread(thread)

			LiveEditEvent.sig_done.connect(self.on_thread_done)
			LiveEditEvent.sig_event.connect(self.on_thread_message)
			LiveEditEvent.sig_move_event.connect(self.on_move_message)

			self.thread_abort.connect(LiveEditEvent.abort)
			thread.started.connect(LiveEditEvent.run)
			thread.start()

	@pyqtSlot(list)
	def on_thread_message(self, doc_info):
		cur_url = self.browser.url().toString()[:-5]
		try:
			self.file_dict[doc_info[1]] = doc_info[2]
			if cur_url == doc_info[2]:
				self.browser.reload()
			elif cur_url == doc_info[0]:
				self.browser.reload()
		except:
			print('File changed {}'.format(doc_info[1]))

	@pyqtSlot(list)
	def on_move_message(self, doc_move_info):
		cur_url =self.browser.url().toString()[:-5]
		try:
			self.file_dict[doc_move_info[2]] = doc_move_info[4]
			if cur_url == doc_move_info[3]: # if it matches the old file, load the new file
				self.browser.load(QUrl(doc_move_info[4]))
			elif cur_url == doc_move_info[0]:
				self.browser.reload()
		except:
			print('File moved from {} to {}'.format(doc_move_info[1], doc_move_info[2]))

	@pyqtSlot(str)
	def on_thread_done(self, message):
		print('Live Edit Existed')

	def abort_live_edit(self):
		self.thread_abort.emit()
		print('sending signal: turning off all live folder watch')
		for thread, EditEvent in self.__threads:  # note nice unpacking by Python, avoids indexing
			thread.quit()  # this will quit **as soon as thread event loop unblocks**
			thread.wait()  # <- so you need to wait for it to *actually* quit
			self.__threads = [] 

		self.print('All threads exited')