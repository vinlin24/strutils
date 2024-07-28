#!/bin/bash
# USAGE: ./test.sh [PATTERN]

self="$(basename $0)"
script_dir="$(dirname "$0")"
test_dir="${script_dir}/test"
pattern="$1"

if [ -n "$pattern" ]; then
    echo "$self: running only tests whose name contains: $pattern"
    python3 -m unittest discover --start-directory "$test_dir" -k "$pattern"
else
    echo "$self: running ALL tests under $test_dir"
    python3 -m unittest discover --start-directory "$test_dir"
fi
