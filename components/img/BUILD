load("@pip_deps//:requirements.bzl", "requirement")

package(default_visibility = ["//visibility:public"])

py_library(
    name = "generator",
    srcs = ["generator.py"],
    deps = [
        "//protos:planning",
        requirement("pillow"),
    ],
    data = [":assets"],
)

py_test(
    name = "generator_test",
    srcs = ["generator_test.py"],
    deps = [
        ":generator",
    ],
)

filegroup(
    name = "assets",
    srcs = glob([
        "assets/*",
    ]),
)
