#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Apply Python's chr() on all the input numbers, with support for
different bases, such as hexadecimal, octal, and binary, by inferring
from their respective prefixes (0x, 0o/0, 0b) or with a flag.

EXAMPLES:

    $ chr 65 66 67
    A B C

    $ chr -e 0x50 0x52 0x4F
    80 82 79
    P  R  O

    $ chr -d _ $(seq 68 75)
    D_E_F_G_H_I_J_K
"""

import argparse
import sys

from .common.functional import program_options_struct
from .common.output import exit_with_error, print_stderr

__author__ = "Vincent Lin"


@program_options_struct
class ProgramOptions:
    code_points: list[str]
    echo_requested: bool
    use_literal_spaces: bool
    delimiter: str
    one_per_line: bool
    print_as_is: bool
    use_hexadecimal: bool
    use_octal: bool
    use_binary: bool


parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawTextHelpFormatter,
    add_help=False,
)

parser.add_argument(
    "--help",
    action="help",
    default=argparse.SUPPRESS,
    help="show this message and exit",
)
parser.add_argument(
    "code_points",
    metavar="CODE",
    nargs="*",
    help="numbers to interpret as Unicode codepoints",
)
parser.add_argument(
    "-e", "--echo",
    action="store_true",
    dest="echo_requested",
    help="print the original code points alongside",
)
parser.add_argument(
    "-s", "--literal-spaces",
    action="store_true",
    dest="use_literal_spaces",
    help="print space characters as spaces instead of SPC",
)

sep_group = parser.add_mutually_exclusive_group()

sep_group.add_argument(
    "-d", "--delimiter",
    metavar="DELIM",
    default=" ",
    dest="delimiter",
    help="string to use between each character",
)
sep_group.add_argument(
    "-1",
    action="store_true",
    dest="one_per_line",
    help="print each entry on its own line",
)
sep_group.add_argument(
    "-p", "--print",
    action="store_true",
    dest="print_as_is",
    help="decode and print characters as they are",
)

radix_group = parser.add_mutually_exclusive_group()

radix_group.add_argument(
    "-x", "-h", "--hexadecimal", "--hex",
    action="store_true",
    dest="use_hexadecimal",
    help="interpret code points as hexadecimal",
)
radix_group.add_argument(
    "-o", "--octal", "--oct",
    action="store_true",
    dest="use_octal",
    help="interpret code points as octal",
)
radix_group.add_argument(
    "-b", "--binary", "--bin",
    action="store_true",
    dest="use_binary",
    help="interpret code points as binary",
)


def validate_int_with_possible_radix_prefix(
    value: str,
    *,
    base: int | None = None,
) -> int:
    """
    Validator for a non-negative integer input, possibly of varying
    radixes as denoted by their conventional prefix. If base is
    provided, interpret value with that base regardless of prefix.
    """
    if value.startswith("-"):
        exit_with_error(f"{value} is negative or not an int.")

    def cast_int(string: str, base: int) -> int:
        try:
            return int(string, base)
        except ValueError:
            exit_with_error(
                f"{value} could not be interpreted "
                f"as an integer with base {base}.",
            )

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


def get_codes_from_stdin(*, base: int | None = None) -> list[int]:
    tokens = sys.stdin.read().split()
    return [
        validate_int_with_possible_radix_prefix(token, base=base)
        for token in tokens
    ]


def escaped(ch: str, literal_spaces: bool) -> str:
    r"""
    Return a string representation that can be safely printed without
    messing up formatting.

    NOTE: len(escaped(ch)) may not necessarily be 1. This is true for
    characters that have an escape sequence representation like \n or
    \x1e.
    """
    safe = repr(ch).strip("'\"")
    if safe == " " and not literal_spaces:
        return "SPC"
    return repr(ch).strip("'\"")


def print_one_per_line(
    codes_in_decimal: list[int],
    codes_as_strings: list[str],
    echo: bool,
) -> None:
    """Handle the case where each result goes on a separate line."""
    if echo:
        max_width = max(len(code) for code in codes_as_strings)
        width = max(len(str(code)) for code in codes_in_decimal)

        def format_line(code: int, string: str) -> str:
            return f"{string.ljust(max_width)} {chr(code).ljust(width)}"
    else:
        def format_line(code: int, string: str) -> str:
            del code
            return string

    lines = "\n".join(
        format_line(code, string)
        for code, string in zip(codes_in_decimal, codes_as_strings)
    )
    print(lines)


def main() -> None:
    """Main driver function."""
    args = parser.parse_args()
    options = ProgramOptions(**vars(args))

    if options.use_hexadecimal:
        base = 16
    elif options.use_octal:
        base = 8
    elif options.use_binary:
        base = 2
    else:
        base = None

    codes_as_strings: list[str] = options.code_points
    codes_in_decimal: list[int] = [
        validate_int_with_possible_radix_prefix(code, base=base)
        for code in options.code_points
    ]

    if not codes_in_decimal:
        codes_in_decimal = get_codes_from_stdin(base=base)

    # Ignore echo, doesn't make sense to use it with --print.
    if options.echo_requested and options.print_as_is:
        print_stderr("WARNING: Ignoring --echo since --print was used.")
    # The simplest case, where we literally decode all the characters
    # and print them side-by-side. Useful when you're decoding a message
    # and just want to see the content as it was originally written.
    if options.print_as_is:
        print("".join(chr(code) for code in codes_in_decimal))
        return

    if options.one_per_line:
        print_one_per_line(
            codes_in_decimal,
            codes_as_strings,
            options.echo_requested,
        )
        return

    max_width = 0
    if options.echo_requested:
        max_width = max(len(str(code)) for code in codes_in_decimal)

    if options.echo_requested:
        echoed = options.delimiter.join(
            str(code).ljust(max_width)
            for code in codes_in_decimal
        )
        print(echoed)

    # Actual chr() logic lol.
    def format_chr(code: int) -> str:
        try:
            return escaped(
                chr(code).ljust(max_width),
                options.use_literal_spaces,
            )
        # chr() can raise if arg is not in range(0x110000).
        except ValueError as error:
            msg = f"could not get the character of code point {code}: {error}"
            exit_with_error(msg)

    output = options.delimiter.join(
        format_chr(code)
        for code in codes_in_decimal
    )
    print(output)


if __name__ == "__main__":
    main()
