# Howto use Sphinx

### Step 1: Install Sphinx

Create virtual environment in project folder:

```shell
cd path-to-your-project
python3 -m venv .venv
source .venv/bin/activate
```

Install and check Sphinx:

```shell
pip install sphinx
sphinx-build --version
```

### Step 2: Create Sphinx documentation structure

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
├── Makefile
├── build
├── make.bat
└── source
    ├── _static
    ├── _templates
    ├── conf.py
    └── index.rst
```

Generate HTML doccumentation:

```shell
make html

# Alternatively, if you're using Windows, use the command:
make.bat html

tree .
```

Open `build/html/index.html` file and see initial (empty) documentation page in web browser.

> **Note:** If you have LaTeX installed on your computer, you can generate documentation using the command: `make latexpdf` and find the pdf file in `build/latex/` folder.

### Step 3: Update the theme

The default Sphinx theme is the **Alabaster**. If you want to change it, see the list of themes on [Sphinx Themes Gallery](https://sphinx-themes.org/), select your favorite one(s), such as **Read the Docs**, **Furo**, etc. and download them to your computer.

```
pip install sphinx-rtd-theme
pip install furo
```

Change the default `alabaster` theme by `sphinx_rtd_theme` or `furo` in `source/conf.py` file

```shell
vim source/conf.py

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

Create a new file in `source` folder:

```shell
vim source/installation.rst

Installation
============

1. Clone Repository

.. code-block:: console

    $ git clone https://github.com/tomas-fryza/esp-micropython.git

2. Install Thonny IDE

3. Run the examples from `examples` or `solution` folder.
```

Update the `source/index.rst` and add the new documentation page at the end of the file:

```shell
vim source/index.rst

.. MicroPython Examples documentation master file, created by
   sphinx-quickstart on Sun Nov 10 14:04:56 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

MicroPython Examples documentation
==================================

Welcome to our MicroPython Documentation portal.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation
```

Regenerate the documentation and see reload the `index.html` page in web browser.

```shell
make html
```




Step 6: Add the Python module
=============================

TBD



Step 7: Commit your documentation
=================================

TBD



### Tested on

macOS



References
==========

- https://www.sphinx-doc.org/en/master/usage/installation.html

- https://www.youtube.com/watch?app=desktop&v=BWIrhgCAae0&ab_channel=LearnProgrammingwithJoel

- https://www.youtube.com/watch?v=pB6nNb-o1AQ&ab_channel=MiddlewareTechnologies
