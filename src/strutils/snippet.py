#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Convert the contents of a text stream into a JSON array of strings that
can be pasted into the "body" field of a VS Code snippets file.

EXAMPLES:

    $ cat body.txt | snippet
    $ ./snippet body.txt
"""

import json
import sys
from argparse import ArgumentParser, RawTextHelpFormatter
from pathlib import Path

__author__ = "Vincent Lin"

parser = ArgumentParser(prog=Path(sys.argv[0]).name,
                        description=__doc__,
                        formatter_class=RawTextHelpFormatter)
parser.add_argument("file_path", metavar="FILE", nargs="?", type=Path,
                    help="file with raw snippet; read from stdin if omitted")


def main() -> None:
    namespace = parser.parse_args()
    file_path: Path | None = namespace.file_path

    if file_path is None:
        source = sys.stdin
    else:
        source = file_path.open("rt", encoding="utf-8")

    with source:
        input_lines = source.read().splitlines()

    print("[")
    for line in input_lines:
        escaped = json.dumps(line)
        print(f"  {escaped},")
    print("]")


if __name__ == "__main__":
    main()
