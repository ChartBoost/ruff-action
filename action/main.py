"""GitHub Action for Ruff."""

import os
import re
import shlex
import sys
from pathlib import Path
from subprocess import run

ACTION_PATH = Path(os.environ["GITHUB_ACTION_PATH"])
ARGS = os.getenv("INPUT_ARGS", default="")
SRC = os.getenv("INPUT_SRC", default="")
VERSION = os.getenv("INPUT_VERSION", default="")
CHANGED_FILES = os.getenv("CHANGED_FILES", "")

version_specifier = ""
if VERSION != "":
    if not re.match(r"v?\d\.\d{1,3}\.\d{1,3}$", VERSION):
        print("VERSION does not match expected pattern")
        sys.exit(1)
    version_specifier = f"=={VERSION}"

req = f"ruff{version_specifier}"

# If CHANGED_FILES is not empty, split it into a list; otherwise, use SRC
files_to_check = shlex.split(CHANGED_FILES or SRC)
# Exclude non-Python files
files_to_check = [f for f in files_to_check if f.endswith(".py")]

proc = run(["pipx", "run", req, *shlex.split(ARGS), *files_to_check])

sys.exit(proc.returncode)
