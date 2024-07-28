#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""test_upper.py

Unit tester for the upper command.
"""

from common import TestBase


class TestUpper(TestBase):
    def test_basic(self) -> None:
        result = self.run_command('upper -n "hello there"')
        self.assert_success(result, "HELLO THERE\n")

    def test_title_case(self) -> None:
        result = self.run_command("upper -t", stdin=" hello\n    there\n")
        self.assert_success(result, " Hello\n    There\n")

    def test_force_title_case(self) -> None:
        result = self.run_command("upper -tf", stdin="hello THERE\n")
        self.assert_success(result, "Hello There\n")

    def test_title_case_with_delimiter(self) -> None:
        result = self.run_command(
            'upper -td "-"',
            stdin="hello-there-general-kenobi\n",
        )
        self.assert_success(result, "Hello-There-General-Kenobi\n")
