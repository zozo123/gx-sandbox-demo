#!/usr/bin/env bash
# Run the GX demo in an islo.dev cloud Firecracker microVM.
#
# islo does NOT sync your working directory, so we inject the script over stdin
# (base64) to avoid any file-transfer step. Verified on python:3.12-slim (Py 3.12.13).
#
# Prereqs: islo CLI installed and authenticated (`islo login`).
# Usage:   sandboxes/run_islo.sh [script.py]   (defaults to gx_demo.py)
set -euo pipefail

SCRIPT="${1:-gx_demo.py}"
B64="$(base64 < "$SCRIPT" | tr -d '\n')"

islo use gx-demo -i python:3.12-slim -- bash -lc \
  "pip install -q great_expectations && echo $B64 | base64 -d | python3 -"
