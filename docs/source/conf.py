# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here.
import sys
# from pathlib import Path
# sys.path.insert(0, str(Path('../..', 'modules').resolve()))
import os
sys.path.insert(0, os.path.abspath('../../modules'))

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'MicroPython course'
copyright = '2023-2024, Tomas Fryza'
author = 'Tomas Fryza'
release = '1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.duration',
    'sphinx.ext.autodoc',  # Core library for html generation from docstrings
    # 'sphinx.ext.autosummary',
    'sphinx.ext.linkcode',  # Enable linkcode for linking to external source code
    ]


# Add details about source files from GitHub to Sphinx module documentation
import importlib
import inspect

def linkcode_resolve(domain, info):
    if domain != 'py' or not info['module']:
        return None

    # GitHub repository information
    repo_url = "https://github.com/tomas-fryza/esp-micropython"
    branch = "main"  # Set to the branch you want to link to (e.g., 'main' or 'master')
    
    # Convert module name to path format
    filename = info['module'].replace('.', '/') + ".py"
    
    # Attempt to locate the line number for the symbol
    try:
        # Import the module and retrieve the object by its full name
        module = importlib.import_module(info['module'])
        obj = module
        for part in info['fullname'].split('.'):
            obj = getattr(obj, part)
        
        # Use `inspect.getsourcelines` to get the starting line number of the object
        source, start_lineno = inspect.getsourcelines(obj)

        # Get the end line number by counting the lines in the source code of the object
        end_lineno = start_lineno + len(source) - 1

        # Generate the range of lines and create the GitHub link
        return f"{repo_url}/blob/{branch}/modules/{filename}#L{start_lineno}-L{end_lineno}"

    except (ImportError, AttributeError, TypeError):
        # Fallback: If the object can't be found, link to the module file without line number
        return f"{repo_url}/blob/{branch}/{filename}"


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
