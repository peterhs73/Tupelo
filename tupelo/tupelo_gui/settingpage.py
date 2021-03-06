#!/usr/bin/env python3

# Peter Sun
# hs859@cornell.edu

import os
import json

from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QVBoxLayout, QComboBox, QFrame, QMessageBox, QApplication, QWidget, QFileDialog, QPushButton, QLineEdit, QLabel, QGridLayout, QHBoxLayout, QSizePolicy

# from tupelo_utils.notebook import FolderInfo, notebook_info_grab

class NBSettings(QWidget):

	"""
	Interface for update user settings. Includes GUI settings: Theme (not yet), scaling factor, font?
	Notebook settings, change location, nickname, folder name etc
	
	1. delete ask
	2. update ask
	3. reset to previous option
	"""
	change_sig = pyqtSignal()
	discard_sig = pyqtSignal()

	style = """
	QLabel{
		font: 16px;
		font-family: Verdana;
	}
	QTextEdit{
		font: 16px;
		font-family: Verdana;
	}
	QLineEdit{
		font: 16px;
		font-family: Verdana;
	}
	QPushButton{
		font: 16px;
		font-family: Verdana;
	}
	QComboBox
	{
		font: 16px;
	}
	"""

	def __init__(self, user_dir_tupelo, parent = None):
		super().__init__(parent)
		self.user_dir_tupelo = user_dir_tupelo
		try: # makesure always up to date
			with open(os.path.join(user_dir_tupelo, 'User_Settings.json'), 'r') as uset:
				self.user_settings = json.load(uset)
			print('settings loaded')
		except:
			# no users setting found
			self.user_settings = {
					'ScaleFactor': '1.2',
					'DefaultIndex': None,
					'Theme': 'Dark',
			}

		try:
			with open(os.path.join(user_dir_tupelo, 'User_Info.json'), 'r') as uinfo:
				self.user_info = json.load(uinfo)
		except:
			print("no notebook found")
			self.user_info = []

		self.nb_update = {} # use to track changes

		self.UIinit()
		self.setStyleSheet(self.style)
		sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
		self.setSizePolicy(sizePolicy)

	def UIinit(self):

		"""add function desgin
		"""
		# Labels
		labels = ['view', 'scaling_factor', 'theme', 'default_notebook',
				'notebooks', 'source_folder', 'nickname', 'file_types', 'actions'
		]

		for label in labels:
			setattr(self, label, QLabel(label.replace('_', ' ').title()))

		self.view.setStyleSheet('font: 20pt')
		self.notebooks.setStyleSheet('font: 20pt')

		self._view_status = QLabel('')
		self._nb_status = QLabel('')

		self.nb_default = QComboBox()
		nb_index_urls = []
		for notebook in self.user_info:
			nb_index_urls.append(notebook['index_url'])
			self.nb_default.addItem(notebook['nickname'])
		try:
			self.nb_default.setCurrentIndex(nb_index_urls.index(self.user_settings['DefaultIndex']))
		except ValueError:
			pass

		self.theme_set = QComboBox()
		self.theme_set.addItems(['Dark'])

		self.scale_f = QLineEdit(self.user_settings['ScaleFactor'])

		btns = ['update_view', 'discard', 'confirm']

		for btn in btns:
			setattr(self, btn, QPushButton(btn.replace('_',' ').title()))

		self.update_view.clicked.connect(self.view_setting_update)
		self.discard.clicked.connect(self.discard_change)
		self.confirm.clicked.connect(self.confirm_change)

		###############################################
		## View Grid
		###############################################

		self.view_grid = QGridLayout()
		view_layouts = [
			None,                  None,     		None,                  None,            None,             None,
			self.view,             None,            None,       		   None,            None,             None,           
			self.scaling_factor,   self.scale_f,    self.default_notebook, self.nb_default, self.theme,       self.theme_set,          
			]
		view_positions = [(row, col) for row in range(3) for col in range(6)]
		for pos, widget in zip(view_positions, view_layouts):
			if widget == None:
				continue
			self.view_grid.addWidget(widget, *pos)
		
		for i in range(6):
			self.view_grid.setColumnStretch(i, 1)

		empty_line = QLabel('')
		self.view_grid.addWidget(self._add_line(), 0, 0, 1, 6)
		self.view_grid.addWidget(empty_line, 3, 0, 2, 6)
		self.view_grid.addWidget(self.update_view, 4, 5, 1, 2)
		self.view_grid.addWidget(self._view_status, 4, 0, 1, 4)
		self.view_grid.addWidget(empty_line, 5, 0, 2, 7)

		###############################################
		## Notebook Grid
		###############################################
		self.nb_grid = QGridLayout()

		self.nb_grid.setColumnStretch(0, 4)
		self.nb_grid.setColumnStretch(1, 1)
		self.nb_grid.setColumnStretch(2, 3)
		self.nb_grid.setColumnStretch(3, 1)
		self.nb_grid.setColumnStretch(4, 1)

		self.nb_grid.setColumnMinimumWidth(0,200)
		self.nb_grid.setColumnMinimumWidth(1,120)
		self.nb_grid.setColumnMinimumWidth(2,120)
		self.nb_grid.setColumnMinimumWidth(3,40)
		self.nb_grid.setColumnMinimumWidth(4,40)

		nb_layouts = [
			None,                 None,            None,             None,             # Line
			self.notebooks,       None,            None,             None,           
			self.source_folder,   self.nickname,   self.file_types,  self.actions,    
		]
		for label in [self.source_folder,   self.nickname,   self.file_types,  self.actions]:
			label.setStyleSheet('font-weight: bold')

		self.row_num = 3
		nb_positions = [(row, col) for row in range(self.row_num) for col in range(4)]
		for pos, widget in zip(nb_positions, nb_layouts):
			if widget == None:
				continue
			self.nb_grid.addWidget(widget, *pos)
			

		row_num = self.row_num # need to reset if modified
		
		for nb in self.user_info:
			self.nb_layout(nb, row_num)
			self.nb_update[row_num] = {'del': False, 'update': False}
			row_num += 1

		self.nb_grid.addWidget(self._add_line(), 0, 0, 1, 5)
		self.nb_grid.addWidget(self._add_line(), row_num, 0, 1, 5)
		self.nb_grid.addWidget(empty_line, row_num + 1, 0, 2, 5)
		self.nb_grid.addWidget(self.discard, row_num + 2, 3)
		self.nb_grid.addWidget(self.confirm, row_num + 2, 4)
		self.confirm.setToolTip('This will shut down Tupelo, please restart afterwards')
		self.nb_grid.addWidget(self._nb_status, row_num + 3, 0, 1, 3)

		##############################
		## Combine Grids
		##############################
		self.grid_box = QGridLayout()

		self.grid_box.setRowStretch(0, 1)
		self.grid_box.setRowStretch(3, 2)
		self.grid_box.setColumnMinimumWidth(0,10)
		self.grid_box.setColumnMinimumWidth(2,10)

		self.grid_box.addLayout(self.view_grid, 1, 1)
		self.grid_box.addLayout(self.nb_grid, 2, 1)

		self.setLayout(self.grid_box)


	def nb_layout(self, nb_dict, row_num):

		nb_tag = os.path.basename(nb_dict['dst_folder'])
		item_list = [f'srcfolder_{nb_tag}', f'nickname_{nb_tag}']
		filetype_list = [f'md_{nb_tag}', f'rst_{nb_tag}', f'ipynb_{nb_tag}', f'tex_{nb_tag}', f'docx_{nb_tag}',]
		btn_list = [f'update_{nb_tag}', f'delete_{nb_tag}']

		setattr(self, item_list[0], QLabel(nb_dict['src_folder']))
		setattr(self, item_list[1], QLineEdit(nb_dict['nickname']))
		
		for btn in btn_list:
			setattr(self, btn, QPushButton(btn.split('_')[0]))

		for filetype in filetype_list:
			setattr(self, filetype, QPushButton('.'+ filetype.split('_')[0]))
			getattr(self, filetype).setCheckable(True)

			if '**/*.{}'.format(filetype.split('_')[0]) in nb_dict['filetypes']:
				getattr(self, filetype).setChecked(True)
		
		all_list = item_list + [''] + btn_list # add a spacing in between
		for i in [0, 1, 3, 4]:
			self.nb_grid.addWidget(getattr(self, all_list[i]), row_num, i)

		filetype_layout = QHBoxLayout()
		for ftype in filetype_list:
			filetype_layout.addWidget(getattr(self, ftype))

		self.nb_grid.addLayout(filetype_layout, row_num, 2)

		def update_fn():
			self._nb_status.clear()
			newtypes = []
			for ftype in filetype_list:
				if getattr(self, ftype).isChecked():
					newtypes.append('**/*.{}'.format(ftype.split('_')[0]))

			self.nb_update[row_num]['update'] = True
			self.nb_update[row_num]['nickname'] = getattr(self, f'nickname_{nb_tag}').text()
			self.nb_update[row_num]['filetypes'] = newtypes

			self._status(self._nb_status, 'Notebook {} Updated'.format(nb_dict['src_folder']), 'Green')

		def del_fn():
			respond = self._MessageBox('Delete Notebook',
						f"Are you sure to detele folder {nb_dict['src_folder']}")

			if respond == QMessageBox.Yes:
				for item in item_list + filetype_list + btn_list:
					getattr(self, item).setDisabled(True)
				self.nb_update[row_num]['del'] = True

		getattr(self, f'delete_{nb_tag}').clicked.connect(del_fn)
		getattr(self, f'update_{nb_tag}').clicked.connect(update_fn)

	def discard_change(self):

		respond = self._MessageBox('Discard Changes', 
				'Chnages are not save, are you sure to exit?')
		if respond == QMessageBox.Yes:
			self.discard_sig.emit()
			self.close()

	def info_update(self): # 7 is row number
		for row in range(len(self.user_info)):
			if self.nb_update[row + self.row_num]['del']:
				self.user_info.pop(row)
			elif self.nb_update[row + self.row_num]['update']:
				self.user_info[row]['nickname'] = self.nb_update[row + self.row_num]['nickname']
				self.user_info[row]['filetypes'] = self.nb_update[row + self.row_num]['filetypes']
		with open(os.path.join(self.user_dir_tupelo, 'User_Info.json'), 'w+') as uinfo:
			json.dump(self.user_info, uinfo)

	def confirm_change(self):
		respond = self._MessageBox('Saving Settings', 'Changes are only saved after UPDATE\nRESTART REQUIRED')
		if respond == QMessageBox.Yes:
			self.change_sig.emit()
			self.info_update()
		else:
			pass

	def view_setting_update(self):
		self.user_settings['ScaleFactor'] = self.scale_f.text()
		try: # if there is nothing it will print out '-1'
			self.user_settings['DefaultIndex'] = self.user_info[self.nb_default.currentIndex()]['index_url']
		except:
			self.user_settings['DefaultIndex'] = None
		self.user_settings['Theme'] = self.theme_set.currentText()
		# self.user_settings['default_notebook'] = self.nb_box.text()
		with open(os.path.join(self.user_dir_tupelo, 'User_Settings.json'), 'w+') as uset:
			json.dump(self.user_settings, uset)

		self._status(self._view_status, 'View Setting Updated', 'Green')

	######## Custom shortcodes
	def _MessageBox(self, title, msg):
		return QMessageBox.question(self, title, msg, QMessageBox.Yes | 
				QMessageBox.Cancel, QMessageBox.Cancel)

	def _add_line(self):

		sline = QFrame()
		sline.setFrameShape(QFrame.HLine)
		sline.setFrameShadow(QFrame.Plain)
		return sline

	def _status(self, label, status_text, color):

		label.setText(status_text)
		label.setStyleSheet('color:{}'.format(color))

if __name__ == "__main__":
	import sys
	app = QApplication(sys.argv)
	ex = NBSettings('C:\\Users\\peter\\.tupelo')
	ex.show()
	sys.exit(app.exec_())


