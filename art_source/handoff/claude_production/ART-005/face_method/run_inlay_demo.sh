#!/bin/bash
# ART-015 inlay-eye method demo (Codex brief at 5fafefb). Builds a SCRATCH head with the inlay method; the repository's
# stage scripts and every committed asset stay unchanged.
#   bash run_inlay_demo.sh <absolute empty output dir> [blender binary]
# Copies inbox/build_scripts to <out>/scripts, applies inlay_method.patch there (adds an INLAY switch, OFF by default), and
# runs stages 1 to 3 plus the m001-B hair install with INLAY=1 and the pinned v012 settings (same as build_head_v012.sh).
# Result: <out>/head.blend (no GLB is exported). Render it with render_views.py like head_candidate_v012.blend.
set -euo pipefail
OUT=${1:?usage: run_inlay_demo.sh <absolute empty output dir> [blender]}; B=${2:-/opt/blender/blender-3.5.1-linux-x64/blender}
case "$OUT" in /*) ;; *) echo "REFUSED: absolute path required" >&2; exit 2;; esac
if [ -e "$OUT" ] && [ -n "$(ls -A "$OUT" 2>/dev/null)" ]; then echo "REFUSED: output dir is not empty: $OUT" >&2; exit 3; fi
HERE=$(cd "$(dirname "$0")" && pwd); REPO=$(cd "$HERE/../../../../.." && pwd); INBOX=$REPO/art_source/handoff/claude_simm/inbox
mkdir -p "$OUT/scripts"; cp "$INBOX"/build_scripts/*.py "$OUT/scripts/"
( cd "$OUT/scripts" && patch -p6 --quiet < "$HERE/inlay_method.patch" )
ROUND="D1_arc_body:0.78:1.0:0.0,D2_temple_arc:0.78:1.0:0.0,D4_fringe_sweep:0.78:1.0:0.0,S_fringe_right:0.78:1.0:0.0"
run() { env -i HOME="$OUT" PATH=/usr/bin:/bin LANG=C.UTF-8 PYTHONDONTWRITEBYTECODE=1 EYE_SPREAD=1.0 CROWN_CUT=0.12 HAIR_ROUND="$ROUND" INLAY=1 "$B" --factory-startup -b "$@"; }
S=$OUT/scripts
run "$INBOX/starter_copy/START_HERE_v02.blend" --python "$S/stage1_head.py" -- "$OUT/stage1.blend"
run "$OUT/stage1.blend" --python "$S/stage2_hair.py" -- "$OUT/stage2.blend" 0.0021 42000
run "$OUT/stage2.blend" --python "$S/stage3_finish.py" -- "$OUT/stage3.blend" "$OUT/tex"
run "$OUT/stage3.blend" --python "$S/hair_material_m001.py" -- "$OUT/hair_albedo.png" "$OUT/hair_bake_record.json" "$OUT/head.blend"
echo "BUILT $OUT/head.blend (inlay method, scratch)"
