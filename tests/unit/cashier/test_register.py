# -*- coding: utf-8 -*-
from collections.abc import Callable
from io import StringIO
from pathlib import Path
from unittest import mock
from unittest.mock import patch

import pytest

from src.cashier.register import decide_if_taxed, start_register


@pytest.fixture
def create_default_out() -> list[str]:
    return """---
INPUT format:
\tpattern: ^(\\d+)\\s+(.+)\\s+at\\s+(\\d+)(\\.\\d+)?$
\tsimple input: [item cnt] (imported) [item name] at [price]
\tfinish all purchases: ##
\tstart next purchase: #
---
---
OUTPUT format:
\t[item cnt] (imported) [item name]: [price with taxes]
\tSales Taxes: [value]
\tTotal: [value]
---
---
TAXES:
\textra import sales tax: 0.05
\tbasic sales tax: 0.1
---
creating registry [finished]

please type in the desired item:
input 1 [start]
input pattern was not recognised
---
OUTPUT format:
\t[item cnt] (imported) [item name]: [price with taxes]
\tSales Taxes: [value]
\tTotal: [value]
---
added item (id: 1) successfully
input 1 [finished]
input 2 [start]
### OUTPUT [start]
output 1:
1 chocolate: 1.00
Sales Taxes: 0.00
Total: 1.00
### OUTPUT [finished]

[closed]

[closed]
""".split(
        "\n"
    )


def test_decide_if_taxed():
    with_set = decide_if_taxed({"contains"})
    assert with_set("contains") is False
    assert with_set("missing") is True
    without_set = decide_if_taxed(set())
    assert isinstance(without_set("unknown"), bool)


@pytest.fixture
def register_call() -> Callable[[], str]:
    runner_f = ["#", "1 chocolate at 1.00", "undefined"]

    def create_input() -> str:
        nonlocal runner_f
        if runner_f:
            return runner_f.pop()
        return "##"

    return create_input


@patch("sys.stdout", new_callable=StringIO)
def test_register_simple(mock_stdout, create_default_out, register_call):
    with mock.patch("builtins.input", register_call):
        start_register(None)
    for line_i, line in enumerate(mock_stdout.getvalue().split("\n")):
        assert line == create_default_out[line_i]


@patch("sys.stdout", new_callable=StringIO)
def test_register_file(mock_stdout, create_default_out, register_call):
    with mock.patch("builtins.input", register_call):
        start_register(Path("abc"))
    for line_i, line in enumerate(mock_stdout.getvalue().split("\n")[1:]):
        assert line == create_default_out[line_i]


@patch("sys.stdout", new_callable=StringIO)
def test_register_file_mock(mock_stdout, create_default_out, register_call):
    with (
        mock.patch("builtins.input", register_call),
        mock.patch("pathlib.Path.open", read_data="chocolate\nbook"),
    ):
        start_register(Path("abc"))
    for line_i, line in enumerate(mock_stdout.getvalue().split("\n")):
        assert line == create_default_out[line_i]
