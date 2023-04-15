#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""test_chr.py

Unit tester for the chr program.
"""

import unittest

from common import get_output


class TestChr(unittest.TestCase):
    def test_basic(self) -> None:
        output = get_output("chr 65 66 67")
        self.assertEqual(output, "A B C\n")

    def test_echo(self) -> None:
        output = get_output("chr -e 0x50 0x52 0x4F")
        self.assertEqual(output, "80 82 79\nP  R  O \n")

    def test_delim(self) -> None:
        nums = " ".join(str(num) for num in range(68, 76))
        output = get_output(f"chr -d _ {nums}")
        self.assertEqual(output, "D_E_F_G_H_I_J_K\n")


if __name__ == "__main__":
    unittest.main()
