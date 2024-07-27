import functools
import sys
from pathlib import Path
from typing import Final, NoReturn

PROG: Final = Path(sys.argv[0]).name

print_stderr = functools.partial(print, file=sys.stderr)


def log_message(message: str) -> None:
    print(f"{PROG}: {message}")


def log_warning(message: str) -> None:
    print(f"{PROG}: warning: {message}", file=sys.stderr)


def exit_with_error(message: str, *, code: int = 1) -> NoReturn:
    assert code > 0, "error exit code must be a positive integer"
    print(f"{PROG}: error: {message}", file=sys.stderr)
    sys.exit(code)
