#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""test_ord.py

Unit tester for the ord program.
"""

from common import TestBase


class TestOrd(TestBase):
    def test_basic(self) -> None:
        result = self.run_command("ord -x \"hello there\"")
        self.assert_success(result, "68 65 6c 6c 6f 20 74 68 65 72 65\n")

    def test_echo(self) -> None:
        result = self.run_command("ord -ep", stdin="hello\nthere\n")
        self.assert_success(
            result,
            "h   e   l   l   o   \\n  t   h   e   r   e   \\n \n"
            "104 101 108 108 111 010 116 104 101 114 101 010\n",
        )

    def test_one_per_line(self) -> None:
        result = self.run_command("ord lmao -1")
        self.assert_success(result, "108\n109\n097\n111\n")
