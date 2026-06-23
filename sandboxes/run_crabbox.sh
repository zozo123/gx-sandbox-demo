#!/usr/bin/env bash
# Run the GX demo in a local Apple `container` via crabbox.sh (brokerless).
#
# crabbox syncs your git checkout into the box, so gx_demo.py + requirements.txt
# are already present. The apple-container provider needs no broker/coordinator.
# Verified on python:3.12-slim and python:3.12.
#
# Prereqs: crabbox + Apple `container` CLI installed; run from inside this git repo.
# Usage:   sandboxes/run_crabbox.sh
set -euo pipefail

crabbox run --provider apple-container --apple-container-image python:3.12-slim \
  -- bash -lc 'pip install -q great_expectations && python3 gx_demo.py'
