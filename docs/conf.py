"""Sphinx configuration."""

project = "Fleaky"
author = "Benjamin Vial"
copyright = "2024, Benjamin Vial"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "myst_parser",
]
autodoc_typehints = "description"
html_theme = "furo"
