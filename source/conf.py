# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'dbsec-tutorials'
copyright = '%Y, koi141'
author = 'koi141'
release = '1.8.1'

html_title = 'Oracle DB Sec Tutorial'


# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinxcontrib.seqdiag',
    'sphinx_togglebutton',
    'sphinx.ext.githubpages',
    'sphinx_copybutton',
    'sphinx_design',
    'sphinxext.opengraph'
    ]

templates_path = ['_templates']
exclude_patterns = []

language = 'ja'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output


html_theme = 'sphinx_book_theme'
html_static_path = ['_static']
html_css_files = ['custom.css']
html_theme_options = {
    "collapse_navbar": True,
    "use_download_button": True,
    "repository_url": "https://github.com/koi141/dbsec-tutorials.git",
    "use_repository_button": True,
}

ogp_site_url = "https://koi141.github.io/dbsec-tutorials/"
ogp_site_name = "Oracle DB Security Tutorial"
ogp_type = "website"