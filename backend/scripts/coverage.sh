#!/usr/bin/env bash
set -e

SCRIPT_DIR=$(dirname "$(realpath "$0")")
PROJECT_ROOT="$SCRIPT_DIR/../"

uv run coverage run --source="$SCRIPT_DIR/../" -p -m pytest
uv run coverage combine
uv run coverage html

open "$PROJECT_ROOT/htmlcov/index.html"
