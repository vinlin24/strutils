#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""update_readme.py

Extract the docstring from each script to use in the README entry for
that script.  Intended for use in development.

USAGE: ./update_readme.py
"""

import importlib.util
import re
import sys
from pathlib import Path
from types import ModuleType
from typing import Final

__author__ = "Vincent Lin"

PACKAGE_PATH: Final = Path(__file__).parent / "src" / "strutils"
README_PATH: Final = Path(__file__).parent / "README.md"


def import_script(script_path: Path) -> ModuleType:
    script_stem = script_path.stem
    package_name = PACKAGE_PATH.name
    module_name = f"{package_name}.{script_stem}"

    spec = importlib.util.spec_from_file_location(module_name, script_path)
    assert spec is not None

    module = importlib.util.module_from_spec(spec)
    sys.modules[script_stem] = module
    spec.submodule_search_locations = [str(PACKAGE_PATH)]

    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def write_usage_section(script_name: str, script_usage: str) -> None:
    pattern = rf"## Usage[\s\S]+### {script_name}([\s\S]+?)(?:### .+|$)"
    body = f"\n\n{script_usage.strip()}\n\n\n"
    with README_PATH.open("rt+", encoding="utf-8", newline="\n") as readme:
        content = readme.read()
        match = re.search(pattern, content)
        # Section exists, overwrite it.
        if match is not None:
            start, end = match.span(1)
            updated_content = content[:start] + body + content[end:]

            readme.truncate(0)
            readme.seek(0)
            readme.write(updated_content)
            return

        # Section does not exist, append it.  This assumes that the
        # Usage <h2> is the last section of the README.
        readme.write(f"\n\n### {script_name}")
        readme.write(body)


# A separate I/O because I don't want to think so much.
def ensure_one_trailing_newline() -> None:
    with README_PATH.open("rt+", encoding="utf-8", newline="\n") as readme:
        content = readme.read()
        readme.truncate(0)
        readme.seek(0)
        readme.write(content.rstrip() + "\n")


def main() -> None:
    for file_path in PACKAGE_PATH.iterdir():
        if file_path.name.startswith("_") or file_path.is_dir():
            continue
        module = import_script(file_path)
        # Use instead of `module.__name__` to avoid package prefix.
        script_name = file_path.stem
        script_usage = module.__doc__ or ""
        write_usage_section(script_name, script_usage)
    ensure_one_trailing_newline()


if __name__ == "__main__":
    main()
