#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
Apply Python's ord() on all the characters within the input string, with
support for different bases, such as hexadecimal, octal, and binary, as
well as the option of including their respective prefixes (0x, 0o, 0b).

REQUIRES: Python 3.10+

EXAMPLES:

    * ord -x "hello there"
    * echo -e "hello\nthere\n" | ord -ep
    * ord lmao -1 | awk 'BEGIN {s=0} {s += $1} END {print s}'

NOTE: If you supply multiple strings as a whitespace-separated list at
the command line, it will be interpreted as the concatenation of the
strings with no whitespace joining them. Use quoting to preserve
whitespace in your shell script.
"""

import math
import sys
from argparse import SUPPRESS, ArgumentParser, Namespace, RawTextHelpFormatter
from pathlib import Path

__author__ = "Vincent Lin"

parser = ArgumentParser(prog=Path(sys.argv[0]).name,
                        description=__doc__,
                        formatter_class=RawTextHelpFormatter,
                        add_help=False)

parser.add_argument("--help", action="help", default=SUPPRESS,
                    help="show this message and exit")

parser.add_argument("strings", metavar="STRING", nargs="*",
                    help="text string(s); reads from stdin if omitted")

parser.add_argument("-p", "--prefixed", action="store_true",
                    help="keep the radix prefix (0x, 0o, 0b)")
parser.add_argument("-e", "--echo", action="store_true",
                    help="print the original characters alongside")
parser.add_argument("-u", "--uppercase", "--upper", action="store_true",
                    help="use uppercase letters for hexadecimal digits")

bases_group = parser.add_mutually_exclusive_group()

bases_group.add_argument("-x", "-h", "--hexadecimal", "--hex",
                         action="store_true",
                         help="output code points as hexadecimal")
bases_group.add_argument("-X", action="store_true",
                         help="equivalent to specifying -x and -u")
bases_group.add_argument("-o", "--octal", "--oct", action="store_true",
                         help="output code points as octal")
bases_group.add_argument("-b", "--binary", "--bin", action="store_true",
                         help="output code points as binary")

sep_group = parser.add_mutually_exclusive_group()

sep_group.add_argument("-d", "--delimiter", metavar="DELIM", default=" ",
                       help="string to use between each code point")
sep_group.add_argument("-t", "--tabs", action="store_true",
                       help="use TAB as the delimiter")
sep_group.add_argument("-1", dest="one_per_line", action="store_true",
                       help="print each entry on its own line")


# pylint: disable=too-few-public-methods
class CharFormatter:
    """Configurable code point formatter to use on each character.

    USAGE::

        namespace = parser.parse_args()
        char_formatter = CharFormatter(namespace)
        formatted = char_formatter("A")  # __call__
    """

    def __init__(self, options: Namespace) -> None:
        self.prefixed: bool = options.prefixed
        self.uppercase: bool = options.uppercase or options.X

        # Compute upfront how much fill width we'll need.
        string = "".join(options.strings)
        self._max_codepoint = max(ord(ch) for ch in string)

        match options:
            # TODO: The fill widths below only work assuming all input
            # characters are ASCII.  Unicode characters whose code points
            # are represented beyond width digits will mess up the
            # spacing when echoing them with the ord() values.
            case Namespace(hexadecimal=True) | Namespace(X=True):
                self.caster = hex
                self.prefix = "0x"
                self.width = self._digits_needed(digits_per_bit=4)
            case Namespace(octal=True):
                self.caster = oct
                self.prefix = "0o"
                self.width = self._digits_needed(digits_per_bit=3)
            case Namespace(binary=True):
                self.caster = bin
                self.prefix = "0b"
                self.width = self._digits_needed(digits_per_bit=1)
            case _:
                self.caster = str
                self.prefix = ""
                self.width = len(str(self._max_codepoint))

        # The maximum width needed for a char in the original string.
        self.original_max_width = max(len(escaped(ch)) for ch in string)

    def __call__(self, ch: str, echoing: bool) -> str:
        code = ord(ch)

        if echoing:
            width = max(self.width, self.original_max_width)
        else:
            width = self.width

        casted = self.caster(code).removeprefix(self.prefix).zfill(width)
        if self.uppercase:
            casted = casted.upper()
        return (self.prefix if self.prefixed else "") + casted

    def _digits_needed(self, digits_per_bit: int) -> int:
        if self._max_codepoint == 0:
            next_power_of_2 = 1
        else:
            next_power_of_2 = (2**(self._max_codepoint - 1)).bit_length()
        bits_needed = next_power_of_2.bit_length()
        return math.ceil(bits_needed / digits_per_bit)


def escaped(ch: str) -> str:
    """
    Return a string representation that can be safely printed without
    messing up formatting.
    """
    safe = repr(ch).strip("'\"")
    if safe == " ":
        return "SPC"  # So it doesn't break external parsers, prolly.
    return repr(ch).strip("'\"")


def print_one_per_line(string: str, echo: bool,
                       formatter: CharFormatter,
                       ) -> None:
    """Handle the case where each result goes on a separate line."""
    if echo:
        width = formatter.original_max_width

        def format_line(ch: str, echo: bool, /) -> str:
            return f"{escaped(ch).rjust(width)} {formatter(ch, echo)}"
    else:
        format_line = formatter

    lines = "\n".join(format_line(ch, echo) for ch in string)
    print(lines)


def main() -> None:
    """Main driver function."""
    namespace = parser.parse_args()

    if not namespace.strings:
        namespace.strings = [sys.stdin.read()]
    string: str = "".join(namespace.strings)
    if not string:
        sys.stderr.write("Expected at least one string.\n")
        sys.exit(22)

    echo: bool = namespace.echo
    one_per_line: bool = namespace.one_per_line
    delimiter: str = namespace.delimiter
    tabs: bool = namespace.tabs
    if tabs:
        delimiter = "\t"

    char_formatter = CharFormatter(namespace)

    if one_per_line:
        print_one_per_line(string, echo, char_formatter)
        return

    output = delimiter.join(char_formatter(ch, echo) for ch in string)

    if echo:
        prefixed = char_formatter.prefixed
        decimal = char_formatter.prefix == ""

        width = char_formatter.width + (2 if prefixed and not decimal else 0)
        width = max(width, char_formatter.original_max_width)

        echoed = delimiter.join(escaped(ch).ljust(width) for ch in string)
        print(echoed)
    print(output)


if __name__ == "__main__":
    main()
