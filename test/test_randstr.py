#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""test_randstr.py

Unit tester for the randstr program.
"""

from common import TestBase


class TestRandstr(TestBase):
    SEED = 69

    def test_basic(self) -> None:
        result = self.run_command(f"randstr 42 -s {self.SEED}")
        self.assert_success(
            result,
            "fkLu4W1zZJZtHBzyzjitROUSYgyMe2SxcfbppjDXRN",
        )

    def test_permuting_digits(self) -> None:
        result = self.run_command(f"randstr 10 -u -c D -s {self.SEED}")
        self.assert_success(result, "1294853760")

    def test_weighted_alphabet(self) -> None:
        result = self.run_command(f"randstr 15 -a abbccc -s {self.SEED}")
        self.assert_success(result, "abcbcccbcccbcbb")

    def test_file_source(self) -> None:
        with self.temporary_file() as file:
            file.write(
                "Lorem ipsum dolor sit amet, consectetur adipiscing elit, "
                "sed do eiusmod tempor incididunt ut labore et dolore magna "
                "aliqua. Ut enim ad minim veniam, quis nostrud exercitation "
                "ullamco laboris nisi ut aliquip ex ea commodo consequat. "
                "Duis aute irure dolor in reprehenderit in voluptate velit "
                "esse cillum dolore eu fugiat nulla pariatur. Excepteur sint "
                "occaecat cupidatat non proident, sunt in culpa qui officia "
                "deserunt mollit anim id est laborum.",
            )
            file.flush()

            result = self.run_command(
                f"randstr 10 -f {file.name} -s {self.SEED}"
            )

        self.assert_success(result, "reu naciau")

    def test_multiple_source_types(self) -> None:
        result = self.run_command(f'randstr 40 -c UD -a "?!" -s {self.SEED}')
        self.assert_success(result, "14KAWRUDTJTAIEDCD339ONQPT1CL0VPC!1!773GS")

    def test_length_range_syntax(self) -> None:
        result = self.run_command(f"randstr 10-40 -s {self.SEED}")
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(len(result.stdout), 31)

    def test_repeating_same_character(self) -> None:
        result = self.run_command("randstr 30 -a E")
        self.assert_success(result, "E" * 30)
