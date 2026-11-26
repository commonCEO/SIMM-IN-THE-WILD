# ART-004: gather calibration packet v001 (Codex request at d3f3a94)

Status: diagnostic for Codex's native check. Not a production candidate. Masters untouched.

## The cause, found and reproduced

Codex measured only 0.67 deg between the native `gather` and my `gather_handclear` at 0.4 s, and an exact match at
0.2 s. The cause is my export, not Godot and not an axis or sign problem:

- `gather_handclear.py` exported with `export_nla_strips=False`. In Blender 3.5 that merges every action the armature
  uses into one clip. The exporter warns "Some strips have same channel animation" and the merged clip took the
  ORIGINAL `gather` curve for `upper_arm_l`.
- So `gather_handclear_rig_only.glb` (sha `b99079c0...`) is the original gather under a new name. Its upper_arm_l
  pose relative to rest is a pure rotation about local -X (4.58 deg at 0.2 s, 9.17 deg at 0.4 s) with no Z part at
  all. Rebuilt from the starter today: byte-identical file, same result. That GLB is defective; please discard it.
- That also answers "why does the donor already match the native original at 0.2 s": it was the original.
- The 0.67 deg Codex saw at 0.4 s is therefore the difference between two copies of the ORIGINAL gather: the starter's
  action exported with 25 forced samples (key at frame 12 = -0.16 rad = 9.17 deg) and the native file's 11-key track
  (8.50 deg at 0.4 s by my decomposition of your quaternion against the rest rotation). I cannot see the native
  `simm.glb` from this branch, so I have not established why its track has 11 keys or reads lower at the peak. See
  "For Codex" below.

My Blender measurements in the first delivery (hand clear of the panel, 0 contacts versus 58) were made on the action
inside Blender, where the offset is real. Only the export was wrong. They still need your native check.

`gather_handclear.py` no longer exports a GLB; it stops with a message pointing to `calibration_export.py`.

## What is in the packet

| Path | Purpose |
|---|---|
| `gather_calibration_v001.glb` | sha256 `7caf4ab7719cf03f3a10e2f653236c0890e82bf962ee6c17fc4e68d660593d91`, 633,036 bytes. 17 original rest bones, two clips `gather` (original) and `gather_handclear`, 51 channels each, and one mesh `SCULPT_JACKET_SKIRT` (the lower-panel prototype v2) skinned to `hips`, `thigh_l`, `thigh_r`. No body, head, collar, boots, jacket v003, materials, camera or light. |
| `gather_calibration_v001_manifest.json` | Clip, mesh, skin and bone manifest; source-action fingerprints; frame/time mapping; re-imported samples; panel weights and transform. Written by the script. |
| `calibration_export.py` | Builds the GLB from a blend with the rig, both actions and the panel, then re-imports the GLB into an empty scene and measures the EXPORTED clips. It fails if the exported delta or the hand delta differ from the authored ones, or if any other bone differs between the clips. |

Build chain (all from committed scripts; rebuilt twice, identical GLB and manifest):
1. `jacket_long_proposal/skirt_prototype.py` on `work/boot_candidate_v002.blend` (sha `848c79b4...`), panel v2.
2. `gather_handclear.py` (action only).
3. `calibration_export.py`.

## Source-action fingerprints

sha256 over every F-curve's (data path, index, frame, value, interpolation), sorted:
- `gather` in the starter `START_HERE_v02.blend` (sha `1157d320...`): `dda54d1bb5912f6d538884bc51cf093246cae5ac253cd39e21a7482b46ea0161`
- `gather` in the build file: the same `dda54d1b...`, so the original action is untouched.
- `gather_handclear`: `6d38ab088f55f0ee9e5b880e8d8f32876f031cae408dee6a637af6c96f1dba0a`

Frame/time mapping: the source is 30 fps; time_s = frame / 30. Frame 6 = 0.2 s, 12 = 0.4 s, 18 = 0.6 s, 24 = 0.8 s.
The Blender importer converts with the SCENE frame rate (24 in a factory scene), so the check sets 30 fps first;
measuring at 24 fps would sample the wrong times.

## Measured on the re-imported GLB

upper_arm_l, glTF node rotation (XYZW, parent space, rest included), the same form as Codex's numbers:

| Time | `gather` (exported) | `gather_handclear` (exported) |
|---|---|---|
| 0.2 s | (0.973943, -0.153314, -0.166098, 0.018457) | (0.970494, -0.172375, -0.167233, 0.021463) |
| 0.4 s | (0.972426, -0.146550, -0.172096, 0.057389) | (0.964920, -0.184485, -0.175822, 0.063099) |
| 0.6 s | (0.973943, -0.153314, -0.166098, 0.018457) | (0.970494, -0.172375, -0.167233, 0.021463) |

Note the exported ORIGINAL at 0.4 s equals what you recorded as the DONOR at 0.4 s. That is the evidence for the cause.

Delta between the two exported clips, and the hand:

| Time | Angle between clips | Expected (4.5 * sin^2) | hand_l world delta, glTF Y-up (mm) | Same, authored in Blender |
|---|---|---|---|---|
| 0.2 s | 2.250 deg | 2.250 | (-10.07, +2.03, +3.80) | matches within 0.01 mm |
| 0.4 s | 4.500 deg | 4.500 | (-19.76, +3.27, +8.09) | matches within 0.01 mm |
| 0.6 s | 2.250 deg | 2.250 | (-10.07, +2.03, +3.80) | matches within 0.01 mm |

The delta axis in the bone's local frame is mostly Z, tilted by the X swing: (0, -0.08, 1.00) at 0.2 and 0.6 s,
(0, -0.16, 0.99) at 0.4 s.
At 0.4 s the hand moves about 20 mm outward (-X is Simm's right), 3 mm up, 8 mm in glTF +Z. My first notes said
22.6 mm at 4 deg; that figure came from a separate Blender probe. The exported clip gives 19.8 mm at 4.5 deg.

All other 16 bones: largest local-matrix difference between the two exported clips 1.8e-7 (float noise). Both clips
are 0.8 s with 25 linear samples per channel.

## Panel weights and transform

`SCULPT_JACKET_SKIRT`: 10,194 vertices, 20,384 triangles, object transform identity, child of the armature, Blender
Z 0.479 to 0.664 m. Bones: `hips` (all 10,194 vertices), `thigh_l` (6,473), `thigh_r` (6,471), at most 3 influences
per vertex. Weights rise from 100 percent hips at Z 0.655 to a 0.6 thigh share at the hem; full rule in
`../jacket_long_proposal/skirt_prototype.py`.

Unfinished, as labelled in the manifest: the join with jacket v003's hem is visible; 3 trouser points up to 1.3 mm at
rest (frame 0); largest edge stretch 1.37 in walk frame 6 (walk is not in this packet).

## For Codex

- Please bind this GLB's panel to the original skeleton and compare the two clips in the same native scene. Both
  clips come from the same export, so they are a paired control independent of the native model's own track.
- Your native original `gather` reads 8.50 deg at 0.4 s, the starter's 9.17 deg. If you can list the native
  upper_arm_l gather key times and values (11 keys), I can say whether it is a resample of the same curve or a
  different action. I am not assuming either.
- To apply the change to the native master later, the authored change is one channel: upper_arm_l `rotation_euler` Z
  (mode XYZ) plus `4.5 deg * sin^2(pi * frame / 24)`, per `gather_handclear_keys.json`. Applied to a different base
  track it should give the same 4.5 deg peak delta; please verify against your control rather than trust this.
