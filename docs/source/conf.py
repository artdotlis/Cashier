# -*- coding: utf-8 -*-
import sys
from pathlib import Path

from src.cashier.version import get_version


sys.path.insert(
    0, str(Path(".").absolute().parent.parent.joinpath('src'))
)


# -- Project information -------------------------------------------------------

project = 'Cashier'
copyright = '2021, Artur Lissin'
author = 'Artur Lissin'
release = 'v0.1.0'


# -- General configuration -----------------------------------------------------

extensions = [
    "numpydoc",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "sphinx.ext.ifconfig",
    "sphinx_autodoc_typehints"
]
templates_path = ['_templates']
exclude_patterns = []
source_suffix = '.rst'
pygments_style = 'sphinx'


# -- Options for numpydoc ------------------------------------------------------

numpydoc_use_plots = True
numpydoc_show_class_members = False
numpydoc_show_inherited_class_members = False
numpydoc_class_members_toctree = True
numpydoc_attributes_as_param_list = True
numpydoc_xref_param_type = True
numpydoc_xref_aliases = {
    "PurchasedItem": "src.cashier.purchase.container.PurchasedItem",
    "OutFormatter": "src.cashier.purchase.formatter.OutFormatter",
    "TaxCalculator": "src.cashier.purchase.tax_calculator.TaxCalculator",
    "Callable": "collections.abc.Callable",
    "Path": "pathlib.Path",
    "Decimal": "decimal.Decimal"
}
numpydoc_xref_ignore = {
    'optional', 'type_without_description', 'BadException', 'default'
}
numpydoc_validation_checks = {"all", "GL01", "SA04", "RT03"}
numpydoc_validation_excludeset = {}


# -- Options for intersphinx ---------------------------------------------------

intersphinx_mapping = {'python': ('https://docs.python.org/3', None)}


# -- Options for autosummary ---------------------------------------------------

autosummary_imported_members = False
autosummary_generate = True


# -- Options for autodoc -------------------------------------------------------

autoclass_content = "class"
autodoc_class_signature = "mixed"
autodoc_typehints = "signature"
autodoc_typehints_description_target = "all"
autodoc_inherit_docstrings = False


# -- Options for HTML output ---------------------------------------------------

html_theme = "pydata_sphinx_theme"
html_theme_options = {
  "icon_links": [
      {
          "name": "GitHub",
          "url": "https://github.com/arturOnRails/Cashier",
          "icon": "fab fa-github-square",
      }
  ]
}
html_title = f"Cashier {get_version()} documentation"
html_static_path = ['_static']
master_doc = "index"
html_use_modindex = True
html_copy_source = False
html_domain_indices = True
html_file_suffix = '.html'
add_module_names = False
