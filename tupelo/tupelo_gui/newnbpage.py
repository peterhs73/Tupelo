#!/usr/bin/env python3

import os
import json

from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QFileDialog, QPushButton, QLineEdit, QLabel, QGridLayout, QHBoxLayout

from tupelo_utils.notebook import FolderInfo, notebook_info_grab

class NewNotebook(QWidget):

	setup_sig = pyqtSignal(dict)

	style = """
	QLabel{
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
	"""

	def __init__(self, notebooks_list, user_dir, tupelo_dir, parent = None):
		super().__init__(parent)

		# self.setWindowIcon(QIcon(os.path.normcase('tupelo_gui/gui_files/tupelologo.png')))

		self.notebooks_list = notebooks_list
		self.tupelo_dir = tupelo_dir
		self.user_dir_home = os.path.join(user_dir, 'Desktop')
		self.user_dir_tupelo = os.path.join(user_dir, '.tupelo')
		# Labels
		self.src_label = QLabel('src folder', self)
		self.type_label = QLabel('file types', self)
		self.nickname_label = QLabel('nickname', self)

		self.src_box = QLineEdit(self)
		for ftype in ['.md', '.rst', '.ipynb', '.tex', '.docx']:
			setattr(self, ftype.replace('.',''), QPushButton(ftype, self) )

		filetypes_box = QHBoxLayout()
		for btn in [self.md, self.rst, self.ipynb, self.tex, self.docx]:
			btn.setCheckable(True)
			btn.setChecked(True)
			filetypes_box.addWidget(btn)

		self.nickname_box = QLineEdit(self)

		self.src_folder_btn = QPushButton(QIcon(os.path.join(self.tupelo_dir, 'images','folder.png')), "", self)
		self.src_folder_btn.clicked.connect(self.get_src_folder)

		self.confirm_btn = QPushButton("confirm")
		self.confirm_btn.clicked.connect(self.confirm)

		self.__warning = QLabel('')
		self.__warning.setStyleSheet("color:red")

		grid = QGridLayout()
		grid.setSpacing(7)

		layouts = [
			None, None,                     None,                       None,                None, 
			None, self.src_label,     		self.src_box,               self.src_folder_btn, None,
			None, self.nickname_label,     	self.nickname_box,      	None,                None,
			None, self.type_label,     		None,              			None,                None,
			None, None, 					self.confirm_btn, 	        None,                None,
			None, None,                     None,                       None,                None, 
		]

		positions = [(row, col) for row in range(6) for col in range(5)]
		for pos, widget in zip(positions, layouts):
			if widget == None:
				continue
			grid.addWidget(widget, *pos)

		grid.setColumnStretch(0, 1)
		grid.setColumnStretch(4, 1)
		grid.setRowStretch(0, 1)
		grid.setRowStretch(6, 2)

		grid.addLayout(filetypes_box,3, 2)
		grid.addWidget(self.__warning, 5,1,1,3)

		self.setLayout(grid)
		self.setStyleSheet(self.style)
		self.setWindowTitle("Notebook Setup")
		
	@pyqtSlot()
	def get_src_folder(self):
		self.src_folder = QFileDialog.getExistingDirectory(self, 'Open Source Folder', self.user_dir_home)
		self.src_box.setText(self.src_folder)

	@pyqtSlot()
	def confirm(self):
		src_folder = os.path.normcase(self.src_box.text())
		nickname = self.nickname_box.text()

		if not nickname:
			nickname = os.path.basename(src_folder)

		if not src_folder:
			self.__warning.setText('Please complete input')
		else:
			folder_info = FolderInfo(src_folder, self.user_dir_tupelo)
			src_list, dst_base_list, nickname_list, src_nickname = notebook_info_grab(self.notebooks_list)
			
			if not folder_info.isdir():
				self.__warning.setText('Folder does not exist')
			
			elif src_folder in src_list:
				nick = src_nickname[src_folder]
				self.__warning.setText('Notebook exists, see {}'.format(nick))
			
			elif nickname in nickname_list:
				self.__warning.setText('Nickname already used')
			
			else:
				if os.path.basename(src_folder) in dst_base_list :
					dst_dir, dst_base = os.path.split(folder_info.dst_folder)
					while dst_base in dst_base_list:
						dst_base += "0"
					folder_info.dst_folder = os.path.join(dst_dir, dst_base)
				self.user_info_emit(folder_info, nickname)

	def user_info_emit(self, folder_info, nickname):
		self.__warning.setStyleSheet("color:green")
		self.__warning.setText('...setting up, might take several seconds...')

		# return the objects as the results
		filetypes = []
		for btn in [self.md, self.rst, self.ipynb, self.tex, self.docx]:
			if btn.isChecked():
				filetypes.append('**/*{}'.format(btn.text()))

		# now all notebooks have the same structure
		notebook_info = {
			'src_folder': folder_info.src_folder, 
			'dst_folder': folder_info.dst_folder,
			'nickname': nickname, 
			'index_url': folder_info.index_url(),
			'filetypes': filetypes
		}

		self.setup_sig.emit(notebook_info)

