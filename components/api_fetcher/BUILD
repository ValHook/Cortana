load("@pip_deps//:requirements.bzl", "requirement")

package(default_visibility = ["//visibility:public"])

py_library(
    name = "api_fetcher",
    srcs = ["api_fetcher.py"],
    deps = [
    	"//protos:api_bundle",
    	requirement("requests"),
    ],
)

py_test(
    name = "api_fetcher_test",
    srcs = ["api_fetcher_test.py"],
    deps = [
        ":api_fetcher",
    ],
)
