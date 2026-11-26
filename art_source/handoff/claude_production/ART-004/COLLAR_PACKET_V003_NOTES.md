# ART-004 collar packet v003: standing hood around the neck

Status: delivered for Codex's native test. Made at the user's request: on 26 Nov 2026 the user reviewed a native
side view of head v007 + collar v002 + jacket v001, said "IMO we're still 30% off", and then approved reopening
the collar and the hair, which Codex had on hold: "Yes, this needs to have full parity". Not a parity claim, not
ready_for_user_review. Head v007, jacket v002, body, pack, rig, weights and actions are untouched.

## What was wrong in v002 (measured in Blender on the same files)

| Where | Bare neck in v002 |
|---|---|
| Sides (90 to 120 degrees round the neck) | from the collar at Z 0.99 up to the jaw at Z 1.08 to 1.10: about 9 cm |
| Back | from the hood top at Z 1.017 to the lowest hair at Z 1.061: 44 mm |
| Throat | from the scarf at Z 0.990 to the chin at Z 1.020: 30 mm |

In the reference the head sits down in the hood with almost no neck showing.

## What changed

- **Hood.** A standing hood all round the back and sides of the neck, built from a height profile by direction:
  Z 1.004 at the front edges, 1.036 at 65 degrees, 1.060 at the sides, 1.062 behind the ears, 1.045 at the back
  centre (lower there, because the hair tips hang to Z 1.061). Its inner surface is fitted to the head mesh in this
  file: 11 mm off the neck skin in every direction. Radial thickness 26 mm at the front edges to 42 mm at the back.
  Uneven bulges along its length, a bunch of gathered cloth behind the neck that sits on top of the pack, and a
  soft rolled lip along the top on Simm's right.
- **Lapels.** The long hanging ends are gone. The stand folds over onto the chest in a short flat turn-down.
- **Scarf.** Raised 11 to 20 mm and made about a fifth thinner, dipping in a soft V at the throat. The pale fill
  now reaches Z 1.012 under the chin. The tucked end and the asymmetric wrap move up with it.

## Measured, not native

Clip clearance, `collar_pose_clearance.py`, 13 samples in each of `idle`, `walk` and `gather`, 39 poses, visible
head above Z 1.035. The largest head-against-chest rotation is 3.4 degrees, in `gather`.

| Part | Jaw and chin | Skull base and nape | Hair |
|---|---|---|---|
| `SCULPT_HOOD` | 9.5 mm (gather) | 7.6 mm (gather) | 2.8 mm (gather) |
| `SCULPT_SCARF` | 24.1 mm (gather) | 23.2 mm (gather) | 73.6 mm (gather) |

At rest (`collar_export_check.py`): hood 11.5 mm from the jaw, 9.9 mm from the nape, 7.3 mm from the hair; scarf
15.6 mm from the chin. Pack: 0 hood vertices inside the pack, nearest outer surface 6.3 mm. The scarf has nothing
behind Y 0.10. `verify_candidate.py`: `FROZEN_ALL_UNCHANGED True`.

## Files

| Path | Purpose |
|---|---|
| `collar_packet_v003.glb` | For Codex. `SCULPT_HOOD` (4,502 verts, 9,000 tris) and `SCULPT_SCARF` (1,999 verts, 3,998 tris) under identity root `SCULPT_COLLAR_ROOT`, 12,998 tris, 2 flat materials, same colours as v002. sha256 `f233e2693f5060e234f4741f62c0acad0f9855298b78379ee540f46c96878961`, 343,168 bytes. |
| `renders/collar_v003_side_before_after.png` | The native frame the user reviewed, next to v003 from the side. |
| `renders/collar_v003_colour_ref.png`, `_alt.png`, `_side.png`, `_back.png`, `_front.png`; `_clay_ref.png`, `_clay_alt.png` | Blender Cycles, with the frozen body. Review only. |
| `build_scripts/collar_build.py` | Now holds v003. v002 is in Git at `6d413de`. |

Bounds, Blender axes, metres: hood X -0.114..0.113, Y -0.105..0.174, Z 0.958..1.065; scarf X -0.085..0.086,
Y -0.089..0.074, Z 0.949..1.012. Binding and attachment exactly as v001 and v002: both parts 100 percent `chest`,
`BoneAttachment3D` on `chest` with inverse rest translation (0, -0.84, 0) in Godot axes. No `.blend` committed;
it rebuilds with `blender -b claude_simm/inbox/head_candidate_v007.blend --python collar_build.py -- <absolute>.blend`.

## Known issues

- Hood to hair is 2.8 mm at the worst sample of `gather`: a back hair tip nearly touches the hood top. Hair resting
  on the hood is what the reference shows, but check it natively.
- The bunch behind the neck reads as a separate lump from the side. It may need to merge into the stand.
- A little skin still shows under the ear between the hood and the jaw. That is the jaw, not neck.
- The hood is fitted to the head mesh at rest. The head moves at most 3.4 degrees against the chest in these clips;
  a clip with more head motion would need a fresh check.
- The jacket under it in my frames is the frozen original, not jacket v002. The two have not been seen together.
- Flat colours, not seen in Godot.

## Next

The hair follows as head v008: the back and nape locks brought down to meet the hood, softer and lighter at the
tips, less gloss. Face, skull and palette stay as they are.
