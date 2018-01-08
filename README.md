# Tupelo Notebook ![Tupelo](images/logo.png =50x)

This notebook is designed for ppl who documents often and uses variety source of note format, i.e. markdown, latex, rst. or word documents. The tupelo is designed to create a fast and more readable index of the existing folders of documents. Currently it supports files of markdown, reStructuredText, latex (beta) and Word documents (beta). We are working hard to create a search engine along side the index ability.

## Requirements

To build the application the following packages are required:

- Main
    - [`pandoc`](https://pandoc.org/) for render all files to html for display
        - See [installation](https://pandoc.org/installing.html) page for different platforms.
    - Only supports python3

- Python packages
    - [`pypandoc`](https://pypi.python.org/pypi/pypandoc), a thin wrap of pandoc commands. (`pandoc` still required)
    - [`PyQt5.9`](http://pyqt.sourceforge.net/Docs/PyQt5/introduction.html)
    - [`watchdog`](https://pypi.python.org/pypi/watchdog), for live editing
 
## Changelog

### Beta 0.1
- Supports all platforms

## What's coming
- Search function
- Multi-user functionalities