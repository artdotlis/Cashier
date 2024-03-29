"""A module providing input and output formatters."""
import re
from collections.abc import Callable
from decimal import Decimal
from re import Pattern
from typing import Final, final

from cashier.purchase.container import PItemContainer, PurchasedItem


@final
class OutFormatter:
    """Formats the output of a purchase.

    Args:
        total: The prefix for the total price of an item.
        sales_taxes: The prefix for the sales taxes output.
        imported: The string used as the imported description for an item.
    """

    def __init__(self, total: str, sales_taxes: str, imported: str, /) -> None:
        """To initialise the class."""
        super().__init__()
        self.__total_pre: str = total
        self.__sales_taxes_pre: str = sales_taxes
        self.__imported: str = imported

    def out_sales_taxes(self, sales_taxes: Decimal, /) -> str:
        """To create a string for the sales taxes.

        Args:
            sales_taxes: The sales taxes value used for all purchased items.

        Returns:
            Formatted output string for the sales taxes.
        """
        return f"{self.__sales_taxes_pre}: {sales_taxes}"

    def out_total(self, total: Decimal, /) -> str:
        """To create a string for the total price of a purchased item.

        Args:
            total: The sum of all prices of the purchased items and their sales taxes.

        Returns:
            Formatted output string for the total price of the purchase.
        """
        return f"{self.__total_pre}: {total}"

    def out_list_item(self, p_elem: PItemContainer, /) -> str:
        """To format a purchased item.

        Args:
            p_elem: A container holding the purchased item.

        Returns:
            Formatted output string for the purchased item.
        """
        return (
            f"{p_elem.item.cnt}{' ' + self.__imported if p_elem.item.imported else ''} "
            + f"{p_elem.item.name}: {p_elem.item.price + p_elem.sales_taxes}"
        )

    def __str__(self) -> str:
        """To create a string representation.

        Returns:
            String representation of the ``OutFormatter`` object.
        """
        return (
            "---\nOUTPUT format:\n"
            + f"\t[item cnt] ({self.__imported}) [item name]: [price with taxes]\n"
            + f"\t{self.__sales_taxes_pre}: [value]\n"
            + f"\t{self.__total_pre}: [value]\n---"
        )


# default input pattern: check InFormatter.__str__()
_DI_ITEM: Final[Pattern[str]] = re.compile(r"^(\d+)\s+(.+)\s+at\s+(\d+)(\.\d+)?$")
_DI_IMPORTED: Final[Pattern[str]] = re.compile(r"^(?:.*?\s)?imported(?:\s.*)?$")


@final
class InFormatter:
    """Formats the input of a possible purchase.

    Args:
        term_str: The input string which terminates all ongoing purchases.
        buy_str: The input string which terminates the current ongoing purchase.
        taxed_f: Function which decides whether the basic taxes apply to a given item.
    """

    def __init__(
        self, term_str: str, buy_str: str, taxed_f: Callable[[str], bool], /
    ) -> None:
        """To initialise the class."""
        super().__init__()
        self.__term_str: str = term_str
        self.__buy_str: str = buy_str
        self.__taxed_f: Callable[[str], bool] = taxed_f

    def is_not_term(self, in_str: str, /) -> bool:
        """To determine whether all purchases should be concluded based on the input.

        This function returns False if all purchases should be concluded
        otherwise it returns True.

        Args:
            in_str: The input string which should be analyzed.

        Returns:
            Whether to continue all purchases.
        """
        return in_str.strip() != self.__term_str

    def is_not_bought(self, in_str: str, /) -> bool:
        """To determine whether to stop the current purchase based on the input.

        This function returns False  if the current purchase should be concluded
        otherwise it returns True.

        Args:
            in_str: The input string which should be analyzed.

        Returns:
            Whether to continue the current purchase.
        """
        return in_str.strip() != self.__buy_str

    def analyse_input(self, in_str: str, /) -> tuple[bool, None | PurchasedItem]:
        """To analyse an input string.

        This function first checks whether the input string has a valid format,
        If successful, it creates a ``PurchasedItem`` object based on the input.

        Args:
            in_str: The input string, which should be analysed.

        Returns:
            Returns a boolean and either the ``PurchasedItem`` element if boolean
            is ``True`` or None otherwise.
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
                f"{match_res.group(3)}"
                + f"{'' if match_res.group(4) is None else match_res.group(4)}"
            ),
            cnt=int(match_res.group(1)),
            taxed=self.__taxed_f(item_name),
        )

    def __str__(self) -> str:
        """To create a string representation.

        Returns:
            String representation of the ``InFormatter`` object.
        """
        return (
            "---\nINPUT format:\n"
            + f"\tpattern: {_DI_ITEM.pattern}\n"
            + "\tsimple input: [item cnt] (imported) [item name] at [price]\n"
            + f"\tfinish all purchases: {self.__term_str}\n"
            + f"\tstart next purchase: {self.__buy_str}\n---"
        )
