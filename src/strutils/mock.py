#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
Convert an input string into a version with alternating capitalization
as used in sarcastic texting.

EXAMPLES:

    $ mock hello there
    hElLo ThErE

    $ mock -c hello there
    HeLlO tHeRe

    $ echo -e 'hello\tthere\ngeneral\tkenobi' | mock
    hElLo   ThErE
    gEnErAl KeNoBi

NOTE: If multiple strings are provided as separate command line
arguments, they will be subject to the shell parsing rules.  The script
has no way of knowing the whitespace originally used to separate the
arguments, so it will assume to join them with single spaces.  To
preserve whitespace, use quoting.
"""

import io
import sys
from argparse import ArgumentParser, RawTextHelpFormatter
from pathlib import Path

__author__ = "Vincent Lin"

parser = ArgumentParser(prog=Path(sys.argv[0]).name,
                        description=__doc__,
                        formatter_class=RawTextHelpFormatter)

parser.add_argument(
    "strings",
    metavar="STRING",
    nargs="*",
    help="text to mock; read from stdin if omitted",
)

parser.add_argument(
    "-c", "--caps-first",
    dest="caps_first",
    action="store_true",
    help="start with a uppercase instead of lowercase before alternating",
)


def toggle_case(char: str) -> str:
    return char.lower() if char.isupper() else char.upper()


def main() -> None:
    args = parser.parse_args()

    strings: list[str] = args.strings
    caps_first: bool = args.caps_first

    from_stdin = False
    if not strings:
        strings = [sys.stdin.read()]
        from_stdin = True

    toggle_flag = caps_first

    def mock_token(token: str) -> str:
        nonlocal toggle_flag
        result = io.StringIO()
        for char in token:
            if char.isalpha():
                result.write(toggle_case(char) if toggle_flag else char)
                toggle_flag = not toggle_flag
            else:
                result.write(char)
        return result.getvalue()

    result = " ".join(mock_token(token) for token in strings)

    # Compensate for the missing \n (RET submit) if from command line.
    print(result, end="" if from_stdin else "\n")


if __name__ == "__main__":
    main()
