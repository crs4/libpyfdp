# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import os
import sys
# sys.path.insert(0, os.path.abspath(os.path.join('..', '..')))


project = 'LibPyFDP'
copyright = ('2024, 2025, CRS4 - Center for Advanced Studies, Research and '
             'Development in Sardinia')
author = 'Massimo Gaggero'
release = '0.1.0'

master_doc = 'index'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'myst_nb',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx_copybutton',
    'sphinx_design',
    'sphinx.ext.napoleon',
]

templates_path = ['_templates']

myst_enable_extensions = [
    "colon_fence",
    "deflist",
    "dollarmath",
    "html_image",
]

# exclude_patterns = []

# autodoc_member_order = 'groupwise'
autodoc_member_order = 'bysource'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_book_theme"
html_logo = "_static/logo_text.png"
html_title = "LibPyFDP"
html_favicon = "_static/favicon.ico"

html_static_path = ['_static']

html_theme_options = {
    "collapse_navigation": True,
    "repository_url": "https://github.com/crs4/libpyfdp",
    "use_repository_button": True,
    "use_download_button": False,
    "home_page_in_toc": True,
    "announcement": (
        "LibPyFDP is currently in alpha stage"
    ),
}
