# -*- coding: utf-8 -*-
import sys
from datetime import date
from pathlib import Path


_ABS_CASH = Path(".").absolute().parent
_ABS_SRC = str(_ABS_CASH.joinpath("src"))
sys.path.insert(0, str(_ABS_CASH))
sys.path.insert(0, _ABS_SRC)


_VERSION = __import__("src.cashier.version", fromlist=["get_version"])


# -- Project information -------------------------------------------------------

project = "Cashier"
author = "Artur Lissin"
year = date.today().year
copyright = f"©{year} {author}."


# -- General configuration -----------------------------------------------------

extensions = [
    "sphinx.ext.napoleon",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "sphinx.ext.ifconfig",
    "sphinx_autodoc_typehints",
]
templates_path = ["_templates"]
exclude_patterns = []
source_suffix = ".rst"
add_module_names = False
add_function_parentheses = True


# -- Options for napoleon ------------------------------------------------------

napoleon_google_docstring = True
napoleon_numpy_docstring = False
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = False
napoleon_use_keyword = False
napoleon_preprocess_types = False
napoleon_type_aliases = {}
napoleon_attr_annotations = True


# -- Options for intersphinx ---------------------------------------------------

intersphinx_mapping = {"python": ("https://docs.python.org/3", None)}


# -- Options for autosummary ---------------------------------------------------

autosummary_imported_members = False
autosummary_generate = True


# -- Options for autodoc -------------------------------------------------------

autoclass_content = "class"
autodoc_class_signature = "mixed"
autodoc_typehints = "signature"
autodoc_typehints_description_target = "documented"
autodoc_inherit_docstrings = True


# -- Options for autodoc typehints ---------------------------------------------

set_type_checking_flag = False
typehints_fully_qualified = False
always_document_param_types = False
typehints_document_rtype = True
simplify_optional_unions = True


# -- Options for HTML output ---------------------------------------------------

html_theme = "sphinx_rtd_theme"
html_theme_options = {
    "display_version": True,
    "prev_next_buttons_location": "bottom",
    "style_external_links": False,
    # Toc options
    "collapse_navigation": True,
    "sticky_navigation": True,
    "navigation_depth": 2,
    "includehidden": True,
    "titles_only": False,
}
html_title = f"Cashier v{_VERSION.get_version()}"
html_static_path = ["_static"]
html_css_files = [
    "css/custom.css",
]
html_js_files = [
    "js/custom.js",
]
master_doc = "index"
html_use_modindex = True
html_copy_source = False
html_domain_indices = True
html_file_suffix = ".html"
