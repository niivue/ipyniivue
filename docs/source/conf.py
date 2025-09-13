"""Configuration file for the Sphinx documentation builder."""

import os
import sys

sys.path.insert(0, os.path.abspath("../../src"))

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "IPyNiiVue"
author = "Jan-Hendrik Müller, Trevor Manz, Bradley Alford, Anthony Androulakis, "
author += "Taylor Hanayik, Christian O'Reilly"
project_copyright = "2025, " + author
release = "2.1.0"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ["sphinx.ext.autodoc", "sphinx.ext.viewcode"]

templates_path = ["_templates"]
exclude_patterns = []

# Autodoc options
autodoc_default_options = {
    "members": True,
    "undoc-members": False,
    "inherited-members": False,
    "special-members": "__init__",
    "show-inheritance": True,
}
# autodoc_member_order = "bysource"
autoclass_content = "class"

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "furo"
# html_static_path = ["_static"]
