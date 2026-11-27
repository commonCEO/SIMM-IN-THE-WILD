# ART-004 jacket + neck finish candidate f002: boundary and fold repair (Codex brief at 9de793b)

Status: ONE repaired comparison candidate for Codex's non-saving native study. Jacket v004 stays the fit control and
f001 the comparison experiment. Not approved; A1 unpassed. Head, hair, boots, body, rig, rest pose, actions, socket and
v004's base jacket weights are held.

## What caused the notches (diagnostic first)

`jacket_f001_notch_diagnostic.png` rebuilds f001 one step at a time on the same placket and wrist loops (clay): held
v004, then subdivision, then folds, then trim flatten, then cuff widening (= f001).
- Subdivision and the folds create neither defect.
- **The trim flatten** creates both. It projected every trim vertex onto its own nearest jacket point, and the nearest
  normal jumps from vertex to vertex along an edge. That scalloped the placket and crumpled the cuff.
- **Cuff widening** then enlarged the crumpled cuff.

## f002

| | f001 | f002 |
|---|---|---|
| Placket and cuff rolls | Flattened per vertex onto the nearest jacket normal | Flattened about each roll's own centre (mean of the roll within 10 mm), along a direction smoothed over the roll (60 passes); cuffs along the forearm's radial direction. Height x0.45. Neighbouring points move alike, so the outline stays continuous. |
| Cuff widening | Doubled toward the elbow | None: the wrist edge keeps v004's shape and position |
| Hem roll | Flattened | Not flattened. It already crosses the trousers in v004, and flattening moved those crossings; it only follows the hem waves. |
| Folds near boundaries | Full strength | Faded to zero within about 30 mm of the plackets and cuffs, so those loops keep v004's shape |
| Sleeve folds | Regular sine rings over a 7 cm band, plus a wave below the shoulder | Three unequal compression folds at the inner elbow (4.5, 3.2 and 2.0 mm high, 16 mm above to 19 mm below the elbow, slightly tilted), blending out round the outer arm. The shoulder and upper arm are left quiet; the lowest fold ends about 85 mm above the wrist. |
| Hem waves | Up to 3.8 mm | Same, but an inward wave may not bring the cloth within 3 mm of the trousers |
| Subdivision, pockets, neck colour | as described for f001 | unchanged from f001 (pockets still a separate, removable part; brown neck interpretation kept) |

`jacket_finish_f002_boundaries.png`: placket, wrist and elbow in clay for held, f001 and f002. My reading: the f002
placket and cuff are continuous and close to v004's, the f001 serration and notches are gone, and the elbow has a few
soft unequal folds instead of rings.

## Contact check that does not depend on vertex density

`build_scripts/jacket_contact_check.py`. At each of 97 poses per clip, every garment surface is intersected,
triangle against triangle, with UNCHANGED partner surfaces: the hands, the pack straps, the trousers, and the collar's
hood and scarf carried by the chest bone (so the collar moves). The result is the set of partner triangles crossed;
partner meshes are the same in every file, so the sets compare directly between garments of any density. A crossing
means the surfaces intersect; the method does not measure depth or prove clearance where nothing crosses.

Union over 97 poses: held v004 / f002, with how many crossed triangles are new in f002 and how many are gone
(`surface_contacts_held_vs_f002.json`):

| Clip | Hands | Straps | Collar (in motion) | Trousers |
|---|---|---|---|---|
| idle | 55 / 55, 0 new | 15 / 15, 0 new | 395 / 395, 0 new | 43 / 42, 4 new, 5 gone |
| walk | 48 / 48, 0 new | 15 / 15, 0 new | 405 / 404, 0 new, 1 gone | 211 / 218, 16 new, 9 gone |
| gather_handclear (study) | 55 / 55, 0 new | 32 / 32, 0 new | 411 / 405, 0 new, 6 gone | 43 / 42, 4 new, 5 gone |
| gather (original, negative control) | 116 / 116 | 32 / 32 | 411 / 405 | 43 / 42 |

Separating old from new:
- **Pre-existing in held v004 (unchanged by f002):**
  - Hands: the sleeve-end caps cross the wrist inside the cuff.
  - Straps: the frozen straps cross the jacket's chest.
  - Collar: its seated tuck crosses the neckline.
  - Trousers: all trouser crossings come from the hem roll (isolated: the jacket shell crosses none).
- **f002:** no new hand, strap or collar crossings anywhere. The hem roll's trouser crossings shift slightly as it
  follows the hem waves. Every new trouser triangle lies inside v004's existing crossing band (rest Z 0.479 to 0.481
  at idle; 0.470 to 0.590 in walk, against v004's 0.390 to 0.590).
- f001 under the same method, for comparison: `surface_contacts_f001.json`.

The vertex-based check (`jacket_finish_check.py`, 97 samples) is also in the manifest. It finds no trouser point
outside the cloth at rest and the same 0.03 mm walk graze as f001. Its "6 cloth vertices in a hand" are the
subdivision points on v004's sleeve-end caps described in the f001 notes.

## Files and checksums

| Path | What |
|---|---|
| `jacket_finish_f002.glb` | sha256 `4cbac9bad20fb1986ce92bedc2271f54ce0fe8c4076ec21cc2d6730b288bf3e1`. Three skinned parts on the 17-bone rest copy, 44,388 tris, no actions, cameras or lights. |
| `jacket_finish_f002_manifest.json` | Per-part counts, bounds, held-vertex movement and weight identity, vertex-based clip checks, GLB accounting. |
| `surface_contacts_*.json` | Surface contact sets for held v004, f001 and f002, and the held-vs-f002 difference. |
| `jacket_finish_f002_materials.json` | Unchanged from f001: jacket and trim materials as v004; scarf base colour linear (0.200, 0.112, 0.058). |
| `jacket_finish_f002_comparison.png` | Reference crop; held, f001 and f002 at both cameras, whole and close, colour and clay. |
| `jacket_finish_f002_boundaries.png`, `jacket_f001_notch_diagnostic.png` | The boundary close-ups and the step diagnostic. |

| Part | Vertices (source / GLB) | Triangles | Held v004 vertices | Weights of held vertices |
|---|---|---|---|---|
| `SCULPT_JACKET_LONG` | 17,158 / 18,548 | 34,304 | 4,294; 1,435 moved over 0.1 mm, max 4.5 mm | identical |
| `SCULPT_JACKET_LONG_TRIM` | 3,516 / 4,668 | 6,980 | 3,516; 3,319 moved, max 3.8 mm (f001: 20.6) | identical |
| `SCULPT_JACKET_POCKETS` | 1,560 / 1,560 | 3,104 | new, as f001 | from the nearest jacket vertices |

GLB re-imported: every vertex matches a source vertex within 20 micrometres with identical weights. `verify_candidate.py`
on the working file: `FROZEN_ALL_UNCHANGED True`. Rebuild from `work/jacket_candidate_v004.blend` gives identical
positions in all three parts.

## Honest issue list

1. The surface method shows crossings but not their depth, and proves nothing where no partner triangle is crossed.
   It replaces the vertex counts' density bias, not a cloth solver.
2. The hem roll crossing the trousers and the sleeve-end caps at the wrist are pre-existing v004 conditions, not fixed
   here.
3. The front edge and cuffs are now close to v004's look. The "flatter facing" of f001 is reduced in exchange for a
   clean outline, as the brief preferred.
4. Pockets and the neck colour remain interpretations. Nothing native.

## Rebuild

`build_scripts/jacket_finish_f002_build.py` on `work/jacket_candidate_v004.blend`; then
`gather_adjust/gather_handclear.py` (study copy, scratch only), `build_scripts/jacket_finish_check.py` (vertex checks
and export) and `build_scripts/jacket_contact_check.py` (surface contacts; `GARMENT` env for the held two-part run).
The f001 script gained `FIN_STEPS` for the step diagnostic; its default still rebuilds f001 exactly.
