#!/bin/sh
set -e
bazel run //:buildifier
bazel run //:python_linter -- $(find $(pwd) -name "*.py" | tr '\n' ' ')
