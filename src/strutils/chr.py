#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""chr

TODO.

REQUIRES: Python 3.9+
"""

import sys
from argparse import ArgumentParser, ArgumentTypeError
from pathlib import Path

__author__ = "Vincent Lin"

DESCRIPTION = """\
TODO.
"""


def validate_int(value: str) -> int:
    """
    Validator for a non-negative integer input, possibly of varying
    radixes as denoted by their conventional prefix.
    """
    if value.startswith("-"):
        raise ArgumentTypeError(f"{value} is negative or not an int.")

    if value.startswith("0x"):
        as_int = int(value, 16)
    # Second condition is to support C-style octal numbers e.g. 0755.
    elif value.startswith("0o") or \
            value.startswith("0") and value[1:].isnumeric():
        stripped = value.removeprefix("0").removeprefix("o")
        as_int = int(stripped, 8)
    elif value.startswith("0b"):
        as_int = int(value, 2)
    else:
        as_int = int(value)

    return as_int


parser = ArgumentParser(prog=Path(sys.argv[0]).name,
                        description=DESCRIPTION)

parser.add_argument("codes", metavar="CODE", nargs="*", type=validate_int,
                    help="TODO.")

parser.add_argument("-e", "--echo", action="store_true",
                    help="print the original code points alongside")

sep_group = parser.add_mutually_exclusive_group()

sep_group.add_argument("-d", "--delimiter", metavar="DELIM", default=" ",
                       help="string to use between each character")
sep_group.add_argument("-t", "--tabs", action="store_true",
                       help="use TAB as the delimiter")
sep_group.add_argument("-1", dest="one_per_line", action="store_true",
                       help="print each entry on its own line")


def codes_from_stdin() -> list[int]:
    try:
        return [validate_int(token) for token in sys.stdin.read().split()
                if token and not token.isspace()]
    except (ValueError, ArgumentTypeError) as error:
        invalid_token = error.args[0].split()[-1]
        parser.error(f"invalid validate_int value: {invalid_token}")


def escaped(ch: str) -> str:
    r"""
    Return a string representation that can be safely printed without
    messing up formatting.

    NOTE: len(escaped(ch)) may not necessarily be 1.  This is true for
    characters that have an escape sequence representation like \n or
    \x1e.
    """
    safe = repr(ch).strip("'\"")
    if safe == " ":
        return "SPC"  # TODO: What if they want the actual space?
    return repr(ch).strip("'\"")


def main() -> None:
    """Main driver function."""
    namespace = parser.parse_args()

    codes: list[int] = namespace.codes
    if not codes:
        codes = codes_from_stdin()

    echo: bool = namespace.echo

    delimiter: str = namespace.delimiter
    tabs: bool = namespace.tabs
    if tabs:
        delimiter = "\t"

    one_per_line: bool = namespace.one_per_line
    # TEMP: Will have to handle this differently like in ord when we
    # implement echoing.
    if one_per_line:
        delimiter = "\n"

    max_width = max(len(str(code)) for code in codes) if echo else 0

    if echo:
        echoed = delimiter.join(str(code).ljust(max_width) for code in codes)
        print(echoed)

    output = delimiter.join(escaped(chr(code)).ljust(max_width)
                            for code in codes)
    print(output)


if __name__ == "__main__":
    main()
