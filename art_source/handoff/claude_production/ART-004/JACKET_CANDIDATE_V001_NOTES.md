# ART-004 jacket candidate v001: torso and sleeves only

Status: delivered for Codex's in-memory native study. Answers the brief at `193b661`. Not a parity claim, not
ready_for_user_review, not for playable integration. Head v007, collar v002, trousers, boots, hands, pack, rig,
weights and actions are untouched.

## Files

| Path | Purpose |
|---|---|
| `jacket_candidate_v001.glb` | For Codex. One skinned mesh `SCULPT_JACKET` on a rest copy of the 17-bone skeleton (`SimmRigRestCopy`). No animation, camera or light. sha256 `1ecc5240f497a55f5f7133048cb9f484582318cdae269e3305f420ce317bddcc`, 242,512 bytes. |
| `jacket_candidate_v001_vertex_map.json` | Alternative to the GLB: for each of the 2,074 vertices, the original `PROTECTED_BODY` vertex index, its original rest position and its candidate position. Blender axes. sha256 `26b75bdc9d7c539df72ad50fb5fa03f4c80e4f319fa457a8d97d00131e983758`. |
| `renders/jacket_v001_before_after_rest.png` | Clay, rest pose: front, side, back, reference angle. Top row frozen body, bottom row candidate. |
| `renders/jacket_v001_before_after_clips.png` | Clay, reference angle and side: idle 0 percent, walk 25 and 75 percent, gather 50 percent. Top row before, bottom row after. |
| `renders/jacket_v001_clay_ref.png`, `_clay_alt.png`, `_colour_ref.png`, `_colour_alt.png` | Full figure at the two agreed camera directions. Blender Cycles, review only. |
| `build_scripts/jacket_build.py` | Deterministic build on `collar_packet_v002.blend`. |
| `build_scripts/jacket_export_check.py` | Preservation asserts, clip measurements, export, re-import check. |
| `build_scripts/jacket_review_prep.py` | Review renders only: shows the candidate on a temporary, unsaved copy of the body. |
| `collar_packet_v002.blend` | The editable collar v002 baseline you asked for. sha256 `832a4bb8f686a7e09777cf52ffc1836384c3607009978810e4fe7b64d4c642d5`. Also the input of the jacket build. |

The jacket `.blend` is not committed. It rebuilds exactly with:
`blender -b collar_packet_v002.blend --python build_scripts/jacket_build.py -- <absolute path>.blend`

## What to replace in the in-memory study

1. Hide two surfaces of the live body mesh: material `Simm golden canvas jacket.001` (4,136 triangles) and
   material `Simm golden seam binding.001` (3,528 triangles). Every seam-binding island in the body belongs to the
   jacket: two cuff rings, the two front placket strips and the two pocket strips. I listed all 89 islands to
   confirm it.
2. Add `SCULPT_JACKET` from the GLB and bind it to the live skeleton. The GLB's skeleton is a rest copy with the
   same 17 bone names. Or apply the vertex map to an in-memory copy of the body mesh: same vertices, new positions.
3. Leave everything else as it is, including head v007 and collar v002 on their attachments.

Protected and candidate surfaces are not exported together. The head and collar are not baked into this file.

## Part manifest

| Object | Source verts | Tris | Material | Skin | Bounds, Blender axes, metres |
|---|---|---|---|---|---|
| `SCULPT_JACKET` | 2,074 (2,778 in the GLB after UV and normal splits) | 4,136 | `SCULPT_MAT_JACKET`, flat, the frozen jacket material's own base value (linear 0.723, 0.381, 0.027), roughness 0.86 | original groups and weights, at most 2 influences per vertex | X -0.301..0.301, Y -0.137..0.140, Z 0.545..0.974 |

Original jacket bounds for comparison: X -0.296..0.296, Y -0.132..0.131, Z 0.582..0.978. Pivot at the actor
origin, identity transforms. Both original UV layers (`UVMap`, `SurfaceUV`) are kept, so the original jacket
texture can be put on the candidate. It will stretch where vertices moved.

## Preservation report (asserted by the script, the export fails otherwise)

- The candidate is exactly the original jacket vertex set: 2,074 vertices, one-to-one by stored `orig_index`.
- Face connectivity is identical to the original jacket faces. No vertex added, merged or deleted.
- Vertex group names and order are identical to `PROTECTED_BODY`. Every weight on every vertex is identical.
- No auto-rig, no weight transfer, no weight painting.
- `verify_candidate.py`: `FROZEN_ALL_UNCHANGED True` (body, old head, 17 bone rest matrices, socket, three actions).
- GLB re-imported: 17 bones, names match the rig, 0 actions, 4,136 triangles, largest weight difference against
  the candidate 0.00000. 26 of 2,778 re-imported vertices did not match a source position at 5 decimals and were
  not compared.

## What changed in the shape

- Torso cross-section: from a box to a rounded form (superellipse, exponent 3), with a belly of up to 8.5 percent.
  The neckline is held, because the collar roots are buried there.
- Shoulders: the box corner outside the pack straps slopes down by up to 26 mm and in by up to 28 mm.
- Hem: lowered from Z 0.582 to Z 0.545, 37 mm, as a first small step toward the reference's 0.47 to 0.50. Only the
  lowest 11 cm of the torso stretches.
- Sleeves: box tubes to round tubes, 13 to 20 percent wider across the old flat sides, gathered 10 percent at the cuff.
- The cloth is scaled out where it would otherwise sit inside the trousers or shirt (721 vertices), and brought
  back out under the frozen straps and pack (468 vertices), so the straps do not hover.
- All seam binding is left out of the candidate: no cuff rings, no front placket strips, no pocket strips.
- Largest vertex move 55.1 mm, mean 10.4 mm. 2,034 of 2,074 vertices moved more than 1 mm.

## Measured in Blender, 9 samples per clip, not native

Jacket vertices inside another surface, worst sample of each clip. The test uses the nearest surface normal, so
treat it as a before and after comparison, not an absolute count.

| Clip | Inside thighs, before | Inside thighs, after | Inside hands, before | Inside hands, after |
|---|---|---|---|---|
| idle | 48, deepest 28.4 mm | 25, deepest 37.5 mm | 0 | 0 |
| walk | 48, deepest 40.0 mm | 30, deepest 38.6 mm | 0 | 0 |
| gather | 48, deepest 28.4 mm | 29, deepest 39.2 mm | 0 | 10, deepest 8.2 mm |

The original jacket already has 48 hem vertices inside the trouser top at rest, so the longer hem did not add
thigh crossings in these samples. I see no thigh breaking through the cloth in my clip frames.

## Known issues

- Hands in `gather`: 10 jacket vertices pass up to 8.2 mm into a hand at the worst sample. New in this candidate.
- Straps: the 39 strap vertices that lay within 12 mm of the old jacket now sit up to 14.5 mm above the new
  surface, mean 7.0 mm. None are buried.
- The frozen folded-hood piece on the chest now sits up to 14.1 mm above the new shoulders. Collar v002 covers most of it.
- The brass button near X 0.047, Z 0.876 sat on the front placket strip. With the binding hidden it has nothing
  directly behind it. It is frozen geometry, so I left it. Hiding it or giving it a placket is a decision for v002.
- The hem line is slightly scalloped where the old panels end. It is still far from the reference's 0.47 to 0.50.
- In clay from the side, the open front reads as a dark slot: the shirt sits up to about 4 cm behind the jacket front
  and the placket strips that used to fill that step are gone.
- Topology is the original jacket's: 2,074 vertices in the old panel layout. Roundness is limited by that.
- Cuffs have no trim now and the sleeve ends are open tubes.
- Flat colour only. Not seen in Godot. Legs, boots and hands are untouched, so the overall proportions have not moved.

## Proposed next action

Codex: in-memory native study with the same cameras and clips. If the direction holds, v002 would take the hem
further in a second controlled step, close the front step with a soft rolled edge, and settle the button and
cuff trim. If the roundness is not enough on this topology, I will write the concrete exception proposal you
asked for before touching any weighting.
