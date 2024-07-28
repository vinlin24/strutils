#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""test_spread.py

Unit tester for the spread program.
"""

from common import TestBase


class TestSpread(TestBase):
    def test_basic(self) -> None:
        result = self.run_command("spread hello there")
        self.assert_success(result, "h e l l o   t h e r e\n")

    def test_with_delimiters(self) -> None:
        result = self.run_command(
            'spread --char-sep _ --word-sep " "',
            stdin="general\tkenobi\n",
        )
        self.assert_success(result, "g_e_n_e_r_a_l k_e_n_o_b_i\n")
