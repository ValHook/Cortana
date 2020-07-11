package(default_visibility = ["//visibility:public"])

py_library(
    name = "parser",
    srcs = ["parser.py"],
    deps = [
        "//protos:rated_player",
    ],
)

py_test(
    name = "parser_test",
    srcs = ["parser_test.py"],
    deps = [
        ":parser",
    ],
)
