import os
import json
from datetime import datetime
from glob import glob
import time

import tupelo_utils.render as tupelo_render
from tupelo_utils.shortcodes import _url_path, _file_list_grab, _titlize, _sort_time, _create_folder, _list_comp, _doc_move

def notebook_info_grab(notebook_list):
	src_folder = []
	dst_folder_base = []
	nickname = []
	src_nickname = {} # why 
	for notebook in notebook_list:
		src_folder.append(notebook['src_folder'])
		dst_folder_base.append(os.path.basename(notebook['dst_folder']))
		nickname.append(notebook['nickname'])
		src_nickname[notebook['src_folder']] = notebook['nickname']

	return (src_folder, dst_folder_base, nickname, src_nickname)

class FolderInfo(object):

	def __init__(self, src_folder, document_path):
		self.src_folder = src_folder
		self.title = _titlize(os.path.basename(src_folder))

		# self.istupelo, self.file_list = _file_list_grab(self.src_folder)
		self.dst_folder = os.path.join(document_path, os.path.basename(src_folder))

	def isdir(self):
		return os.path.isdir(self.src_folder)

	def index_url(self):
		return _url_path(os.path.join(self.dst_folder, 'index.html'))

## Custom classes

class DocIndex(object):

	TIME_FORMAT = '%Y-%m-%d %H:%M:%S'

	def __init__(self, doc_path, src_folder, dst_folder, category_list):
		self.doc_src = doc_path
		self.timestamp(doc_path)
		self.inventory(doc_path, src_folder, dst_folder, category_list)

	def timestamp(self, doc_path):
		self.time = datetime.utcfromtimestamp(os.path.getmtime(doc_path)).strftime(self.TIME_FORMAT)
		return self.time

	def inventory(self, doc_path, src_folder, dst_folder, category_list): # reducency, need to fix
		doc_rel = os.path.relpath(doc_path, src_folder)
	
		doc_dir, doc_base = os.path.split(doc_rel) # seprate to path and doc
		doc_name, doc_ext = os.path.splitext(doc_base)
		if doc_name.lower() == 'readme':
			doc_name = os.path.basename(doc_dir) + "_README"
		
		doc_title = _titlize(doc_name)
		self.title = doc_title
		
		self.doc_dst = os.path.join(dst_folder, doc_dir, 'tupelo_' + doc_name + '.html') # Temperally fix, might need to look into
		
		if doc_rel.startswith(tuple(category_list)):
			for category in category_list:
				if doc_rel.startswith(category):
					self.category = _titlize(category)
		else:
			dst_name_main = '{} Main Docs'.format(_titlize(os.path.basename(dst_folder).replace('0','')))
			self.category = dst_name_main

		return (self.title, self.doc_dst, self.category)

class TupeloBase(object):

	def __init__(self, file_types, src_folder, dst_folder):
		self.category_list = []
		self.file_list = []
		self.index_dict = {}

		self.category_info(src_folder)
		self.file_info(file_types, src_folder, dst_folder, self.category_list)
		self.index_info(self.file_list)

	def category_info(self, src_folder):

		"""function that walks the srcginal file
		and creates a the list of the first level
		"""
		for category in os.listdir(src_folder):
			category_path = os.path.join(src_folder, category)
			if os.path.isdir(category_path):
				self.category_list.append(category)
		return self.category_list

	def file_info(self, file_types, src_folder, dst_folder, category_list):

		"""function that creates the list of file in dictionary format
		"""
		for file_ext in file_types:
			for doc_path in glob(os.path.join(src_folder,file_ext), recursive = True):
				self.file_list.append(vars(DocIndex(doc_path, src_folder, dst_folder, category_list)))
		with open(os.path.join(dst_folder, '.tupelo', 'file_log.json'), 'w+') as file_log:
			json.dump(self.file_list, file_log)

		return self.file_list

	def index_info(self, file_list):

		"""function that takes the file list
		sort and create a nested dictionary
		"""
		for doc in sorted(file_list, key = _sort_time, reverse = True):
			if doc['category'] not in self.index_dict:
				self.index_dict[doc['category']] = [doc]
			else:
				self.index_dict[doc['category']].append(doc)
		return self.index_dict

# Function for updating the files.

def tupelo_update(file_types, src_folder, dst_folder, tupelo_dir, file_list_old = []):

	if not file_list_old:
		istupelo, file_list_old = _file_list_grab(dst_folder)
	else:
		istupelo = True

	if not istupelo:
		print('initiating tupelo')
		_create_folder(os.path.join(dst_folder,'.tupelo'))
	else:
		print("calling the update function")

	tupelo_file = TupeloBase(file_types, src_folder, dst_folder)

	tupelo_render.index_page(tupelo_dir, tupelo_file.index_dict, dst_folder)
	tupelo_render.pandoc_temp(tupelo_dir, tupelo_file.index_dict, dst_folder, src_folder)
	# first delete all files need to update
	file_delete_list = _list_comp(file_list_old, tupelo_file.file_list)
	
	for delete_doc in file_delete_list:
		try:
			os.remove(delete_doc['doc_dst'])
		except:
			print('cannot find {}'.format(delete_doc))
			print('files might be corrupted')

	file_update_list = _list_comp(tupelo_file.file_list, file_list_old)

	for doc_update in file_update_list:
		_create_folder(os.path.dirname(doc_update['doc_dst']))
		tupelo_render.pandoc_render(src_folder, dst_folder, doc_update)

	return tupelo_file.file_list

def tupelo_move(file_types, src_folder, dst_folder, tupelo_dir, src_doc_src, src_doc_dst, file_list_old = []):

	if not file_list_old:
		istupelo, _file_list_grab(dst_folder)
	else:
		istupelo = True

	tupelo_file = TupeloBase(file_types, src_folder, dst_folder)
	_doc_move(src_folder, dst_folder, src_doc_src, src_doc_dst)
	tupelo_render.index_page(tupelo_dir, tupelo_file.index_dict, dst_folder)

	return tupelo_file.file_list


