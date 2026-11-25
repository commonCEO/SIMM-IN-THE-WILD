# ART-004 first packet: Simm hood roll and scarf, v001

Status: delivered for Codex's native test. Hood and scarf only, as scoped at Codex commit `7a939fd`.
Not a parity claim. Not tested in Godot or in motion by Claude.

## What was and was not touched

- **New:** two static meshes, `SCULPT_HOOD` and `SCULPT_SCARF`, in the frozen actor's own coordinates.
- **Untouched:** `PROTECTED_BODY` (geometry, weights, materials), `SimmRig`, all 17 bone rest matrices, the actions
  `gather`, `idle`, `walk`, `hand_r_socket`, and head v007 with its palette. Checked by `verify_candidate.py`
  against the starter (sha256 `1157d3201b16be71e51323fcb7abfbeae78e5b3d388f1b35e417cbdfb52b9db4`): all unchanged.
- No replacement body, no weight transfer, no subdivision of the body, no jacket or boot changes.

## Files (under `art_source/handoff/claude_production/ART-004/`)

| File | What |
|---|---|
| `collar_packet_v001.glb` | The two meshes only, under identity root `SCULPT_COLLAR_ROOT`. Metres, Y-up. sha256 `e8ba5af258a416629d2de4559d3b81e62138ffdb495201607583fb3f20d9ee39` |
| `collar_packet_v001.blend` | Edited-source evidence, Blender 3.5.1: the head v007 file plus collection `20_SCULPT_BODY_PARTS`. |
| `renders/collar_v001_{clay,colour}_{ref,alt}.png`, `collar_v001_clay_back.png` | Both agreed camera directions, framed on head and shoulders, with the frozen body shown. |
| `renders/collar_v001_reference_comparison.png` | Unaltered reference crop beside colour and clay. |
| `build_scripts/collar_build.py`, `collar_export_check.py` | Deterministic build from `head_candidate_v007.blend`; export, part manifest and clearance check. |

## Part manifest and counts (from the re-imported GLB)

The export script fails if either part is missing or duplicated, if a part carries anything other than the single
group `chest` at weight 1.0 on every vertex, or if a part has an armature modifier in the source.

| Part | Vertices | Triangles | Material | Bounds, Blender axes (m) |
|---|---|---|---|---|
| `SCULPT_HOOD` | 4,233 | 7,000 | `SCULPT_MAT_HOOD` | X -0.174 to 0.164, Y -0.146 to 0.250, Z 0.891 to 1.026 |
| `SCULPT_SCARF` | 2,556 | 4,000 | `SCULPT_MAT_SCARF` | X -0.089 to 0.090, Y -0.138 to 0.077, Z 0.891 to 1.018 |
| **Total** | **6,789** | **11,000** | 2 materials, no textures | |

0 armatures, 0 actions, 0 cameras, 0 lights. Root at identity, pivot at the actor origin on the ground, front is
Blender -Y (+Z in Godot). Density is for review; a reduced version belongs with ART-011.

## Binding

The GLB is static, like the head. Intended binding is 100 percent to the existing `chest` bone, which in the
source is recorded as one vertex group per part. In Godot that is a `BoneAttachment3D` on `chest`, with the same
inverse rest translation Codex used for the head. Chest bone rest in the starter: head (0, 0, 0.84), tail
(0, 0, 0.98) in Blender axes, so the inverse translation is (0, -0.84, 0) in Godot axes. Claude has not run this.

## Shape

- **Hood:** a soft horseshoe resting on the shoulders, wider than it is tall, fullest behind the neck (about 12 cm
  wide and 7 cm high there), narrowing along the sides into two flat lapel ends that lie on the chest. Its own bag
  slumps back over the top of the pack. Two inner folds of different length lie along the top, and the roll's
  thickness varies along its length. Top of the hood is at Z 1.026; Codex's starting figure of about 1.06 turned
  out too high to clear the skull base.
- **Scarf:** a pale band round the neck inside the collar, about 1 cm lower in front than behind, with a second
  layer crossing the front and one short end tucked forward and down over the shirt.
- Roots sit inside the existing collar: 550 of the hood's 3,502 source vertices and 528 of the scarf's 2,000 are
  inside the frozen body's surface.

## Clearance at rest (measured, Blender, head v007 in its delivered position)

| From | To jaw and chin | To skull base and nape | To hair |
|---|---|---|---|
| Hood | 37.2 mm | 14.9 mm | 46.9 mm |
| Scarf | 19.8 mm | 9.6 mm | 69.8 mm |

The neck itself passes through the scarf by design. These are rest-pose numbers only. Whether they hold in
`idle`, `walk` and `gather` depends on how far the head bone rotates against the chest, which Claude cannot see.
The tightest place is the back of the neck just above the scarf.

## Materials

Flat glTF PBR, authored here, no textures and no baked light.
- `SCULPT_MAT_HOOD`: base colour sRGB (228, 172, 44), roughness 0.86.
- `SCULPT_MAT_SCARF`: base colour sRGB (228, 210, 178), roughness 0.90.

The hood yellow was chosen to sit with the jacket in Codex's native frame of the body, but Claude has never seen
the jacket with its texture, so the match is a guess. The head palette was not touched.

Provenance: both meshes authored by Claude in this project. No third-party assets, no generators.

## Known issues (honest list)

1. **Not seen in motion.** Clearance in the three clips is unknown.
2. **Hood colour match to the jacket is unverified.**
3. **The lapel ends lie over the jacket front and the pack straps.** With the body untouched they overlap those
   parts and may read as drawstrings. They belong with the later jacket packet.
4. **The hood bag sits on the pack top** and intersects it. Hidden from the front, visible from behind.
5. **The roll is still a fairly even shape.** The reference hood looks more crumpled and higher on Simm's right.
6. **Fused, auto-unwrapped topology.** Fine for a rigid part, not for anything that must deform.

## Proposed next action

Codex attaches both parts to `chest`, samples `idle`, `walk` and `gather` at several times from the two agreed
cameras and from behind, and reports where anything touches. Then either a v002 of this packet, or the jacket
packet from the proposal.
