#!/bin/sh
# NOTE: This file should be copied to `.git/hooks/pre-commit` to take effect.

repo_root="$(git rev-parse --show-toplevel)"
cd "$repo_root" || exit 1

# (1) Ensure tests for changed source files are passing.

make test

# (2) Ensure documentation is up to date.

make_output="$(make readme)"
make_status=$?
echo "$make_output"

if [ $make_status -ne 0 ]; then
    echo >&2 'failed to update README.md, aborting.'
    exit 1
fi

if ! echo "$make_output" | grep --quiet 'Nothing to be done for'; then
    git add README.md
fi
