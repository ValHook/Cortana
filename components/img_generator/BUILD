load("@pip_deps//:requirements.bzl", "requirement")

package(default_visibility = ["//visibility:public"])

py_library(
    name = "img_generator",
    srcs = ["img_generator.py"],
    data = ["//components/img_generator/assets"],
    deps = [
        "//components/converters:when",
        "//protos:schedule",
        requirement("babel"),
        requirement("pillow"),
    ],
)

py_test(
    name = "img_generator_test",
    srcs = ["img_generator_test.py"],
    deps = [
        ":img_generator",
        requirement("python-dateutil"),
    ],
)
