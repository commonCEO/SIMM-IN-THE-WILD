# ART-004 jacket candidate v004: one longer jacket (Codex brief at 6532120)

Status: review candidate for Codex's native fit check. Not approved; A1 still needs the user. Jacket v003 is archived
unchanged (`jacket_candidate_v003.glb`, sha `e53ebe5d...`, and its .blend). No animation is bundled: the corrected
gather stays Codex's separate relative-copy integration.

## What changed

The lower panel prototype is now part of the jacket itself, not a layer hanging under the old hem.

- **One surface.** Jacket v003's torso is a closed shell with thickness, open at the front. It is cut once at
  Z 0.655 (one clean loop, 148 vertices: outer face, both front edges, inner face) and everything of the torso below
  that line is removed (296 v003 vertices, highest at Z 0.651). The cut loop is carried straight down as 16 new rows
  to the new hem at Z 0.480. The outer face, front edges and inner face continue without a seam, so there is no
  doubled or scalloped join. Non-manifold edges: 0. A flat cap closes the bottom, under a hem roll.
- **Shape.** Each row is pushed out by one offset per direction: a gentle 16 mm flare at the hem, raised where needed
  to keep 16 mm of air over the frozen trousers and never under 12 mm. Outer and inner faces normally share the
  offset, so the cloth keeps v003's thickness (up to 7 mm). Where a resting hand leaves less room (at the hips: 58 of the
  2,304 direction-and-row cells), the outer face stops short of the hand and the inner face gives way to 8.5 mm over
  the trousers, thinning the cloth to no less than 2 mm there.
- **Weights.** Each new column starts with the cut loop's own original weights and blends to hips plus a thigh share
  at the hem (0.6, softer at the back centre; the prototype's rule). New this version: the sides reach their thigh
  share sooner, because the swinging thigh has no spare room under the resting hand. New vertices use only `hips`,
  `spine`, `thigh_l`, `thigh_r`, at most 4 influences, normalised.
- **Front edges.** The v003 placket rolls keep every ring above Z 0.665, with identical positions and weights. Below
  that, each continues down the new front edge as a matching roll (26 rings, same 7.5 mm section, eased onto the
  kept ring) to the hem. Its weights are the jacket's own, averaged from the 8 nearest vertices and smoothed along
  the roll.
- **Hem roll.** A 6.5 mm roll of the trim material runs round the hem from one front corner to the other, weighted
  the same way.
- **Held, by evidence.** Everything above the cut: 1,778 jacket and 1,596 trim vertices keep v003's exact positions
  and weights (checked vertex by vertex: largest move 0, largest weight difference 0). That covers sleeves, cuff
  rings, chest, neckline, the strap and pack seating, and the upper plackets. Head v009, collar v004, boots v002, pack,
  trousers and material base values are untouched (GLBs re-hashed: `255f781e...`, `b093418b...`, `f430933f...`).

## Files

| Path | What |
|---|---|
| `jacket_candidate_v004.glb` | sha256 `2b73bba6a02a1dc1e83fb4be6a2ac4ce64565b4238fe8cc4ccd9d88657b66fe6`, 836,676 bytes. Two skinned parts on the 17-bone rest copy, no actions, cameras or lights. |
| `jacket_candidate_v004_manifest.json` | Parts, counts, bounds, bones, kept/new/removed vertex counts, source checksums, every residual with clip, frame and vertex ID, the GLB accounting. |
| `build_scripts/jacket_long_build.py` | Builds v004 from `work/boot_candidate_v002.blend` (sha `848c79b4...`). |
| `build_scripts/jacket_long_check.py` | Manifest and held-area checks, the 97-sample clip measurements, export and re-import accounting. Fails on a missing or duplicate part, a moved v003 vertex, more than 4 influences, or any unaccounted GLB vertex or weight. |
| `renders_jacket_v004/` | Five sheets and the check log (below). |

Rebuilt from scratch twice: identical GLB.

## Parts (re-imported GLB)

| Part | Replaces | Vertices in file | Triangles | Material | Bounds, Blender Z-up (m) |
|---|---|---|---|---|---|
| `SCULPT_JACKET_LONG` | `SCULPT_JACKET` | 5,002 (4,294 in Blender: 1,778 v003, 2,516 new) | 8,576 | `SCULPT_MAT_JACKET` | (-0.301, -0.145, 0.480) to (0.301, 0.149, 0.974) |
| `SCULPT_JACKET_LONG_TRIM` | `SCULPT_JACKET_TRIM` | 4,668 (3,516: 1,596 v003, 1,920 new) | 6,980 | `SCULPT_MAT_JACKET_TRIM` | (-0.300, -0.148, 0.479) to (0.300, 0.153, 0.965) |

Total 15,556 triangles. Both parts are children of `SimmRigRestCopy` at the origin with identity transforms; glTF
Y-up, metres, front -Y in Blender. Every GLB vertex matches a source vertex within 20 micrometres with identical
weights, and every source vertex is covered. `verify_candidate.py` on the working file: `FROZEN_ALL_UNCHANGED True`
(body, old head, rig, socket, the three actions). The trim has 36 open edges, all on kept v003 vertices (Z 0.649 to 0.965;
none touch new geometry). v003's trim had 48.

UVs: kept vertices keep their UVs; new faces have none, which is fine for the flat material. Textures and stitches
wait, as the brief says.

## Measured in Blender, 97 samples per clip (sampled, not continuous)

The corrected gather was measured as a study copy of `gather_handclear` added to a scratch file, built by
`gather_adjust/gather_handclear.py`. It is not in the working file or the GLB.

| Clip | Trouser points through the cloth | Cloth vertices in a hand | Smallest hand gap | Closest covered trouser point | Stretch, new edges (jacket / trim) |
|---|---|---|---|---|---|
| idle | 0 | 0 | 0.01 mm (frame 2.81, jacket vertex 2746) | 3.8 mm | 1.01 / 1.01 |
| walk, first half | 1 (body vertex 1174, 0.18 mm, frame 6.0) | 0 | 2.97 mm | 0.0 mm | 1.36 / 1.22 at frame 6 |
| walk, second half | 1 (body vertex 1183, 0.07 mm, frame 18.0) | 0 | | | 1.36 / 1.19 at frame 18 |
| gather_handclear (corrected) | 0 | 0 | 0.15 mm, at frame 0 (rest) | 3.7 mm | 1.16 / 1.00 |
| gather (original, negative control) | 0 | 35, up to 8.1 mm, frame 12 | | 3.7 mm | 1.16 / 1.00 |

Every residual, with frame and vertex ID, is in the manifest's `residuals` list. Not clean, stated plainly:
- **Walk:** two trouser vertices on the ring at Z 0.59 graze the cloth for a sample or three around the passing
  frames: 1174 (back of the left-side thigh, +X) by 0.18 mm at frame 6, 0.01 mm at 5.75 and 6.25; 1183 (front-side
  thigh, +X) by 0.07 mm at frame 18. Prototype v2 had 3 points up to 1.3 mm at rest; at rest these are now 3.8 mm
  clear.
- **Hand margin at rest is about zero.** At the left hip (+X, jacket vertex 2746, Z 0.589) the resting hand sits
  about 10 mm off the trousers. Floor, cloth and air cannot all fit there, so the cloth touches without passing in
  (gap 0.01 mm in idle, 0.15 mm in the corrected gather's rest frame). During the corrected gather itself the hand
  moves away from the cloth; the smallest gap is at its rest frame. The original gather still puts the hand 8 mm
  into the cloth, as expected for the negative control.
- **Held v003 stretch.** The largest stretch in the whole garment, 1.60 in walk and 2.11 in gather, is on held v003
  edges in the armpits (Z 0.89 to 0.91, between `chest`/`upper_arm` and `upper_arm` vertices). Those edges and
  weights are identical to v003, so v003 behaves the same. Out of scope for this brief; reported, not fixed.

## Frames (`renders_jacket_v004/`)

- `jacket_v003_v004_reference_comparison.png`: the approved reference beside v003 and v004 at the reference and side
  cameras in colour, plus clay front and side. Same lights, cameras and framing for both.
- `jacket_v004_full_clay.png`, `jacket_v004_full_colour.png`: front, reference (`ref`), alternate (`alt`) and side.
- `jacket_v004_close_join_hands.png`: the cut line (no visible join), the resting hand at the hip, front edges, hem.
- `jacket_v004_close_walk_gather.png`: walk frames 6 and 18; corrected gather and ORIGINAL gather at frame 12.
- `jacket_v004_check_97_samples.txt`: the check log.

Proportion: the hem is now at Z 0.480, about a third of the figure's height, in line with the reference (about 0.33).
That is a measurement against the reference, not a claim of parity.

## Provenance and licence

The kept geometry is the Blender Studio CC0 base, via jacket v003. Everything new is scripted here. No generators,
purchased assets or outside services.

## Open issues

1. Hand margin at the left hip at rest is about zero (above). Options, for Codex or the user to choose: accept a
   graze at rest; thin the cloth there to about 1 mm; or a small rest-arm change, which is protected and not mine
   to make.
2. Two sub-millimetre trouser grazes in walk (above).
3. Held v003 armpit stretch (above).
4. Frozen trouser pocket flaps sit just under the hem at the front and touch its edge in walk frame 6 (see the walk
   sheet). They are frozen geometry, below the cloth, not counted as breakthroughs.
5. Not done here: native Godot fit, game-scale camera, continuous motion, performance.

## Proposed next action

Codex binds `jacket_candidate_v004.glb` in place of v003 on the original rig and checks idle, walk and the relative
corrected gather natively. If the whole-silhouette candidate holds, the next Fable step is the one Codex names:
probably the hand-margin choice above, then texture and stitch work.
