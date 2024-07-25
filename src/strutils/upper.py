#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
Apply Python's str.upper() or str.capitalize() on the input words.

EXAMPLES:

    $ upper -n 'hello there'
    HELLO THERE

    $ echo -e " hello\n    there" | upper -t
     Hello
        There

    $ echo 'hello THERE' | upper -tf
    Hello There

    $ echo 'hello-there-general-kenobi' | upper -td '-'
    Hello-There-General-Kenobi

NOTE: If you supply multiple strings as a whitespace-separated list at
the command line, it will be interpreted as the concatenation of the
strings with a single space joining them. Use quoting to preserve
whitespace in your shell script. The determining of WORDs when using
title case is done WITHIN each input STRING. That is, the single token
"hello there" will still be treated as two WORDs.
"""

import argparse
import io
import sys

parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawTextHelpFormatter,
)

parser.add_argument(
    "strings",
    metavar="STRING",
    nargs="*",
    help="strings to convert to uppercase (reads from stdin if omitted)",
)
parser.add_argument(
    "-t", "--title", "--title-case",
    dest="use_title_case",
    action="store_true",
    help="capitalize only the first character of each WORD (defined by DELIM)",
)
parser.add_argument(
    "-f", "--force", "--force-title",
    dest="force_title_case",
    action="store_true",
    help="when using title case, force non-first characters to lowercase "
         "(default is to leave them unmodified)",
)
parser.add_argument(
    "-d", "--delimiter",
    metavar="DELIM",
    dest="delimiter",
    help="string that defines boundaries between WORDs for title case "
         "(default is to delimit by any whitespace)",
)
parser.add_argument(
    "-n", "--newline",
    dest="use_trailing_newline",
    action="store_true",
    help="append a newline to the output",
)


def transform_to_title_case(
    string: str, *,
    delimiter: str | None = None,
    force: bool = False,
) -> str:
    # Specially handle default delimiter (any whitespace) since we would
    # like to preserve the original whitespace. If we just used
    # str.split(), we wouldn't know what to str.join() on.
    if delimiter is None:
        result = io.StringIO()

        # Iterate through the string as a state machine. Note that we
        # treat the start as whitespace state to capture the case of
        # start -> word transition requiring capitalization.
        at_whitespace = True
        for char in string:
            # whitespace | word -> whitespace.
            if char.isspace():
                result.write(char)
                at_whitespace = True
            # whitespace -> word (first character of word).
            elif at_whitespace:
                result.write(char.upper())
                at_whitespace = False
            # word -> word (non-first character of word).
            else:
                result.write(char.lower() if force else char)
                at_whitespace = False

        return result.getvalue()

    # Otherwise, we can just cheese it with str.split() and str.join().
    words = string.split(delimiter)
    if force:
        return delimiter.join(word.capitalize() for word in words)
    return delimiter.join(word[:1].upper() + word[1:] for word in words)


def main() -> None:
    args = parser.parse_args()

    strings: list[str] = args.strings
    use_title_case: bool = args.use_title_case
    force_title_case: bool = args.force_title_case
    delimiter: str | None = args.delimiter
    use_trailing_newline: bool = args.use_trailing_newline

    if not strings:
        strings = [sys.stdin.read()]

    if use_title_case:
        transformed = (
            transform_to_title_case(
                string,
                delimiter=delimiter,
                force=force_title_case,
            ) for string in strings
        )
    else:
        transformed = (string.upper() for string in strings)

    print(*transformed, end=("\n" if use_trailing_newline else ""))


if __name__ == "__main__":
    main()
