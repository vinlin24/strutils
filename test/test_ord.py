#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""test_ord.py

Unit tester for the ord program.
"""

from common import TestBase


# pylint: disable=too-many-public-methods
class TestOrd(TestBase):
    def test_decimal(self) -> None:
        result = self.run_command("ord \"hello there\"")
        self.assert_success(
            result,
            "104 101 108 108 111 032 116 104 101 114 101\n",
        )

    def test_concatenate_tokens(self) -> None:
        result = self.run_command("ord hello there")
        self.assert_success(
            result,
            "104 101 108 108 111 116 104 101 114 101\n",
            #                   ^ Note the missing space.
        )

    def test_stdin(self) -> None:
        result = self.run_command("ord", stdin="hello there")
        self.assert_success(
            result,
            "104 101 108 108 111 032 116 104 101 114 101\n",
        )

    def test_no_strings_received(self) -> None:
        result = self.run_command("ord", stdin="")
        self.assert_immediate_exit_with_error_message(result)

    def test_mutually_exclusive_radix_option(self) -> None:
        result = self.run_command("ord -x -o -b hello")
        self.assert_immediate_exit_with_error_message(result)

    def test_hexadecimal(self) -> None:
        result = self.run_command("ord -x \"hello there\"")
        self.assert_success(result, "68 65 6c 6c 6f 20 74 68 65 72 65\n")

    def test_hexadecimal_uppercase(self) -> None:
        result = self.run_command("ord -xu \"hello there\"")
        self.assert_success(result, "68 65 6C 6C 6F 20 74 68 65 72 65\n")

    def test_hexadecimal_uppercase_shorthand(self) -> None:
        result = self.run_command("ord -X \"hello there\"")
        self.assert_success(result, "68 65 6C 6C 6F 20 74 68 65 72 65\n")

    def test_octal(self) -> None:
        result = self.run_command("ord -o \"hello there\"")
        self.assert_success(
            result,
            "150 145 154 154 157 040 164 150 145 162 145\n",
        )

    def test_octal_c_style_without_prefix(self) -> None:
        result = self.run_command("ord -0 \"hello there\"")
        self.assert_success(
            result,
            "150 145 154 154 157 040 164 150 145 162 145\n",
        )

    def test_binary(self) -> None:
        result = self.run_command("ord -b \"hello there\"")
        self.assert_success(
            result,
            "1101000 1100101 1101100 1101100 1101111 0100000 "
            "1110100 1101000 1100101 1110010 1100101\n",
        )

    def test_decimal_prefixed_has_no_effect(self) -> None:
        result = self.run_command("ord -p \"hello there\"")
        self.assert_success(
            result,
            "104 101 108 108 111 032 116 104 101 114 101\n",
        )

    def test_hexadecimal_prefixed(self) -> None:
        result = self.run_command("ord -xp \"hello there\"")
        self.assert_success(
            result,
            "0x68 0x65 0x6c 0x6c 0x6f 0x20 0x74 0x68 0x65 0x72 0x65\n",
        )

    def test_octal_prefixed(self) -> None:
        result = self.run_command("ord -op \"hello there\"")
        self.assert_success(
            result,
            "0o150 0o145 0o154 0o154 0o157 0o040 "
            "0o164 0o150 0o145 0o162 0o145\n",
        )

    def test_octal_prefixed_c_style(self) -> None:
        result = self.run_command("ord -0p \"hello there\"")
        self.assert_success(
            result,
            "0150 0145 0154 0154 0157 0040 "
            "0164 0150 0145 0162 0145\n",
        )

    def test_binary_prefixed(self) -> None:
        result = self.run_command("ord -bp \"hello there\"")
        self.assert_success(
            result,
            "0b1101000 0b1100101 0b1101100 0b1101100 0b1101111 0b0100000 "
            "0b1110100 0b1101000 0b1100101 0b1110010 0b1100101\n",
        )

    def test_echo(self) -> None:
        result = self.run_command("ord -e hello")
        self.assert_success(
            result,
            "h   e   l   l   o  \n"
            "104 101 108 108 111\n",
        )

    def test_echo_with_space(self) -> None:
        result = self.run_command("ord -e \"hello there\"")
        self.assert_success(
            result,
            "h   e   l   l   o   SPC t   h   e   r   e  \n"
            "104 101 108 108 111 032 116 104 101 114 101\n",
        )

    def test_echo_with_newlines(self) -> None:
        result = self.run_command("ord -e", stdin="hello\nthere\n")
        self.assert_success(
            result,
            "h   e   l   l   o   \\n  t   h   e   r   e   \\n \n"
            "104 101 108 108 111 010 116 104 101 114 101 010\n",
        )

    def test_mutually_exclusive_separation_option(self) -> None:
        result = self.run_command("ord -d, -t hello")
        self.assert_immediate_exit_with_error_message(result)

    def test_delimiter(self) -> None:
        result = self.run_command("ord -d, hello")
        self.assert_success(result, "104,101,108,108,111\n")

    def test_tabs(self) -> None:
        result = self.run_command("ord -t hello")
        self.assert_success(result, "104\t101\t108\t108\t111\n")

    def test_one_per_line(self) -> None:
        result = self.run_command("ord lmao -1")
        self.assert_success(result, "108\n109\n097\n111\n")

    def test_echo_one_per_line(self) -> None:
        result = self.run_command("ord -e1 hello")
        self.assert_success(
            result,
            "h 104\n"
            "e 101\n"
            "l 108\n"
            "l 108\n"
            "o 111\n",
        )
