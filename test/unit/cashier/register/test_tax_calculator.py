# -*- coding: utf-8 -*-
from decimal import Decimal

import pytest

from src.cashier.purchase.container import PurchasedItem
from src.cashier.purchase.tax_calculator import TaxCalculator


pytest_plugins = ("test.unit.fixture.taxes",)


def _p_it_cr(item_i: int, price: Decimal, cnt: int, imp: bool, tax: bool) -> PurchasedItem:
    return PurchasedItem(
        imported=imp, name=f"item_{item_i}",
        price=price,
        cnt=cnt,
        taxed=tax
    )


@pytest.fixture
def tax_tests_basic() -> tuple[list[tuple[Decimal, int, str]], Decimal]:
    basic_taxes = Decimal('0.1')
    return ([
        (Decimal('10.00'), 1, '1.00'),
        (Decimal('10.10'), 1, '1.00'),
        (Decimal('10.20'), 1, '1.00'),
        (Decimal('10.24'), 1, '1.00'),
        (Decimal('10.30'), 1, '1.05'),
        (Decimal('10.40'), 1, '1.05'),
        (Decimal('10.50'), 1, '1.05'),
        (Decimal('10.60'), 1, '1.05'),
        (Decimal('10.70'), 1, '1.05'),
        (Decimal('10.74'), 1, '1.05'),
        (Decimal('10.80'), 1, '1.10'),
        (Decimal('10.90'), 1, '1.10'),
        (Decimal('10.00'), 3, '3.00')
    ], basic_taxes)


@pytest.fixture
def zero_taxed_items() -> list[PurchasedItem]:
    return [
        _p_it_cr(0, Decimal('10.00'), 2, True, True),
        _p_it_cr(1, Decimal('10.00'), 2, False, True),
        _p_it_cr(1, Decimal('10.00'), 2, True, False)
    ]


@pytest.fixture
def taxed_items(tax_tests_basic) -> tuple[Decimal, list[tuple[PurchasedItem, str]]]:
    sales_only_tax = [
        (_p_it_cr(item_i, item_el[0], item_el[1], False, True), item_el[2])
        for item_i, item_el in enumerate(tax_tests_basic[0], 1)
    ]
    sales_only_tax.extend(
        (_p_it_cr(item_i, -1 * item_el[0], item_el[1], False, True), item_el[2])
        for item_i, item_el in enumerate(tax_tests_basic[0], 1)
    )
    return tax_tests_basic[1], sales_only_tax


@pytest.fixture
def taxed_imported_items(tax_tests_basic) \
        -> tuple[Decimal, Decimal, list[tuple[PurchasedItem, str]]]:
    import_tax = Decimal('0.05')
    imported_taxes = [
        (_p_it_cr(1, Decimal('10.00'), 1, True, True), '1.50'),
        (_p_it_cr(2, Decimal('10.00'), 3, True, True), '4.50'),
        (_p_it_cr(3, Decimal('-10.00'), 1, True, True), '1.50'),
        (_p_it_cr(4, Decimal('-10.00'), 3, True, True), '4.50'),
        (_p_it_cr(5, Decimal('10.00'), 1, True, False), '0.50'),
        (_p_it_cr(6, Decimal('-10.00'), 3, True, False), '1.50')
    ]
    return tax_tests_basic[1], import_tax, imported_taxes


@pytest.fixture
def no_tax() -> list[tuple[PurchasedItem, str]]:
    return [
        (_p_it_cr(1, Decimal('10.00'), 1, False, False), '0.00'),
        (_p_it_cr(2, Decimal('10.00'), 3, False, False), '0.00'),
        (_p_it_cr(3, Decimal('-10.00'), 1, False, False), '0.00'),
        (_p_it_cr(4, Decimal('-10.00'), 3, False, False), '0.00')
    ]


@pytest.fixture
def init_tax() -> list[tuple[float, float]]:
    return [
        (0.0, 0.0), (-2.0, 1.0), (2.0, 2.0)
    ]


class TestTaxCalculator:

    def test_input(self, init_tax):
        for tax_i in init_tax:
            assert TaxCalculator.check_taxes(tax_i[0], tax_i[1], "") == tax_i[1]

    def test_tax_zero(self, tax_calc, zero_taxed_items):
        tax_calc.new_normal_tax(float(Decimal('0.00')))
        tax_calc.new_import_tax(float(Decimal('0.00')))
        for test_i in zero_taxed_items:
            assert str(tax_calc.tax(test_i)) == '0.00'

    def test_tax_basic(self, tax_calc, taxed_items):
        tax_calc.new_normal_tax(float(taxed_items[0]))
        for test_i in taxed_items[1]:
            assert str(tax_calc.tax(test_i[0])) == test_i[1]

    def test_tax_basic_import(self, tax_calc, taxed_imported_items):
        tax_calc.new_normal_tax(float(taxed_imported_items[0]))
        tax_calc.new_import_tax(float(taxed_imported_items[1]))
        for test_i in taxed_imported_items[2]:
            assert str(tax_calc.tax(test_i[0])) == test_i[1]

    def test_tax_none(self, tax_calc, no_tax):
        for test_i in no_tax:
            assert str(tax_calc.tax(test_i[0])) == test_i[1]
