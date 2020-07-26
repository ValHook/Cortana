load("@com_google_protobuf//:protobuf.bzl", "py_proto_library")

package(default_visibility = ["//visibility:public"])

py_proto_library(
    name = "activity",
    srcs = ["activity.proto"],
    deps = [
        ":activity_id",
        ":squad",
    ],
)

py_proto_library(
    name = "activity_id",
    srcs = ["activity_id.proto"],
    deps = [":when"],
)

py_proto_library(
    name = "api_bundle",
    srcs = ["api_bundle.proto"],
    deps = [":activity_id"],
)

py_proto_library(
    name = "planning",
    srcs = ["planning.proto"],
    deps = [
        ":activity",
    ],
)

py_proto_library(
    name = "intent",
    srcs = ["intent.proto"],
    deps = [
        ":activity_id",
        ":squad",
    ],
)

py_proto_library(
    name = "rated_player",
    srcs = ["rated_player.proto"],
)

py_proto_library(
    name = "squad",
    srcs = ["squad.proto"],
    deps = [":rated_player"],
)

py_proto_library(
    name = "when",
    srcs = ["when.proto"],
)
