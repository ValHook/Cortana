#!/bin/sh
set -e
bazel run //:buildifier_check
echo "Bazel files check done."
bazel run //:python_linter_check -- $(find $(pwd) -name "*.py" | tr '\n' ' ')
echo "Python files check done."
echo "No support for protos file checking yet."
