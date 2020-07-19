#!/bin/sh
set -e
bazel test $(bazel query "kind(test, //...)")
