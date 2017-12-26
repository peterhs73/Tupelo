#!/usr/bin/env python3

import traceback
import sys

from PyQt5.QtCore import QObject, QRunnable, pyqtSignal, pyqtSlot

class TupeloThreadSignals(QObject):

	finished = pyqtSignal()
	error = pyqtSignal(tuple)
	result = pyqtSignal(object)

class TupeloThread(QRunnable):

	def __init__(self, func, *args, **kwargs):
		super().__init__()
		# Store constructor arguments (re-used for processing)
		self.func = func
		self.args = args
		self.kwargs = kwargs
		self.signals = TupeloThreadSignals()

	@pyqtSlot()
	def run(self):
		'''
		Initialise the runner function with passed args, kwargs.
		'''
		try:
			result = self.func(*self.args, **self.kwargs)
		except:
			traceback.print_exc()
			exctype, value = sys.exc_info()[:2]
			self.signals.error.emit((exctype, value, traceback.format_exc()))
		else:
			self.signals.result.emit(result)  # Return the result of the processing
		finally:
			self.signals.finished.emit()  # Done