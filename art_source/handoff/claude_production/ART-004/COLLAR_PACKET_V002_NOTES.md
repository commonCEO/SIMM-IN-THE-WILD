# ART-004 collar packet v002: hood roll and scarf

Status: delivered for Codex's native test. Answers the v001 review at `65387e5`. Not a parity claim, not
ready_for_user_review. Head v007, the body, the pack, the rig, the weights and the actions are untouched.

## Files

| Path | Purpose |
|---|---|
| `collar_packet_v002.glb` | For Codex. `SCULPT_HOOD` and `SCULPT_SCARF` under identity root `SCULPT_COLLAR_ROOT`. sha256 `a3146c83dca0b95d31d96f328091df899dc6bca5c53cfa4776ea825766349e73`, 277,852 bytes. |
| `renders/collar_v002_colour_front.png`, `_side.png`, `_back.png`, `_ref.png`, `_alt.png` | Colour, with the frozen body and head v007. Blender Cycles, review only. |
| `renders/collar_v002_clay_back.png` | Clay back view: the pack is not hidden. |
| `renders/collar_v002_vs_v001.png` | v001 left, v002 right: reference angle in colour, then back in clay. |
| `build_scripts/collar_build.py` | Deterministic build. Now holds the v002 shapes. |
| `build_scripts/collar_pose_clearance.py` | New. Read-only clearance through the three clips, and collar against pack. |
| `build_scripts/collar_export_check.py` | Unchanged. Manifest asserts, rest clearance, GLB export. |

No `.blend` is committed for v002, under the lighter delivery rule. It rebuilds exactly with:
`blender -b claude_simm/inbox/head_candidate_v007.blend --python collar_build.py -- <absolute path>.blend`

## Part manifest

| Object | Verts | Tris | Material | Binding | Bounds, Blender axes, metres |
|---|---|---|---|---|---|
| `SCULPT_HOOD` | 3,501 | 6,998 | `SCULPT_MAT_HOOD`, flat sRGB 228,172,44, roughness 0.86 | 100 percent `chest` | X -0.144..0.138, Y -0.127..0.115, Z 0.935..1.024 |
| `SCULPT_SCARF` | 2,000 | 4,000 | `SCULPT_MAT_SCARF`, flat sRGB 228,210,178, roughness 0.90 | 100 percent `chest` | X -0.089..0.090, Y -0.095..0.077, Z 0.946..1.018 |

Total 10,998 triangles. No textures, no rig, no animation, no camera, no light. Attach as in v001:
`BoneAttachment3D` on `chest`, inverse rest translation (0, -0.84, 0) in Godot axes. Colours are held from v001.

## What changed, against the four points of the brief

1. Pack. The hood bag over the pack flap is gone. v001 reached Y 0.250 behind the neck; v002 stops at Y 0.115.
   The roll now sits in the valley between the nape and the front of the pack dome. The pack is not edited.
2. Lapels and roll. The lapel ends are about 45 mm shorter (lowest point of the hood: v001 Z 0.891, v002 Z 0.935) and taper to
   a soft tip. The roll is narrower (lateral radius about 0.030, was up to 0.062) and its centre line is pulled in
   by about 20 mm at the sides, so it slumps against the neck instead of lying on the shoulders as a shelf. The two
   top folds have different lengths and thicknesses. The top is at Z 1.024 (v001 1.026), so the neck is still framed.
3. Scarf. The hanging end is gone: the end now goes straight down into the shirt opening and stops at Z 0.946.
   The wrap-over is lower and about a quarter thinner. The ring and its tilt are unchanged, so the pale neck fill
   and the asymmetric fold remain.
4. Inspection. Front, side and back were looked at in clay and in colour before export, then the clips were
   measured (below). The back frame is included.

## Measured, not native

Clip clearance, `collar_pose_clearance.py`: 13 evenly spaced samples in each of `idle`, `walk` and `gather`, 39
poses. The head and hair are carried by `head`, the collar by `chest`. The largest head-against-chest rotation
found was 3.4 degrees, in `gather`. Smallest distance from each part to the visible head (head mesh above Z 1.035):

| Part | Jaw and chin | Skull base | Hair |
|---|---|---|---|
| `SCULPT_HOOD` | 27.5 mm (gather) | 10.7 mm (gather) | 43.9 mm (gather) |
| `SCULPT_SCARF` | 22.5 mm (gather) | 19.6 mm (gather) | 68.4 mm (gather) |

`verify_candidate.py`: `FROZEN_ALL_UNCHANGED True` (body, old head, 17 bone rest matrices, socket, three actions).

## Contact I am reporting, not hiding

- Neck. Both parts are built in contact with the neck column (head mesh below Z 1.035). A scarf and a hood roll
  rest on the neck, and the roll is partly sunk into its back. `collar_export_check.py` still uses its old
  Z 1.015 line, so its "skull base and nape" figure for the hood reads 0.0 mm: that is this neck contact, not the
  skull. In `gather` the neck moves about 3 degrees inside the roll. Please look for skin showing through at the
  nape in the gather clip.
- Pack. The pack and the collar are both on `chest`, so this is one rigid measurement and does not change in the
  clips. 236 hood vertices lie behind Y 0.10. 4 of them are under the pack surface, by up to 11.5 mm, on the
  underside of the roll at the centre back (about X 0, Y 0.10, Z 0.966) where the roll tucks under the front lip of
  the pack. They face down and are not visible in my back or side frames. The visible outer surface comes within
  3.2 mm of the pack at its closest. The scarf has nothing behind Y 0.10.
- Body. 250 of 3,501 hood vertices and 623 of 2,000 scarf vertices are inside the frozen body surface. These are
  the roots buried in the jacket collar and the shirt, as the brief allows.
- Strap. In the side view a pack shoulder strap crosses the roll as a thin green line. The strap is frozen body
  geometry, so I left it.

## Known issues

- The scarf now shows as a thin pale band. It may be too little. A thicker front fold is a small change if wanted.
- The lapel tips are softer but are still tapered tubes, not cut cloth.
- From the back the hood is a low band above the pack. With the bag removed there is no hood volume left to read
  as a hood. If the reference needs more hood, it has to go up, not back, and the skull base limits that to
  about 10 mm.
- The tucked scarf end may still show a few millimetres at the shirt opening in the front view.
- Flat colours only. Not seen in Godot. Not seen in motion with my own eyes: the clip figures are distances, not frames.
