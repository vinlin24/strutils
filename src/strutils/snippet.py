#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
Convert the contents of a text stream into a JSON array of strings that
can be pasted into the "body" field of a VS Code snippets file.

EXAMPLES:

    $ snippet
    #!/usr/bin/env ${1:python3}
    # -*- coding: utf-8 -*-
    $0
    ^D
    [
        "#!/usr/bin/env ${1:python3}",
        "# -*- coding: utf-8 -*-",
        "$0"
    ]

    $ snippet header.txt --indent 2 --prefix header
    "prefix": "header",
    "body": [
      "#!/usr/bin/env ${1:python3}",
      "# -*- coding: utf-8 -*-",
      "\"\"\"${TM_FILENAME}",
      "",
      "${2:_description_}",
      "\"\"\"",
      "$0"
    ]

TIP: You can pipe the output of this script into a command like clip to
automatically save it to your clipboard.
"""

import io
import json
import sys
from argparse import ArgumentParser, ArgumentTypeError, RawTextHelpFormatter
from pathlib import Path

__author__ = "Vincent Lin"


def valid_num_spaces_indent(value: str) -> int:
    as_int = int(value)
    valid_range = range(0, 17)
    if as_int not in valid_range:
        raise ArgumentTypeError(f"{value} is not in {valid_range}.")
    return as_int


parser = ArgumentParser(prog=Path(sys.argv[0]).name,
                        description=__doc__,
                        formatter_class=RawTextHelpFormatter)
parser.add_argument("file_path", metavar="FILE", nargs="?", type=Path,
                    help="file with raw snippet; read from stdin if omitted")
parser.add_argument("-c", "--trailing-comma", action="store_true",
                    help="end the last entry in the list with a comma")
parser.add_argument("-p", "--prefix", metavar="PREFIX",
                    help="if provided, include prefix of snippet in output")
indentation_group = parser.add_mutually_exclusive_group()
indentation_group.add_argument("-i", "--indent", type=valid_num_spaces_indent,
                               help="number of spaces to use as indentation")
indentation_group.add_argument("-t", "--tabs", action="store_true",
                               help="use tabs for indentation")


def get_body_array(input_lines: list[str],
                   indentation: str,
                   trailing_comma: bool
                   ) -> str:
    num_lines = len(input_lines)

    output = io.StringIO()
    output.write("[\n")
    for line_num, line in enumerate(input_lines, start=1):
        escaped = json.dumps(line)
        output.write(indentation)
        output.write(escaped)
        if line_num < num_lines or trailing_comma:
            output.write(",")
        output.write("\n")
    output.write("]")

    return output.getvalue()


def main() -> None:
    namespace = parser.parse_args()

    file_path: Path | None = namespace.file_path
    trailing_comma: bool = namespace.trailing_comma
    prefix: str | None = namespace.prefix
    indent: int | None = namespace.indent
    tabs: bool = namespace.tabs

    if tabs:
        indentation = "\t"
    elif indent is not None:
        indentation = " " * indent
    # Default to 4 spaces if no indentation strategy provided.
    else:
        indentation = " " * 4

    if file_path is None:
        source = sys.stdin
    else:
        source = file_path.open("rt", encoding="utf-8")

    with source:
        input_lines = source.read().splitlines()

    body_array = get_body_array(input_lines, indentation, trailing_comma)

    if prefix is None:
        print(body_array)
        return

    prefix_part = f"\"prefix\": {json.dumps(prefix)}"
    output = f"{prefix_part},\n\"body\": {body_array}"
    print(output)


if __name__ == "__main__":
    main()
