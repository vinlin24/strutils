#!/bin/bash

self="$(basename "$0")"
script_dir="$(dirname "$0")"
test_dir="${script_dir}/test"

##### PARSE COMMAND LINE ARGUMENTS #####

usage() {
    echo "usage: $0 [-v|--verbose] [-h|--help] [-l|--lazy] [PROG1] [PROG2] ..."
}

POSITIONAL_ARGS=()
VERBOSE=0
RUN_AS_NEEDED=0

while [ $# -gt 0 ]; do
    case $1 in
    -h | --help)
        usage
        exit 0
        ;;
    -v | --verbose)
        VERBOSE=1
        shift
        ;;
    -l | --lazy)
        RUN_AS_NEEDED=1
        shift
        ;;
    -*)
        echo >&2 "$self: invalid option: $1"
        usage >&2
        exit 1
        ;;
    *)
        POSITIONAL_ARGS+=("$1")
        shift
        ;;
    esac
done

verbosity_flag=''
if [ $VERBOSE -eq 1 ]; then
    verbosity_flag='--verbose'
fi

##### TRANSFORM PROGRAM NAMES TO UNITTEST PATTERNS #####

get_changed_progs() {
    local changed_sources
    changed_sources=$(
        git diff --name-only HEAD -- src/strutils/*.py &&
            git ls-files --others --exclude-standard src/strutils/*.py
    )
    # NOTE: This breaks if the file paths have spaces in them, but at this point
    # I'm done with caring. Shell is a dogwater language.
    for changed_source in $changed_sources; do
        local file_stem
        file_stem="$(basename "$changed_source")"
        file_stem="${file_stem%.py}"
        echo "$file_stem"
    done
}

src_common_code_unchanged() {
    changed_sources=$(
        git diff --name-only HEAD -- src/strutils/common/*.py &&
            git ls-files --others --exclude-standard src/strutils/common/*.py
    )
    if [ -z "$changed_sources" ]; then
        return 0
    fi
    return 1
}

get_test_case_pattern_for_prog() {
    local program_to_test="$1" # e.g. "len"
    if [ -z "$program_to_test" ]; then
        echo >&2 "$self: fatal: function expected to be passed a program name"
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
# For display purposes.
test_names_to_run=()

if [ $RUN_AS_NEEDED -eq 1 ]; then
    for program_to_test in $(get_changed_progs); do
        test_names_to_run+=("$program_to_test")
        test_case_pattern="$(get_test_case_pattern_for_prog "$program_to_test")"
        test_case_pattern_tokens+=('-k' "$test_case_pattern")
    done
else
    for program_to_test in "${POSITIONAL_ARGS[@]}"; do
        test_names_to_run+=("$program_to_test")
        test_case_pattern="$(get_test_case_pattern_for_prog "$program_to_test")"
        test_case_pattern_tokens+=('-k' "$test_case_pattern")
    done
fi

##### INVOKE UNITTEST #####

if [ $RUN_AS_NEEDED -eq 1 ] &&
    [ ${#test_names_to_run[@]} -eq 0 ] &&
    src_common_code_unchanged; then

    echo "$self: no scripts have changed since last commit, no tests to run"
    exit 0
fi

if [ ${#test_names_to_run[@]} -gt 0 ]; then
    echo "$self: running only tests for programs: ${test_names_to_run[*]}"
else
    echo "$self: running ALL tests under: $test_dir"
fi

python3 -m unittest discover \
    $verbosity_flag \
    --start-directory "$test_dir" \
    "${test_case_pattern_tokens[@]}"
