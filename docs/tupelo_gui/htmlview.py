#!/usr/bin/env python3

import platform
import os

from PyQt5.QtCore import QUrl, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QDesktopServices, QIcon
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings, QWebEnginePage

from tupelo_utils.shortcodes import _doc_open

SYSTEM = platform.system()

class TupeloWebView(QWebEngineView):
	"""docstring for WebView"""
	def __init__(self, url):
		super().__init__()
		self.setPage(TupeloWebPage(url, parent = self))
		self.home_url = url
		self.loadFinished.connect(self.on_load_finished)

	def doc_edit(self, file_dict): # need to figure out a better way to pass this info
		cur_url = self.url().toString()
		try:
			print('file found, open')
			print(cur_url)
			print(file_dict)
			print('wutwww')
			print(file_dict[cur_url])
			_doc_open(SYSTEM, file_dict[cur_url]) 
		except:
			print('something went wrong, cannot edit files')		

	def go_home(self):
		self.load(QUrl(self.home_url))

	def on_load_finished(self):
		print('URL {} Loaded'.format(self.url()))

class TupeloWebPage(QWebEnginePage):

	link_clicked = pyqtSignal(str)

	def __init__(self, url, parent = None):
		super().__init__(parent)

		# Settings for the webpage
		# self.settings().setAttribute(QWebEngineSettings.LocalContentCanAccessRemoteUrls, True )
		# self.settings().setAttribute(QWebEngineSettings.PluginsEnabled, True)
		# self.settings().setAttribute(QWebEngineSettings.JavascriptEnabled, True)
		self.load(QUrl(url))

	def acceptNavigationRequest(self, url, nav_type, is_frame):
		if nav_type == 0:
			if url.toString().lower().startswith('https://') or url.toString().lower().startswith('http://') or url.toString().lower().endswith('.pdf'):
				QDesktopServices.openUrl(url)
				return False
			else:
				return True
		else:
			return True
