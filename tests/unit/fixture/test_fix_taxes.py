import pytest

from cashier.purchase.tax_calculator import TaxCalculator


@pytest.fixture()
def tax_calc() -> TaxCalculator:
    return TaxCalculator(0.05, 0.1)
