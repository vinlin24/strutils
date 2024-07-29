#!/bin/sh
# NOTE: This file should be copied to `.git/hooks/pre-push` to take effect.

repo_root="$(git rev-parse --show-toplevel)"
cd "$repo_root" || exit 1

# Ensure ALL tests are passing.

make test-all
