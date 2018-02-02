#!/usr/bin/env python3

## cx_freeze is currently located in the docs folder due to inability to 

import sys
import os
from cx_Freeze import setup, Executable

# cx_freeze options

## add system to include two packages directly
sys.path.append('tupelo')
## A fix for cx_freeze inability to find dependencies when burried.

if sys.platform == "win32":
	base = "Win32GUI"
	PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))
	os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tcl8.6')
	os.environ['TK_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tk8.6')

	files = ["tupelo/templates", "tupelo/images", "tupelo/css", "tupelo/js",
			os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tk86t.dll'), os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tcl86t.dll')]

else:
	base = None
	files = ["tupelo/templates", "tupelo/images", "tupelo/css", "tupelo/js"]

## Setup Options

build_exe_options = {
		"packages": ["idna", "os", "sys", "platform", "json", "datetime", "time", "subprocess", "traceback", 
					"pathlib", "glob", "shutil", "functools", "watchdog", "jinja2", "asyncio",
					"tupelo_gui", "tupelo_utils"
					],
		"includes": ["PyQt5.QtGui", "PyQt5.QtCore", "PyQt5.QtWebEngineWidgets", "PyQt5.QtWidgets"],
		"include_files": files
		}

bdist_msi_options = {
	"upgrade_code": "{7d3855f1-1647-4415-a268-0edb37c160ff}",
	"add_to_path": True
}

tupelo_target = Executable(
	script = "tupelo/tupelo.py", 
	base = base,
	icon = "tupelo/images/logo.ico",
	shortcutName = "Tueplo-0.2.0",
	shortcutDir = "DesktopFolder"
	)

#### Now the setup

with open('README.md') as README:
    readme = README.read()

with open('LICENSE.txt') as LICENSE:
    license = LICENSE.read()

setup(
	name = "Tupelo",
	version = "0.2.0",
	license=license,
	author = "Peter Sun",
	author_email = 'hs859@cornell.edu',
	description = "A simple tool for indexing notes",
	long_description=readme,
	options = {
		"build_exe": build_exe_options,
		"bdist_msi": bdist_msi_options
		},
	executables = [tupelo_target],
)