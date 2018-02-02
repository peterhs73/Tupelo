#!/usr/bin/env python3

import time
import json
import os

from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QApplication

from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

from tupelo_utils.shortcodes import _filetype_cor, _file_list_grab, _url_path
from tupelo_utils.notebook import  tupelo_update, tupelo_move

class LiveHandleSignal(QObject):

	file_event = pyqtSignal(list)
	move_event = pyqtSignal(list)

class LiveEditHandle(PatternMatchingEventHandler):
	
	patterns = ['*.md', '*.rst']

	def __init__(self, file_types, src_folder, dst_folder, tupelo_dir):
		super().__init__()
		self.file_types = file_types
		self.src_folder = src_folder
		self.dst_folder = dst_folder
		self.file_list_old = _file_list_grab(dst_folder)[1] # reuse the function, the second value is the file list
		self.tupelo_dir = tupelo_dir
		self.signal = LiveHandleSignal()

		self.patterns = _filetype_cor(self.file_types)

	def process(self, event):
		print('{}'.format(event))
		doc_dir, doc_base = os.path.split(os.path.splitext(os.path.join(self.dst_folder, os.path.relpath(event.src_path, self.src_folder)))[0])
		if doc_base.lower() == 'readme':
			dst_url = _url_path(os.path.join(doc_dir, 'tupelo_' + os.path.basename(doc_dir) + '_README' + '.html'))
		else:
			dst_url = _url_path(os.path.join(doc_dir, 'tupelo_' + doc_base + '.html'))
		self.signal.file_event.emit([
				_url_path(os.path.join(self.dst_folder, 'index.html')),
				event.src_path, # The source of the file
				dst_url # The html dst of
			])

	def move_process(self, event):
		"""
		This serves 2 main goals:
		1. Update file logs
		2. if it is current on index page, refresh the index page
		3. if it is current on the moved page, load to the correct page
		"""
		print('{}'.format(event))
		doc_old_dir, doc_old_base = os.path.split(os.path.splitext(os.path.join(self.dst_folder, os.path.relpath(event.src_path, self.src_folder)))[0])
		doc_new_dir, doc_new_base = os.path.split(os.path.splitext(os.path.join(self.dst_folder, os.path.relpath(event.dest_path, self.src_folder)))[0])
		
		if doc_old_base.lower() == 'readme':
			dst_old_url = _url_path(os.path.join(doc_old_dir, 'tupelo_' + os.path.basename(doc_old_dir) + '_README' + '.html'))
			dst_new_url = _url_path(os.path.join(doc_new_dir, 'tupelo_' + os.path.basename(doc_new_dir) + '_README' + '.html'))
		else:
			dst_old_url	= _url_path(os.path.join(doc_old_dir, 'tupelo_' + doc_old_base + '.html'))
			dst_new_url = _url_path(os.path.join(doc_new_dir, 'tupelo_' + doc_new_base + '.html'))

		self.signal.move_event.emit([
				_url_path(os.path.join(self.dst_folder, 'index.html')),
				event.src_path, 
				event.dest_path, # needed for log update
				dst_old_url, 
				dst_new_url # needed for log update
			])

	def on_any_event(self, event):
		if event.is_directory:
			print('directory change, do nothing')
			return None

		elif event.event_type == 'created' or event.event_type == 'modified' or event.event_type == 'deleted':
			self.file_list_old = tupelo_update(self.file_types, self.src_folder, self.dst_folder, self.tupelo_dir, self.file_list_old) #update the file list
			self.process(event)

		elif event.event_type == 'moved':
			print('{}'.format(event))
			self.file_list_old = tupelo_move(self.file_types, self.src_folder, self.dst_folder, self.tupelo_dir, event.src_path, event.dest_path, self.file_list_old)
			self.move_process(event)

class LiveEdit(QObject):
	"""
	The two signal are the same, used for clearity
	"""
	sig_change_event = pyqtSignal(list)
	sig_move_event = pyqtSignal(list)
	sig_done = pyqtSignal(str)  
	sig_msg = pyqtSignal(str)  

	def __init__(self, notebook, tupelo_dir):
		super().__init__()
		self.__abort = False
		self.observer = Observer()
		self.notebook = notebook
		self.tupelo_dir = tupelo_dir

	@pyqtSlot()
	def run(self):

		event_handler = LiveEditHandle(self.notebook['filetypes'], self.notebook['src_folder'], self.notebook['dst_folder'], self.tupelo_dir)
		
		self.observer.schedule(event_handler, self.notebook['src_folder'], recursive=True)
		self.observer.start()

		print('Live Edit Started: single thread for {}'.format(self.notebook['src_folder']))
		event_handler.signal.file_event.connect(self.event_change)
		event_handler.signal.move_event.connect(self.event_move)

		try:
			while True:
				time.sleep(0.1)
				QApplication.processEvents()

		except:
			print("Exception called, terminate thread")
			self.observer.stop()

		self.observer.join()
		self.sig_done.emit('Finished and cleaned up')

	def event_change(self, doc_info):
		self.sig_change_event.emit(doc_info)

	def event_move(self, doc_move_info):
		self.sig_move_event.emit(doc_move_info)

	def abort(self):
		self.sig_msg.emit('Disable signal received, try to terminate the thread')
		self.__abort = True

