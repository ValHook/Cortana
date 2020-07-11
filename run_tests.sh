#!/bin/sh
bazel test $(bazel query "kind(test, //...)") --test_summary=detailed --test_output=all
