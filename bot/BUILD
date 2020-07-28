load("@pip_deps//:requirements.bzl", "requirement")

package(default_visibility = ["//visibility:public"])

py_binary(
    name = "bot",
    srcs = ["bot.py"],
    deps = [
        "//components/intent_executor",
        "//components/intent_parser",
        requirement("appdirs"),
        requirement("discord"),
    ],
)
