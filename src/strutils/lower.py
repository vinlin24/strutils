#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
Apply Python's str.lower() on the input strings.

EXAMPLES:

    $ lower -n 'HELLO THERE'
    hello there

    $ echo -e " HELLO\n    thERe" | lower
     hello
         there

NOTE: If you supply multiple strings as a whitespace-separated list at
the command line, it will be interpreted as the concatenation of the
strings with a single space joining them. Use quoting to preserve
whitespace in your shell script.
"""

import argparse
import sys

parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawTextHelpFormatter,
)

parser.add_argument(
    "strings",
    metavar="STRING",
    nargs="*",
    help="strings to convert to lowercase (reads from stdin if omitted)",
)
parser.add_argument(
    "-n", "--newline",
    dest="use_trailing_newline",
    action="store_true",
    help="append a newline to the output",
)


def main() -> None:
    args = parser.parse_args()

    strings: list[str] = args.strings
    use_trailing_newline: bool = args.use_trailing_newline

    if not strings:
        strings = [sys.stdin.read()]

    transformed = (string.lower() for string in strings)
    print(*transformed, end=("\n" if use_trailing_newline else ""))


if __name__ == "__main__":
    main()
