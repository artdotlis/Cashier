import pytest

from cashier.purchase.bill import Bill
from cashier.purchase.formatter import InFormatter, OutFormatter
from cashier.purchase.tax_calculator import TaxCalculator
from cashier.register import (
    DI_BUY,
    DI_TERM,
    DO_IMP,
    DO_SALES_T,
    DO_TOTAL,
    decide_if_taxed,
)


@pytest.fixture()
def start_register() -> tuple[InFormatter, OutFormatter, TaxCalculator]:
    in_form = InFormatter(DI_TERM, DI_BUY, decide_if_taxed(set()))
    out_form = OutFormatter(DO_TOTAL, DO_SALES_T, DO_IMP)
    tax_calc = TaxCalculator(0.05, 0.1)

    return in_form, out_form, tax_calc


@pytest.fixture()
def create_input(shared_datadir) -> list[str]:
    with shared_datadir.joinpath("test_run_in.txt").open("r") as fh_in:
        return [line.rstrip() for line in fh_in]


@pytest.fixture()
def create_output(shared_datadir) -> list[str]:
    with shared_datadir.joinpath("test_run_out.txt").open("r") as fh_out:
        return [out_str for line in fh_out if (out_str := line.rstrip())]


def _parse_input(
    bill_list: list[Bill],
    input_str: str,
    state: tuple[InFormatter, OutFormatter, TaxCalculator],
) -> bool:
    in_form, out_form, tax_calc = state[0], state[1], state[2]
    if in_form.is_not_term(input_str):
        if in_form.is_not_bought(input_str):
            p_item = in_form.analyse_input(input_str)
            if p_item[0] and p_item[1] is not None:
                bill_list[-1].add_item(p_item[1])
        else:
            bill_list.append(Bill(out_form, tax_calc))
        return False
    return True


def test_integration_run(create_input, create_output, start_register):
    bill_list = [Bill(start_register[1], start_register[2])]
    act_i = 0
    for a_i, input_act in enumerate(create_input, 1):
        parsed = _parse_input(bill_list, input_act, start_register)
        act_i = a_i
        if parsed:
            break
    assert act_i == len(create_input)
    adder_run = 0
    for res_i, res_e in enumerate(bill_list, 1):
        res_out = res_e.finish()
        if res_out[0]:
            assert f"output {res_i}:" == create_output[adder_run + res_i - 1]
            adder_run += 1
            s_i = 0
            for s_i, s_e in enumerate(res_out[1].split("\n")):
                assert s_e == create_output[s_i + adder_run + res_i - 1]
            adder_run += s_i
