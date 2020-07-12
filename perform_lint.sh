#!/bin/sh
set -e
SCRIPTDIR=$( cd "$(dirname "$0")" ; pwd -P )
bazel run //:buildifier
bazel run //:python_linter -- $(find $SCRIPTDIR -name "*.py" | tr '\n' ' ')
