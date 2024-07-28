#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""test_len.py

Unit tester for the len program.
"""

from common import TestBase


class TestLen(TestBase):
    def test_basic(self) -> None:
        result = self.run_command('len "hello there"')
        self.assert_success(result, "11\n")

    def test_count_for_each_token(self) -> None:
        result = self.run_command("len general kenobi you are a bold one")
        self.assert_success(result, "7 6 3 3 1 4 3\n")

    def test_one_per_line(self) -> None:
        result = self.run_command("len -1 -- separate lines please")
        self.assert_success(result, "8\n5\n6\n")

    def test_count_tokens_themselves(self) -> None:
        result = self.run_command("len -t -- there are 5 tokens here")
        self.assert_success(result, "5\n")
