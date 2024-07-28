#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""test_chr.py

Unit tester for the chr program.
"""

import unittest

from common import TestBase


class TestChr(TestBase):
    def test_basic(self) -> None:
        result = self.run_command("chr 65 66 67")
        self.assert_success(result, "A B C\n")

    def test_echo(self) -> None:
        result = self.run_command("chr -e 0x50 0x52 0x4F")
        self.assert_success(result, "80 82 79\nP  R  O \n")

    def test_delim(self) -> None:
        nums = " ".join(str(num) for num in range(68, 76))
        result = self.run_command(f"chr -d _ {nums}")
        self.assert_success(result, "D_E_F_G_H_I_J_K\n")


if __name__ == "__main__":
    unittest.main()
