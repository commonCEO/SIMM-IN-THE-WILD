# ART-004 boot candidate v001: rigid two-part boots per leg

Status: review candidate for Codex's native fit, answering `465ccf1`. Not a parity claim, not for live swap. Built
on the current fit file; head v009, collar v004 and jacket v003 are byte-identical to what Codex verified
(rechecked: `255f781e...94e7b`, `b093418b...8056f`, `e53ebe5d...dfcd3`). `verify_candidate.py`:
`FROZEN_ALL_UNCHANGED True` (body, old head, 17 rest matrices, socket, three actions).

## Files

| Path | Purpose |
|---|---|
| `boot_candidate_v001.glb` | For Codex. Identity root `SCULPT_BOOTS_ROOT` with four static meshes in actor space (geometry baked at rest), metres, Y-up. No armature, animation, camera or light. sha256 `0d5c3a0d5a769b27081340348247664086265da279098660b75a29fc7d1221d3`, 620,928 bytes. |
| `renders/boot_v001_full_figure.png` | Reference, then before and after at the reference camera in colour and clay, and from the side; all scaled to one figure height with the 0.20 and 0.33 lines. |
| `renders/boot_v001_junction_and_sole.png` | Close frames of the ankle junction and the sole on the ground: rest, walk at 25 and 75 percent (both legs forward in turn), gather at 50 percent; side, reference camera and low camera. |
| `renders/boot_v001_colour_ref.png`, `_colour_alt.png`, `_clay_ref.png` | Full figure. Blender Cycles, review only. |
| `build_scripts/boot_build.py` | Deterministic build. Input: `work/collar_packet_v004.blend` (any file with PROTECTED_BODY and SimmRig). |
| `build_scripts/boot_check.py` | Manifest, hidden-surface ownership, clip checks, export and re-import. `SAMPLES` sets samples per clip. |
| `build_scripts/boot_review_prep.py` | Review renders only. |

No `.blend` committed; `blender -b work/collar_packet_v004.blend --python build_scripts/boot_build.py -- <absolute>.blend`
rebuilds it.

## Part manifest (asserted by `boot_check.py`)

| Part | Bone (attach with the bone's inverse global rest) | Verts in GLB | Tris | Materials | Bounds, Blender axes, metres |
|---|---|---|---|---|---|
| `SCULPT_BOOT_SHAFT_L` | `shin_l` | 3,102 | 5,000 | leather | X -0.192..-0.042, Y -0.087..0.071, Z 0.100..0.290 |
| `SCULPT_BOOT_FOOT_L` | `foot_l` | 4,175 | 7,200 | leather, sole | X -0.194..-0.046, Y -0.190..0.090, Z 0.000..0.168 |
| `SCULPT_BOOT_SHAFT_R` | `shin_r` | 3,172 | 5,000 | leather | X 0.042..0.192, Y -0.087..0.071, Z 0.100..0.290 |
| `SCULPT_BOOT_FOOT_R` | `foot_r` | 4,189 | 7,200 | leather, sole | X 0.046..0.194, Y -0.190..0.090, Z 0.000..0.168 |

Total 24,400 triangles. Each part is 100 percent on one existing bone (one vertex group at 1.0 in the source, and a
`bind_bone` extra in the GLB). `*_l` bones are on -X in this rig. Materials: `SCULPT_MAT_BOOT_LEATHER` is the
original `Simm brown boot leather` base value (linear 0.181, 0.080, 0.033), roughness 0.72; `SCULPT_MAT_BOOT_SOLE`
is the original `Simm dark soles` base value, roughness 0.85. Flat colours, no texture.

## What a native study hides: correction to the contract

**Hide by material AND foot ownership, not by material alone.** `Simm brown boot leather` has 1,160 triangles, but
376 of them are 100 percent on `chest` at Z 0.834 to 0.918: the brown straps on the backpack. Hiding the whole
material would strip them.

| Material | Triangles | Foot-owned (hide) | Not foot-owned (keep) |
|---|---|---|---|
| `Simm dark soles` | 744 | 744 | 0 |
| `Simm brown boot leather` | 1,160 | 784 | 376 (`chest`, the pack straps) |
| `Simm worn jacket edges` | 256 | 256 | 0 |
| Total | 2,160 | **1,784** | 376 |

Plus `Simm folded hood canvas` (320), as already suppressed in your studies. Trousers are not touched: the trouser leg
inside each shaft stays and is hidden by it. Rollback: show those 1,784 faces again and remove the four parts.

## Shape

- **Shaft:** one smooth leather tube round the trouser leg, Z 0.100 to 0.290, slightly wider at the top, ending in a
  soft turned-down cuff. Its lower 7 cm sits inside the boot foot.
- **Foot:** one lofted boot from heel to toe instead of the blockout's ellipsoids. It is 128 mm wide; the original
  shoe was about 177 mm. The ankle rises round the shaft, and the instep slopes to a rounded toe at the original's
  length.
- **Sole:** a separate dark shell, 22 mm, with a 30 mm heel, 3 mm proud of the upper. It has a gentle rocker: toe
  spring over the front 85 mm and a rounded heel edge, so it rolls with the foot bone in the walk.
- **Proportion:** the cuff is at Z 0.29, which is 0.20 of figure height, as in the reference.

## Measured in Blender, 97 samples per clip (dense sampling, not continuous proof)

| Clip | Trouser vertices outside a shaft | Shaft lower edge outside the boot foot (visible crack) | Lowest point of either boot | Original soles, same samples |
|---|---|---|---|---|
| idle | 0 | 0 | Z 0.000 | Z 0.000 |
| walk | 0 | 0 | Z -0.007 to 0.005 | Z -0.001 to 0.013 |
| gather | 0 | 0 | Z -0.002 to 0.000 | Z -0.000 to 0.003 |

The crack test asks whether any vertex of the shaft's lowest 8 mm band leaves the boot-foot volume (odd ray
crossings). It no longer counts the shaft's outer surface as "outside", as the proposal's numbers did. The trouser
test counts trouser vertices at rest Z 0.140 to 0.275 that leave the shaft.

## Known issues

- In walk the new sole dips up to 7 mm below the floor at the worst sample; the original dips up to 1 mm. The
  sole is wider and its rocker is a first guess. It was 19 mm before the rocker.
- The flat leather colour reads lighter and more orange than the original textured shoe and the reference's
  boots. That is a material question for later; the brief said to hold materials.
- The heel is fairly upright from the side, and the toe box is plain. Shape detail for a later pass.
- Not seen in Godot. The exposed-trouser and jacket-length gap remains (0.20 against the reference's 0.13 of
  figure height).
