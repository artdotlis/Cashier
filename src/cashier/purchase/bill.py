# -*- coding: utf-8 -*-
"""A module saving and describing a purchase."""
from collections.abc import Iterable
from decimal import Decimal
from typing import final

from src.cashier.purchase.container import PurchasedItem
from src.cashier.purchase.formatter import OutFormatter
from src.cashier.purchase.tax_calculator import TaxCalculator


@final
class Bill:
    """A container holding all purchased item.

    Args:
        formatter: The formatter used for creating the output of the current purchase.
        tax_calc: The calculator for the sales taxes.
    """

    def __init__(self, formatter: OutFormatter, tax_calc: TaxCalculator, /) -> None:
        """To initialise the class."""
        super().__init__()
        self.__taxes: dict[int, Decimal] = {}
        self.__items: dict[int, PurchasedItem] = {}
        self.__item_id_gen: int = 0
        self.__max_id: int = 1_000_000
        self.__tax_calc: TaxCalculator = tax_calc
        self.__bill_format: OutFormatter = formatter

    def _calc_total(self) -> tuple[Decimal, Decimal]:
        """To calculate the sum of all sales taxes and item prices.

        Returns:
            Returns to sums, the sum of all sales taxes and
            the sum of all item prices including their sales taxes.
        """
        sales_taxes: Decimal = Decimal(str(sum(self.__taxes.values())))
        total: Decimal = Decimal(
            str(
                sum(
                    item_v.price * item_v.cnt + self.__taxes[item_k]
                    for item_k, item_v in self.__items.items()
                )
            )
        )
        return sales_taxes, total

    def _format_item_list(self) -> Iterable[str]:
        """To iteratively generate the output of an item.

        Yields:
            A formatted output for a purchased item.
        """
        for item_k, item_v in self.__items.items():
            yield self.__bill_format.out_list_item(item_v, self.__taxes[item_k])

    def _format_price(self) -> Iterable[str]:
        """To iteratively sum up the whole purchase.

        Yields:
            A part of the formatted output summing up the whole purchase.
            Is either the total sales taxes or the price for the whole purchase.
        """
        total_out = self._calc_total()
        yield self.__bill_format.out_sales_taxes(total_out[0])
        yield self.__bill_format.out_total(total_out[1])

    def _join_generator(self) -> Iterable[str]:
        """To iteratively generate the output for the whole purchase.

        Yields:
            A part of the formatted output for the whole purchase.
        """
        for item_i in self._format_item_list():
            yield item_i
        for price_i in self._format_price():
            yield price_i

    def finish(self) -> tuple[bool, str]:
        """To finish the current purchase.

        Returns:
            Returns a boolean and a string. The boolean
            describes whether the current purchase is empty or not and
            the string is a description of the whole purchase.
        """
        if not self.__items:
            return False, ""
        return True, "\n".join(self._join_generator())

    def add_item(self, p_item: PurchasedItem, /) -> str:
        """To add an item to the current purchase.

        Args:
            p_item: The purchased item to be add.

        Returns:
            Description for the adding action.
        """
        if self.__item_id_gen >= self.__max_id:
            return (
                f"the amount of items [{self.__item_id_gen}]"
                + f" reached max. value ({self.__max_id})"
            )
        if p_item.price <= 0:
            return "the item price can't be negative"
        self.__item_id_gen += 1
        self.__items[self.__item_id_gen] = p_item
        self.__taxes[self.__item_id_gen] = self.__tax_calc.tax(p_item)
        return f"added item (id: {self.__item_id_gen}) successfully"

    def rem_item(self, item_id: int, /) -> bool:
        """To remove an item based on its id from the current purchase.

        Args:
            item_id: The id of the item, which should be removed.

        Returns:
            Whether the item was removed or not.
        """
        item_to_rem = self.__items.get(item_id, None)
        if item_to_rem is None:
            return False
        del self.__items[item_id]
        del self.__taxes[item_id]
        return True
