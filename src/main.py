# -*- coding: utf-8 -*-
import argparse

from src.cashier.register.registrer import start_register
from src.cashier.version import VERSION


def main() -> None:
    arg_parser = argparse.ArgumentParser(
        prog='cashier',
        description="A library for calculating sales taxes for purchased items."
    )
    arg_parser.add_argument('--version', action='version', version=VERSION)
    start_register()
    print("[closed]")


if __name__ == '__main__':
    main()
