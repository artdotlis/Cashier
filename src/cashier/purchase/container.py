# -*- coding: utf-8 -*-
"""A module providing global data containers."""
from dataclasses import dataclass, field
from decimal import Decimal
from typing import final


@final
@dataclass(frozen=True, slots=True)
class PurchasedItem:
    """A container describing the purchased item."""

    imported: bool = field()
    """Whether the item is imported or not."""
    name: str = field()
    """The name of the item."""
    price: Decimal = field()
    """The price of the item."""
    cnt: int = field()
    """The amount of the items to purchase."""
    taxed: bool = field()
    """Describes whether the basic sales taxes should be applied."""


@dataclass(frozen=True, slots=True)
class PItemContainer:
    """A container for holding a purchased item and its sales taxes."""

    item: PurchasedItem
    """The purchased item."""
    id: int
    """The id of the purchased item."""
    sales_taxes: Decimal
    """The sales taxes of the purchased item."""
