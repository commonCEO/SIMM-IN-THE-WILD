#!/bin/bash
# ART-016 head blockout B1 (Codex brief at faa8749): builds the B1 CLAY blockout head in a SCRATCH folder; the repository's
# stage scripts and every committed asset stay unchanged.
#   bash b1_build.sh <absolute empty output dir> [blender binary]
# 1. copies inbox/build_scripts to <out>/scripts and changes ONLY the eye-opening half sizes in that copy
#    (stage1_head.py and stage3_finish.py: OVAL_A 0.0174 -> 0.0162, OVAL_B 0.0264 -> 0.0208: rounder, smaller openings;
#    eye centres, eyeball size, lid construction, mouth, nose, chin and the neck are untouched);
# 2. runs stages 1 to 3 with the pinned v012 settings (as build_head_v012.sh, env -i, factory startup);
# 3. replaces the hair with the B1 silhouette-first mass (b1_hair.py) -> <out>/head_b1.blend.
set -euo pipefail
OUT=${1:?usage: b1_build.sh <absolute empty output dir> [blender]}; B=${2:-/opt/blender/blender-3.5.1-linux-x64/blender}
case "$OUT" in /*) ;; *) echo "REFUSED: absolute path required" >&2; exit 2;; esac
if [ -e "$OUT" ] && [ -n "$(ls -A "$OUT" 2>/dev/null)" ]; then echo "REFUSED: output dir is not empty: $OUT" >&2; exit 3; fi
HERE=$(cd "$(dirname "$0")" && pwd); REPO=$(cd "$HERE/../../../../.." && pwd); INBOX=$REPO/art_source/handoff/claude_simm/inbox
mkdir -p "$OUT/scripts"; cp "$INBOX"/build_scripts/*.py "$OUT/scripts/"
for f in stage1_head.py stage3_finish.py; do
  grep -q "OVAL_A = 0.0174; OVAL_B = 0.0264" "$OUT/scripts/$f"
  sed -i "s/OVAL_A = 0.0174; OVAL_B = 0.0264/OVAL_A = 0.0162; OVAL_B = 0.0208/" "$OUT/scripts/$f"
done
ROUND="D1_arc_body:0.78:1.0:0.0,D2_temple_arc:0.78:1.0:0.0,D4_fringe_sweep:0.78:1.0:0.0,S_fringe_right:0.78:1.0:0.0"
run() { env -i HOME="$OUT" PATH=/usr/bin:/bin LANG=C.UTF-8 PYTHONDONTWRITEBYTECODE=1 EYE_SPREAD=1.0 CROWN_CUT=0.12 HAIR_ROUND="$ROUND" "$B" --factory-startup -b "$@"; }
S=$OUT/scripts
run "$INBOX/starter_copy/START_HERE_v02.blend" --python "$S/stage1_head.py" -- "$OUT/stage1.blend"
run "$OUT/stage1.blend" --python "$S/stage2_hair.py" -- "$OUT/stage2.blend" 0.0021 42000
run "$OUT/stage2.blend" --python "$S/stage3_finish.py" -- "$OUT/stage3.blend" "$OUT/tex"
run "$OUT/stage3.blend" --python "$HERE/b1_hair.py" -- "$OUT/head_b1.blend"
echo "BUILT $OUT/head_b1.blend (B1 blockout, scratch)"
