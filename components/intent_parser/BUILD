load("@pip_deps//:requirements.bzl", "requirement")

package(default_visibility = ["//visibility:public"])

py_library(
    name = "parser",
    srcs = ["parser.py"],
    deps = [
        "//protos:intent",
        requirement("unidecode"),
    ],
)

py_test(
    name = "parser_test",
    srcs = ["parser_test.py"],
    deps = [
        ":parser",
    ],
)
