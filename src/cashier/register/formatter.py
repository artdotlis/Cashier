# -*- coding: utf-8 -*-
"""Module providing input and output formatters."""
import re
from re import Pattern
from decimal import Decimal
from collections.abc import Callable
from typing import final, Final

from src.cashier.register.container import PurchasedItem


@final
class OutFormatter:
    """
    Formats the output of a purchase.

    Notes
    -----
        ``OutFormatter`` is a ``@final`` class and thus should not be used as a superclass.
    """
    def __init__(self, total: str, sales_taxes: str, imported: str, /) -> None:
        """
        Parameters
        ----------
        total : `str`
            The prefix for the total price of an item.
        sales_taxes : `str`
            The prefix for the sales taxes output.
        imported : `str`
            The string used as the imported description of an items.
        """
        super().__init__()
        self.__total_pre: str = total
        self.__sales_taxes_pre: str = sales_taxes
        self.__imported: str = imported

    def out_sales_taxes(self, sales_taxes: Decimal, /) -> str:
        """
        Creates a string for the sales taxes.

        Parameters
        ----------
        sales_taxes : `decimal.Decimal`
            The value for sales taxes of all purchased item.

        Returns
        -------
        `str`
            Formatted output string for the sales taxes.
        """
        return f"{self.__sales_taxes_pre}: {sales_taxes}"

    def out_total(self, total: Decimal, /) -> str:
        """
        Creates a string for the total price of an purchased item.

        Parameters
        ----------
        total : `decimal.Decimal`
            The sum of all prices of the purchased items and their sales taxes.

        Returns
        -------
        `str`
            Formatted output string for the total price of the purchase.
        """
        return f"{self.__total_pre}: {total}"

    def out_list_item(self, p_item: PurchasedItem, tax_v: Decimal, /) -> str:
        """
        Formats a purchased item.

        Parameters
        ----------
        p_item : `src.cashier.register.container.PurchasedItem`
            The purchased item.
        tax_v : `decimal.Decimal`
            The value for the sales taxes of the purchased item.

        Returns
        -------
        `str`
            Formatted output string for the purchased item.
        """
        return f"{p_item.cnt}{' ' + self.__imported if p_item.imported else ''} " \
               + f"{p_item.name}: {p_item.price + tax_v}"

    def __str__(self) -> str:
        return "---\nOUTPUT format:\n" + \
               f"\t[item cnt] ({self.__imported}) [item name]: [price with taxes]\n" + \
               f"\t{self.__sales_taxes_pre}: [value]\n" + \
               f"\t{self.__total_pre}: [value]\n---"


# default input pattern: check InFormatter.__str__()
_DI_ITEM: Final[Pattern[str]] = re.compile(r"^(\d+)\s+(.+)\s+at\s+(\d+)(\.\d+)?$")
_DI_IMPORTED: Final[Pattern[str]] = re.compile(r"^(?:.*?\s)?imported(?:\s.*)?$")


@final
class InFormatter:
    """
    Formats the input of a possible purchase.

    Notes
    -----
        ``InFormatter`` is a ``@final`` class and thus should not be used as a superclass.
    """
    def __init__(
            self, term_str: str, buy_str: str,
            taxed_f: Callable[[str], bool], /
    ) -> None:
        """
        Parameters
        ----------
        term_str : `str`
            The input string which terminates all ongoing purchases.
        buy_str : `str`
            The input string which terminates the current ongoing purchase.
        taxed_f : `collections.abc.Callable` [[ `str` ], `bool` ]
            The function which decides whether the basic taxes apply to a given item.
        """
        super().__init__()
        self.__term_str: str = term_str
        self.__buy_str: str = buy_str
        self.__taxed_f: Callable[[str], bool] = taxed_f

    def is_not_term(self, in_str: str, /) -> bool:
        """
        Determines based on input whether all purchases should be concluded.

        This function returns False if all the purchases should be concluded
        otherwise it returns True.

        Parameters
        ----------
        in_str : `str`
            The input string to be analyzed.

        Returns
        -------
        `bool`
            Whether to continue all purchases.
        """
        return in_str.strip() != self.__term_str

    def is_not_bought(self, in_str: str, /) -> bool:
        """
        Determines based on input whether to stop the current purchase.

        This function returns False  if the current purchase should be concluded
        otherwise it returns True.

        Parameters
        ----------
        in_str : `str`
            The input string to be analyzed.

        Returns
        -------
        `bool`
            Whether to continue the current purchase.
        """
        return in_str.strip() != self.__buy_str

    def analyse_input(self, in_str: str, /) -> tuple[bool, None | PurchasedItem]:
        """
        Analyses an input string.

        This function first checks whether the input string has a valid format,
        If successful, it creates a ``PurchasedItem`` object based on the input.

        Parameters
        ----------
        in_str : `str`
            The input string to be analyzed.

        Returns
        -------
        `tuple` [ `bool`, `None` | `src.cashier.register.container.PurchasedItem` ]
            A tuple containing two elements.
            The first value describes whether the input string is valid.
            The second value contains either None or ``PurchasedItem``.

        """
        match_res = _DI_ITEM.match(in_str.strip())
        if match_res is None or not match_res.group(2).strip():
            return False, None
        item_name: str = match_res.group(2)
        imported_match = _DI_IMPORTED.match(item_name)
        if imported_match is not None:
            item_name = item_name.replace("imported", "").replace("  ", " ")
        item_name = item_name.strip()
        return True, PurchasedItem(
            imported=imported_match is not None,
            name=item_name,
            price=Decimal(
                f"{match_res.group(3)}{'' if match_res.group(4) is None else match_res.group(4)}"
            ),
            cnt=int(match_res.group(1)),
            taxed=self.__taxed_f(item_name)
        )

    def __str__(self) -> str:
        return "---\nINPUT format:\n" + \
               f"\tpattern: {_DI_ITEM.pattern}\n" + \
               "\tsimple input: [item cnt] (imported) [item name] at [price]\n" + \
               f"\tfinish all purchases: {self.__term_str}\n" + \
               f"\tstart next purchase: {self.__buy_str}\n---"
