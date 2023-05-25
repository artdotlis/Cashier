import pytest

from cashier.purchase.formatter import InFormatter, OutFormatter
from cashier.register import DI_BUY, DI_TERM, DO_IMP, DO_SALES_T, DO_TOTAL


@pytest.fixture()
def out_formatter() -> OutFormatter:
    out_str = DO_TOTAL, DO_SALES_T, DO_IMP
    return OutFormatter(out_str[0], out_str[1], out_str[2])


@pytest.fixture()
def in_formatter() -> InFormatter:
    in_term_str = DI_TERM, DI_BUY
    # lambda str_val: True
    # Because the exact behavior of this function is
    # not implemented in cashier.purchase.formatter
    return InFormatter(in_term_str[0], in_term_str[1], lambda _: True)
