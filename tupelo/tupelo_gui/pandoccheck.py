#!/usr/bin/python3

import sys
from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QHBoxLayout, QApplication, QDesktopWidget
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtCore import QUrl


class PandocCheck(QWidget):
	"""This class checks if pandoc is installed, if not, a prompt would show up
	"""

	style = """
	QLabel{
		font: 17px;
		font-family: Verdana;
		color:orange;
	}
	QWidget
	{
    	background-color: #302F2F;
	}
	QPushButton
	{
    	color: silver;
    	background-color: #302F2F;
    	border-width: 2px;
    	border-color: #4A4949;
    	border-style: solid;
    	padding: 2px 10px 2px 10px;
    	font: 17px;
    	font-family: Verdana;
	}
	QPushButton:hover {
    	border: 2px solid #78879b;
    	color: silver;
	}
	QPushButton:pressed
	{
    	background-color: #3b9633;
	}
	"""

	def __init__(self):
		super().__init__()

		self.setStyleSheet(self.style)
		self.initUI()
		
	def initUI(self):


		install_label = QLabel("Please install Pandoc first:\n\n(Restart Tupelo after Installation)")
		install_link = QPushButton("Pandoc Installation Instruction")

		hbox = QHBoxLayout()
		hbox.addStretch(1) # add empty space
		hbox.addWidget(install_label)
		hbox.addWidget(install_link)
		hbox.addStretch(1)
		
		self.setLayout(hbox)    
		
		self.resize(500, 200)
		self.move_center()
		self.setWindowTitle('Tupelo - Pandoc Installation Required')
		install_link.clicked.connect(self.pandoc_link)  
		self.show()
	
	def move_center(self): # show window in the middle

		qtRectangle = self.frameGeometry()
		centerPoint = QDesktopWidget().availableGeometry().center()
		qtRectangle.moveCenter(centerPoint)
		self.move(qtRectangle.topLeft())

	def pandoc_link(self):
		QDesktopServices.openUrl(QUrl('https://pandoc.org/installing.html'))
		self.close()

def pandoc_install():
	app = QApplication(sys.argv)
	ex = PandocCheck()
	sys.exit(app.exec_())
	
