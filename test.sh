#!/bin/bash
# USAGE: ./test.sh [-v|--verbose] [PATTERN]

self="$(basename "$0")"
script_dir="$(dirname "$0")"
test_dir="${script_dir}/test"

POSITIONAL_ARGS=()
VERBOSE=0

while [ $# -gt 0 ]; do
    case $1 in
    -v | --verbose)
        VERBOSE=1
        shift
        ;;
    *)
        POSITIONAL_ARGS+=("$1")
        shift
        ;;
    esac
done

verbosity_flag=''
if [ $VERBOSE -eq 1 ]; then
    verbosity_flag=--verbose
fi
pattern="${POSITIONAL_ARGS[0]}"

if [ -n "$pattern" ]; then
    echo "$self: running only tests whose name contains: $pattern"
    python3 -m unittest discover \
        $verbosity_flag --start-directory "$test_dir" -k "$pattern"
else
    echo "$self: running ALL tests under $test_dir"
    python3 -m unittest discover \
        $verbosity_flag --start-directory "$test_dir"
fi
