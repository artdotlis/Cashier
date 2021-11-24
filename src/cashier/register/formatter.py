# -*- coding: utf-8 -*-
import re
from re import Pattern
from decimal import Decimal
from collections.abc import Callable
from typing import final, Final

from src.cashier.register.container import PurchasedItem


@final
class OutFormatter:

    def __init__(self, total: str, sales_taxes: str, imported: str, /) -> None:
        super().__init__()
        self.__total_pre: str = total
        self.__sales_taxes_pre: str = sales_taxes
        self.__imported: str = imported

    def out_sales_taxes(self, sales_taxes: Decimal, /) -> str:
        return f"{self.__sales_taxes_pre}: {sales_taxes}"

    def out_total(self, total: Decimal, /) -> str:
        return f"{self.__total_pre}: {total}"

    def out_list_item(self, p_item: PurchasedItem, tax_v: Decimal, /) -> str:
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

    def __init__(
            self, term_str: str, buy_str: str,
            taxed_f: Callable[[str], bool], /
    ) -> None:
        super().__init__()
        self.__term_str: str = term_str
        self.__buy_str: str = buy_str
        self.__taxed_f: Callable[[str], bool] = taxed_f

    def is_not_term(self, in_str: str, /) -> bool:
        return in_str.strip() != self.__term_str

    def is_not_bought(self, in_str: str, /) -> bool:
        return in_str.strip() != self.__buy_str

    def analyse_input(self, in_str: str, /) -> tuple[bool, None | PurchasedItem]:
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
