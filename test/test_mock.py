#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""test_mock.py

Unit tester for the mock program.
"""

from common import TestBase


class TestMock(TestBase):
    def test_basic(self) -> None:
        result = self.run_command("mock hello there")
        self.assert_success(result, "hElLo ThErE\n")

    def test_inverted(self) -> None:
        result = self.run_command("mock -c hello there")
        self.assert_success(result, "HeLlO tHeRe\n")

    def test_whitespace_handling(self) -> None:
        result = self.run_command(
            "mock",
            stdin="hello\tthere\ngeneral\tkenobi\n",
        )
        self.assert_success(result, "hElLo\tThErE\ngEnErAl\tKeNoBi\n")
