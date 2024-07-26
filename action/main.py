"""GitHub Action for Ruff."""

import os
import re
import shlex
import subprocess
import sys
from pathlib import Path

ACTION_PATH = Path(os.environ["GITHUB_ACTION_PATH"])
ARGS = os.getenv("INPUT_ARGS", default="")
SRC = os.getenv("INPUT_SRC", default="")

VERSION = os.getenv("INPUT_VERSION", default="")
USE_PYPROJECT = os.getenv("INPUT_USE_PYPROJECT") == "true"
RUFF_VERSION_RE = re.compile(r"^ruff([^A-Z0-9._-]+.*)$", re.IGNORECASE)

# Changed files support
CHANGED_FILES = os.getenv("CHANGED_FILES", "")
CHANGED_FILES_ENABLED = os.getenv("CHANGED_FILES_ENABLED", default="false") == "true"


def determine_version() -> str:
    """
    Determine the version to install.

    The version can be specified either via the `with.version` input or via the
    pyproject.toml file if `with.use_pyproject` is set to `true`.
    """
    if USE_PYPROJECT and VERSION:
        print(
            "::error::'with.version' and 'with.use_pyproject' inputs are mutually exclusive.",
            file=sys.stderr,
            flush=True,
        )
        sys.exit(1)

    if USE_PYPROJECT:
        return read_version_from_pyproject()

    elif VERSION and VERSION[0] in "0123456789":
        return f"=={VERSION}"

    else:
        return VERSION


def read_version_from_pyproject() -> str:
    """Read the version specifier from the pyproject.toml file."""
    if sys.version_info < (3, 7):
        print(
            "::error::'with.use_pyproject' input requires Python 3.7 or later.",
            file=sys.stderr,
            flush=True,
        )
        sys.exit(1)

    import tomllib  # type: ignore[import-not-found,unreachable]

    try:
        with Path("pyproject.toml").open("rb") as fp:
            pyproject = tomllib.load(fp)
    except FileNotFoundError:
        print(
            "::error::'with.use_pyproject' input requires a pyproject.toml file.",
            file=sys.stderr,
            flush=True,
        )
        sys.exit(1)

    version = pyproject.get("tool", {}).get("ruff", {}).get("required-version")
    if version is not None:
        return f"=={version}"

    arrays = [
        pyproject.get("project", {}).get("dependencies"),
        *pyproject.get("project", {}).get("optional-dependencies", {}).values(),
    ]
    for array in arrays:
        version = find_version_in_array(array)
        if version is not None:
            break

    if version is None:
        print(
            "::error::'ruff' dependency missing from pyproject.toml.",
            file=sys.stderr,
            flush=True,
        )
        sys.exit(1)

    return version


def find_version_in_array(array: object) -> str | None:
    """Find the version specifier in an array of dependencies."""
    if not isinstance(array, list):
        return None

    try:
        for item in array:
            item = item.split(";")[0]
            if item == "ruff":
                print(
                    "::error::Version specifier missing for 'ruff' dependency in pyproject.toml.",
                    file=sys.stderr,
                    flush=True,
                )
                sys.exit(1)
            elif m := RUFF_VERSION_RE.match(item):
                return m.group(1).strip()
    except TypeError:
        pass

    return None


if CHANGED_FILES_ENABLED and not CHANGED_FILES:
    print(
        "::error::'changed_files' input is enabled but no files were provided.",
        file=sys.stderr,
        flush=True,
    )
    sys.exit(0)

version_specifier = determine_version()
exc = subprocess.run(
    [
        sys.executable,
        "run",
        "check",
        f"ruff{version_specifier}",
        *shlex.split(ARGS),
        *shlex.split(CHANGED_FILES or SRC),
    ],
    check=False,
)
sys.exit(exc.returncode)
