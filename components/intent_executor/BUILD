load("@pip_deps//:requirements.bzl", "requirement")

package(default_visibility = ["//visibility:public"])

py_library(
    name = "intent_executor",
    srcs = ["intent_executor.py"],
    deps = [
        "//components/api_fetcher",
        "//components/storage",
        "//protos:api_bundle",
        "//protos:planning",
    ],
)

py_test(
    name = "intent_executor_test",
    srcs = ["intent_executor_test.py"],
    data = ["//components/intent_executor/test_assets"],
    deps = [
        ":intent_executor",
    ],
)
