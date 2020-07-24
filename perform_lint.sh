#!/bin/sh
set -e
bazel run //:buildifier
echo "All bazel files are properly formatted."
echo "Skipping Python & protobuf linting because there is no linter set up yet."
