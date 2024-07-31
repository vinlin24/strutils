import argparse
from pathlib import Path

from .. import __author__, __version__


class StrUtilsParser(argparse.ArgumentParser):
    def __init__(
        self,
        description: str,
        *,
        disable_short_help: bool = False,
    ) -> None:
        super().__init__(
            description=description,
            formatter_class=argparse.RawTextHelpFormatter,
            epilog=f"{__package__} {__version__} by {__author__}.",
            add_help=not disable_short_help,
        )

        # Re-add the long version.
        if disable_short_help:
            self.add_argument(
                "--help",
                action="help",
                default=argparse.SUPPRESS,
                help="show this message and exit",
            )


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
