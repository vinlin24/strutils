#!/bin/bash
# USAGE: ./test.sh [-v|--verbose] [PROG]

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
program_to_test="${POSITIONAL_ARGS[0]}"

if [ -n "$program_to_test" ]; then
    echo "$self: running only tests for program: $program_to_test"

    # Match only tests whose fully qualified name includes `test_<name>.`, which
    # would be the prefix for tests of the script `test_<name>.py`.
    test_case_pattern="test_${program_to_test}."

    python3 -m unittest discover \
        $verbosity_flag --start-directory "$test_dir" -k "$test_case_pattern"
else
    echo "$self: running ALL tests under $test_dir"
    python3 -m unittest discover \
        $verbosity_flag --start-directory "$test_dir"
fi
