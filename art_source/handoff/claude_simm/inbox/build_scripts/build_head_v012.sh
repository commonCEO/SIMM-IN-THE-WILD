#!/bin/bash
# Cold rebuild of head candidate v012 + hair material m001-B from the committed starter copy (ART-012 ledger).
#   bash build_head_v012.sh <absolute output dir, must not exist or must be empty> [blender binary]
# Writes stage1/2/3.blend, tex/, hair albedo + bake record, head.blend and head.glb into the output dir; nothing in the
# repository is changed and nothing is deleted. A non-empty output dir is refused, never overwritten.
#
# Hermetic against the caller's shell (Codex review at e01071e): every Blender call runs under `env -i` with only the
# variables below, so experimental or diagnostic switches set by the caller (EYE_SPREAD, CROWN_CUT, HAIR_ROUND,
# HAIR_SKIP, HAIR_SOURCE_COPY, MOUTH_DEBUG, PYTHONPATH, BLENDER_USER_* ...) cannot change the build. --factory-startup
# keeps user preferences and add-ons out. The v012 values are pinned explicitly, not taken from script defaults:
#   EYE_SPREAD=1.0 (stage 1 and 3), CROWN_CUT=0.12 (stage 3),
#   HAIR_ROUND = the four v012 locks, each width 0.78, thickness 1.0, inward 0.0 (stage 2),
#   HAIR_SKIP, HAIR_SOURCE_COPY, MOUTH_DEBUG unset; stage 2 arguments 0.0021 (voxel size) and 42000 (triangle target).
# Expected: hair albedo sha256 135bec57... (textures_v012/simm_head_hair_basecolor.png), skin/eye textures as
# textures_v012, geometry identical to head_candidate_v012.glb; GLB bytes may differ in the eye meshes' triangle order.
set -euo pipefail
OUT=${1:?usage: build_head_v012.sh <absolute output dir> [blender binary]}
B=${2:-/opt/blender/blender-3.5.1-linux-x64/blender}
case "$OUT" in /*) ;; *) echo "REFUSED: output dir must be an absolute path" >&2; exit 2;; esac
if [ -e "$OUT" ] && [ -n "$(ls -A "$OUT" 2>/dev/null)" ]; then echo "REFUSED: output dir is not empty: $OUT" >&2; exit 3; fi
HERE=$(cd "$(dirname "$0")" && pwd); INBOX=$(dirname "$HERE"); ST=$INBOX/starter_copy/START_HERE_v02.blend
mkdir -p "$OUT"
ROUND="D1_arc_body:0.78:1.0:0.0,D2_temple_arc:0.78:1.0:0.0,D4_fringe_sweep:0.78:1.0:0.0,S_fringe_right:0.78:1.0:0.0"
run() {
  env -i HOME="$OUT" PATH=/usr/bin:/bin LANG=C.UTF-8 PYTHONDONTWRITEBYTECODE=1 \
      EYE_SPREAD=1.0 CROWN_CUT=0.12 HAIR_ROUND="$ROUND" \
      "$B" --factory-startup -b "$@"
}
run "$ST" --python "$HERE/stage1_head.py" -- "$OUT/stage1.blend"
run "$OUT/stage1.blend" --python "$HERE/stage2_hair.py" -- "$OUT/stage2.blend" 0.0021 42000
run "$OUT/stage2.blend" --python "$HERE/stage3_finish.py" -- "$OUT/stage3.blend" "$OUT/tex"
run "$OUT/stage3.blend" --python "$HERE/hair_material_m001.py" -- "$OUT/hair_albedo.png" "$OUT/hair_bake_record.json" "$OUT/head.blend"
run "$OUT/head.blend" --python "$HERE/stage4_export.py" -- "$OUT/head.glb"
echo "BUILT $OUT/head.glb"
