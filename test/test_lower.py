#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""test_lower.py

Unit tester for the lower program.
"""

from common import TestBase


class TestLower(TestBase):
    def test_basic(self) -> None:
        result = self.run_command('lower -n "HELLO THERE"')
        self.assert_success(result, "hello there\n")

    def test_whitespace_handling(self) -> None:
        result = self.run_command("lower", stdin=" HELLO\n    thERe\n")
        self.assert_success(result, " hello\n    there\n")
