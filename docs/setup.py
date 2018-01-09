#!/usr/bin/env python3

## cx_freeze is currently located in the docs folder due to inability to 

import sys
import os
from cx_Freeze import setup, Executable

## This is a fix for cx_freeze inability to find dependencies when burried.
PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))
os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tk8.6')

base = None

if sys.platform == "win32":
	base = "Win32GUI"

build_exe_options = {
		"packages": ["idna", "os", "sys", "platform", "json", "datetime", "time", "subprocess", "traceback", 
					"pathlib", "glob", "shutil", "functools", "PyQt5", "watchdog", "pypandoc", "jinja2", "asyncio",
					"tupelo_gui", "tupelo_utils"
					],
		"include_files": ["templates", "images", "css", "js",
						os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tk86t.dll'), os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tcl86t.dll')
						]
		}

bdist_msi_options = {
	"upgrade_code": "{000001-2309-PSJMJB}",
	"add_to_path": False
}

tupelo_target = Executable(
	script = "tupelo.py", 
	base = base,
	icon = "images/logo.ico",
	# shortcutName = "Tueplo",
	# shortcutDir = "DesktopFolder"
	)

setup(
	name = "Tupelo",
	version = "0.1",
	author = "Peter Sun",
	description = "A simple tool for indexing notes",
	options = {
		"build_exe": build_exe_options,
		"bdist_msi": bdist_msi_options
		},
	executables = [tupelo_target],
)