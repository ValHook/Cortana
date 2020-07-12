#!/bin/sh
set -e
bazel test $(bazel query "kind(test, //...)") --test_summary=detailed --test_output=all --verbose_failures
