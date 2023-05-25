from decimal import Decimal

import pytest

from cashier.purchase.container import PItemContainer, PurchasedItem
from cashier.register import DI_BUY, DI_TERM, DO_IMP, DO_SALES_T, DO_TOTAL

pytest_plugins = ("tests.unit.fixture.test_fix_formatter",)


@pytest.fixture()
def out_p_item_list() -> list[tuple[PurchasedItem, Decimal, str]]:
    out_str = DO_TOTAL, DO_SALES_T, DO_IMP
    return [
        (
            PurchasedItem(
                imported=True, name="item_0", price=Decimal("2.45"), cnt=2, taxed=True
            ),
            Decimal("1.00"),
            f"2 {out_str[2]} item_0: 3.45",
        ),
        (
            PurchasedItem(
                imported=False,
                name="item_1",
                price=Decimal("2.45"),
                cnt=1,
                taxed=False,
            ),
            Decimal("0.00"),
            "1 item_1: 2.45",
        ),
    ]


class TestOutFormatter:
    def test_sales_taxes(self, out_formatter):
        out_str = DO_TOTAL, DO_SALES_T, DO_IMP
        assert out_formatter.out_sales_taxes(Decimal("1.45")) == f"{out_str[1]}: 1.45"

    def test_total(self, out_formatter):
        out_str = DO_TOTAL, DO_SALES_T, DO_IMP
        assert out_formatter.out_total(Decimal("1.45")) == f"{out_str[0]}: 1.45"

    def test_list_item(self, out_formatter, out_p_item_list):
        for out_i in out_p_item_list:
            assert (
                out_formatter.out_list_item(
                    PItemContainer(id=0, item=out_i[0], sales_taxes=out_i[1])
                )
                == out_i[2]
            )

    def test_str(self, out_formatter):
        assert isinstance(str(out_formatter), str)


@pytest.fixture()
def in_p_item_list() -> list[tuple[str, tuple[bool, None | PurchasedItem]]]:
    return [
        (
            "1 imported bottle of perfume at 27.99",
            (
                True,
                PurchasedItem(
                    imported=True,
                    name="bottle of perfume",
                    price=Decimal("27.99"),
                    cnt=1,
                    taxed=True,
                ),
            ),
        ),
        (
            "1 bottle of imported perfume at 27.99",
            (
                True,
                PurchasedItem(
                    imported=True,
                    name="bottle of perfume",
                    price=Decimal("27.99"),
                    cnt=1,
                    taxed=True,
                ),
            ),
        ),
        (
            "2 bottle of perfumeimported at 27",
            (
                True,
                PurchasedItem(
                    imported=False,
                    name="bottle of perfumeimported",
                    price=Decimal("27.00"),
                    cnt=2,
                    taxed=True,
                ),
            ),
        ),
        ("2 bottle of perfumeimported at ", (False, None)),
        ("2 bottle of perfumeimported 27.99 ", (False, None)),
        ("bottle of perfumeimported at 27.99 ", (False, None)),
        ("2 at 27.99 ", (False, None)),
    ]


@pytest.fixture()
def term_behavior() -> list[tuple[str, bool]]:
    in_term_str = DI_TERM, DI_BUY
    return [(in_term_str[1], True), (in_term_str[0], False), ("", True)]


@pytest.fixture()
def buy_behavior() -> list[tuple[str, bool]]:
    in_term_str = DI_TERM, DI_BUY
    return [(in_term_str[1], False), (in_term_str[0], True), ("", True)]


class TestInFormatter:
    def test_term_str(self, in_formatter, term_behavior):
        for input_i in term_behavior:
            assert in_formatter.is_not_term(input_i[0]) == input_i[1]

    def test_buy_str(self, in_formatter, buy_behavior):
        for input_i in buy_behavior:
            assert in_formatter.is_not_bought(input_i[0]) == input_i[1]

    def test_analyse_input(self, in_formatter, in_p_item_list):
        for input_i in in_p_item_list:
            results = in_formatter.analyse_input(input_i[0])
            assert results[0] == input_i[1][0]
            assert results[1] == input_i[1][1]

    def test_str(self, in_formatter):
        assert isinstance(str(in_formatter), str)
