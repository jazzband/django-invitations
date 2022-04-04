# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
from __future__ import annotations

import sys
from pathlib import Path

import tomlkit

# -- Path setup --------------------------------------------------------------

here = Path(__file__).parent.resolve()
sys.path.insert(0, str(here / ".."))

# -- Project information -----------------------------------------------------


def _get_project_meta():
    with open("../pyproject.toml") as pyproject:
        file_contents = pyproject.read()

    return tomlkit.parse(file_contents)["tool"]["poetry"]


pkg_meta = _get_project_meta()
project = str(pkg_meta["name"])
copyright = "-"
author = "-"

# The short X.Y version
version = str(pkg_meta["version"])
# The full version, including alpha/beta/rc tags
release = version

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx.ext.viewcode",
]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = [
    "_build",
    "venv",
]

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "furo"

# -- Options for LaTeX output ------------------------------------------

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title, author, documentclass
# [howto/manual]).
latex_documents = [
    (
        "index",
        "django-invitations.tex",
        "django-invitations Documentation",
        "Jazzband",
        "manual",
    ),
]

# -- Options for Intersphinx -------------------------------------------

intersphinx_mapping = {
    "django": (
        "https://docs.djangoproject.com/en/stable/",
        "https://docs.djangoproject.com/en/stable/_objects/",
    ),
}
