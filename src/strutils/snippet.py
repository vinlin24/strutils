#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""snippet

Convert the contents of a text file into a JSON array of strings that
can be pasted into the "body" field of a VS Code snippets file.

USAGE: `cat body.txt | ./snippet`

-OR-

USAGE: `./snippet body.txt`
"""

import json
import sys

__author__ = "Vincent Lin"


def main() -> None:
    try:
        file_path = sys.argv[1]
        source = open(file_path, "rt", encoding="utf-8")
    except IndexError:
        source = sys.stdin

    with source:
        input_lines = source.read().splitlines()

    print("[")
    for line in input_lines:
        escaped = json.dumps(line)
        print(f"  {escaped},")
    print("]")


if __name__ == "__main__":
    main()
