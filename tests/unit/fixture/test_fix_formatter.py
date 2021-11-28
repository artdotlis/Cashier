# -*- coding: utf-8 -*-
import pytest

from src.cashier.purchase.formatter import InFormatter
from src.cashier.purchase.formatter import OutFormatter
from src.cashier.register import get_default_out
from src.cashier.register import get_default_terms


@pytest.fixture
def out_formatter() -> OutFormatter:
    out_str = get_default_out()
    return OutFormatter(out_str[0], out_str[1], out_str[2])


@pytest.fixture
def in_formatter() -> InFormatter:
    in_term_str = get_default_terms()
    # lambda str_val: True
    # Because the exact behavior of this function is
    # not implemented in src.cashier.purchase.formatter
    return InFormatter(in_term_str[0], in_term_str[1], lambda str_val: True)
