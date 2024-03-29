"""A module used for calculating taxes."""
import decimal
from decimal import Decimal
from typing import final

from cashier.purchase.container import PurchasedItem


@final
class TaxCalculator:
    """Calculates sales taxes for a purchased item.

    Args:
        import_taxes: Sales taxes for imported items.
        normal_taxes: Basic sales taxes.
    """

    def __init__(self, import_taxes: float, normal_taxes: float, /) -> None:
        """To initialise the class."""
        super().__init__()
        # precision for: one decimal place, two decimal places
        self.__precision: tuple[Decimal, Decimal] = (Decimal("0.0"), Decimal("0.00"))
        self.__multiplier: Decimal = Decimal("2")
        # taxes: imported, normal, none
        self.__taxes: tuple[Decimal, Decimal, Decimal] = (
            Decimal(
                str(
                    self.check_taxes(
                        import_taxes,
                        0.05,
                        "Import sales taxes can't be negative, setting to 0.05.",
                    )
                )
            ),
            Decimal(
                str(
                    self.check_taxes(
                        normal_taxes,
                        0.1,
                        "Basic sales taxes can't be negative, setting to 0.10.",
                    )
                )
            ),
            Decimal("0"),
        )

    @staticmethod
    def check_taxes(tax: float, default_t: float, msg: str, /) -> float:
        """To check whether the given tax is negative.

        Args:
            tax: Tax value that should be tested.
            default_t: Replacement value for a negative ``tax`` value.
            msg: Message to be printed when ``tax`` is negative.

        Returns:
            The corrected value for the sales tax.
        """
        if tax >= 0:
            return tax
        print(msg)
        return default_t

    def _calc_tax(self, price: Decimal, tax: Decimal, cnt: int, /) -> Decimal:
        """To calculate sales taxes.

        This method returns the sales tax for ``cnt`` items
        with the same ``price``. The sales tax value is rounder and
        formatted based on the rules defined in ``TaxCalculator``.

        Args:
            price: Price of the purchased item. Must be greater than zero.
            tax: Sales tax, which will be used in the tax-calculation.
            cnt: Amount of the purchased item.

        Returns:
            Calculated and formatted sales taxes.

        Note:
            The taxes are rounded similar to the ``round(20 * total) / 20``
            approach and only print two decimal places.
        """
        decimal.getcontext().rounding = decimal.ROUND_HALF_UP
        taxes: Decimal = (price * tax * self.__multiplier * cnt).quantize(
            self.__precision[0]
        ) / self.__multiplier
        decimal.getcontext().rounding = decimal.ROUND_DOWN
        return taxes.quantize(self.__precision[1])

    def tax(self, p_item: PurchasedItem, /) -> Decimal:
        """To calculate sales taxes for a purchased item.

        Args:
            p_item: Purchased item.

        Returns:
            Calculated and formatted sales taxes for the purchased item ``p_item``.
        """
        abs_price: Decimal = abs(p_item.price)
        imported_tax: Decimal = self.__taxes[0] if p_item.imported else self.__taxes[2]
        if p_item.taxed:
            return self._calc_tax(abs_price, self.__taxes[1] + imported_tax, p_item.cnt)
        if p_item.imported:
            return self._calc_tax(abs_price, imported_tax, p_item.cnt)
        return self.__taxes[2].quantize(self.__precision[1])

    def new_import_tax(self, tax: float, /) -> None:
        """To set a new value for the import sales taxes.

        Args:
            tax: New value for the import sales taxes.
        """
        self.__taxes = (Decimal(str(tax)), self.__taxes[1], self.__taxes[2])

    def new_normal_tax(self, tax: float, /) -> None:
        """To set a new value for the basic sales taxes.

        Args:
            tax: New value for the basic sales taxes.
        """
        self.__taxes = (self.__taxes[0], Decimal(str(tax)), self.__taxes[2])

    def __str__(self) -> str:
        """To create a string representation.

        Returns:
            String representation of the ``TaxCalculator`` object.
        """
        return (
            "---\nTAXES:\n"
            + f"\textra import sales tax: {self.__taxes[0]}\n"
            + f"\tbasic sales tax: {self.__taxes[1]}\n---"
        )
