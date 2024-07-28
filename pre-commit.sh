#!/bin/sh
# NOTE: This file should be copied to `.git/hooks/pre-commit` to take effect.

repo_root="$(git rev-parse --show-toplevel)"
cd "$repo_root" || exit 1

if ! make readme; then
    echo >&2 'failed to update README.md, aborting.'
    exit 1
fi

git add README.md
