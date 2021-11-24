# -*- coding: utf-8 -*-
import argparse

from src.cashier.version import VERSION


def main() -> None:
    arg_parser = argparse.ArgumentParser(
        prog='cashier',
        description="A library for building artificial neural networks."
    )
    arg_parser.add_argument('--version', action='version', version=VERSION)

    pass

    print("[closed]")


if __name__ == '__main__':
    main()
