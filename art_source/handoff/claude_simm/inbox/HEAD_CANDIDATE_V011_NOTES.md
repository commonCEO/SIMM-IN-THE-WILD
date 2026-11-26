# Head candidate v011: lower crown and upper hair (bounded height study, Codex brief at eb48d10)

Status: review candidate for Codex's native matched-camera check. Reversible: v010 stays archived
(`head_candidate_v010.glb`, sha `26721da8...`) and rebuilds with `CROWN_CUT=0`. Not a parity claim, no A1 approval.

## The study

Control (v010) against two brackets, about 8% and 12% less height from the eye line to the top of the hair. Height
is measured on the actual render silhouette, at the reference (`ref`) and alternate (`alt`) cameras, as a multiple
of the eye-line-to-chin depth from the same camera. The study measures two things separately:
- **full top:** the highest hair pixel, tufts included;
- **main crown mass:** the top of the silhouette after a morphological opening with a 31 px square, which removes thin
  tufts and spikes. Doing this means trimming the tallest tuft alone could not hide an oversized dome.

| | Full top, `ref` | Main mass, `ref` | Full top, `alt` | Main mass, `alt` |
|---|---|---|---|---|
| Reference (read by hand from the blurred crop) | about 2.2 (2.05 to 2.35) | about 1.8 (1.67 to 2.0) | no reference view | no reference view |
| v010 control | 2.57 | 2.38 | 2.77 | 2.63 |
| -8% | 2.37 | 2.21 | 2.56 | 2.43 |
| **-12% (chosen, v011)** | **2.27** | **2.12** | **2.45** | **2.34** |

Openings of 21 and 41 px give the same ordering (`renders_v011/crown_height_measurements.json`). The dome itself was
high, not only the tuft: the main mass sat at 2.38 against about 1.8.

## Why -12%

- At the reference camera, the full height lands inside the reference range; the main mass comes closer but stays
  above it (2.12 against 1.67 to 2.0). I did not go further than the brief's bracket.
- It improves both cameras by about the same share, and the whole-figure frame reads a little more compact.
- In clay at the reference, alternate, front, left side and back, the swept asymmetric shape, the separated soft
  tips and the tuft stay. There is no flat cap or straight scalp line, and the scalp stays covered all round.
- -8% was the same direction but left the full height just above the reference range.

## What changed, and only this

One step at the end of `build_scripts/stage3_finish.py` (`CROWN_CUT`, default now 0.12): hair, upper scalp and the
hair guide curves get the same smooth vertical compression above Z 1.235 (final head coordinates; the eye line is at
1.152 and the brow tops at 1.208). The compression starts with no change in slope and ramps in over 40 mm, so there
is no crease. Above that, heights shrink by a factor of 0.815. Because hair and scalp share one height-only map, nothing
can pass through anything that it did not before.

| Mesh | Evidence (v010 against v011 source meshes) |
|---|---|
| `SCULPT_HAIR` | 12,779 of 21,390 vertices lowered, all at Z 1.2352 or above; largest drop 35.0 mm (the tuft tip: hair top 1.444 to 1.409). X and Y unchanged. |
| `SCULPT_HEAD` | 254 of 4,118 base vertices lowered, all at Z 1.2360 or above (the upper scalp under the hair); largest drop 13.3 mm. Everything below Z 1.235 unchanged (largest difference 0.000007 mm, float rounding). |
| `SCULPT_EYE_L/R`, `SCULPT_BROWS`, `SCULPT_LASHES` | 0 vertices moved. |
| Textures | All four byte-identical to v010. |

Held, as the brief asked: eye centres and meshes, lids, lashes, brows, nose, mouth, jaw, fringe tips, ears, neck
attachment, head root and transform, palette, all clothing.

## Files

| Path | What |
|---|---|
| `head_candidate_v011.glb` | Static head only. sha256 `3c0d0d2c94ae467d5303d81b9980cbc77ec653b8e39fb89a89ef9d23bcce2d2e`, 3,299,504 bytes, 80,346 tris. Root `SCULPT_HEAD_ROOT` at the origin, identity. Bounds (Blender Z-up after re-import) (-0.251, -0.134, 0.936) to (0.225, 0.274, 1.409): only the top changed from v010 (was 1.444). Same object names and materials as v010. No rig, animation, camera or light. |
| `head_candidate_v011.blend` | Editable source, rebuilt from `starter_copy/START_HERE_v02.blend` through stages 1 to 4 with the defaults. |
| `textures_v011/` | The four embedded textures (same as v010). |
| `renders_v011/head_v011_crown_height_comparison.png` | The study sheet: reference, control, -8% and -12% at the `ref` and `alt` clay cameras and colour `ref`, with eye line, chin, full top and main-mass lines, plus a whole-figure row. |
| `renders_v011/head_v010_top_v011_bottom_front_side_back_clay.png` | Coverage check: front, left side and back in clay. |
| `renders_v011/head_v011_{colour,clay}_{ref,alt,front}.png`, `head_v011_colour_side.png` | Single frames, Blender Cycles, review only, with the frozen body. |
| `build_scripts/head_silhouette.py` | New: alpha mask of head and hair at an agreed camera, for the height measurement. |

`verify_candidate.py`: `FROZEN_ALL_UNCHANGED True` (body, old head, rig, socket, actions). Mesh lines: `SCULPT_HEAD`
21,673 verts / 33,000 tris; `SCULPT_HAIR` 32,461 / 41,986 in the GLB (the same 21,390 source vertices as v010; the
exporter splits 3 more for normals); eyes 922 / 1,840 each; brows 348 / 560; lashes 656 / 1,120. The rejected -8%
variant is not delivered as a binary.

Provenance: as v010 (Blender Studio CC0 base head; hair, eyes and textures scripted here). No generators, purchases
or outside services.

## Honest issue list

1. The main crown mass is still above the reference's estimated range (2.12 against 1.67 to 2.0), by design of the
   bracket. A further cut risks flattening the swept top; judge natively first.
2. The hair is thinner over the crown by the same factor (about 18 percent): still covered, but a slightly thinner
   top layer.
3. The reference lines are read by hand from a blurred crop. The ratios are ranges, not a score; the camera is not
   solved against the reference.
4. Hair material and lock surfaces are unchanged, as the brief sequenced.
5. Not run in Godot.

## Proposed next action

Codex checks v011 natively against v010 at the matched cameras and in the full figure. If it holds, the next head
step Codex named is hair material and lock-surface refinement.
