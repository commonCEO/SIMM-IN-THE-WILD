# ART-004 collar packet v004: hood seated on jacket v003

Status: delivered for Codex's native test, answering `bdf4942`. Built on and shown with the held study candidates
head v009 and jacket v003; their files are byte-identical to what Codex verified (head v009 `255f781e...94e7b`,
jacket v003 `e53ebe5d...dfcd3`, collar v003 `f233e269...78961`, all rechecked). Not a parity claim.

## What changed from v003

- **No separate bunch behind the neck.** Its volume went into the stand: 3 to 7 mm more radial thickness at the
  back and back sides, and two soft diagonal folds on the back of the stand, half buried in it.
- **Seated on the real jacket.** For each direction round the neck, the stand's lower edge goes down to the surface
  under the stand's centre line, plus a hidden 6 mm skirt into it. The surface is jacket v003 where it is
  highest, or the frozen pack, straps, folded-hood piece or shirt where those are higher. Directions with no
  surface below take their neighbours' height. The base is smoothed along the path, never raised, and may drop at
  most 70 mm below the v003 base. The stand keeps v003's rounded cross-section. A separate seat band below it,
  fused in by the remesh, carries it down to the jacket. One tall stretched section gave a knife-thin top ridge
  that rendered as dark pits; the final mesh has no edge thinner than 2.5 mm and no open edges.
- **Rolled top lip removed** for the same reason. Lapel turn-downs and the scarf are unchanged from v003.

## Jacket weights under the collar (checked before relying on `chest`)

Jacket v003 vertices within 17 cm of the neck centre and above Z 0.93: every direction is 100 percent `chest`,
except at the shoulder points (about 60 and 90 degrees each side), where 2 to 3 vertices per side blend in
`upper_arm` at 4 to 26 percent. No weight was changed for the join.

## Measured, not native

| Check | Result |
|---|---|
| Seat gap, 32 directions round the neck, at rest | largest 5.0 mm; 3 directions over 1 mm |
| Seat gap, 25 samples per clip (idle, walk, gather) | largest 5.0 mm, always at about 72 degrees (Simm's left, front side); never more than 3 directions over 1 mm |
| Seat gap, 97 samples per clip (dense sampling, not continuous proof) | same: 5.0 mm, 3 directions |
| Hood to jaw and chin, 39 poses | 9.5 mm (gather) |
| Hood to skull base and nape | 8.1 mm (gather) |
| Hood to hair | 5.6 mm (gather) |
| Scarf to chin / nape / hair | 24.1 / 23.2 / 73.6 mm |
| Pack | 292 hood vertices are below the pack's top surface, up to 16.7 mm: this is the hidden skirt on the pack top. No hood surface hangs over the flap |

The gap is the same in every sample because the hood and almost all the jacket under it follow `chest` together.
The 5 mm direction is where the stand's front edge meets the jacket's front neckline. It shows as a narrow shadow
line in `renders/collar_v004_close_base_contact.png` (left).

`verify_candidate.py`: `FROZEN_ALL_UNCHANGED True`.

## Files

| Path | Purpose |
|---|---|
| `collar_packet_v004.glb` | For Codex. `SCULPT_HOOD` (4,502 verts, 9,000 tris) and `SCULPT_SCARF` (1,999 verts, 3,998 tris) under `SCULPT_COLLAR_ROOT`, both 100 percent `chest`, same attachment as v001 to v003. sha256 `b093418b37d135b44ec2762cbfac76e9b975e3fcc3a382730738ceb76588056f`, 341,932 bytes. Hood bounds X -0.116..0.115, Y -0.105..0.150, Z 0.920..1.064. |
| `renders/collar_v004_before_after.png` | v003 above, v004 below, side and back, both on jacket v003 and head v009. |
| `renders/collar_v004_colour_side.png`, `_back.png`, `_ref.png`, `_alt.png`, `_bq.png` | Idle, side, back, both agreed cameras, back three-quarter. |
| `renders/collar_v004_gather50_colour_side.png`, `_ref.png`, `_back.png` | Gather at 50 percent, where every clearance minimum falls. |
| `renders/collar_v004_close_base_contact.png` | Close: front side (the 5 mm spot) and back three-quarter. |
| `renders/collar_v004_clay_ref.png`, `_alt.png` | Clay at both cameras. |
| `build_scripts/collar_build.py` | v004 (v003 at `fb2bcac`). Build input: `work/jacket_candidate_v003.blend`. |
| `build_scripts/collar_seat_check.py` | New. Seat gap through the clips; `SAMPLES` sets samples per clip. |

## Known issues

- **The frozen body's own "folded hood canvas" piece** (material `Simm folded hood canvas`, 320 triangles, 100
  percent `chest`) still shows: a flat band at the front neckline under the scarf, and a small flap at the back
  right (close frame, right). It is protected geometry, so I have not touched it. **Proposal:** in the study,
  hide that material along with the two jacket materials, since the collar now does its job. Codex's decision.
- 5 mm seat gap at Simm's left front side, constant through the clips.
- Hood to hair is 5.6 mm at the worst gather sample.
- Flat colours; not seen in Godot.
