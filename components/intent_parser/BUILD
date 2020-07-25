load("@pip_deps//:requirements.bzl", "requirement")

package(default_visibility = ["//visibility:public"])

py_library(
    name = "intent_parser",
    srcs = ["intent_parser.py"],
    deps = [
        "//protos:api_bundle",
        "//protos:intent",
        requirement("dateparser"),
        requirement("unidecode"),
    ],
)

py_test(
    name = "intent_parser_test",
    srcs = ["intent_parser_test.py"],
    data = ["//components/intent_parser/test_assets"],
    deps = [
        ":intent_parser",
        requirement("python-dateutil"),
    ],
)
