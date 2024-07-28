#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""test_snippet.py

Unit tester for the snippet program.
"""

import json
from pathlib import Path

from common import TestBase


class TestSnippet(TestBase):
    dummy_file: Path
    dummy_file_as_json: list[str]

    @classmethod
    def setUpClass(cls) -> None:
        cls.dummy_file = Path("temp.txt")
        cls.dummy_file.touch(0o600)
        cls.dummy_file.write_text(
            "#!/usr/bin/env ${1:python3}\n"
            "# -*- coding: utf-8 -*-\n"
            '"""${TM_FILENAME}\n'
            "\n"
            "${2:_description_}\n"
            '"""\n'
            "$0",
            encoding="utf-8",
        )

        cls.dummy_file_as_json = [
            "#!/usr/bin/env ${1:python3}",
            "# -*- coding: utf-8 -*-",
            '"""${TM_FILENAME}',
            "",
            "${2:_description_}",
            '"""',
            "$0",
        ]

    @classmethod
    def tearDownClass(cls) -> None:
        cls.dummy_file.unlink(missing_ok=True)

    def test_basic(self) -> None:
        stdout, _, exit_code = self.run_command(
            "snippet",
            stdin="#!/usr/bin/env ${1:python3}\n"
                  "# -*- coding: utf-8 -*-\n"
                  "$0\n",
        )
        received_json = json.loads(stdout)
        expected_json = [
            "#!/usr/bin/env ${1:python3}",
            "# -*- coding: utf-8 -*-",
            "$0",
        ]
        self.assertEqual(exit_code, 0)
        self.assertEqual(received_json, expected_json)

    def test_file_input(self) -> None:
        result = self.run_command(f"snippet {self.dummy_file.name}")

        received_json = json.loads(result.stdout)
        expected_json = self.dummy_file_as_json
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(received_json, expected_json)

    def test_custom_indent(self) -> None:
        result = self.run_command(f"snippet {self.dummy_file.name} --indent 2")

        received_json_string = result.stdout
        expected_json_string = json.dumps(self.dummy_file_as_json, indent=2)

        self.assertEqual(result.exit_code, 0)
        self.assertEqual(
            received_json_string.strip(),
            expected_json_string.strip(),
        )

    def test_include_prefix(self) -> None:
        result = self.run_command(f"snippet {self.dummy_file.name} -p header")

        received_json = json.loads(f"{{{result.stdout}}}")
        expected_json = {
            "prefix": "header",
            "body": self.dummy_file_as_json,
        }
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(received_json, expected_json)
