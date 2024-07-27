import argparse
from pathlib import Path


def non_negative_int(value: str) -> int:
    try:
        num = int(value)
        if num < 0:
            raise ValueError
        return num
    except ValueError:
        raise argparse.ArgumentTypeError(
            f"expected non-negative integer, received {value!r}",
        ) from None


def valid_regular_file_path(value: str) -> Path:
    path = Path(value)
    if not path.exists():
        raise argparse.ArgumentTypeError(f"{path} does not exist")
    if not path.is_file():
        raise argparse.ArgumentTypeError(f"{path} is not a regular file")
    return path.resolve()
