#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""test_chr.py

Unit tester for the chr program.
"""

import re

from common import TestBase


# pylint: disable=too-many-public-methods
class TestChr(TestBase):
    def test_no_options(self) -> None:
        result = self.run_command("chr 65 66 67")
        self.assert_success(result, "A B C\n")

    def test_echo(self) -> None:
        result = self.run_command("chr -e 65 66 67")
        self.assert_success(result, "65 66 67\nA  B  C \n")

    def test_read_from_stdin(self) -> None:
        result = self.run_command("chr", stdin="65 66 67")
        self.assert_success(result, "A B C\n")

    def test_literal_spaces(self) -> None:
        result = self.run_command("chr -s 76 32 82")
        self.assert_success(result, "L   R\n")

    def test_mutually_exclusive_separation_options(self) -> None:
        result = self.run_command("chr -d _ -1 65 66 67")
        self.assert_immediate_exit_with_error_message(result)

    def test_delimiter(self) -> None:
        nums = " ".join(str(num) for num in range(68, 76))
        result = self.run_command(f"chr -d _ {nums}")
        self.assert_success(result, "D_E_F_G_H_I_J_K\n")

    def test_one_per_line(self) -> None:
        result = self.run_command("chr -1 65 66 67")
        self.assert_success(result, "A\nB\nC\n")

    def test_print_as_is(self) -> None:
        result = self.run_command("chr -p 65 66 67")
        self.assert_success(result, "ABC\n")

    def test_mutually_exclusive_radix_option(self) -> None:
        result = self.run_command("chr -x -o -b 65 66 67")
        self.assert_immediate_exit_with_error_message(result)

    def test_interpret_as_hexadecimal(self) -> None:
        result = self.run_command("chr -x 65 66 67")
        self.assert_success(result, "e f g\n")

    def test_interpret_as_octal(self) -> None:
        result = self.run_command("chr -o 65 66 67")
        self.assert_success(result, "5 6 7\n")

    def test_interpret_as_binary(self) -> None:
        result = self.run_command("chr -b 1110011 1100110 1101110")
        self.assert_success(result, "s f n\n")

    def test_infer_hexadecimal(self) -> None:
        result = self.run_command("chr 0x50 0x52 0x4F")
        self.assert_success(result, "P R O\n")

    def test_infer_octal_python_style(self) -> None:
        result = self.run_command("chr 0o107 0o115 0o103")
        self.assert_success(result, "G M C\n")

    def test_infer_octal_c_style(self) -> None:
        result = self.run_command("chr 0107 0115 0103")
        self.assert_success(result, "G M C\n")

    def test_infer_binary(self) -> None:
        result = self.run_command("chr 0b1110011 0b1100110 0b1101110")
        self.assert_success(result, "s f n\n")

    def test_mixed_inference(self) -> None:
        result = self.run_command("chr 0x52 0b1101110 65 0107 0o103")
        self.assert_success(result, "R n A G C\n")

    def test_print_overrides_echo(self) -> None:
        result = self.run_command("chr -ep 65 66 67")
        self.assert_success(result, "ABC\n", stderr_ok=True)
        self.assertRegex(result.stderr, re.compile(r"warning:", re.IGNORECASE))

    def test_echo_converts_code_points_to_decimal(self) -> None:
        result = self.run_command("chr -xe 65 66 67")
        self.assert_success(result, "101 102 103\ne   f   g  \n")

    def test_reject_negative_code_point(self) -> None:
        result = self.run_command("chr -- 65 66 -67")
        self.assert_immediate_exit_with_error_message(
            result,
            re.compile(r"error: -67", re.IGNORECASE),
        )

    def test_invalid_decimal_code_point(self) -> None:
        result = self.run_command("chr 65 66 6A")
        self.assert_immediate_exit_with_error_message(
            result,
            re.compile(r"error: 6A", re.IGNORECASE),
        )

    def test_invalid_hexadecimal_code_point(self) -> None:
        result = self.run_command("chr -x 6A 6F 6G")
        self.assert_immediate_exit_with_error_message(
            result,
            re.compile(r"error: 6G", re.IGNORECASE),
        )

    def test_invalid_octal_code_point(self) -> None:
        result = self.run_command("chr -o 65 66 68")
        self.assert_immediate_exit_with_error_message(
            result,
            re.compile(r"error: 68", re.IGNORECASE),
        )

    def test_invalid_binary_code_point(self) -> None:
        result = self.run_command("chr -b 1110011 1100110 1102110")
        self.assert_immediate_exit_with_error_message(
            result,
            re.compile(r"error: 1102110", re.IGNORECASE),
        )
