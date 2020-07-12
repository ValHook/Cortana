load("@com_github_bazelbuild_buildtools//buildifier:def.bzl", "buildifier")
load("@pip_deps//:requirements.bzl", "requirement")

buildifier(
    name = "buildifier",
    verbose = True,
)

buildifier(
    name = "buildifier_check",
    mode = "check",
)

py_binary(
    name = "python_linter",
    srcs = ["python_linter.py"],
    main = "python_linter.py",
    deps = [
        requirement("autopep8"),
    ],
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
