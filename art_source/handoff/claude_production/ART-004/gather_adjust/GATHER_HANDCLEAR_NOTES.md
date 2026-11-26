# ART-004: `gather_handclear`, an adjusted copy of the gather clip (user decision "1 adjust")

**Correction, 26 Nov 15:15 UTC:** `gather_handclear_rig_only.glb` is defective. Its export merged all actions and
wrote the ORIGINAL gather curve under the new name (Codex found it natively at d3f3a94). The action in Blender is
correct; the file was not. Use `gather_calibration_v001.glb` and `GATHER_CALIBRATION_V001_NOTES.md` instead. The
"22.6 mm at 4 deg" figure below came from a separate probe; the exported clip gives 19.8 mm at 4.5 deg.

Status: candidate for Codex's native validation. Made at the user's direct choice, 26 Nov 2026: option 1 of the
long-jacket proposal, "adjust the gather clip so the hand stays clear of the hip". The original `gather`, `idle` and
`walk` actions, the rest pose, all bones and the socket are unchanged. Not integrated into the game.

## What it is

A NEW action, `gather_handclear`: a copy of `gather` in which exactly one channel differs, `upper_arm_l`
`rotation_euler` Z (rotation mode XYZ). In this rig `*_l` is Simm's right side (-X). It adds an outward rotation of
`4.5 deg * sin^2(pi * t)`, where t runs from 0 at the first frame to 1 at the last. So:
- the clip starts and ends exactly as `gather` does, and still loops;
- the offset peaks at mid-clip, frame 12, where the original hand has drifted 20 mm inward of its rest position;
- at frame 12, 4 degrees on that channel moves the hand 22.6 mm outward and almost nothing in the other directions
  (measured: -22.6, -8.8, +2.7 mm in X, Y, Z).

The other 53 channels are asserted identical to `gather` when the action is built. `gather_handclear_keys.json` lists
every key of the changed channel: original, offset and new value.

## Files

| Path | Purpose |
|---|---|
| `gather_handclear_rig_only.glb` | For Codex. The 17-bone skeleton at rest and one animation named `gather_handclear`, 51 channels, frames 0 to 24. No mesh. sha256 `b99079c04688bebb84612cf7912aa98b1090f02273f4ca31f75cb9ad06b14f29`, 154,472 bytes. Re-imported: 17 bones, names match, largest rest joint difference 0.0000007 m. |
| `gather_handclear_keys.json` | The changed channel, key by key. Enough to apply the change to the master animation by hand. |
| `gather_handclear.py` | Builds the action from `gather` and exports the GLB. Rebuilt once to check: identical GLB and JSON. |
| `gather_original_vs_handclear.png` | Frame 12 from the front, three-quarter and side, original above, adjusted below, with the long-jacket prototype and boots v002. |

## Measured in Blender, 49 samples per clip (sampled, not continuous)

With the long-jacket prototype panel (v2, below):

| Clip | Panel vertices inside a hand (hand-only triangles) | Trouser points outside the panel | Largest panel edge stretch |
|---|---|---|---|
| idle | 0 | 3, up to 1.3 mm, at frame 0 | 1.00 |
| walk | 0 | 3, up to 1.3 mm, at frame 0 | 1.37 at frame 6 |
| gather (original) | 58 at frame 12 | 3, up to 1.3 mm, at frame 0 | 1.00 |
| **gather_handclear** | **0** | 3, up to 1.3 mm, at frame 0 | 1.00 |

Without any jacket change, the original `gather` already puts the hand into the frozen trousers by up to 4.4 mm.
The adjusted clip moves the hand outward through the whole contact window, so it should clear that too. That trouser
figure has not been re-measured with the new clip; please confirm natively.

Proof that the originals are untouched: `idle`, `walk` and `gather` compared key by key against the starter
(1,674, 486 and 486 keys): zero difference. `verify_candidate.py` flags "actions CHANGED" only because the working
file now also contains `gather_handclear`. Body, old head, rig and socket: unchanged.

## Long-jacket prototype v2 (for reference, still a prototype)

`../jacket_long_proposal/skirt_prototype.py` now also keeps the panel's sides 5 mm off the hands where they hang at
rest, never closer than 10 mm to the trousers. The first version touched both hands at rest (5 vertices each).
Measurements are in `../jacket_long_proposal/long_jacket_measurements_v2_with_gather_handclear.txt`.

## For Codex

- Validate natively: the hand at gather frames 7 to 17 against the hip, the trousers, jacket v003 and the long panel,
  and whether the slightly wider elbow reads naturally from the game camera.
- `hand_r_socket` is on the other arm and is not affected.
- If accepted, apply the one-channel change to the master `gather` in your integration step. I have not edited it.
- Then the long jacket can go forward as a production candidate under your earlier brief.
