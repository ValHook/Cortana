#!/bin/sh
set -e
bazel run //:buildifier_check || (echo "ERROR: Bazel files not formatted, please run \`bazel run //:buildifier\`" >&2; exit 1)
bazel test $(bazel query "kind(test, //...)") --test_summary=detailed --test_output=all --verbose_failures
