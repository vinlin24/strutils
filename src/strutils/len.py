#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
Compute the length of each string. For most purposes, just saves a few
keystrokes from the more versatile `echo -n "$string" | wc` pattern, but
also serves as a way to apply the counting on EACH input token.

EXAMPLES:

    $ len "hello there"
    11

    $ len general kenobi you are a bold one
    7 6 3 3 1 4 3

    $ len -1 -- separate lines please
    8
    5
    6

    $ len -t -- there are 5 tokens here
    5

NOTE: "Tokens" are determined by how the shell running this script
parses the input at the command line. If you intend a string with
whitespace to be parsed as one token, be sure to follow your shell's
quoting rules. Reading from stdin always treats the string as one token.
"""

import sys
from argparse import ArgumentParser, RawTextHelpFormatter
from pathlib import Path

parser = ArgumentParser(prog=Path(sys.argv[0]).name,
                        description=__doc__,
                        formatter_class=RawTextHelpFormatter)
parser.add_argument("strings", metavar="STRING", nargs="*",
                    help="text to analyze; read from stdin if omitted")
parser.add_argument("-1", dest="one_per_line", action="store_true",
                    help="print each result on its own line")
parser.add_argument("-t", "--tokens", dest="count_tokens", action="store_true",
                    help="print number of tokens received instead")


def main() -> None:
    """Main driver function."""
    namespace = parser.parse_args()
    strings: list[str] = namespace.strings
    one_per_line: bool = namespace.one_per_line
    count_tokens: bool = namespace.count_tokens

    if not strings:
        strings = [sys.stdin.read()]

    if count_tokens:
        lengths = [len(strings)]
    else:
        lengths = [len(string) for string in strings]

    delimiter = "\n" if one_per_line else " "
    print(delimiter.join(str(length) for length in lengths))


if __name__ == "__main__":
    main()
