# strutils

Unix-like interfaces to Python string manipulation utilities.

Many of these scripts were originally developed on my
[startup-config](https://github.com/vinlin24/startup-config) repository as part
of scripts to be included in my custom `$HOME/bin` `PATH` directory. They have
been moved to their own repository to separate concerns. Furthermore, Python's
[setuptools](https://setuptools.pypa.io/en/latest/setuptools.html) provides a
convenient way to install command line scripts.


## Setup

**REQUIREMENT:** Python 3.10+

The scripts are mostly standalone but are bundled as a Python package to make
distribution and installation more convenient. To install it globally on your
machine:

```sh
git clone https://github.com/vinlin24/strutils.git
make install
```

This adds the scripts to your `PATH` such that you can use them like ordinary
shell commands.

You can sync the scripts with upstream changes by pulling and installing again:

```sh
cd /path/to/strutils
git pull origin main
make install
```


## Development

After fresh clones, run this rule to set up Git hooks:

```sh
make hooks
```

You can install the project globally in [**editable**
mode](https://setuptools.pypa.io/en/latest/userguide/development_mode.html) such
that the scripts are a "live" copy. This makes it easier to develop and see the
changes take effect immediately:

```sh
make editable
```

To run unit tests for all scripts:

```sh
make test-all
# OR:
./test.sh
```

To run unit tests only for a program(s) e.g. `len`, `chr`:

```sh
./test.sh len
./test.sh len chr
```

To run unit tests only for the programs that have been modified since the last
commit:

```sh
make test
# OR:
./test.sh --lazy
```

[test.sh](test.sh) has been outfitted with a CLI. To see usage:

```sh
./test.sh --help
```


## Usage


### ord

Apply Python's ord() on all the characters within the input string, with
support for different bases, such as hexadecimal, octal, and binary, as
well as the option of including their respective prefixes (0x, 0o, 0b).

EXAMPLES:

    $ ord -x "hello there"
    68 65 6c 6c 6f 20 74 68 65 72 65

    $ echo -e "hello\nthere" | ord -ep
    h   e   l   l   o   \n  t   h   e   r   e   \n
    104 101 108 108 111 010 116 104 101 114 101 010

    $ ord lmao -1 | awk 'BEGIN {s=0} {s += $1} END {print s}'
    425

NOTE: If you supply multiple strings as a whitespace-separated list at
the command line, it will be interpreted as the concatenation of the
strings with no whitespace joining them. Use quoting to preserve
whitespace in your shell script.


### chr

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


### spread

Spread out the tokens and characters within a token of an input string.

The tokenization of the input string is as follows:

    - If provided as command line arguments, they are treated directly
      as the tokens to use. This means you should watch out for the
      quoting and whitespace rules of the shell used to invoke this
      script.
    - If provided through stdin, the input is tokenized according to the
      rule of Python's str.split() method (unless -1/--one-token is
      provided, which forces the input to be treated as a single
      string).

EXAMPLES:

    $ spread hello there
    h e l l o   t h e r e

    $ echo -e 'general\tkenobi' | spread --char-sep _ --word-sep ' '
    g_e_n_e_r_a_l k_e_n_o_b_i


### snippet

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


### mock

Convert an input string into a version with alternating capitalization
as used in sarcastic texting.

EXAMPLES:

    $ mock hello there
    hElLo ThErE

    $ mock -c hello there
    HeLlO tHeRe

    $ echo -e 'hello\tthere\ngeneral\tkenobi' | mock
    hElLo   ThErE
    gEnErAl KeNoBi

NOTE: If multiple strings are provided as separate command line
arguments, they will be subject to the shell parsing rules.  The script
has no way of knowing the whitespace originally used to separate the
arguments, so it will assume to join them with single spaces.  To
preserve whitespace, use quoting.


### len

Compute the length of each string. For most purposes, just saves a few
keystrokes from the more versatile `echo -n "$string" | wc` pattern, but
also serves as a way to apply the counting on EACH input token.

EXAMPLES:

    $ len "hello there"
    11

    $ len general kenobi you are a bold one
    7 6 3 3 1 4 3

    $ len -1 -- separate lines please
    8
    5
    6

    $ len -t -- there are 5 tokens here
    5

NOTE: "Tokens" are determined by how the shell running this script
parses the input at the command line. If you intend a string with
whitespace to be parsed as one token, be sure to follow your shell's
quoting rules. Reading from stdin always treats the string as one token.


### upper

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


### lower

Apply Python's str.lower() on the input strings.

EXAMPLES:

    $ lower -n 'HELLO THERE'
    hello there

    $ echo -e " HELLO\n    thERe" | lower
     hello
         there

NOTE: If you supply multiple strings as a whitespace-separated list at
the command line, it will be interpreted as the concatenation of the
strings with a single space joining them. Use quoting to preserve
whitespace in your shell script.


### randstr

Generate strings of random characters of fixed or random length.

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
