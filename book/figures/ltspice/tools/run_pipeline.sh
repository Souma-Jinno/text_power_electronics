#!/bin/bash
# Run the asc -> net -> ngspice -> svg pipeline for one .asc file.
# Usage: run_pipeline.sh path/to/circuit.asc
set -euo pipefail

ASC="$1"
DIR="$(dirname "$ASC")"
BASE="$(basename "$ASC" .asc)"
TOOLS="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
NGSPICE=/home/soumajinno/miniforge3/bin/ngspice
PY=/home/soumajinno/miniforge3/bin/python3

echo "== $BASE: asc -> net =="
env HOME=/home/soumajinno "$PY" "$TOOLS/asc_to_net.py" "$ASC"

echo "== $BASE: ngspice sim -> raw =="
env "$NGSPICE" -b -r "$DIR/$BASE.raw" "$DIR/$BASE.net"

echo "== $BASE: asc -> svg =="
env HOME=/home/soumajinno LTSPICE_LIB_PATH="$TOOLS/symbols" /home/soumajinno/.local/bin/ltspice_to_svg "$ASC"

echo "== $BASE: done =="
