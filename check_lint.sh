#!/bin/sh
set -e
bazel run //:buildifier_check
bazel run //:python_linter_check -- $(find $(pwd) -name "*.py" | tr '\n' ' ')
