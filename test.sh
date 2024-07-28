#!/bin/bash
# USAGE: ./test.sh [-v|--verbose] [PROG1] [PROG2] ...

self="$(basename "$0")"
script_dir="$(dirname "$0")"
test_dir="${script_dir}/test"

##### PARSE COMMAND LINE ARGUMENTS #####

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

##### TRANSFORM PROGRAM NAMES TO UNITTEST PATTERNS #####

get_test_case_pattern_for_prog() {
    local program_to_test="$1" # e.g. "len"
    if [ -z "$program_to_test" ]; then
        echo >&2 'fatal: function expected to be passed a program name'
        exit 1
    fi

    # Match only tests whose fully qualified name includes `test_<name>.`, which
    # would be the prefix for tests of the script `test_<name>.py`. For example,
    # "len" becomes "test_len.".
    local test_case_pattern="test_${program_to_test}."
    echo -n "$test_case_pattern"
}

# -k PATTERN1 -k PATTERN2 ...
test_case_pattern_tokens=()
for program_to_test in "${POSITIONAL_ARGS[@]}"; do
    test_case_pattern="$(get_test_case_pattern_for_prog "$program_to_test")"
    test_case_pattern_tokens+=('-k' "$test_case_pattern")
done

##### INVOKE UNITTEST #####

if [ ${#POSITIONAL_ARGS[@]} -gt 0 ]; then
    echo "$self: running only tests for programs: ${POSITIONAL_ARGS[*]}"
else
    echo "$self: running ALL tests under: $test_dir"
fi

python3 -m unittest discover \
    $verbosity_flag \
    --start-directory "$test_dir" \
    "${test_case_pattern_tokens[@]}"
