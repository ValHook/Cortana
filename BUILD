load("@com_github_bazelbuild_buildtools//buildifier:def.bzl", "buildifier")
load("@pip_deps//:requirements.bzl", "requirement")

buildifier(
    name = "buildifier",
    verbose = True,
)

buildifier(
    name = "buildifier_check",
    mode = "check",
    verbose = True,
)

py_binary(
    name = "python_linter_check",
    srcs = ["python_linter_check.py"],
    data = [".pylintrc"],
    main = "python_linter_check.py",
    deps = [
        requirement("pylint"),
    ],
)
