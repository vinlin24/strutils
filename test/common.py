"""common.py

Code to share among tests.
"""

import subprocess


def get_output(script: str) -> str:
    stdout = subprocess.check_output(script, shell=True)
    as_str = stdout.decode()
    normalized = as_str.replace("\r\n", "\n")
    return normalized
