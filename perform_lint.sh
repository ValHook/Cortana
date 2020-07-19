#!/bin/sh
set -e
SCRIPTDIR=$( cd "$(dirname "$0")" ; pwd -P )
bazel run //:buildifier
echo "All bazel files are properly formatted."
echo "Skipping Python & protobug linting because there is no linter set up yet."
