# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.

import sys
import inspect
from pathlib import Path
from datetime import datetime
import pygeosolve


# -- Project information -----------------------------------------------------

project = "pygeosolve"
copyright = f"2015-{datetime.now().year}, Sean Leavey"
author = "Sean Leavey"
version = "master" if ".dev" in pygeosolve.__version__ else pygeosolve.__version__
release = pygeosolve.__version__


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named "sphinx.ext.*") or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx.ext.linkcode",
    "numpydoc",
    "jupyter_sphinx"
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "alabaster"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]


# -- Options for autosummary extension ---------------------------------------

# Boolean indicating whether to scan all found documents for autosummary directives, and
# to generate stub pages for each.
autosummary_generate = True

numpydoc_show_class_members = False


# -- Options for viewcode extension ------------------------------------------

def linkcode_resolve(domain, info):
    """Determine the URL corresponding to Python object.

    This code is stolen with thanks from `scipy`.
    """
    if domain != "py" or not info["module"]:
        return None

    def find_source(module, fullname):
        obj = sys.modules[module]

        for part in fullname.split("."):
            obj = getattr(obj, part)

        try:  # Unwrap a decorator.
            obj = obj.im_func.func_closure[0].cell_contents
        except (AttributeError, TypeError):
            pass

        # Get filename.
        sourcepath = Path(inspect.getsourcefile(obj))
        filename = sourcepath.relative_to(Path(pygeosolve.__file__).parent).as_posix()
        # Get line numbers of this object.
        source, lineno = inspect.getsourcelines(obj)

        if lineno:
            return "{}#L{:d}-L{:d}".format(
                filename,
                lineno,
                lineno + len(source) - 1,
            )

        return filename

    try:
        fileref = find_source(info["module"], info["fullname"])
    except (
        AttributeError,  # Object not found.
        OSError,  # File not found.
        TypeError,  # Source for object not found.
        ValueError,  # File not from pygeosolve.
    ):
        return None

    return f"https://github.com/SeanDS/pygeosolve/tree/{version}/pygeosolve/{fileref}"


# -- Options for theme -------------------------------------------------------

html_theme_options = {
    "github_user": "SeanDS",
    "github_repo": "pygeosolve",
    "github_banner": True,
    "fixed_sidebar": True,
}
