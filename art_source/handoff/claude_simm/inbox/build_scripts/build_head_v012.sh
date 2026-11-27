#!/bin/bash
# Cold rebuild of head candidate v012 + hair material m001-B from the committed starter copy (ART-012 ledger).
#   bash build_head_v012.sh <absolute output dir> [blender binary]
# Writes stage1/2/3.blend, tex/, hair albedo + bake record, head.blend and head.glb into the output dir; nothing in the
# repository is changed. Stage defaults reproduce v012 (stage1/3 EYE_SPREAD 1.0, stage3 CROWN_CUT 0.12, stage2 HAIR_ROUND
# = the four v012 locks). The stage 2 arguments 0.0021 (voxel size) and 42000 (triangle target) are NOT the script's
# defaults and are required for v012.
# Expected: hair albedo sha256 135bec57... (textures_v012/simm_head_hair_basecolor.png) and identical geometry to
# head_candidate_v012.glb; GLB bytes may differ only in the eye meshes' triangle order (see HEAD_CANDIDATE_V012_NOTES.md).
set -euo pipefail
export PYTHONDONTWRITEBYTECODE=1
OUT=${1:?output dir}; B=${2:-/opt/blender/blender-3.5.1-linux-x64/blender}
HERE=$(cd "$(dirname "$0")" && pwd); INBOX=$(dirname "$HERE"); ST=$INBOX/starter_copy/START_HERE_v02.blend
mkdir -p "$OUT"
"$B" -b "$ST" --python "$HERE/stage1_head.py" -- "$OUT/stage1.blend"
"$B" -b "$OUT/stage1.blend" --python "$HERE/stage2_hair.py" -- "$OUT/stage2.blend" 0.0021 42000
"$B" -b "$OUT/stage2.blend" --python "$HERE/stage3_finish.py" -- "$OUT/stage3.blend" "$OUT/tex"
"$B" -b "$OUT/stage3.blend" --python "$HERE/hair_material_m001.py" -- "$OUT/hair_albedo.png" "$OUT/hair_bake_record.json" "$OUT/head.blend"
"$B" -b "$OUT/head.blend" --python "$HERE/stage4_export.py" -- "$OUT/head.glb"
echo "BUILT $OUT/head.glb"
