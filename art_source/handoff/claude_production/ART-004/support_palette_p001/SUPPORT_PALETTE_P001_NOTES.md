# ART-004 supporting palette p001 (Codex brief at 2625b68)

Status: ONE material-only proposal for Codex's native study, as a JSON override packet. No GLB, no texture, no mesh
edit. Not approved; A1 unpassed. Held unchanged: head v012 + m001-B, skin, jacket f002 + m002, collar v004 and its brown
neck layer, boots v002, brass fasteners, undershirt, soles, and the body's geometry, weights, normals, UVs, rig, rest
pose, actions and socket. No step saves any .blend.

## The packet

`simm_support_palette_p001.json`: for each of the four materials Codex named, the region, current and proposed factor in
linear and sRGB, luminance, intent, and roughness/specular (unchanged).

| Source material | Region (checked face by face) | Factor now (sRGB) | Proposed (sRGB) | Proposed (linear) |
|---|---|---|---|---|
| Simm charcoal olive trousers | trousers: 1,080 faces, thigh and shin, Z 0.16 to 0.59 | 65, 72, 59 | 83, 74, 56 | 0.0872, 0.0680, 0.0392 |
| Simm olive canvas | backpack: 628 faces, all behind the back, chest bone | 102, 114, 68 | 131, 103, 74 | 0.2261, 0.1357, 0.0678 |
| Simm woven olive straps | two front shoulder straps: 56 faces, chest bone | 89, 98, 59 | 84, 66, 50 | 0.0880, 0.0545, 0.0317 |
| Simm canvas seams | pack seams and top binding: 192 faces, chest bone | 72, 85, 56 | 99, 79, 58 | 0.1249, 0.0774, 0.0425 |

Choices:
- **Pack:** same value as now, hue moved to a warm khaki-brown. It is yellower and lighter than the red-brown boot
  leather (118, 80, 51) and lighter than the undershirt (101, 80, 58), so the browns do not merge.
- **Trousers:** brown-olive, slightly lighter than the charcoal green, still the darkest cloth mass under the jacket.
- **Straps:** darker than before (luminance 0.112 to 0.060) so they read as dark webbing against the yellow jacket.
- **Seams:** keep their contrast against the pack canvas.

Roughness and specular are not changed. The reference pixels (pack about sRGB 122, 76, 33; trousers about 95 to 110,
64 to 78, 28 to 39) are warm and sunlit, so I took their hue direction, not their values.

## How the factor is applied

In the source each target is Principled BSDF with Base Color = MULTIPLY(Color1, `cloth_tone.png`). Blender's glTF
exporter writes that as baseColorFactor = Color1 with baseColorTexture = cloth_tone. The override replaces only
Color1 / baseColorFactor and keeps the cloth_tone texture.

Godot (untested): set albedo_color from the proposed linear factor and keep albedo_texture = cloth_tone. I expect, but
have not verified, that Godot 4's glTF importer converts baseColorFactor to an sRGB albedo_color, in which case the
inspector shows the sRGB column / 255.

## Shared use

`palette_shared_use_check.json` (`build_scripts/support_palette_apply.py`): each target is used on PROTECTED_BODY only in
the region above. The four also sit in material slots of the hidden REFERENCE_FAILED_OLD_HEAD object, on 0 of its faces.
No unintended body region uses them, so nothing had to be split. The review copies (`<name> P001`) go only into the shown
body's slots.

## Evidence

- `support_palette_p001_comparison.png`: reference crop; control (held f002 + m002, current palette) above p001 at the
  ref, alt and back cameras; factor swatches.
- `support_palette_p001_gamescale.png`: ref and back at 150 px, actual pixels and enlarged 3x.

Same file, lights, exposure, pose and cameras in control and candidate.

**Limitation:** `cloth_tone.png` is not in Git. Both control and p001 render with the same flat 0.5 stand-in in its
place, so these images are darker than native. Natively the factor multiplies the real texture: absolute brightness will
differ, but the control-to-p001 relation carries over.

My reading: the pack reads warm brown from the back and the side, the straps as dark brown bands over the jacket, and
the trousers as a dark brown-olive mass. Boots, pack and undershirt stay three distinguishable browns. At 150 px the
change is clearly visible on the pack and the trousers.

## Honest issue list

1. The values are interpreted, not measured base colours. The sunlit reference cannot give them directly.
2. Under the 0.5 stand-in the trousers read almost black-brown. With the real cloth_tone they will be lighter; if they
   still read too dark natively, the trouser factor is the one to raise first.
3. There are now more browns on the figure (hair, undershirt, neck layer, pack, straps, boots, trousers). They differ in
   hue and value, but whether they separate under the native warm light is Codex's evaluation.
4. Nothing native.

## Rebuild

```
SUPPORT_PALETTE=support_palette_p001/simm_support_palette_p001.json blender -b work/jacket_material_m002.blend \
  --python build_scripts/jacket_review_prep.py --python build_scripts/boot_review_prep.py \
  --python build_scripts/support_palette_apply.py --python <inbox>/build_scripts/render_views.py -- <out> colour 1100 32 ref,alt,back nobody 0.72 2.0
```

Leave `SUPPORT_PALETTE` unset for the control. `work/jacket_material_m002.blend` is rebuilt from the committed f002 blend
with `build_scripts/jacket_material_m002.py`.
