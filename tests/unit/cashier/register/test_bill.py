# -*- coding: utf-8 -*-
from decimal import Decimal

import pytest

from src.cashier.purchase.bill import Bill
from src.cashier.purchase.container import PurchasedItem

pytest_plugins = ("tests.unit.fixture.fix_formatter", "tests.unit.fixture.fix_taxes")


@pytest.fixture
def bill(tax_calc, out_formatter) -> Bill:
    return Bill(out_formatter, tax_calc)


@pytest.fixture
def add_act() -> list[tuple[PurchasedItem, int, str, bool]]:
    return [
        (PurchasedItem(imported=True, name="i0", price=Decimal("1"), cnt=1, taxed=True),
         1, "added item (id: 1) successfully", True),
        (PurchasedItem(imported=True, name="i0", price=Decimal("1"), cnt=1, taxed=True),
         0, "the amount of items [0] reached max. value (0)", False),
        (PurchasedItem(imported=True, name="i0", price=Decimal("-1"), cnt=1, taxed=True),
         1, "the item price can't be negative", False),
    ]


@pytest.fixture
def fin_container(bill) -> tuple[Bill, str]:
    items = [
        PurchasedItem(imported=False, name="book",
                      price=Decimal("12.49"), cnt=1, taxed=False),
        PurchasedItem(imported=False, name="music CD",
                      price=Decimal("14.99"), cnt=1, taxed=True),
        PurchasedItem(imported=False, name="chocolate bar",
                      price=Decimal("0.85"), cnt=1, taxed=False)
    ]
    output = "\n".join([
        "1 book: 12.49",
        "1 music CD: 16.49",
        "1 chocolate bar: 0.85",
        "Sales Taxes: 1.50",
        "Total: 29.83"
    ])
    for item_i in items:
        bill.add_item(item_i)
    return bill, output


class TestBill:
    def test_add_rem_item(self, bill, add_act):
        for item_i in add_act:
            bill._Bill__max_id = item_i[1]
            assert bill.add_item(item_i[0]) == item_i[2]
            assert bill.rem_item(1) == item_i[3]
            bill._Bill__item_id_gen = 0

    def test_finish(self, fin_container):
        assert ''.join(fin_container[0].finish()[1]) == fin_container[1]
