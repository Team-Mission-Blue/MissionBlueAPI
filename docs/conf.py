"""Sphinx configuration."""
project = "Mission Blue API"
author = "Caleb Aguirre-Leon"
copyright = "2025, Caleb Aguirre-Leon"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_click",
    "myst_parser",
]
autodoc_typehints = "description"
html_theme = "furo"
