# -*- coding: utf-8 -*-
"""Library version."""
from typing import Final


_VERSION: Final[str] = "0.1.0"


def get_version() -> str:
    """
    To return the global version constant.

    Returns
    -------
    str
        Global software version.
    """
    return _VERSION
