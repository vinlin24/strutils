"""
Apply Python's chr() on all input numbers (decoding Unicode code points
to characters).

Different bases are supported:

    - Decimal (base 10, default)
    - Hexadecimal (base 16)
    - Octal (base 8)
    - Binary (base 2)

Non-decimal base systems can be inferred by their respective prefixes
(0x, 0o/0, 0b), or the inputs can be explicitly interpreted with a
chosen base by including the command line flag for it.

EXAMPLES::

    $ chr 65 66 67
    A B C

    $ chr -e 0x50 0x52 0x4F
    80 82 79
    P  R  O

    $ chr -d _ $(seq 68 75)
    D_E_F_G_H_I_J_K
"""

import sys

from .common import parsing
from .common.functional import readonly_struct
from .common.output import exit_with_error, print_stderr


@readonly_struct
class ProgramOptions:
    code_points: list[str]
    echo_requested: bool
    use_literal_spaces: bool
    delimiter: str
    one_per_line: bool
    print_as_is: bool
    use_hexadecimal: bool
    use_octal: bool
    use_binary: bool


# Disable -h to use it for hexadecimal.
parser = parsing.StrUtilsParser(__doc__, __package__, disable_short_help=True)

parser.add_argument(
    "code_points",
    metavar="CODE",
    nargs="*",
    help="numbers to interpret as Unicode codepoints",
)
parser.add_argument(
    "-e", "--echo",
    action="store_true",
    dest="echo_requested",
    help="print the original code points alongside",
)
parser.add_argument(
    "-s", "--literal-spaces",
    action="store_true",
    dest="use_literal_spaces",
    help="print space characters as spaces instead of SPC",
)

sep_group = parser.add_mutually_exclusive_group()

sep_group.add_argument(
    "-d", "--delimiter",
    metavar="DELIM",
    default=" ",
    dest="delimiter",
    help="string to use between each character",
)
sep_group.add_argument(
    "-1",
    action="store_true",
    dest="one_per_line",
    help="print each entry on its own line",
)
sep_group.add_argument(
    "-p", "--print",
    action="store_true",
    dest="print_as_is",
    help="decode and print characters as they are",
)

radix_group = parser.add_mutually_exclusive_group()

radix_group.add_argument(
    "-x", "-h", "--hexadecimal", "--hex",
    action="store_true",
    dest="use_hexadecimal",
    help="interpret code points as hexadecimal",
)
radix_group.add_argument(
    "-o", "--octal", "--oct",
    action="store_true",
    dest="use_octal",
    help="interpret code points as octal",
)
radix_group.add_argument(
    "-b", "--binary", "--bin",
    action="store_true",
    dest="use_binary",
    help="interpret code points as binary",
)


class CodePoint:
    """
    Wrapper class for bundling a raw string with its code point value,
    interpreted using a specific or inferred base.
    """

    def __init__(
        self,
        raw_representation: str,
        base_to_interpret_as: int | None = None,
    ) -> None:
        self.raw = raw_representation
        self.value = self._convert_int_with_possible_radix_prefix(
            raw_representation,
            base=base_to_interpret_as,
        )

    def char(self) -> str:
        """Return the character mapped by this code point value.

        Raises:
            ValueError: chr() failed on the code point value. This
            happens if the value is not in `range(0x110000)`.
        """
        try:
            return chr(self.value)
        # chr() can raise if arg is not in range(0x110000).
        except ValueError as error:
            msg = (
                "could not get the character of code point "
                f"{self.raw!r} (decimal {self.value}): {error}"
            )
            exit_with_error(msg)

    def _convert_int_with_possible_radix_prefix(
        self,
        value: str,
        base: int | None,
    ) -> int:
        """
        Validator for a non-negative integer input, possibly of varying
        radixes as denoted by their conventional prefix. If base is
        provided, interpret value with that base regardless of prefix.
        """
        if value.startswith("-"):
            exit_with_error(f"{value} is negative or not an int.")

        if base is not None:
            value = value.lstrip("0xob")
            return self._cast_int(value, base)

        if value.startswith("0x"):
            return self._cast_int(value, 16)

        # Second condition is to support C-style octal numbers e.g. 0755.
        if value.startswith("0o") or \
                value.startswith("0") and value[1:].isnumeric():
            stripped = value.removeprefix("0").removeprefix("o")
            return self._cast_int(stripped, 8)

        if value.startswith("0b"):
            return self._cast_int(value, 2)

        return self._cast_int(value, 10)

    def _cast_int(self, value: str, base: int) -> int:
        try:
            return int(value, base)
        except ValueError:
            exit_with_error(
                f"{value} could not be interpreted "
                f"as an integer with base {base}.",
            )


def get_codes_from_stdin(*, base: int | None = None) -> list[CodePoint]:
    """Get code point input from stdin."""
    tokens = sys.stdin.read().split()
    return [CodePoint(token, base) for token in tokens]


def escaped(ch: str, literal_spaces: bool) -> str:
    r"""
    Return a string representation that can be safely printed without
    messing up formatting.

    NOTE: len(escaped(ch)) may not necessarily be 1. This is true for
    characters that have an escape sequence representation like \n or
    \x1e.
    """
    safe = repr(ch).strip("'\"")
    if safe == " " and not literal_spaces:
        return "SPC"
    return safe


def print_as_is(codes: list[CodePoint]) -> None:
    """
    Handle the simplest case, where we literally decode all the
    characters and print them side-by-side. This is useful when you're
    decoding a message and just want to see the content as it was
    originally written.
    """
    print("".join(code.char() for code in codes))


def print_one_per_line(codes: list[CodePoint]) -> None:
    """Handle the case where each result goes on a separate line."""
    for code in codes:
        print(code.char())


def echo_one_per_line(codes: list[CodePoint]) -> None:
    """
    Handle the case where each result goes on a separate line, with the
    original string encoding echoed beside the decoded values."""
    max_width = max(len(code.raw) for code in codes)
    width = max(len(str(code.value)) for code in codes)

    for code in codes:
        echo_column = code.raw.ljust(max_width)
        decoded_column = code.char().ljust(width)
        print(f"{echo_column} {decoded_column}")


def print_horizontally(
    codes: list[CodePoint],
    *,
    echo: bool,
    delimiter: str,
    use_literal_spaces: bool,
) -> None:
    """
    Handle the ordinary case where we decode the code point strings and
    display them side by side. If `echo` is requested, two lines are
    printed instead:

        1. The decimal value of the provided code point strings.
        2. The actual decoded values.

    The lines will be lined up and spaced evenly according to the max
    length needed per entry.
    """
    max_width = 0
    if echo:
        max_width = max(len(str(code.value)) for code in codes)

    # If echoed, the first line is the echo line. The decoded values are
    # on the line below.
    if echo:
        echo_line = delimiter.join(
            str(code.value).ljust(max_width)
            for code in codes
        )
        print(echo_line)

    def format_char(code: CodePoint) -> str:
        padded_char = code.char().ljust(max_width)
        escaped_char = escaped(padded_char, use_literal_spaces)
        return escaped_char

    decoded_line = delimiter.join(format_char(code) for code in codes)
    print(decoded_line)


def main() -> None:
    """Main driver function."""
    args = parser.parse_args()
    options = ProgramOptions(**vars(args))

    if options.use_hexadecimal:
        base = 16
    elif options.use_octal:
        base = 8
    elif options.use_binary:
        base = 2
    else:
        base = None

    codes = [CodePoint(encoded, base) for encoded in options.code_points]
    if not codes:
        codes = get_codes_from_stdin(base=base)

    # Ignore echo, doesn't make sense to use it with --print.
    if options.echo_requested and options.print_as_is:
        print_stderr("WARNING: Ignoring --echo since --print was used.")

    if options.print_as_is:
        print_as_is(codes)
        return

    if options.one_per_line:
        if options.echo_requested:
            echo_one_per_line(codes)
        else:
            print_one_per_line(codes)
        return

    print_horizontally(
        codes,
        echo=options.echo_requested,
        delimiter=options.delimiter,
        use_literal_spaces=options.use_literal_spaces
    )


if __name__ == "__main__":
    main()
