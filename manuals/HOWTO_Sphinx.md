# Howto use Sphinx

[Sphinx](https://www.sphinx-doc.org/en/master/index.html) is an open-source documentation generator primarily used for creating technical documentation for Python projects. It takes [reStructuredText](https://sphinx-tutorial.readthedocs.io/step-1/) (reST) files, processes them, and generates various output formats, including HTML, PDF, LaTeX, ePub, and more.

### Step 1: Install Sphinx

1. Create virtual environment in project folder:

   ```shell
   cd path-to-your-project
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. Install and check Sphinx:

   ```shell
   pip install sphinx
   sphinx-build --version
   ```

### Step 2: Create Sphinx documentation structure

1. Set up the basic structure of the documentation project:

   ```shell
   mkdir docs
   cd docs
   sphinx-quickstart
   # Set separate `source` and `build` directories and basic project parameters, like name, author(s), etc.
   ```

   See the documentation structure:

   ```shell
   tree .
   # On macOS, you need to install `brew install tree` first.

   .
   ├── Makefile        # Building the documentation on Unix-like systems (Linux, macOS)
   ├── build           # Output folder for built dodumentation
   ├── make.bat        # Building the docs on Windows systems
   └── source
       ├── _static     # Images, CSS files, or JavaScript files
       ├── _templates  # Custom templates
       ├── conf.py     # Configuration file for Sphinx settings
       └── index.rst   # Root document, serves as the home page
   ```

2. Generate HTML doccumentation:

   ```shell
   make html

   # Alternatively, if you're using Windows, use the command:
   make.bat html
   ```

   Open `build/html/index.html` file and see initial (empty) documentation page in web browser.

   > **Note:** If you have LaTeX installed on your computer, you can generate documentation using the command: `make latexpdf` and find the pdf file in `build/latex/` folder.

### Step 3: Update the theme

The default Sphinx theme is the **Alabaster**. If you want to change it, see the list of themes on [Sphinx Themes Gallery](https://sphinx-themes.org/), select your favorite one(s), such as **Read the Docs**, **Furo**, etc.

1. Download your favorite theme(s):

   ```shell
   pip install sphinx-rtd-theme
   pip install furo
   ```

2. Change the default `alabaster` theme by `sphinx_rtd_theme` or `furo` in `source/conf.py` file

   ```shell
   ...
   # html_theme = 'alabaster'
   html_theme = 'sphinx_rtd_theme'
   # html_theme = 'furo'
   ...
   ```

   and regenerate the documentation

   ```shell
   make html
   ```

### Step 4: Create a new documentation file

In the Sphinx documentation system, **reStructuredText** (lightweight markup language, often abbreviated as reST or `.rst`) files are plain text files used to write the content of your documentation. Each `.rst` file can represent a section or page of your documentation.

1. Create a new `installation.rst` file in `source` folder and write its content, such as:

   ```rst
   Installation
   ============

   To get started with MicroPython, follow these steps to install and run it on your hardware.

   1. Install the `MicroPython <https://micropython.org/>`_ firmware on your board.

   2. Install the `Thonny IDE <https://thonny.org/>`_.

   3. Clone the course repository

      .. code-block:: console

          $ git clone https://github.com/tomas-fryza/esp-micropython.git

   4. Run scripts from the :file:`examples` folder.
   ```

2. Update the main `source/index.rst` file and add the new documentation page:

   ```rst
   .. MicroPython Examples documentation master file, created by
      sphinx-quickstart on Sun Nov 10 14:04:56 2024.
      You can adapt this file completely to your liking, but it should at least
      contain the root `toctree` directive.

   Welcome to MicroPython course's documentation!
   ==============================================

   General documentation
   ---------------------

   .. toctree::
      :maxdepth: 2

      installation
   ```

3. Regenerate the documentation and reload the `index.html` page in web browser.

   ```shell
   make html
   ```

### Step 5: Add the Python module

Sphinx includes ways to automatically create the object definitions for your own code.

1. First, add the path to your Python modules and enable `autodoc` extension in Sphinx configuration file `sources/conf.py`

   ```python
   import sys
   import os
   sys.path.insert(0, os.path.abspath('../../modules'))
   # Here, the source files are located in `modules` folder:
   # .
   # ├── docs
   # │   ├── Makefile
   # │   ├── build
   # │   ├── make.bat
   # │   └── source
   # │       ├── conf.py
   # │       ├── index.rst
   # │       └── installation.rst
   # └── modules
   #     └── wifi_module.py

   extensions = [
       'sphinx.ext.autodoc',  # Core library for html generation from docstrings
       ]
   ```

2. Create a new documentation page `wifi.rst` in `source` folder:

   ```rst
   Wi-Fi
   =====

   .. automodule:: wifi_module
      :members:
      :undoc-members:
      :show-inheritance:
   ```

   The `automodule` directive tells Sphinx to automatically extract documentation from the `wifi_module` Python file.
      * `:members:` includs all members (classes, functions, methods, etc.)
      * `:undoc-members:` tells Sphinx to include also members that do not have docstrings
      * `:show-inheritance:` option is used to show the class inheritance hierarchy in the generated documentation

3. And finally, add the new documentation file to home page in `index.rst`

   ```rst
   ...
   General documentation
   ---------------------

   .. toctree::
      :maxdepth: 2

      installation

   Modules
   -------

   .. toctree::
      :maxdepth: 1

      wifi
   ```

4. Regenerate the documentation and reload the `index.html` page in web browser.

   ```shell
   make html
   ```

### Step 7: Deploying Sphinx documentation to GitHub Pages

See [this exercise], how to use GitHub action to rebuild the documentation on `git push` command.

### Tested on

| **Version**                | **Result (yyyy-mm-dd)** | **Note**
| :------------------------- | :---------------------: | :-------
| macOS Sonoma 14.6.1        | OK (2024-11-11)         | MacBook

## References

1. [Installing Sphinx](https://www.sphinx-doc.org/en/master/usage/installation.html)

2. Sphinx. [Getting started](https://www.sphinx-doc.org/en/master/usage/quickstart.html)

3. youtube. [Sphinx - How to generate documentation from python doc strings](https://www.youtube.com/watch?app=desktop&v=BWIrhgCAae0&ab_channel=LearnProgrammingwithJoel)

4. CodeRefinery. [Deploying Sphinx documentation to GitHub Pages](https://coderefinery.github.io/documentation/gh_workflow/)