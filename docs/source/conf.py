# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join('..', '..')))


project = 'LibPyFDP'
copyright = ('2024, 2025, CRS4 - Center for Advanced Studies, Research and '
             'Development in Sardinia')
author = 'Massimo Gaggero'
release = '0.1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.autodoc',
              'sphinx.ext.autosummary',
              'sphinx.ext.napoleon',
              'sphinx_favicon',
              'sphinx_copybutton']

templates_path = ['_templates']
exclude_patterns = []

#  autodoc_member_order = 'groupwise'
autodoc_member_order = 'bysource'


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# html_theme = 'alabaster'
# html_theme = 'sphinx_rtd_theme'
# html_theme = 'sphinx_book_theme'
# html_theme = 'cloud'
# html_theme = 'groundwork'
# html_theme = "sphinxawesome_theme"
# html_theme = "furo"
html_theme = "sphinx_book_theme"

html_static_path = ['_static']
favicons = [
    'favicon.ico',
]
