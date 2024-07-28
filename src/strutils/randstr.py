"""Generate strings of random characters of fixed or random length.

There are three `SOURCE`s of characters to make up the final weighted
`ALPHABET` from which the `STRING` is generated:

    1. `LITERALS` supplied to the `-a`/`--alphabet` option.
    2. Text `FILE`s supplied to the `-f`/`--file` option. Binary files
       are currently not supported.
    3. Character class `FLAG`s supplied to the `-c`/`--classes` option.

The resolution from `SOURCE`s to `ALPHABET` is as follows:

    1. Each `SOURCE` resolves to its own weighted `CHARSET`. The command
       line option for each `SOURCE` can also be repeated an arbitrary
       number of times. The characters and their counts from each option
       instance are simply combined before resolving.
    2. The three `CHARSET`s are then combined to create the final
       weighted `ALPHABET`. This means that the counts (weights) of
       shared characters across `CHARSET`s are added.

The final `STRING` is then chosen as a random combination of this
`ALPHABET` (with or without replacement depending on `-u`/`--unique`).

If no `SOURCE` is provided, or they resolve to an empty alphabet, a
default alphabet of all ASCII letters and digits is used. In other
words, providing no `SOURCE` equivalent to providing `--classes AD`.

NOTE: Regarding resolution within each `CHARSET`:

    - All characters within `LITERALS` as well as characters read from
      `FILE`s contribute a count of 1 for their character in the
      `CHARSET`. Repeated characters are weighted accordingly.
    - Character class `FLAG`s are "merged" before creating its
      `CHARSET`. That is, overlapping `FLAG`s will not contribute
      duplicate counts of the represented characters. For example, `AL`
      is equivalent to `A` as `A` is a superset of `L`. It follows that
      repetitions have no effect e.g. `DDD` is equivalent to `D`. In
      other words, the UNION of the flags' character sets are used.

EXAMPLES:

    Generate a string of 42 random characters (followed by a newline,
    for display purposes)::

        $ randstr -n 42
        Cm1xiz2QFmy6jlsuBvH6TIQPQ8zDhz2pWf5BRTVXkP

    Permuting the 10 digit characters using the "digits" character class
    and the "unique" option::

        $ randstr -n 10 -u -c D
        9832607541

    Alphabets are weighted based on the counts of characters provided.
    Note the relative ratio between a, b, c::

        $ randstr -n 15 -a 'abbccc'
        cbbcbbccccbcacb

    Using characters within a text file as the alphabet source::

        $ randstr -n 10 -f Makefile
        -aiOca a_V

    Combining "ASCII uppercase" and "digits" character classes as well
    as the literal "!" character to draw from::

        $ randstr 30 -c UD -a '!'
        C4R1N58V4G!0N52!3ZTWJTWB0BCOIL

    Using range syntax for random length (seed set for determinism)::

        $ randstr 10-20 -s 456789252 | wc -c
        17

    Repeating the same character 30 times::

        $ randstr 30 -na E
        EEEEEEEEEEEEEEEEEEEEEEEEEEEEEE

    Repeating the same character a random number of times::

        $ randstr 5-40 -na E
        EEEEEEEEEEEE

REFERENCE:

    The supported character class `FLAG`s are listed below. They have a
    one-to-one mapping to the constants defined in the Python `string`
    standard library.

        - S : whitespace
        - L : ASCII lowercase
        - U : ASCII uppercase
        - A : ASCII letters (equivalent to L + U)
        - D : digits
        - H : hexadecimal digits
        - O : octal digits
        - P : punctuation
        - * : printable (equivalent to D + A + P + S)
"""

import argparse
import collections
import random
import string
import sys
from pathlib import Path
from typing import Final

from .common import argument_validators
from .common.functional import readonly_struct
from .common.output import exit_with_error, log_warning, print_stderr

FLAG_WHITESPACE: Final = "S"
FLAG_ASCII_LOWERCASE: Final = "L"
FLAG_ASCII_UPPERCASE: Final = "U"
FLAG_ASCII_LETTERS: Final = "A"
FLAG_DIGITS: Final = "D"
FLAG_HEXDIGITS: Final = "H"
FLAG_OCTDIGITS: Final = "O"
FLAG_PUNCTUATION: Final = "P"
FLAG_PRINTABLE: Final = "*"

FLAG_TO_CHARSET: Final = {
    FLAG_WHITESPACE: string.whitespace,
    FLAG_ASCII_LOWERCASE: string.ascii_lowercase,
    FLAG_ASCII_UPPERCASE: string.ascii_uppercase,
    FLAG_ASCII_LETTERS: string.ascii_letters,
    FLAG_DIGITS: string.digits,
    FLAG_HEXDIGITS: string.hexdigits,
    FLAG_OCTDIGITS: string.octdigits,
    FLAG_PUNCTUATION: string.punctuation,
    FLAG_PRINTABLE: string.printable,
}

WeightedAlphabet = collections.Counter


def main() -> None:
    options = parse_options()

    seed_in_use = set_rng_seed(options.rng_seed)
    if options.verbosity_level >= 1:
        print_stderr(f"SEED: {seed_in_use}")

    alphabet = resolve_weighted_alphabet_from_sources(
        literal_charsets=options.alphabet_literals,
        charset_files=options.alphabet_files,
        charset_class_flag_strings=options.alphabet_class_flag_strings,
    )
    if options.verbosity_level >= 2:
        print_stderr(f"ALPHABET: {alphabet}")

    generated_string = generate_random_string(
        length_range=options.string_length_range,
        weighted_alphabet=alphabet,
        unique=options.use_unique_chars,
    )
    print(generated_string, end=("\n" if options.use_trailing_newline else ""))


@readonly_struct
class ProgramOptions:
    string_length_range: range
    alphabet_literals: list[str]
    alphabet_files: list[Path]
    alphabet_class_flag_strings: list[str]
    use_unique_chars: bool
    use_trailing_newline: bool
    rng_seed: int | None
    verbosity_level: int


def parse_options() -> ProgramOptions:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawTextHelpFormatter,
    )

    ##### POSITIONAL #####

    parser.add_argument(
        "string_length_range",
        metavar="NUM_OR_RANGE",
        type=string_length_arg_to_range,
        help="number of characters to generate, or a range in the format "
             "`LO-HI`; all numbers must be non-negative integers",
    )

    ##### ALPHABET SOURCES #####

    parser.add_argument(
        "-a", "--alphabet",
        metavar="LITERALS",
        action="append",
        default=[],
        dest="alphabet_literals",
        help="allowed characters to include in the alphabet; "
             "duplicates are allowed (the count of a character "
             "simply serves as its weight in being chosen)",
    )
    parser.add_argument(
        "-f", "--file",
        metavar="FILE",
        action="append",
        default=[],
        type=argument_validators.valid_regular_file_path,
        dest="alphabet_files",
        help="file containing characters to include in the alphabet; "
             "duplicates are allowed (the count of a character simply "
             "serves as its weight in being chosen)",
    )
    parser.add_argument(
        "-c", "--classes",
        metavar="FLAGS",
        action="append",
        default=[],
        dest="alphabet_class_flag_strings",
        help="string of flags representing character classes to include "
             "in the alphabet; overlapping character classes are merged "
             "so no duplicates are contributed to the final alphabet "
             "(in other words, the union of the character sets is used)",
    )

    ##### RANDOMNESS CONFIGURATION #####

    parser.add_argument(
        "-u", "--unique",
        dest="use_unique_chars",
        action="store_true",
        help="choose without replacement from alphabet "
             "(error if LENGTH is greater than size of alphabet)",
    )
    parser.add_argument(
        "-s", "--seed",
        metavar="SEED",
        dest="rng_seed",
        type=int,
        help="integer seed to use to initialize the random number generator "
             "(useful for reproducing strings)",
    )

    ##### OUTPUT FORMATTING #####

    parser.add_argument(
        "-n", "--newline",
        dest="use_trailing_newline",
        action="store_true",
        help="append a newline to the output",
    )
    parser.add_argument(
        "-v", "--verbose",
        dest="verbosity_level",
        action="count",
        default=0,
        help="dump to STDERR: (verbosity level 1) seed used, in the format "
             "`SEED: <seed>\\n` and (verbosity level 2) resolved weighted "
             "alphabet used, in the format `ALPHABET: <Counter>\\n`, where "
             "<Counter> is the string representation of a Python "
             "collections.Counter instance",
    )

    args = parser.parse_args()
    return ProgramOptions(**vars(args))


def string_length_arg_to_range(value: str) -> range:
    parts = value.split("-")

    # `value` is simply a "NUM".
    if len(parts) == 1:
        num = argument_validators.non_negative_int(value)
        return range(num, num + 1)

    # `value` is of the form "LO-HI".
    if len(parts) == 2:
        lo, hi = parts
        lo_num = argument_validators.non_negative_int(lo)
        hi_num = argument_validators.non_negative_int(hi)
        if lo_num > hi_num:
            raise argparse.ArgumentTypeError(
                "lower bound should be no larger than upper bound when "
                f"using range argument (received {lo_num} > {hi_num})"
            )
        return range(lo_num, hi_num + 1)

    raise argparse.ArgumentTypeError(
        "expected argument either of form `NUM` or `LO-HI` "
        f"(received {value!r})"
    )


def set_rng_seed(seed: int | None) -> int:
    # NOTE: While we could call random.seed(None) to use a seed from the
    # OS, Python currently lacks a way to query the seed, so we should
    # generate the seed ourselves if we want to reference it later. See:
    # https://stackoverflow.com/questions/5012560/how-to-query-seed-used-by-random-random
    if seed is None:
        seed = random.randrange(sys.maxsize)
    random.seed(seed)
    return seed


def resolve_weighted_alphabet_from_sources(
    *,
    literal_charsets: list[str],
    charset_files: list[Path],
    charset_class_flag_strings: list[str],
) -> WeightedAlphabet:
    charset_from_literals = "".join(literal_charsets)

    charset_from_files = "".join(
        file.read_text(encoding="utf-8") for file in charset_files
    )

    charset_from_flags = "".join(
        resolve_class_flags(flag_string)
        for flag_string in charset_class_flag_strings
    )

    concatenated_charsets = (
        charset_from_literals + charset_from_files + charset_from_flags
    )

    # If nothing was supplied manually, default to this alphabet.
    if not concatenated_charsets:
        concatenated_charsets = string.ascii_letters + string.digits

    return WeightedAlphabet(concatenated_charsets)


def resolve_class_flags(flags: str) -> str:
    # Use a set to remove duplicates: "overlapping character classes are
    # merged so no duplicates are contributed to the final alphabet".
    charset_union = set[str]()

    for char in flags:
        try:
            charset = FLAG_TO_CHARSET[char]
            charset_union.update(charset)
        except KeyError:
            log_warning(f"ignoring unknown character class flag {char!r}")

    # Sort to ensure determinism.
    sorted_charset_union = sorted(charset_union)
    return "".join(sorted_charset_union)


def generate_random_string(
    *,
    length_range: range,
    weighted_alphabet: WeightedAlphabet,
    unique: bool,
) -> str:
    random_length = random.randrange(length_range.start, length_range.stop)

    # NOTE: These two sequences are guaranteed to be parallel. See:
    # https://stackoverflow.com/a/835430/14226122
    charset = "".join(weighted_alphabet.keys())
    counts = list(weighted_alphabet.values())

    if unique:
        if random_length > len(charset):
            exit_with_error(
                f"cannot choose {random_length} unique characters from "
                f"alphabet of {len(charset)} unique characters",
            )

        chars = random.sample(charset, k=random_length, counts=counts)
    else:
        chars = random.choices(charset, k=random_length, weights=counts)

    return "".join(chars)


if __name__ == "__main__":
    main()
