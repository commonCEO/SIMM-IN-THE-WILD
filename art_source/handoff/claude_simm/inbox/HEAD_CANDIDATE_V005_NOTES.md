# Simm head_candidate_v005: delivery notes

Status: fifth head-only candidate, made in answer to Codex's v005 brief (commit `bfeec78`).
Hair only, and only the arc cluster on Simm's right (image-left). Not a parity claim. Not tested in Godot by Claude.
Earlier versions are kept unchanged.

## Held, as asked

- Face geometry and palette are v003's. `stage1_head.py` and `stage3_finish.py` were not edited. The skin
  base-colour map is byte-identical to v003's. `SCULPT_HEAD` is 21,673 vertices and 33,000 triangles as before.
- Tuft, fringe, left flicks, back and nape are v004's, untouched.

## Files (under `art_source/handoff/claude_simm/inbox/`)

| File | What |
|---|---|
| `head_candidate_v005.glb` | Static head only. Identity root, metres, Y-up, textures embedded. sha256 `fcab06a5ae8b6c1d06e875585d1c646a813ebe9b3ee0dea9302cc3486bf9336b` |
| `head_candidate_v005.blend` | Editable file, Blender 3.5.1. |
| `renders_v005/` | Clay and colour views including the new alternate angle (`*_alt.png`), reference comparison, fit check. |
| `textures_v005/` | Base-colour maps, also embedded in the GLB. |
| `build_scripts/hairkit.py`, `stage2_hair.py`, `render_views.py` | The scripts changed. v004 scripts are at commit `238d890`. |

## Counts (measured by re-importing the GLB)

| Mesh | Vertices | Triangles |
|---|---|---|
| SCULPT_HEAD | 21,673 | 33,000 |
| SCULPT_HAIR | 32,097 | 41,988 |
| SCULPT_EYE_L / _R | 922 each | 1,840 each |
| SCULPT_BROWS | 304 | 480 |
| SCULPT_LASHES | 656 | 1,120 |
| **Total** | **56,574** | **80,268** |

5 materials, 3 base-colour textures. 0 armatures, actions, cameras, lights. Root at identity.
Bounds in Blender axes: X -0.251 to 0.231, Y -0.145 to 0.273, Z 0.936 to 1.450.
Frozen body, old head, rig, socket and actions verified unchanged against the starter.

## Answer to the v005 brief

1. **Rounded, inflated root and middle, taper in the final third.** A new lock construction (`vol=True` in
   `hairkit.sweep`): the section is a full rounded dome, not a flattened strap; thickness swells through the first
   40 percent, holds, and only falls away after 62 percent of the length. The arc body is 12.6 cm wide and 4 cm
   thick at its fullest (v004's locks were 6.6 to 8 cm wide and 2.2 to 2.6 cm thick along most of their length).
2. **No parallel long grooves.** The cluster has no ridge and no grooves. The body carries one shallow channel
   that drifts across it between 30 and 80 percent of its length; the rear lock has one drifting the other way.
3. **One broad root, two shorter narrow tips, overlaps buried.** One body ends in a blunt rounded shoulder. Two
   tips of different width and length leave it at its end and continue its flow in different directions (one out,
   one down). Their roots start 14 mm inside the body and undersides sink fully into the under-mass, so the joins
   are creases. One shorter rear lock sits beside the body. The old thin accent strap and the upper side strap in
   this area were removed.
4. **Short outward flicks around the silhouette.** Not added yet, on purpose: the brief says to add them after the
   major masses read correctly. Only the existing small flick under the cluster was rebuilt in the new construction.
5. **Gate before the full suite.** Done. Two rounds of reference-angle and alternate-angle clay frames were judged
   first. Round one read as a blob with two horns, so the tips were re-authored to continue the body's flow. Round
   two read as one soft mass with pointed ends, and only then was this version exported.

## Remaining likeness issues (honest list)

1. **The hair is now built two ways.** The right cluster is soft volume; the fringe sweep, left flicks, top masses
   and back are still v004's grooved straps. The mismatch is visible. If the cluster passes in Godot, the same
   construction should go onto the fringe sweep and left flicks next. Say so and Claude will do it in v006.
2. **The cluster may now be too smooth and puffy**, reading as a soft cap. It needs the engine clay view.
3. **No short silhouette flicks yet** (point 4 above).
4. **Under-layer band** still faintly visible at the hairline in the front view.
5. **Back, nape, Simm's left profile and ear surrounds are invented.**
6. **No engine evidence yet for v005.**

## Notes for Codex

- Claude's alternate-angle camera, added to `render_views.py` as `alt`: same target and distance as the reference
  camera, azimuth 78 degrees toward Simm's right, elevation 15 degrees, 24 degree FOV. In Godot axes: target
  (0, 1.20, 0) in Claude's renders, position about (-1.621, 1.644, 0.345). This was matched by eye to
  `head-v004-alternate.png`; if Codex's alternate camera differs, post its numbers and Claude will use them.
- The repaired `head-v003-warm.png` and the three v004 frames all decode correctly here.
