# -*- coding: utf-8 -*-
"""Module used for calculating taxes."""
import decimal
from decimal import Decimal
from typing import final

from src.cashier.register.container import PurchasedItem


@final
class TaxCalculator:
    """
    Calculates sales taxes for a purchased item.

    Notes
    -----
        ``TaxCalculator`` is a ``@final`` class and thus should not be used as a superclass.
    """
    def __init__(self, import_taxes: float, normal_taxes: float, /) -> None:
        """
        Parameters
        ----------
        import_taxes : `float`
            The sales taxes for imported items.
        normal_taxes : `float`
            The basic sales taxes.
        """
        super().__init__()
        # precision for: one decimal place, two decimal places
        self.__precision: tuple[Decimal, Decimal] = (Decimal("0.0"), Decimal("0.00"))
        self.__multiplier: Decimal = Decimal("2")
        # taxes: imported, normal, none
        self.__taxes: tuple[Decimal, Decimal, Decimal] = (
            Decimal(str(self.check_taxes(
                import_taxes, 0.05, "Import sales taxes cant be negative, setting to 0.05."
            ))),
            Decimal(str(self.check_taxes(
                normal_taxes, 0.1, "Basic sales taxes cant be negative, setting to 0.10."
            ))), Decimal("0")
        )

    @staticmethod
    def check_taxes(tax: float, default_t: float, msg: str, /) -> float:
        """
        Checks whether the given tax is negative.

        Parameters
        ----------
        tax : `float`
            The tax value is to be tested.
        default_t : `float`
            The replacement value for a negative ``tax`` value.
        msg : `str`
            The message to be printed when ``tax`` is negative.

        Returns
        -------
        `float`
            The corrected value for the sales tax.
        """
        if tax >= 0:
            return tax
        print(msg)
        return default_t

    def _calc_tax(self, price: Decimal, tax: Decimal, cnt: int, /) -> Decimal:
        """
        Calculates sales taxes.

        This method returns the sales tax for ``cnt`` items
        with the same ``price``. The sales tax value is rounder and
        formatted based on the rules defined in ``TaxCalculator``.

        Parameters
        ----------
        price : `decimal.Decimal`
            The price of the purchased item. Must be greater than zero.
        tax : `decimal.Decimal`
            The sales tax, which will be used in the tax-calculation.
        cnt : int
            The amount of the purchased item.

        Returns
        -------
        `decimal.Decimal`
            Calculated and formatted sales taxes.

        Notes
        -----
            The taxes are rounded similar to the``round(20 * total) / 20``
            approach and only print two decimal places.
        """
        decimal.getcontext().rounding = decimal.ROUND_HALF_UP
        taxes: Decimal = (
                price * tax * self.__multiplier * cnt
        ).quantize(self.__precision[0]) / self.__multiplier
        decimal.getcontext().rounding = decimal.ROUND_DOWN
        return taxes.quantize(self.__precision[1])

    def tax(self, p_item: PurchasedItem, /) -> Decimal:
        """
        Calculates sales taxes for a purchased item.

        Parameters
        ----------
        p_item: `src.cashier.register.container.PurchasedItem`
            The purchased item.

        Returns
        -------
        `decimal.Decimal`
            Calculated and formatted sales taxes for the purchased item ``p_item``.
        """
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
        """
        Sets a new value for the import sales taxes.

        Parameters
        ----------
        tax : `float`
            The new value for the import sales taxes.
        """
        self.__taxes = (Decimal(str(tax)), self.__taxes[1], self.__taxes[2])

    def new_normal_tax(self, tax: float, /) -> None:
        """
        Sets a new value for the basic sales taxes.

        Parameters
        ----------
        tax : `float`
            The new value for the basic sales taxes.
        """
        self.__taxes = (self.__taxes[0], Decimal(str(tax)), self.__taxes[2])

    def __str__(self) -> str:  # pragma: no cover
        return "---\nTAXES:\n" + \
               f"\textra import sales tax: {self.__taxes[0]}\n" + \
               f"\tbasic sales tax: {self.__taxes[1]}\n---"
