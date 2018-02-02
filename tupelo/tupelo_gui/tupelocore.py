#!/usr/bin/env python3

# Peter Sun
# hs859@cornell.edu

import os
import sys
import json
import shutil
from functools import partial

from PyQt5.QtCore import QUrl, pyqtSignal, pyqtSlot, QThreadPool, QThread
from PyQt5.QtWidgets import QAction, QDesktopWidget, QFrame

from tupelo_utils.shortcodes import _create_folder, _file_dict, _href_link_path 
from tupelo_utils.notebook import tupelo_update, notebook_info_grab
from tupelo_utils.threads import TupeloThread
from tupelo_utils.watcher import LiveEdit

from tupelo_gui.newnbpage import NewNotebook
from tupelo_gui.settingpage import NBSettings
from tupelo_gui.mainwindow import TupeloWindow


class TupeloCore(TupeloWindow):

	thread_abort = pyqtSignal()

	def __init__(self, tupelo_dir, user_dir):
		super().__init__()

		# File Location Setup
		self.tupelo_dir = tupelo_dir
		self.user_dir = user_dir
		self.user_dir_tupelo = os.path.join(user_dir, '.tupelo')
		self.user_info_path = os.path.join(user_dir, '.tupelo', 'User_Info.json')

		# Multi-Thread Initiate
		self.thread_pool = QThreadPool()
		self.notebooks = []
		self.__threads = []

		# Start the GUI
		self.initUI()

		# Update Current file_logs
		self.file_dict = {}
		for notebook_info in self.notebooks:
			self.file_dict.update(_file_dict(notebook_info['dst_folder']))
		if self.view_settings['DefaultIndex'] is not None and os.path.exists(self.view_settings['DefaultIndex'].replace('file:///','')):
			self.add_browser(self.view_settings['DefaultIndex'])

		self.show()

	def initUI(self):
		self.set_basics()
		self.move_center()
		self.set_style(self.tupelo_dir)
		self.import_settings(self.user_dir_tupelo)
		self.set_notebook_links()

	# This part takes care of notebook setups when startup 
	def set_notebook_links(self):
		"""this part is to design to auto add the menu when startup. 
		1. update the notebook list
		2. add the notebook actions
		3. delete dst folder if
				- src folder deleted
				- src folder entry deleted
		"""
		try:
			notebooks_list_new = []
			with open(self.user_info_path, 'r') as user_info:
				self.notebooks = json.load(user_info)
			for notebook_info in self.notebooks:
				if os.path.isdir(notebook_info['src_folder']): # check if dir still exsit
					notebooks_list_new.append(notebook_info)
					action = self.note_menu.addAction(notebook_info['nickname'])
					action.triggered.connect(partial(self.add_browser, notebook_info['index_url']))  #Load the broswer
					self.notebook_update_thread(notebook_info)
				elif os.path.isdir(notebook_info['dst_folder']):
					print('{} is deleted, deleted folder {}'.format(notebook_info['src_folder'], notebook_info['nickname']))
					shutil.rmtree(notebook_info['dst_folder'])
			
			with open(self.user_info_path, 'w+') as user_info:
				json.dump(notebooks_list_new, user_info)

			self.notebooks = notebooks_list_new  #clean up the notebook list
		except:
			self.notebooks = []

		# if source entry deleted, deleted dst folder
		dst_list = os.listdir(self.user_dir_tupelo)
		dst_list_user = notebook_info_grab(self.notebooks)[1]
		for tupelo_dst in dst_list:
			folder = os.path.join(self.user_dir_tupelo, tupelo_dst)
			if os.path.isdir(folder) and tupelo_dst not in dst_list_user:
				shutil.rmtree(folder)

		print('Tupelo Statup Completed, start live update thread')
		self.start_liveedit_threads(self.notebooks)

	def notebook_update_thread(self, notebook_info):
		# Thread for updating notebooks
		notebook_update = TupeloThread(tupelo_update, notebook_info['filetypes'], notebook_info['src_folder'], notebook_info['dst_folder'], self.tupelo_dir)
		notebook_update.signals.finished.connect(self.thread_complete)
		self.thread_pool.start(notebook_update)

	#################
	############ Notebook Settings

	def tupelo_settings(self):
		try:
			self.background_image.close()
			try:
				self.browser.close()
			except:
				pass
			self.user_info.close()
		except:
			print('Already closed')

		for action in self.browser_action_lst:
			action.setDisabled(True)

		self.NB_settings = NBSettings(self.user_dir_tupelo, parent = self)
		self.NB_settings.setGeometry(25, 100, 1050, 500) # set for the resize (1100 - 1000/2, 750 - 500/125)
		self.NB_settings.show()
		self.NB_settings.change_sig.connect(self.tupelo_settings_restart)
		self.NB_settings.discard_sig.connect(self.tupelo_settings_discard)

	def tupelo_settings_restart(self):
		print("requires restart")
		self.close()

	def tupelo_settings_discard(self):
		print("change not applied")
		self.background_image.show()

	###################### 
	############# Notebook Setup

	@pyqtSlot()
	def new_nb_setup(self):

		for action in [self.backAct, self.editAct, self.homeAct, self.view_menu]:
			action.setDisabled(True)
		try:
			self.background_image.close()
			try:
				self.browser.close()
			except:
				pass
			self.NB_settings.close()
		except:
			pass

		self.user_info = NewNotebook(self.notebooks, self.user_dir, self.tupelo_dir, parent = self)
		self.user_info.setGeometry(350, 250, 400, 170) # set for the resize (1100 - 350 /2, 750 - 150 /2)
		self.user_info.show()

		self.user_info.setup_sig.connect(self.notebook_gen_thread) # collect the signal from NotebookInfo, which is a notebook dictionary

	######################### 
	########## Method for adding new notebook
	def notebook_gen(self, notebook_info): 
		
		tupelo_update(notebook_info['filetypes'], notebook_info['src_folder'], notebook_info['dst_folder'], self.tupelo_dir)
		# update the live edit thread
		print('Adding {} to live edit thread'.format(notebook_info['src_folder']))
		self.start_liveedit_threads([notebook_info])

	def notebook_gen_complete(self, notebook_info):

		print('notebook setup finished')

		self.add_browser(notebook_info['index_url'])
		action = self.note_menu.addAction(notebook_info['nickname'])
		action.triggered.connect(partial(self.add_browser, notebook_info['index_url']))
		
		self.notebooks.append(notebook_info)

		with open(self.user_info_path, 'w+') as user_info:
			json.dump(self.notebooks, user_info)
		self.file_dict.update(_file_dict(notebook_info['dst_folder']))

	# This thread response to two different event:
	# 1. notebook update upon startup
	# 2. notebook update when new notebook added

	@pyqtSlot(dict)
	def notebook_gen_thread(self, notebook_info):

		notebook_gen = TupeloThread(self.notebook_gen, notebook_info)
		notebook_gen.signals.finished.connect(partial(self.notebook_gen_complete, notebook_info))
		self.thread_pool.start(notebook_gen)

	def thread_complete(self):
		print("notebook updated")
	
	############################# Live Update Thread
	def start_liveedit_threads(self, notebooks_list):

		for notebook in notebooks_list:
			LiveEditEvent = LiveEdit(notebook, self.tupelo_dir)
			thread = QThread()
			# thread.setObjectName('watch folder' + notebook['src_folder'])
			self.__threads.append((thread, LiveEditEvent))
			LiveEditEvent.moveToThread(thread)

			LiveEditEvent.sig_done.connect(self.liveedit_finish)
			LiveEditEvent.sig_change_event.connect(self.liveedit_on_change)
			LiveEditEvent.sig_move_event.connect(self.liveedit_on_move)

			self.thread_abort.connect(LiveEditEvent.abort)
			thread.started.connect(LiveEditEvent.run)
			thread.start()

	@pyqtSlot(list)
	def liveedit_on_change(self, doc_info):
		cur_url = self.browser.url().toString()
		try: # Need to change index to a dictionary for clearity
			self.file_dict[doc_info[2]] = doc_info[1]
			if cur_url == doc_info[2]:
				self.browser.reload()
			elif cur_url == doc_info[0]:
				self.browser.reload()
		except:
			print('File changed {}'.format(doc_info[1]))

	@pyqtSlot(list)
	def liveedit_on_move(self, doc_move_info):
		cur_url =self.browser.url().toString()
		try:
			self.file_dict[doc_move_info[4]] = doc_move_info[2]
			if cur_url == doc_move_info[3]: # if it matches the old file, load the new file
				self.browser.load(QUrl(doc_move_info[4]))
			elif cur_url == doc_move_info[0]:
				self.browser.reload()
		except:
			print('File moved from {} to {}'.format(doc_move_info[1], doc_move_info[2]))

	@pyqtSlot(str)
	def liveedit_finish(self, message):
		print('Live Edit Existed')

	def liveedit_abort(self):
		self.thread_abort.emit()
		print('Sending signal: turning off all live folder watch')
		for thread, EditEvent in self.__threads:  # note nice unpacking by Python, avoids indexing
			thread.quit()  # this will quit **as soon as thread event loop unblocks**
			thread.wait()  # <- so you need to wait for it to *actually* quit
			self.__threads = [] 

		print('All threads exited')

