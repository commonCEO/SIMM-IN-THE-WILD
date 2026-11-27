# ART-004 jacket material m002 (Codex brief at 68e1524)

Status: ONE material-only candidate on the held f002 clothing finish, for Codex's native study. Not approved; A1
unpassed; no native evidence. Held unchanged: f002 geometry, positions, normals and skin weights, collar v004 geometry and
its brown neck layer, head v012 + m001-B (hair roughness 0.70), skin, boots v002, body, rig, rest pose, actions, socket.

## What changed

Only the materials and UVs of the three jacket parts.

| | f002 control | m002 |
|---|---|---|
| UVs | `UVMap` and `SurfaceUV`: overlapping, outside 0..1, never used by a texture. Pockets had none. | One shared unwrap `M002_UV` for shell, trim and pockets, all inside 0..1. No island pixel is shared by two parts (checked in the bake). |
| Jacket shell and pockets | flat linear 0.723, 0.381, 0.027, roughness 0.86 | albedo map: front panels keep the f002 colour; sleeves lighter and slightly more lemon; back panel and the lower band deeper ochre; slight low-frequency dye variation. Roughness map 0.86 to 0.90. |
| Trim (binding) | flat linear 0.468, 0.220, 0.019, roughness 0.86 | linear 0.400, 0.190, 0.022 (sRGB 170, 121, 41), a slightly deeper, restrained ochre; roughness 0.80 so it separates a little from the canvas |
| Metallic, specular, IOR, double-sided | as v004 | unchanged |
| Neck layer | brown, linear 0.200, 0.112, 0.058 | unchanged |

Exact values, blends and noise are in `jacket_material_m002_materials.json`; per-part ranges in `m002_build_record.json`.

How the maps are made: every value is computed per vertex from the rest pose (panel by skin weight and position, noise
in 3D) and baked as emission into the atlas. No light, occlusion, curvature or cavity enters the maps, and there are no
seam lines, stitching, weave or grunge. Panel transitions are about 5 cm wide. The variation is my artistic reading of
"broad colour variation across panels", not something measured from the reference.

Normal map: none. There is no sculpt to bake from, so a normal map would only be procedural noise.

## Evidence

- `jacket_material_m002_comparison.png`: reference crop; f002 control beside m002, whole figure and close, colour at
  both cameras; clay at both cameras. Same lights, head and other materials. The clay images match the control to within
  1 level on at most 27 pixels (denoiser noise).
- `jacket_material_m002_gamescale.png`: both at 150 px, actual pixels and enlarged 3x.
- `jacket_material_m002_texture_preview.png`: the two maps, an unlit front and back (emission = albedo, Standard view
  transform, exposure 0, grey sRGB 128 background) and the noise-free panel colours in sRGB and linear. An unshaded Godot
  material on the same albedo should give the same pixel values: lighter and greyer means the albedo was read as linear,
  darker and more saturated means it was converted twice.

My reading of the renders: the sleeves read a touch lighter and more lemon than the body, the back and the lower band a
little deeper, and the binding darker. At game scale the difference is small but visible as a lighter sleeve against a
deeper body. The jacket is still a clean toy-like canvas, not weathered.

## Geometry is f002's (asserted in `build_scripts/jacket_material_m002_export.py`)

- In Blender, before against after the build: every mesh object in the file keeps identical positions, weights, faces,
  modifiers and transforms; split normals within 1e-5 (edit-mode float noise).
- Raw GLB against `../jacket_finish_f002/jacket_finish_f002.glb`, per part: the same distinct (position, joints, weights)
  records bit for bit, the same triangles over those records, every normal within 5e-4 (largest difference 9.4e-5). The
  new UV seams only duplicate existing records.
- Re-import: every GLB vertex matches a source vertex within 20 micrometres with identical weights, every source vertex
  is covered.
- `verify_candidate.py` on the working file: `FROZEN_ALL_UNCHANGED True`; GLB 44,388 triangles, 1 armature, 0 actions,
  cameras or lights.

| Part | Source vertices | GLB vertices (f002 / m002) | Triangles | Material | GLB attributes |
|---|---|---|---|---|---|
| `SCULPT_JACKET_LONG` | 17,158 | 18,548 / 19,437 | 34,304 | `SCULPT_MAT_JACKET_M002` | POSITION, NORMAL, TEXCOORD_0, COLOR_0 (white, as f002), JOINTS_0, WEIGHTS_0 |
| `SCULPT_JACKET_LONG_TRIM` | 3,516 | 4,668 / 5,657 | 6,980 | `SCULPT_MAT_JACKET_TRIM_M002` | as above |
| `SCULPT_JACKET_POCKETS` | 1,560 | 1,560 / 2,195 | 3,104 | `SCULPT_MAT_JACKET_M002` | as above without COLOR_0 (as f002) |

f002 also carried TEXCOORD_1 (its second, unused UV layer); m002 has only TEXCOORD_0.

## Files and checksums

| Path | sha256 |
|---|---|
| `jacket_material_m002.glb` | `ab0d800f3342338ecfdc324cb79e5cfbf30e03b5040878c22759f039e1ae736d` (2,409,492 bytes) |
| `jacket_m002_albedo.png` (sRGB) | `49f81dd17285e1de59423ae318269aca3f0a533b41d84729a023398eaab68555`, embedded byte-identical in the GLB |
| `jacket_m002_roughness.png` (linear) | `9cf43b68f32e0e01a8da6eb7ef66e1fd6e5b2065072829bebc72b8cf0fb28fe1`; the exporter re-packs it as metallicRoughness `b0203bccc76f5b7156292398e7738dda409cd0f6b80354e2d75260d65abad883` (G = roughness, R and B = 255, metallicFactor 0) |
| `jacket_material_m002_manifest.json` | export record: counts, bounds, f002 comparison, materials, textures, samplers |
| `../jacket_finish_f002/jacket_finish_f002.blend` | `d842a126172e695583618a7a53ec2052df87d84277f395db5bf6fcd07dceff12`: the f002 editable source, now committed as the working clothing baseline (compressed copy of the working file; jacket positions checked identical) |

## Blender values against proposed Godot settings

What Blender shows is Principled BSDF with the maps above, specular 0.2. Through glTF this becomes baseColorTexture,
metallicRoughnessTexture (roughness in G), metallicFactor 0, KHR_materials_specular (specularColorFactor 0.474) and
KHR_materials_ior 1.45, the last two unchanged from f002. These do not map one-to-one into Godot. Proposed starting point,
untested: albedo texture as sRGB, roughness texture channel green with roughness 1.0, metallic 0; if the importer
ignores the specular extension, metallic_specular stays at 0.5 and could be lowered (about 0.3) if the cloth reads
glossy under the native lights. Codex owns the import, shader and light evaluation.

## Honest issue list

1. The panel variation is an interpretation. The reference's stronger value range comes mostly from its lighting, which
   the brief says not to bake; m002 does not close that gap.
2. Softer cloth response: roughness rises only from 0.86 to about 0.88 on the canvas; specular is unchanged. Most of a
   softer look would come from the engine side (specular, rim or sheen), not from these maps.
3. A few UV seams show a faint hairline in the unlit close view. Not visible to me in the lit renders.
4. Bake fix during this run: baking the three parts into one image let one part's margin paint over another part's
   islands (trim-coloured flecks on the shell). Each part is now baked on its own and composited; a rebuild gives
   byte-identical maps.
5. GLB checksum: two exports of the same file differ in a few jacket normals by up to 1e-4 (float noise, as in f001), so
   the GLB checksum can change between rebuilds while positions, weights, UVs, materials and images stay identical.
6. Nothing native. Contact and motion conditions are f002's, unchanged.

## Rebuild

```
blender -b work/jacket_finish_f002.blend --python build_scripts/jacket_material_m002.py -- <out.blend> <texture dir>
blender -b <out.blend> --python build_scripts/jacket_material_m002_export.py -- <out.glb> <manifest.json> <f002 glb>
blender -b <out.blend> --python build_scripts/jacket_m002_neutral_preview.py -- <out prefix> 512
```

`work/jacket_finish_f002.blend` is the committed `jacket_finish_f002/jacket_finish_f002.blend`.
