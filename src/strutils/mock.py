#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
Convert an input string into a version with alternating capitalization
as used in sarcastic texting.

EXAMPLES:

    $ mock hello there
    hElLo ThErE

    $ echo -e 'hello\tthere\ngeneral\tkenobi' | mock
    hElLo   ThErE
    gEnErAl KeNoBi

NOTE: If multiple strings are provided as separate command line
arguments, they will be subject to the shell parsing rules.  The script
has no way of knowing the whitespace originally used to separate the
arguments, so it will assume to join them with single spaces.  To
preserve whitespace, use quoting.

NOTE: This is a Python port of my original mock.c program, which can be
found in the commit history of my startup-config repository.
"""

import io
import sys
from argparse import ArgumentParser, RawTextHelpFormatter
from pathlib import Path

__author__ = "Vincent Lin"

parser = ArgumentParser(prog=Path(sys.argv[0]).name,
                        description=__doc__,
                        formatter_class=RawTextHelpFormatter)
parser.add_argument("strings", metavar="STRING", nargs="*",
                    help="text to mock; read from stdin if omitted")


def toggle_case(char: str) -> str:
    return char.lower() if char.isupper() else char.upper()


def main() -> None:
    namespace = parser.parse_args()
    strings: list[str] = namespace.strings
    from_stdin = False
    if not strings:
        strings = [sys.stdin.read()]
        from_stdin = True

    toggle_flag = False

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
