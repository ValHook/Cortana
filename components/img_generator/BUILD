load("@pip_deps//:requirements.bzl", "requirement")

package(default_visibility = ["//visibility:public"])

py_library(
    name = "img_generator",
    srcs = ["img_generator.py"],
    deps = [
        "//protos:planning",
        requirement("babel"),
        requirement("pillow"),
    ],
    data = [":assets"],
)

py_test(
    name = "img_generator_test",
    srcs = ["img_generator_test.py"],
    deps = [
        ":img_generator",
    ],
)
