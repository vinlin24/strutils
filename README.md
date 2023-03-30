# strutils

Unix-like interfaces to Python string manipulation utilities.

Many of these scripts were originally developed on my
[startup-config](https://github.com/vinlin24/startup-config) repository as part
of scripts to be included in my custom `$HOME/bin` `PATH` directory. They have
been moved to their own repository to separate concerns. Furthermore, Python's
[setuptools](https://setuptools.pypa.io/en/latest/setuptools.html) provides a
convenient way to install command line scripts.


## Setup

The scripts are mostly standalone but are bundled as a Python package to make
distribution and installation more convenient. To install it globally on your
machine:

```sh
git clone https://github.com/vinlin24/strutils.git
pip install ./strutils
```

The installation process adds the scripts to your `PATH` such that you can use
them like ordinary shell commands.


## Usage


### ord

Apply Python's ord() on all the characters within the input string, with
support for different bases, such as hexadecimal, octal, and binary, as
well as the option of including their respective prefixes (0x, 0o, 0b).

EXAMPLES:

    $ ord -x "hello there"
    68 65 6c 6c 6f 20 74 68 65 72 65

    $ echo -e "hello\nthere\n" | ord -ep
    h   e   l   l   o   \n  t   h   e   r   e   \n  \n
    104 101 108 108 111 010 116 104 101 114 101 010 010

    $ ord lmao -1 | awk 'BEGIN {s=0} {s += $1} END {print s}'
    425

NOTE: If you supply multiple strings as a whitespace-separated list at
the command line, it will be interpreted as the concatenation of the
strings with no whitespace joining them. Use quoting to preserve
whitespace in your shell script.


### chr

Apply Python's chr() on all the input numbers, with support for
different bases, such as hexadecimal, octal, and binary, through the use
of their respective prefixes (0x, 0o/0, 0b).

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

    $ cat body.txt | snippet
    $ ./snippet body.txt --indent 2
