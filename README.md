# Tupelo Notebook

## Queue

### To-Do-list

#### Next
1. check if pandoc is installed
2. mathjax seems not working at all???
3. ability to change ~.md temp files ocassionally
    - If the file starts with '.', avoid render
4. add option to render ipython notebook with nbconvert and customized template
5. add the setup file
6. Fix the problem when there is toc (which also involves links) need to test if toc is empty
7. If there is a main folder, need to change it to Main folder
8. get a license, and check how it works
9. add the ability to change folder settings (a message for confirm)

#### Windows Specific

1. DPI Problem
2. PyQt crahes kernal sometimes?

#### Other
- add warning if pandoc is not installed?
- need to add ability to change file types and re-render 
- investigate why is it so slow at startup for mac
- problem of js null when there is no toc 

## Future feature to add
- modify custom css (dark and light mode)
- set default folder on startup
- add feature: show slideshow
    - use yaml to as a global setting for the slides ouput
- need a good 404 page 
- add ability to email the error file to me
- add option to render ipython notebook with nbconvert and customized template
- file_emit for users
- add the ability to print the current page
- add full screen mode for presentations
- add satatus menu

# pipeline:

## Internal

### Initiate
- Search destination structure determine if it is update or initiate
- Copy css and js folder to destination folder
- Search and grab .md, .tex, .rst files in origin folder
    - grab the last edit timestamp and store filename(loc): lastupdatetime to json
- Create Index Layer 0 html base on the first layer of folders (just one layer for now)
    - store the index layer info to json as well.
    - display all links (link is the file loc), ranked by timestamp, with sections split by first layer folder name. 
    - nav bar display links to folder names (#) and the ones outside of files.
- Create template for pandoc, correct nav links and file links. 
- Pandoc convert all search files
- Use javascript to change the image path

### Update

- Scan origin folder for updated timestamp
- Compare to the json file to determine which files to update
- Search index layer structure if needs to update the template
- Update index.html
- Pandoc convert the new files

### Live Edit

- Watchdog listening to all files in the directory
- If Created not at the index level/edited, update the file and refresh
- If created at the index level, need to change all files, not recommend?? or just not use those links at all.

It is possible to pass any Python object as a signal argument by specifying PyQt_PyObject as the type of the argument in the signature. For example:

`finished = pyqtSignal('PyQt_PyObject')`

### GUI
- Display the index file
- Use user preference to locate all index files, and displayed into a menu
    - switch folder by simply click to the files

- User: determine origin folder and storage destination 

## Changelog

### v1.0 Beta

- add last update as the meta data
- fixed syntax hightlighting with highlight.js (although loses the copy feature)
- fixed mathjax2.7 link
- now follow PEP 8 Python code style
- added jinja2 function to create index.html and pandoc_temp.html (very fast 10 - 20 ms)
- load template from anywhere, no need to copy
- create the pipline to create necessary dictionary, and index page properly ranked.
- fixed/used pypandoc for the whole process
- fiexed pyqt signal process
- added the user_info input window, now can switch from different pyqt widgets.
- added notebooks lists once loaded
- fixed the edit abilities
- links are now opened externally
- fixed the file directory change (seems to be slow when images are large)
- aded threading to the pandoc generation
- update folders on list when at startup
- corrected the new notebook functionality, avoid notebook duplications
- added live update, approximately 0.2 s for a single file.
- now able to display pdf correctly
- add the ability to edit files without guessing
- add the ability to move files and corresponde update.
- Index page uses 'Main', and other sorted by alphabet
- the windows menu bar problem is solved by updating intel graphic card chip. For dell (XPS 13 & 15) the best option is to use dell support assistance that came with the computer.


# Source Code

## Naming Grossary

- `src_`: the folder/path of all docs
- `dst_`: the folder/path to store all html and relevent files
- `doc_`: the individual files
- `file_`: the whole file system
- `tupelo_`: tupelo folder/path; app levelled scripts (tupelo_dir) or system specific code (universially applied)
- `category_`: the first level of folders that displays on the index page
- `index_`: index page related functions/names
- `_info`: the list of files 
- `notebook_`: mostly at the GUI stage, represent a complete src-dst-doc connection


```python
pandoc -s --template /home/petersun/Desktop/wut_2.html --resource-path=/home/petersun/Dropbox/Ocelot --no-highlight --toc -M update='time time time' -o rt.html /home/petersun/Dropbox/Ocelot/rt.md
```