# -*- coding: utf-8 -*-
from typing import Final

from src.cashier.register.bill import Bill
from src.cashier.register.formatter import InFormatter, OutFormatter
from src.cashier.register.tax_calculator import TaxCalculator


# default values for the input-formatter
_DI_TERM: Final[str] = "##"
_DI_BUY: Final[str] = "#"
# default values for the output-formatter
_DO_TOTAL: Final[str] = "Total"
_DO_SALES_T: Final[str] = "Sales Taxes"
_DO_IMP: Final[str] = "imported"
# default tax exemptions
_D_TAX_E: Final[set[str]] = {
    "book", "books",
    "chocolate", "chocolates",
    "pill", "pills"
}


def get_default_terms() -> tuple[str, str]:
    return _DI_TERM, _DI_BUY


def get_default_out() -> tuple[str, str, str]:
    return _DO_TOTAL, _DO_SALES_T, _DO_IMP


def decide_if_taxed(in_str: str, /) -> bool:
    for item_sub_name in in_str.split(" "):
        if item_sub_name in _D_TAX_E:
            return False
    return True


def start_register() -> None:  # pragma: no cover
    in_form = InFormatter(_DI_TERM, _DI_BUY, decide_if_taxed)
    print(str(in_form))
    out_form = OutFormatter(_DO_TOTAL, _DO_SALES_T, _DO_IMP)
    print(str(out_form))
    tax_calc = TaxCalculator(0.05, 0.1)
    print(str(tax_calc))
    print("creating registry [finished]")
    bill_list = [Bill(out_form, tax_calc)]
    print("\nplease type in the desired item:")
    print(f"input {len(bill_list)} [start]")
    while in_form.is_not_term(input_str := input()):
        if in_form.is_not_bought(input_str):
            p_item = in_form.analyse_input(input_str)
            if p_item[0]:
                print(bill_list[-1].add_item(p_item[1]))
            else:
                print("input pattern was not recognised")
                print(str(out_form))
        else:
            print(f"input {len(bill_list)} [finished]")
            bill_list.append(Bill(out_form, tax_calc))
            print(f"input {len(bill_list)} [start]")
    print("### OUTPUT [start]")
    for item_i, item_v in enumerate(bill_list, 1):
        out_str = item_v.finish()
        if out_str[0]:
            print(f"output {item_i}:")
            print(out_str[1])
    print("### OUTPUT [finished]")
