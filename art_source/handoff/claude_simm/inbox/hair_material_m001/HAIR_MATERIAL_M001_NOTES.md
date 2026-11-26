# ART-001 hair material test m001 on frozen head v011 (Codex brief at 4f9ac05)

Status: material-only diagnostic packet for Codex's isolated native study. No head GLB or .blend is duplicated:
geometry, normals, UVs, transforms and the face, eye, skin, brow and lash textures are v011's, unchanged.
`head_candidate_v011.*` is untouched (its .blend re-hashed after the runs). Not a parity claim, no A1 approval.

## What it is

One new hair albedo, `simm_head_hair_basecolor_m001.png` (1024 x 1024, sRGB, sha256
`c5f4549be9cba12e152e17f71fb234bcd788ead410dad8b667673832ceebe99f`), baked through the hair's existing UV map.
Codex overrides only `SCULPT_MAT_HAIR`'s base colour image, and its roughness for setting C.

Colour design (albedo only; no lighting is baked in):
- Root and body masses: deeper warm brown, by how far the hair surface sits above the scalp (palette sRGB root
  72, 39, 24 and body 104, 58, 34).
- Outer lock surfaces: a restrained amber (146, 90, 50), stronger where a whole lock faces up and forward. The facing
  term is smoothed over entire locks, so it doesn't draw a highlight that would look wrong from other cameras.
- One broad, soft drift across the head: about +-7 percent value and +-4 percent toward red or yellow, at wavelengths
  of 9 to 15 cm.
- No black grooves, comb lines or fine noise.

Covered texels, median sRGB: v011 140, 81, 39 (the orange read); m001 112, 64, 37. The reference's hair measured
earlier, WITH its lighting, has a median of 138, 76, 36. That is a lit photograph, not an albedo swatch, so m001 is
deliberately not matched to it.

## The three settings (`hair_material_m001_comparison.png`)

Same cameras (`ref`, `alt`), lights, exposure, geometry and every other material in each frame, plus a small whole
figure:

| Setting | Image | Roughness | Metallic | Specular (Blender) |
|---|---|---|---|---|
| A | v011 unchanged | 0.70 | 0 | 0.25 |
| B | m001 | 0.70 | 0 | 0.25 |
| C | m001 | 0.50 | 0 | 0.25 |

My Blender read (opinion, not a native result): B removes the orange wash and reads as chestnut, with the amber
staying on broad lock tops. C adds a soft sheen across the crown that separates the upper locks a little. It doesn't
read as plastic in Blender, but Godot's specular response differs, so the 0.70 or 0.50 call belongs to the native
review. If C reads as plastic there, keep 0.70.

## Exported values, exactly as the Blender 3.5.1 exporter writes them

From hair-only probe exports, made with the same options as `stage4_export.py` and kept as measuring devices, not
deliveries:

| | A | B | C |
|---|---|---|---|
| `pbrMetallicRoughness.metallicFactor` | 0 | 0 | 0 |
| `pbrMetallicRoughness.roughnessFactor` | 0.7 (0.699999988) | 0.7 | 0.5 |
| `KHR_materials_specular.specularColorFactor` | 0.5928 (grey) | 0.5928 | 0.5928 |
| `KHR_materials_ior.ior` | 1.45 | 1.45 | 1.45 |
| `doubleSided` | true | true | true |

Assumptions stated, not checked: whether Godot's importer reads `KHR_materials_specular` and `KHR_materials_ior`. If
it ignores them, it uses its own default specular for all three settings alike. There are no custom or export-only
nodes: the hair material is one Principled BSDF with one image texture. The bake's temporary emission material is in
no delivered file.

## Compatibility proof (`hair_material_m001_parameters.json`)

- The UV map is asserted unchanged before and after the bake (sha256 of the float32 UVs `d36f5fd3...`).
- In all three probe exports, the hair's `TEXCOORD_0` and `POSITION` data are byte-identical to those in
  `head_candidate_v011.glb`.
- The image is the same size as v011's hair texture. Coverage matches: 13 of 837,518 covered texels differ, at
  island margins (same 10 px bake margin).
- Rebuilt twice, the PNG is byte-identical.

## Files

| Path | What |
|---|---|
| `simm_head_hair_basecolor_m001.png` | The new albedo. |
| `hair_material_m001_parameters.json` | Settings A, B, C with exported material blocks, checksums, compatibility proof and assumptions. |
| `hair_material_m001_comparison.png` | Reference, A, B, C at `ref` and `alt`, plus a whole-figure row. |
| `../build_scripts/hair_material_m001.py` | Builds the albedo from `head_candidate_v011.blend` (read only). |
| `../build_scripts/hair_material_apply.py` | Review-only override of the hair image and roughness, for renders and probes. |
| `../build_scripts/hair_material_probe.py` | Hair-only probe export; records what the exporter writes. |

## Not addressed, by design

The broad overlapping plate surfaces of the locks are geometry. A material cannot fix them, and lock-surface
refinement is Codex's separate later decision. Nothing native was run here.

## Proposed next action

Codex overrides `SCULPT_MAT_HAIR` in the isolated native study with B and C against A, then picks the setting, or
none.
