# -*- coding: utf-8 -*-
import decimal
from decimal import Decimal
from typing import final

from src.cashier.register.container import PurchasedItem


@final
class TaxCalculator:
    def __init__(self, import_taxes: float, normal_taxes: float, /) -> None:
        super().__init__()
        # precision for: one decimal place, two decimal places
        self.__precision: tuple[Decimal, Decimal] = (Decimal("0.0"), Decimal("0.00"))
        self.__multiplier: Decimal = Decimal("2")
        # taxes: imported, normal, none
        self.__taxes: tuple[Decimal, Decimal, Decimal] = (
            Decimal(str(import_taxes)), Decimal(str(normal_taxes)), Decimal("0")
        )

    def _calc_tax(self, price: Decimal, tax: Decimal, cnt: int, /) -> Decimal:
        # round(20 * total) / 20,  but more accurate
        decimal.getcontext().rounding = decimal.ROUND_HALF_UP
        taxes: Decimal = (
                price * tax * self.__multiplier * cnt
        ).quantize(self.__precision[0]) / self.__multiplier
        decimal.getcontext().rounding = decimal.ROUND_DOWN
        return taxes.quantize(self.__precision[1])

    def tax(self, p_item: PurchasedItem, /) -> Decimal:
        abs_price: Decimal = abs(p_item.price)
        imported_tax: Decimal = self.__taxes[0] if p_item.imported else self.__taxes[2]
        if p_item.taxed:
            return self._calc_tax(
                abs_price, self.__taxes[1] + imported_tax, p_item.cnt
            )
        if p_item.imported:
            return self._calc_tax(abs_price, imported_tax, p_item.cnt)
        return self.__taxes[2].quantize(self.__precision[1])

    def new_import_tax(self, tax: float, /) -> None:
        self.__taxes = (Decimal(str(tax)), self.__taxes[1], self.__taxes[2])

    def new_normal_tax(self, tax: float, /) -> None:
        self.__taxes = (self.__taxes[0], Decimal(str(tax)), self.__taxes[2])

    def __str__(self) -> str:
        return "---\nTAXES:\n" + \
               f"\textra import sales tax: {self.__taxes[0]}\n" + \
               f"\tbasic sales tax: {self.__taxes[1]}\n---"
