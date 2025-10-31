# SPDX-License-Identifier: Apache-2.0
# Copyright 2024-2025 CRS4 - Center for Advanced Studies, Research and
# Development in Sardinia
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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
    "show_toc_level": 2,
}
