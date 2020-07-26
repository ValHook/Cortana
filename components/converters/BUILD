load("@pip_deps//:requirements.bzl", "requirement")

package(default_visibility = ["//visibility:public"])

py_library(
    name = "when",
    srcs = ["when.py"],
    deps = [
        "//protos:when",
    ],
)

py_test(
    name = "when_test",
    srcs = ["when_test.py"],
    deps = [
        ":when",
    ],
)
