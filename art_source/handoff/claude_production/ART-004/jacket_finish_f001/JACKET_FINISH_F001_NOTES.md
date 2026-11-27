# ART-004 jacket + neck finish candidate f001 (Codex brief at b87f56a)

Status: ONE comparison candidate on the held jacket v004 fit, for Codex's non-saving native study. Not approved; A1
unpassed. Held as controls, unchanged: jacket v004 (`../jacket_candidate_v004.glb`), collar v004 geometry, boots
v002, head v012 + m001-B, the body, rig, rest pose, actions and socket. Envelope, hem length, hand-clear fit and strap
paths are kept; no garment length or weight experiments were reopened.

## What changed

| Change | How | Visible result (my reading of the renders) |
|---|---|---|
| Cloth folds | One smooth displacement field from rest position, applied the same way to the jacket shell (outer and inner faces) and the trim, so thickness and seating hold. Soft rings across the inner elbow (up to 3.6 mm, 24 mm apart), a gentle wave below the front of the shoulder (up to 2.2 mm), and low waves round the lower band (up to 3.8 mm, 7 round the body). They fade to nothing where the hands hang (about +-82 degrees) and above the waist. | Soft folds at the elbows; the hem waves are subtle. |
| Mesh for the folds | The v004 sleeves had 408 vertices each, too coarse to carry folds. The jacket is subdivided once: 4,294 to 17,158 vertices. Original vertices keep their v004 weights exactly (asserted); the 12,864 new ones have interpolated weights, cleaned of influences under 0.01 and renormalised. | Needed for the folds to show at all. |
| Front edges, hem and cuffs | The trim rolls are flattened toward the jacket surface (height x0.4), so they read as a thick cloth facing, not tubing. The two cuff rolls are also doubled along the arm into bands (about 11 to 22 mm), growing toward the elbow only so the wrist edge stays put. Positions only; trim weights identical to v004. | Flatter front edges; cuffs read as bands. |
| Pockets (interpretation) | Two low patch pockets with a flap on the lower front (+-45 degrees, centre Z 0.548), a separate part `SCULPT_JACKET_POCKETS` in the jacket colour, weighted from the nearest jacket vertices (at most 4 influences). The low-resolution reference does not clearly show lower pockets, so this is my interpretation of Codex's cue. Being a separate part, it can be dropped. No stitching added: the reference doesn't support a pattern. | Pockets read at both cameras. |
| Neck | The scarf (`SCULPT_MAT_SCARF`, collar v004) was cream, the conspicuous "white ring". Now a warm shirt-like brown (linear 0.200, 0.112, 0.058; about sRGB 124, 93, 67), reading as a layer between the shirt and the yellow hood. Geometry unchanged. The reference does not establish a scarf pattern; this is an interpretation. | No white ring; a quiet brown layer. |

No decorative hardware, no new outfit pieces, no rig or body edits.

## Checks (97 samples per clip; same script run on held v004 for a like-for-like baseline)

| Clip | Held v004 | f001 |
|---|---|---|
| idle: trousers through the jacket / cloth in a hand / straps inside the jacket | 0 / 0 / 0 | 0 / 6 (see below) / 0 |
| walk | 1 (0.01 mm) / 0 / 0 | 2 (0.03 mm) / 6 (see below) / 0 |
| gather_handclear (study copy) | 0 / 0 / 4 at frame 10 | 0 / 6 (see below) / 4 at frame 10 |
| gather (original, negative control) | 0 / 35, 8.11 mm / 4 | 0 / 139, 8.06 mm / 4 |
| Smallest hand gap: idle / walk / handclear | 0.01 / 2.97 / 0.15 mm | 0.00 / 0.91 / 0.14 mm |

Reading these honestly:
- **The 6 "cloth in a hand" vertices are not new geometry.** They are subdivision points lying exactly (0.0000 mm) on v004's own downward-facing sleeve-end triangles at Z 0.651, inside the cuff where the hand enters. v004's sleeve end already crossed the wrist; it had no vertex there for the vertex-based test to find. Same cause for the higher original-gather count (139 against 35) at the same depth: more sample points on the same surfaces.
- **Straps:** no change (the same 4 strap vertices at gather frame 10 in both).
- **Collar:** checked at rest only. The jacket points inside the hood and scarf at rest from ORIGINAL v004 vertices are 38 and 10 in both files: that is the collar's existing tuck over the neckline. The extra counts with all vertices (130, 27) are subdivision points on the same faces. Held vertices above Z 0.85 move at most 2.0 mm (the shoulder fold on the sleeves).
- **Walk:** the smallest hand gap drops from 2.97 to 0.91 mm, still clear. Trouser grazes are the same sub-millimetre points as v004.

Manifests (`jacket_finish_f001_manifest.json`; held run in `held_v004_same_checks.json`):

| Part | Vertices (source / GLB) | Triangles | Held v004 | Weights of held vertices |
|---|---|---|---|---|
| `SCULPT_JACKET_LONG` | 17,158 / 18,548 | 34,304 | 4,294 vertices, 8,576 tris; 1,792 moved over 0.1 mm, max 3.8 mm | identical |
| `SCULPT_JACKET_LONG_TRIM` | 3,516 / 4,668 | 6,980 | same vertices; 3,500 moved, max 20.6 mm (the cuffs doubled along the arm) | identical |
| `SCULPT_JACKET_POCKETS` | 1,560 / 1,560 | 3,104 | new | from the nearest jacket vertices |

`jacket_finish_f001.glb`: sha256 `832b42fc2c4376e19d900c1028d2e0175450bdb8682951af532837e5bad8998b`, three skinned parts on the
17-bone rest copy, no actions, cameras or lights. Every GLB vertex matches a source vertex within 20 micrometres with
identical weights. Bounds and material per part are in the manifest. A rebuild gives identical positions, weights and
JSON; one normal on one jacket vertex differs by 0.00007 (float noise in the normal computation), so the checksum
can differ.

`verify_candidate.py` on the working file: `FROZEN_ALL_UNCHANGED True` (body, old head, rig, socket, actions); the
GLB has 44,388 triangles, 1 armature, 0 actions, cameras or lights.

Materials (`jacket_finish_f001_materials.json`): jacket and trim materials unchanged from v004; the pockets use the
jacket material; the scarf colour is the only material change. No textures.

## Frames

`jacket_finish_f001_comparison.png`: the approved reference crop beside held v004 and f001, whole figure and close,
colour and clay, at the `ref` and `alt` cameras. Camera, pose and scale differ from the reference: read the clothing
cues, not proportions. Lights, head and every other material are fixed.

## Honest issue list

1. The pockets and the brown neck layer are interpretations of a low-resolution reference.
2. The hem waves are subtle; the elbow folds carry most of the cloth read.
3. The trim still sits as a separate facing, flattened, not merged into the jacket edge.
4. The v004 sleeve-end caps cross the wrist (pre-existing, hidden by the hand); not fixed here.
5. Collar intersections were checked at rest only. Nothing native.

## Rebuild

`build_scripts/jacket_finish_build.py` on `work/jacket_candidate_v004.blend`, then `gather_adjust/gather_handclear.py`
(study action, scratch only) and `build_scripts/jacket_finish_check.py` (checks and GLB export).
