"""A module providing a starting procedure."""
from collections.abc import Callable
from pathlib import Path
from typing import Final

from cashier.purchase.bill import Bill
from cashier.purchase.formatter import InFormatter, OutFormatter
from cashier.purchase.tax_calculator import TaxCalculator

# default values for the input-formatter
DI_TERM: Final[str] = "##"
DI_BUY: Final[str] = "#"
# default values for the output-formatter
DO_TOTAL: Final[str] = "Total"
DO_SALES_T: Final[str] = "Sales Taxes"
DO_IMP: Final[str] = "imported"
# default tax exemptions
_D_TAX_E: Final[set[str]] = {
    "book",
    "books",
    "chocolate",
    "chocolates",
    "pill",
    "pills",
}


def decide_if_taxed(n_taxed: set[str]) -> Callable[[str], bool]:
    """To create a decider function for omitting taxation.

    Args:
        n_taxed: The set containing all items which shouldn't be taxed.
            If empty, a default set will be chosen.

    Returns:
        Decider function for omitting taxation.
    """
    local_set = _D_TAX_E
    if n_taxed:
        local_set = n_taxed

    def _decide_if_taxed(in_str: str, /) -> bool:
        """To check whether an item is taxed.

        A very simple function which looks up the item in a
        given set. This set contains all item names which should be omitted
        from taxation.

        Args:
            in_str: The name of the purchased item which should be checked for taxation.

        Returns:
            Whether the item is taxed.
        """
        for item_sub_name in in_str.split(" "):
            if item_sub_name in local_set:
                return False
        return True

    return _decide_if_taxed


def _read_tax_file(tax_file: None | Path, /) -> set[str]:
    """To create a set with all item names which shouldn't be taxed.

    The file should contain one name per line.

    Args:
        tax_file: The file containing item names which shouldn't be taxed.

    Returns:
        A set with items which shouldn't be taxed.
        The set can be empty.
    """
    if tax_file is None:
        return set()
    try:
        with tax_file.open("r") as fh_r:
            return {line.rstrip() for line in fh_r}
    except IOError as ex_n:
        print(str(ex_n))
    return set()


def start_register(tax_file: None | Path, /) -> None:
    """To start the software.

    Args:
        tax_file: The optional file containing the names of not-taxed items.
    """
    in_form = InFormatter(DI_TERM, DI_BUY, decide_if_taxed(_read_tax_file(tax_file)))
    print(str(in_form))
    out_form = OutFormatter(DO_TOTAL, DO_SALES_T, DO_IMP)
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
            if p_item[0] and p_item[1] is not None:
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
