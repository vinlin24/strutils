"""common.py

Code to share among tests.
"""

import contextlib
import re
import subprocess
import unittest
from io import TextIOWrapper
from pathlib import Path
from typing import Generator, Mapping, NamedTuple


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
        environment: Mapping[str, str] | None = None,
    ) -> ProcessResult:
        process = subprocess.run(
            script,
            shell=True,
            capture_output=True,
            input=stdin,
            text=True,
            env=environment,
            check=False,
        )
        return ProcessResult(
            process.stdout,
            process.stderr,
            process.returncode,
        )

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

    def assert_immediate_exit_with_error_message(
        self,
        process_result: ProcessResult,
        regex: re.Pattern | str | None = None,
    ) -> None:
        stdout, stderr, exit_code = process_result
        self.assertNotEqual(exit_code, 0)
        if regex is None:
            self.assertNotEqual(stderr, "")
        else:
            self.assertRegex(stderr, regex)
        self.assertEqual(stdout, "")

    @contextlib.contextmanager
    def temporary_file(self) -> Generator[TextIOWrapper, None, None]:
        path = Path("temporary_file")
        path.touch(0o600, exist_ok=True)
        file = path.open("rt+", encoding="utf-8")
        try:
            yield file
        finally:
            file.close()
            path.unlink(missing_ok=True)
