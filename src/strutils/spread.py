#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
Spread out the tokens and characters within a token of an input string.

The tokenization of the input string is as follows:

    * If provided as command line arguments, they are treated directly
      as the tokens to use.  This means you should watch out for the
      quoting and whitespace rules of the shell used to invoke this
      script.
    * If provided through stdin, the input is tokenized according to the
      rule of Python's str.split() method (unless -1/--one-token is
      provided, which forces the input to be treated as a single
      string).

EXAMPLES:

    $ ./spread hello there
    h e l l o   t h e r e

    $ echo -e 'general\tkenobi' | ./spread --char-sep _ --word-sep ' '
    g_e_n_e_r_a_l k_e_n_o_b_i

REQUIRES: Python 3.10+
"""

import sys
from argparse import ArgumentParser, RawTextHelpFormatter
from pathlib import Path

parser = ArgumentParser(prog=Path(sys.argv[0]).name,
                        description=__doc__,
                        formatter_class=RawTextHelpFormatter)
parser.add_argument("strings", metavar="STRING", nargs="*",
                    help="text string(s); reads from stdin if omitted")
parser.add_argument("-c", "--char-sep", metavar="SEP",
                    default=" ", dest="char_sep",
                    help="string to use between each character of each token\n"
                         "defaults to a single space")
parser.add_argument("-w", "--word-sep", "-t", "--token-sep", metavar="SEP",
                    default="   ", dest="token_sep",
                    help="string to use between each token\n"
                         "defaults to three spaces")
parser.add_argument("-1", "--one-token", action="store_true",
                    help="treat input as one token, whitespace included")


def spread_tokens(tokens: list[str], char_sep: str, token_sep: str) -> str:
    return token_sep.join(
        (char_sep.join(char for char in token)
         for token in tokens)
    )


def main() -> None:
    namespace = parser.parse_args()

    strings: list[str] = namespace.strings
    char_sep: str = namespace.char_sep
    token_sep: str = namespace.token_sep
    one_token: bool = namespace.one_token

    if not strings:
        raw_stdin = sys.stdin.read()
        if one_token:
            strings = [raw_stdin]
        else:
            strings = raw_stdin.split()

    result = spread_tokens(strings, char_sep, token_sep)
    print(result)


if __name__ == "__main__":
    main()
