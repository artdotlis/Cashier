# -*- coding: utf-8 -*-
"""Library version."""
from typing import Final

_VERSION: Final[str] = "0.2.0-alpha"


def get_version() -> str:
    """To return the global version constant.

    Returns:
        Global software version.
    """
    return _VERSION
