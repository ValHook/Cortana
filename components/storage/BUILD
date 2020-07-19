package(default_visibility = ["//visibility:public"])

py_library(
    name = "storage",
    srcs = ["storage.py"],
    deps = [
        "//protos:api_bundle",
    ],
)

py_test(
    name = "storage_test",
    srcs = ["storage_test.py"],
    deps = [
        ":storage",
    ],
)
