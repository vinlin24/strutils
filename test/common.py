"""common.py

Code to share among tests.
"""

import subprocess
import unittest
from typing import NamedTuple


class ProcessResult(NamedTuple):
    stdout: str
    stderr: str
    exit_code: int


class TestBase(unittest.TestCase):
    def run_command(
        self,
        script: str,
        *,
        stdin: str | None = None,
    ) -> ProcessResult:
        process = subprocess.run(
            script,
            shell=True,
            capture_output=True,
            input=stdin,
            text=True,
            check=False,
        )
        return ProcessResult(process.stdout, process.stderr, process.returncode)

    def assert_success(
        self,
        process_result: ProcessResult,
        expected_stdout: str,
        *,
        stderr_ok: bool = False,
    ) -> None:
        stdout, stderr, exit_code = process_result
        self.assertEqual(exit_code, 0)
        self.assertEqual(stdout, expected_stdout)
        if not stderr_ok:
            self.assertEqual(stderr, "")
