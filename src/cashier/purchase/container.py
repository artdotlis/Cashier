# -*- coding: utf-8 -*-
"""A module providing global data containers."""
from dataclasses import dataclass
from decimal import Decimal
from typing import final


@final
@dataclass
class PurchasedItem:
    """A container describing the purchased item."""

    imported: bool
    """Whether the item is imported or not."""
    name: str
    """The name of the item."""
    price: Decimal
    """The price of the item."""
    cnt: int
    """The amount of the items to purchase."""
    taxed: bool
    """Describes whether the basic sales taxes should be applied."""
