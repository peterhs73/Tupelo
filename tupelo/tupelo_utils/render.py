#!/usr/bin/env python3
 
import os
import time
import subprocess

from jinja2 import Environment, FileSystemLoader, DictLoader
from tupelo_utils.shortcodes import _titlize, _href_link_path

# This is necessary for the rendering environment

def render_template(tupelo_dir, template_filename, context):
	template_env = Environment(
		loader=FileSystemLoader(os.path.join(tupelo_dir, 'templates')),
	)
	return template_env.get_template(template_filename).render(context)

def index_page(tupelo_dir, index_dict, dst_folder):
	"""
	Render the index html use the index_temp.html from tupelo dir to the dst_folder.
	Make sure the main doc are displayed first 
	"""
	dst_name_main = '{} Main Docs'.format(_titlize(os.path.basename(dst_folder)))
	index_key_list = []
	for keys in index_dict.keys():
		index_key_list.append(keys)
	
	if dst_name_main in index_key_list:
		index = index_key_list
		index.remove(dst_name_main)
		index_key_list = [dst_name_main]
		index_key_list.extend(index)

	template_info = {
		'tupelo_dir': _href_link_path(tupelo_dir), 
		'index_key': index_key_list, 
		'index_info': index_dict,
		'dst_folder': _href_link_path(dst_folder),
		'baseurl':'index.html'
		}

	with open(os.path.join(dst_folder,'index.html'),'w') as index_page:
		index_page.write(render_template(tupelo_dir, 'index_temp.html', template_info))

def pandoc_temp(tupelo_dir, index_dict, dst_folder, src_folder):

	"""
	Render the pandoc html use pandoc_temp.html from tupelo dir to dst_folder/.tupelo
	"""

	template_info = {
		'tupelo_dir': _href_link_path(tupelo_dir),
		'src_folder': _href_link_path(src_folder),
		'index_info': index_dict, 
		'dst_folder': _href_link_path(dst_folder),
		'baseurl':'index.html'
		}

	with open(os.path.join(dst_folder, '.tupelo', 'pandoc.html'),'w') as pandoc_temp:
		pandoc_temp.write(render_template(tupelo_dir, 'pandoc_temp.html', template_info))

def pandoc_render(src_folder, dst_folder, doc_update):
	"""
	Function that takes care of the pandoc render. Added the meta information for javascript img/link path modification
	"""
	pan_args = [
		'pandoc',
		'--standalone',
		'--template={}'.format(os.path.join(_href_link_path(dst_folder), '.tupelo/pandoc.html')),
		'--no-highlight',
		'--toc',
		'-M', 'pagetitle={}'.format(doc_update['title']),
		'-M', 'timestamp={}'.format(doc_update['time']),
		'-M', 'src_folder={}'.format(_href_link_path(src_folder)),
		'-M', 'dst_folder={}'.format(_href_link_path(dst_folder)),
		'-o', '{}'.format(doc_update['doc_dst']),
		'{}'.format(doc_update['doc_src'])
	]

	try:
		## security check
		if ';' in (doc_update['doc_src'], doc_update['doc_dst']):
			subprocess.run(pan_args)
			print('semi-colon in filename, please change that')
		else:
			subprocess.run(pan_args, shell = True)
	except:
		print('Cannot convert file, skip')

from tupelo_utils.jupyter_temp import JUPYTER_FULL
from nbconvert import HTMLExporter
import nbformat

def ipython_render(tupelo_dir, index_dict, dst_folder, doc_update):
	"""
	A very rough and temperarary solution to the weird ipython nbconvert API
	NOT PRETTY
	"""
	## make it to forward slash
	tupelo_dir_f = _href_link_path(tupelo_dir)
	dst_folder_f = _href_link_path(dst_folder)

	nav_links = []	
	for category in index_dict.keys():
		nav_links.append(JUPYTER_FULL['navlinks'].format(category = category))
	template = ''.join([
				JUPYTER_FULL['header'], 
				JUPYTER_FULL['headerjs'].format(tupelo_dir = tupelo_dir_f),
				JUPYTER_FULL['bodyheader'],
				JUPYTER_FULL['bodylogo'].format(tupelo_dir = tupelo_dir_f, dst_folder = dst_folder_f),
				*nav_links,
				JUPYTER_FULL['content'],
				JUPYTER_FULL['bodyjs'].format(tupelo_dir = tupelo_dir_f),
				JUPYTER_FULL['footer']
			])

	jupyter_template = DictLoader({'full.tpl': template})

	with open(doc_update['doc_src'], 'r') as ipython_doc:
		nbdoc = nbformat.reads(ipython_doc.read(), as_version = 4)
	exportHTML = HTMLExporter(extra_loaders = [jupyter_temp])
	(body, resources) = exportHTML.from_notebook_node(nbdoc)

	with open(doc_update['doc_dst'], 'w+') as ipython_html:
		ipython_html.write(body)

		## incorrecct index