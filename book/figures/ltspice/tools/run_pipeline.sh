#!/bin/bash
# Run the asc -> net -> ngspice -> svg pipeline for one .asc file.
# Usage: run_pipeline.sh path/to/circuit.asc
set -euo pipefail

ASC="$1"
DIR="$(cd "$(dirname "$ASC")" && pwd)"
BASE="$(basename "$ASC" .asc)"
TOOLS="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
NGSPICE=/home/soumajinno/miniforge3/bin/ngspice
PY=/home/soumajinno/miniforge3/bin/python3

echo "== $BASE: asc -> net =="
env HOME=/home/soumajinno "$PY" "$TOOLS/asc_to_net.py" "$ASC"

echo "== $BASE: ngspice sim -> raw =="
LTSPICE_ROOT="$(cd "$TOOLS/.." && pwd)"
if grep -q '^\.control' "$DIR/$BASE.net"; then
  # Netlists with a .control/.endc block (chapter02+: needed to print internal
  # device currents like @q1[ic]) must write their own .raw via a "write ..."
  # line inside the control block. Passing -b -r together with a .control
  # block was observed on this machine to silently produce no .raw file at
  # all (ngspice logs "binary raw file ..." twice but nothing lands on disk) --
  # so for these netlists we deliberately omit -r and rely on the in-deck
  # "write" command instead. That in-deck "write chapterNN/xxx.raw" path is
  # relative to LTSPICE_ROOT (book/figures/ltspice/), so cd there first --
  # otherwise the write silently fails when this script is invoked from a
  # different working directory.
  (cd "$LTSPICE_ROOT" && env "$NGSPICE" -b "${DIR#$LTSPICE_ROOT/}/$BASE.net")
else
  env "$NGSPICE" -b -r "$DIR/$BASE.raw" "$DIR/$BASE.net"
fi

echo "== $BASE: asc -> svg =="
env HOME=/home/soumajinno LTSPICE_LIB_PATH="$TOOLS/symbols" /home/soumajinno/.local/bin/ltspice_to_svg "$ASC"

echo "== $BASE: fix viewBox (avoid long TEXT-comment clipping, see fix_viewbox.py) =="
env HOME=/home/soumajinno "$PY" "$TOOLS/fix_viewbox.py" "$DIR/$BASE.svg"

echo "== $BASE: done =="
