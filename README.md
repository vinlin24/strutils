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

Apply Python's chr() on all the input numbers, with support for
different bases, such as hexadecimal, octal, and binary, by inferring
from their respective prefixes (0x, 0o/0, 0b) or with a flag.

EXAMPLES:

    $ chr 65 66 67
    A B C

    $ chr -e 0x50 0x52 0x4F
    80 82 79
    P  R  O

    $ chr -d _ $(seq 68 75)
    D_E_F_G_H_I_J_K

TODO: Improvements to be made. Some options or combination of options do
not yet work as intended.


### spread

Spread out the tokens and characters within a token of an input string.

The tokenization of the input string is as follows:

* If provided as command line arguments, they are treated directly
  as the tokens to use.  This means you should watch out for the
  quoting and whitespace rules of the shell used to invoke this
  script.
* If provided through stdin, the input is tokenized according to the
  rule of Python's str.split() method (unless -1/--one-token is
  provided, which forces the input to be treated as a single
  string).

EXAMPLES:

    $ ./spread hello there
    h e l l o   t h e r e

    $ echo -e 'general\tkenobi' | ./spread --char-sep _ --word-sep ' '
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

    $ ./snippet header.txt --indent 2 --prefix header
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

NOTE: You can pipe the output of this script into a command like clip to
automatically save it to your clipboard.


### mock

Convert an input string into a version with alternating capitalization
as used in sarcastic texting.

EXAMPLES:

    $ mock hello there
    HeLlO tHeRe

    $ mock -c hello there
    HeLlO ThErE

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
