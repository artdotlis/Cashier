# -*- coding: utf-8 -*-
"""Main function."""
import argparse
import sys

from src.cashier.register import start_register
from src.cashier.version import get_version


def main() -> None:
    """
    To start the purchase simulation.

    Analyses the given arguments and starts the software.
    """
    arg_parser = argparse.ArgumentParser(
        prog="cashier",
        description="A library for calculating sales taxes for purchased items.",
    )
    arg_parser.add_argument("--version", action="version", version=get_version())
    arg_parser.add_argument(
        "-i",
        "--input",
        action="store",
        type=str,
        required=False,
        default=None,
        help="the path for the omit-taxes file.",
        dest="tax_file",
        metavar="str",
    )
    args = arg_parser.parse_args(args=sys.argv[1:])
    start_register(args.tax_file)
    print("[closed]")


if __name__ == "__main__":
    main()
