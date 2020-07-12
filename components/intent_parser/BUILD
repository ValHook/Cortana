package(default_visibility = ["//visibility:public"])

py_library(
    name = "parser",
    srcs = ["parser.py"],
)

py_test(
    name = "parser_test",
    srcs = ["parser_test.py"],
    deps = [
        ":parser",
        "//protos:intent",
    ],
)
