# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here.
import sys
from pathlib import Path

sys.path.insert(0, str(Path('../..', 'solutions/03-oop').resolve()))
sys.path.insert(0, str(Path('../..', 'solutions/05-display').resolve()))
sys.path.insert(0, str(Path('../..', 'solutions/06-serial').resolve()))
sys.path.insert(0, str(Path('../..', 'solutions/07-wifi').resolve()))

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'MicroPython course'
copyright = '2023-2024, Tomas Fryza'
author = 'Tomas Fryza'
release = '0.2'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.duration',
    'sphinx.ext.autodoc',  # Core library for html generation from docstrings
    'sphinx.ext.autosummary',
    ]

templates_path = ['_templates']
exclude_patterns = []

# Mock module(s) to avoid import errors in the build process
autodoc_mock_imports = [
    'machine',
    'framebuf',
    'utime',
    ]

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# html_theme = 'alabaster'
html_theme = 'sphinx_rtd_theme'
# html_theme = 'furo'
html_static_path = ['_static']
