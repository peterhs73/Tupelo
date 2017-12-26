#!/usr/bin/env python3

import os
import sys
import shutil
import json
from datetime import datetime
import subprocess
import pathlib

def _sort_time(doc):
	"""
	This is for sorting the dictionaries
	"""
	return doc['time']

def _titlize(str_name):
	"""
	Function for make a string with underscore into a title. 
	"""
	return str_name.replace("_"," ").title()

def _create_folder(folder):
	"""
	Make the necessary directories, it will skip if exist
	"""
	os.makedirs(folder, exist_ok = True)

def _doc_move(src_folder, dst_folder, src_doc_src, src_doc_dst):
	"""
	This is the function that responde to the file move
	<FileMovedEvent: src_path='/Users/petersun/Desktop/Coding/Support_Letter_Peter Sun 2017.docx', 
	dest_path='/Users/petersun/Desktop/Coding/Python/Support_Letter_Peter Sun 2017.docx'>
	"""

	doc_src = os.path.splitext(os.path.relpath(src_doc_src, src_folder))[0]
	doc_dst = os.path.splitext(os.path.relpath(src_doc_dst, src_folder))[0]

	doc_src_dir, doc_src_name = os.path.split(doc_src)
	doc_dst_dir, doc_dst_name = os.path.split(doc_dst)

	if doc_dst_dir: # cannot create empty string
		_create_folder(os.path.join(doc_dst_dir))

	dst_doc_src = os.path.join(dst_folder, doc_src_dir, 'tupelo_{}.html'.format(doc_src_name))
	dst_doc_dst = os.path.join(dst_folder, doc_dst_dir, 'tupelo_{}.html'.format(doc_dst_name))
	shutil.move(dst_doc_src, dst_doc_dst)

	return 'tupelo files {} moved to {}'.format(dst_doc_src, dst_doc_dst)

def _list_comp(list_comp, list_ref):
	"""This is the function that prints out the difference of the list of dictionaries
	"""
	list_diff = []
	for item in list_comp:
		if item not in list_ref:
			list_diff.append(item)
	return list_diff

def _doc_open(system, doc_path):
	"""This is a universial document opener
	"""
	print(system)
	print(doc_path)
	if system == 'Linux':
		try:
			subprocess.run(['xdg-open', doc_path])
		except:
			print('cannot open file')
	elif system == 'Windows':
		try:
			os.startfile(doc_path)
		except:
			print('cannot open file')
	else:
		try:
			subprocess.run(['open', doc_path])
		except:
			print('cannot open file')

def _html_path(path):
	return pathlib.Path(path).as_uri() # This is function that automatically change path to html address based on system

def _filetype_cor(file_types):
	"""
	This functions changes the file types needed for glob: ['**/*.md'] to ['*.md']
	"""
	new_type = []
	for filetype in file_types:
		new_type.append(filetype.replace('**/', ''))
	return new_type

def _file_list_grab(dst_folder):
	"""
	This is to check if the file list (and pandoc.html) exist, and return the file list for update
	"""
	filelog_path = os.path.join(dst_folder, '.tupelo', 'file_log.json')
	pandoc_path = os.path.join(dst_folder, '.tupelo', 'pandoc.html')
	if os.path.exists(filelog_path) and os.path.exists(pandoc_path):
		with open(filelog_path, 'r') as filelog:
			print('this is the file_path {}'.format(filelog_path))
			filelog_list = json.load(filelog)
			print("json file log loaded")
		return (True, filelog_list)
	else:
		return (False, [])

def _item_exist(list_file, key_name, new_item): # is this needed
	for items in list_file:
		if new_item == items['key_name']:
			return True
			break
	return False

def _file_dict(dst_folder):
	files_dict = {}
	print('this happened')
	with open(os.path.join(dst_folder, '.tupelo','file_log.json'), 'r') as file_log:
		file_list = json.load(file_log)
	for file in file_list:
		files_dict[_html_path(file['doc_dst'])] = file['doc_src']
	return files_dict
