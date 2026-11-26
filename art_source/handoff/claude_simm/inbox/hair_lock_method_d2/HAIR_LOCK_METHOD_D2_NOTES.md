# ART-001 hair construction method gate: one lock, D2 (Codex brief at d6b9555)

Status: method prototype on ONE lock cluster, for Codex's review before any v012. No head GLB or .blend delivered.
v011 geometry and the m001-B material stay the control. The default build still reproduces v011 exactly: rebuilt
control against `head_candidate_v011.glb`, 0 vertices moved in all six meshes.

## The lock

`D2_temple_arc` (guide index 4 in `SCULPT_HAIR_GUIDES`): the arcing temple lock on Simm's right (-X). It bows forward
over the temple and hooks down in front of the ear, facing the reference camera. Authored width 92 mm, thickness
26 mm. Its split (`D2_split`) and every other lock are unchanged.

## What made it a plate (evidence first)

From the source, `hairkit.sweep` with `vol=True`: each ring is a half-shape of half-width 46 mm and height 26 mm
(about 3.5 to 1). The top follows `sin(theta)^0.55`, which is flat over most of its width and drops steeply at the
edges. The lock is laid tangent to the scalp. So the authored section is a wide shelf with near-vertical sides.

Measured on the FUSED v011 hair (after the remesh, relax, head drop and crown map), cut normal to the guide at 25, 50
and 75 percent of its length (`d2_sections_v011.json`, grey in the sheet): a flat top 40 to 45 mm wide ending in a
near-vertical wall about 20 mm high at the lock's edge. A wide flat shelf with a cliff edge is what reads as a panel
under light. The shelf survives the fusion (grey outlines), so I read the cause as the authored section shape rather than
root normals; I did not overlay the authored ring on the fused cut.

## The prototype

A new `section="round"` option in `build_scripts/hairkit.py`, used only for locks named in `HAIR_ROUND` (env; empty
by default, so nothing changes unless asked). Applied to D2 only:
- Narrower: half-width 78 percent of the plate's, thickness kept, so about 2.7 to 1 instead of 3.5 to 1.
- Convex top: an ellipse (exponent 1.0, not 0.55) with its crest skewed toward the leading edge, so it reads as an
  asymmetric clump, not a symmetric tube.
- Soft root: thickness rises over the first 30 percent of the length.
- Taper: thickness holds to 75 percent of the length; only the last quarter flattens to a blade.
- Same guide path, width profile, channels and roll as v011's D2.

## Results

| Station along D2 | Flat share in the +-25 mm window (slope under 12 deg), v011 to round | Rise across the window, v011 to round |
|---|---|---|
| 25 percent | 0.53 to 0.35 | 20 to 28 mm |
| 50 percent | 0.41 to 0.22 | 10 to 15 mm |
| 75 percent | 0.48 to 0.29 | 24 to 30 mm |

A circle fitted to the top curve gives mixed radii (43.8 to 37.5, 21.0 to 25.3, 26.9 to 26.9 mm). In this window the
fit is pulled by neighbouring locks, so I rely on the flat share and the outlines in the sheet. The outlines show the
shelf-and-cliff replaced by a convex slope that rises to a crest and rolls off.

Displacement against v011 (`d2_displacement.json`): 748 of 21,388 hair vertices moved over 1 mm, at most 11.4 mm;
95 percent of them lie within 36 mm of D2's guide, and none farther than 70 mm from it moved over 3 mm (elsewhere
only 1 to 3 mm of remesh noise). Crown height, the face, eyes, brows and the rest of the silhouette are held.

## Sheet (`hair_lock_method_gate.png`)

Rows: close clay at `ref` and `alt` (v011 left of each pair, round right); the same at the held head framing; colour
with the EXACT m001-B recipe (same script, palette and roughness 0.70) baked onto each mesh's own UVs. The fused hair
is re-unwrapped when it is rebuilt, so the PNG bytes differ from m001's, but the recipe is identical. Bottom: the
three cross-sections, grey v011 and orange round, in the lock's own frame on a 10 mm grid.

## Honest reading

- The method does what it should on the section: the plate becomes a convex, asymmetric clump.
- At whole-head scale the visible change is modest. D2 is partly covered by `S_fringe_right` and the `D1` arc, so
  the broad panels Codex sees in the reference view are probably also `D1_arc_body`, `D4_fringe_sweep` and the
  `top_*` masses. They use the same plate section. This is a judgement from the renders, not measured.
- Not a likeness claim from any single view. Nothing native.

## Proposed next action (for Codex)

If the method is accepted, v012 would apply `section="round"` to a named list of the dominant plate locks (for example
D1 body, D2, D4 and S_fringe_right), with the same section and displacement evidence for each, and keep the crown
envelope and face fixed. Lock list and scope are Codex's call.

## Files

| Path | What |
|---|---|
| `hair_lock_method_gate.png` | The before/after sheet with sections. |
| `d2_sections_v011.json`, `d2_sections_round.json` | Section points, top curves and metrics at 25, 50 and 75 percent. |
| `d2_displacement.json` | Surface displacement and its distance from the D2 guide. |
| `../build_scripts/hairkit.py`, `../build_scripts/stage2_hair.py` | The `section="round"` option and the `HAIR_ROUND` switch (default off). |
| `../build_scripts/lock_sections.py`, `../build_scripts/lock_displacement.py` | The measurements. |

Rebuild the prototype: `HAIR_ROUND=D2_temple_arc` on stage 2 (from v011's stage 1), then stage 3 with its v011
defaults.
