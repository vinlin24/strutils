#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Apply Python's chr() on all the input numbers, with support for
different bases, such as hexadecimal, octal, and binary, through the use
of their respective prefixes (0x, 0o/0, 0b).

EXAMPLES:

    $ chr 65 66 67
    A B C

    $ chr -e 0x50 0x52 0x4F
    80 82 79
    P  R  O

    $ chr -d _ $(seq 68 75)
    D_E_F_G_H_I_J_K

TODO: Improvements to be made. Some options or combination of options do
not yet work as intended.
"""

import sys
from argparse import SUPPRESS, ArgumentParser, RawTextHelpFormatter
from pathlib import Path
from typing import NoReturn

__author__ = "Vincent Lin"

PROG = Path(sys.argv[0]).name

parser = ArgumentParser(prog=PROG,
                        description=__doc__,
                        formatter_class=RawTextHelpFormatter,
                        add_help=False)
parser.add_argument("--help", action="help", default=SUPPRESS,
                    help="show this message and exit")

parser.add_argument("codes", metavar="CODE", nargs="*",
                    help="numbers to interpret as Unicode codepoints")

parser.add_argument("-e", "--echo", action="store_true",
                    help="print the original code points alongside")

sep_group = parser.add_mutually_exclusive_group()

sep_group.add_argument("-d", "--delimiter", metavar="DELIM", default=" ",
                       help="string to use between each character")
sep_group.add_argument("-1", dest="one_per_line", action="store_true",
                       help="print each entry on its own line")


radix_group = parser.add_mutually_exclusive_group()

radix_group.add_argument("-x", "-h", "--hexadecimal", "--hex",
                         action="store_true",
                         help="interpret code points as hexadecimal")
radix_group.add_argument("-o", "--octal", "--oct", action="store_true",
                         help="interpret code points as octal")
radix_group.add_argument("-b", "--binary", "--bin", action="store_true",
                         help="interpret code points as binary")


def exit_with_message(message: str, *, code: int = 0) -> NoReturn:
    sys.stderr.write(f"{PROG}: {message}\n")
    sys.exit(code)


def validate_int(value: str, *, base: int | None = None) -> int:
    """
    Validator for a non-negative integer input, possibly of varying
    radixes as denoted by their conventional prefix.  If base is
    provided, interpret value with that base regardless of prefix.
    """
    if value.startswith("-"):
        exit_with_message(f"{value} is negative or not an int.", code=22)

    def cast_int(string: str, base: int) -> int:
        try:
            return int(string, base)
        except ValueError:
            exit_with_message(f"{value} could not be interpreted as "
                              f"an integer with base {base}.",
                              code=22)

    if base is not None:
        value = value.lstrip("0xob")
        return cast_int(value, base)

    if value.startswith("0x"):
        return cast_int(value, 16)
    # Second condition is to support C-style octal numbers e.g. 0755.
    if value.startswith("0o") or \
            value.startswith("0") and value[1:].isnumeric():
        stripped = value.removeprefix("0").removeprefix("o")
        return cast_int(stripped, 8)
    if value.startswith("0b"):
        return cast_int(value, 2)

    return cast_int(value, 10)


def codes_from_stdin(*, base: int | None = None) -> list[int]:
    return [validate_int(token, base=base)
            for token in sys.stdin.read().split()
            if token and not token.isspace()]


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

    hexadecimal: bool = namespace.hexadecimal
    octal: bool = namespace.octal
    binary: bool = namespace.binary

    if hexadecimal:
        base = 16
    elif octal:
        base = 8
    elif binary:
        base = 2
    else:
        base = None

    codes: list[int] = [validate_int(code, base=base)
                        for code in namespace.codes]
    if not codes:
        codes = codes_from_stdin(base=base)

    echo: bool = namespace.echo

    delimiter: str = namespace.delimiter

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
