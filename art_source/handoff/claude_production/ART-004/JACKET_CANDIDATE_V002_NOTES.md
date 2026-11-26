# ART-004 jacket candidate v002: torso, sleeves and soft trim

Status: delivered for Codex's in-memory native study. Answers the six-point brief at `367f484`. Not a parity
claim, not ready_for_user_review, not for playable integration. Head v007, collar v002, trousers, boots, hands,
pack, rig, weights, actions and socket are untouched.

## Files

| Path | Purpose |
|---|---|
| `jacket_candidate_v002.glb` | For Codex. Two skinned meshes, `SCULPT_JACKET` and `SCULPT_JACKET_TRIM`, on a rest copy of the 17-bone skeleton (`SimmRigRestCopy`). No animation, camera or light. sha256 `c985517f0f8519e8f4e56d599a8ef99dd25bf6eb39c96ecb0ef8d67e314f2e61`, 478,704 bytes. |
| `jacket_candidate_v002_vertex_map.json` | Per part: original `PROTECTED_BODY` vertex index, original rest position, candidate position. sha256 `21691fad3d474ae263e6cc563396ca9d58e01d6905b761dcb4c85365f5eff04f`. |
| `renders/jacket_v002_before_after_clips.png` | Colour, reference angle and side: idle 0 percent, walk 25 and 75 percent, gather 50 percent. Top row frozen body, bottom row v002. |
| `renders/jacket_v002_before_after_rest.png` | Colour, rest pose: front, side, back, reference angle. Top row before, bottom row after. |
| `renders/jacket_v002_clay_ref.png`, `_clay_alt.png`, `_colour_ref.png`, `_colour_alt.png` | Full figure at the two agreed camera directions. Blender Cycles, review only. |
| `build_scripts/jacket_build.py` | Deterministic build on `collar_packet_v002.blend`. Now holds v002; v001 is in Git at `43144e9`. |
| `build_scripts/jacket_hand_sweep.py`, `jacket_hand_sweep.json` | New. Read-only measurement of where the frozen hands and thighs travel in the three clips, and its result, which the build reads. sha256 of the data `3239014815bbad34efea3ff300ad43a20eda8ba47f0f7b822b1206870503fe02`. |
| `build_scripts/jacket_export_check.py` | Rewritten. Per-part preservation asserts, clip measurements, export, full re-import accounting. |
| `build_scripts/jacket_review_prep.py` | Review renders only. |

No `.blend` is committed. It rebuilds exactly with:
`blender -b collar_packet_v002.blend --python build_scripts/jacket_build.py -- <absolute path>.blend`

## What to replace in the in-memory study

Same as v001. Hide the two original surfaces, material `Simm golden canvas jacket.001` (4,136 triangles) and
material `Simm golden seam binding.001` (3,528 triangles). Add `SCULPT_JACKET` and `SCULPT_JACKET_TRIM` on the
live skeleton, bind indices remapped by bone name as you did for v001. Keep everything else, including the frozen
brass button: it is now seated (point 3 below). The trim is its own named mesh so it can be switched off.

## Part manifest

| Object | Source verts | In the GLB | Tris | Material | Skin | Bounds, Blender axes, metres |
|---|---|---|---|---|---|---|
| `SCULPT_JACKET` | 2,074 | 2,778 | 4,136 | `SCULPT_MAT_JACKET`, flat, linear 0.723, 0.381, 0.027 | original weights, at most 2 influences; chest, spine, hips, upper arms, forearms | X -0.302..0.302, Y -0.137..0.140, Z 0.545..0.974 |
| `SCULPT_JACKET_TRIM` | 1,644 | 2,828 | 3,240 | `SCULPT_MAT_JACKET_TRIM`, flat, linear 0.468, 0.22, 0.019 | original weights, 1 influence: front rolls 100 percent `spine`, cuff rolls 100 percent `forearm_l` or `forearm_r` | X -0.306..0.306, Y -0.141..0.049, Z 0.593..0.965 |

Total 7,376 triangles. Both colours are the frozen materials' own base values. Both original UV layers are kept
on both parts. Pivot at the actor origin, identity transforms. Provenance: every vertex is an original vertex of
`PROTECTED_BODY` from `START_HERE_v02.blend`, moved. Nothing new was modelled and nothing was generated.

## The six points of the brief

1. **Hand overlap, hem not lowered.** The hem's lowest point is still Z 0.545. `jacket_hand_sweep.py` measures
   where the hands and the trousers travel over 17 samples of each clip, in hips and forearm rest space. The
   bottom band of the jacket is then drawn to one smooth outline that clears the swinging thighs by 7 mm and the
   hands by 6 mm. In 14 of 72 directions, at both hips, there is under 6 mm of room between the swinging thigh
   and the hand, so no outline clears both. There the hem is lifted to just above the height the hand reaches:
   a side vent, up to 80 mm, in 21 of 72 directions. Result in my samples: 0 jacket vertices in a hand in all
   three clips (v001: 10, up to 8.2 mm, in gather).
2. **Rolled front edge and cuff lip, sewn hem.** The two original front placket strips and the two original cuff
   rings are reshaped into soft round rolls, 15 mm thick at the front and 12 mm at the cuffs. The pocket strips
   and 12 two-triangle fragments are left out (204 vertices). No dense piping is back. The hem follows one smooth
   outline instead of each trouser detail.
3. **Button.** Both front rolls come forward at chest height so that the frozen button sits on the roll: its
   back face is 1.9 to 2.9 mm from the roll surface. The button itself is not touched and stays in the scene.
4. **Strap contact.** The cloth is lifted under each strap and pack vertex toward its old seating height. The 39
   tracked strap vertices sat up to 11.8 mm (mean 5.9 mm) above the old jacket. They now sit up to 12.9 mm
   (mean 6.4 mm) above the new one; v001 was 14.5 mm (mean 7.0 mm). 2 are under the cloth. 3 were still more
   than 1.5 mm high after the last pass. Measured in 3D at rest, not from one view.
5. **Every exported vertex accounted for.** The delivered GLB is re-imported and each of its 5,606 vertices is
   matched to a source vertex by position within 20 micrometres, trying every coincident source vertex. Unmatched:
   0 of 2,778 and 0 of 2,828. Source vertices covered: 2,074 of 2,074 and 1,644 of 1,644. Largest weight
   difference 0.0000000. The run fails on any unmatched vertex, uncovered source vertex or weight difference
   above 0.00001. The v001 gap of 26 came from rounding positions into 10-micrometre buckets, not from the file.
   Skeleton in the GLB: 17 bones, names and parents match, largest rest joint difference 0.0000007 m, no
   animation. `verify_candidate.py`: `FROZEN_ALL_UNCHANGED True` (body, old head, rest matrices, socket, actions).
6. **Before and after.** In `renders/`, with side views. Surfaces to replace and trim binding are stated above.

## Preservation report (asserted, the export fails otherwise)

- `SCULPT_JACKET` is exactly the original jacket vertex set and its faces: 2,074 of 2,074 vertices, 4,136 of
  4,136 faces. `SCULPT_JACKET_TRIM` is a subset of the original seam binding: 1,644 of 1,848 vertices, 3,240 of
  3,528 faces, every kept vertex with all of its original faces.
- Vertex group names and order identical to `PROTECTED_BODY`. Every weight on every vertex identical.
- No auto-rig, no weight transfer, no weight painting, no new vertex.
- Moved: jacket up to 67.3 mm (mean 11.2 mm), trim up to 24.8 mm (mean 9.6 mm).

## Other shape changes since v001

- The sleeve now opens 17 percent toward the cuff instead of gathering 10 percent. The frozen mitten hand is
  wider than a gathered sleeve end, and the cuff roll has to clear it. Sleeve end radius 43 mm, roll centre
  radius 51 to 52 mm, 2.5 to 2.8 mm of air to the hand over the clips.
- The hem is wider at the front and back than in v001, because it now clears the thighs' swing.

## Measured in Blender, 9 samples per clip, not native

Vertices inside another surface, worst sample of each clip. Nearest-surface test: a before and after comparison.

| Clip | Jacket in thighs, before | after | Jacket in hands, before | after | Trim in thighs, after | Trim in hands, after |
|---|---|---|---|---|---|---|
| idle | 48 | 8 | 0 | 0 | 0 | 0 |
| walk | 48 | 8 | 0 | 0 | 0 | 0 |
| gather | 48 | 10 | 0 | 0 | 3, up to 35.8 mm | 0 |

Farthest trim vertex from the jacket surface: 22.4 to 22.8 mm in all three clips (original binding: 13.8 to
21.1 mm). It does not grow with the pose: it is the outer side of the cuff roll.

## Known issues

- **Side vents.** The hem arches up by as much as 80 mm at each hip. It is visible in the side view. It is the
  price of clearing both the thigh and the hand there. If it reads wrong natively, the choice is between the
  vent, a trouser corner through the hem in walk, or the hand touching the hem in gather. I chose the vent.
- **v001 had a fault I missed.** In walk the leading thigh came through the lowered hem. My v001 note said I saw
  no thigh breaking through; that was wrong, the clay frames were too small to show it. It showed in colour.
- In gather, 3 vertices of the lower end of a front roll pass up to 35.8 mm into the thigh at the worst sample.
  The roll is bound to `spine` and the thigh rises in the crouch.
- 3 hem-band vertices read as inside the trousers at rest by my test (deepest 31 mm). I did not track down
  where they are. Nothing shows in my frames.
- The cuff roll is a ring about 8 mm wider than the sleeve end, with a gap of about 2.5 mm between them.
- The hem edge has small regular bumps from the original hem vertices.
- The folded-hood piece on the chest sits up to 14.1 mm above the shoulders, as it did on the old jacket (12.0 mm).
- Hem height is unchanged from v001 and still far from the reference's 0.47 to 0.50. Topology is the original's.
- Flat colours. Not seen in Godot. Samples, not continuous motion: between samples I have no evidence.

## Proposed next action

Codex: the same in-memory study. Please look first at the side vents in walk and gather, and at the cuff rolls.
If the vents are rejected, I need your call on which of the three faults above is the least bad, or approval to
propose a weighting exception for the hem band, which is 100 percent `hips` today.
