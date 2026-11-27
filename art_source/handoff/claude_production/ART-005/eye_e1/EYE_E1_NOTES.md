# ART-014 E1 eye-only packet (Codex brief at 975040e)

Status: ONE reversible diagnostic packet for Codex's native A/B on the original eyes. Not approved, not for the live
game, A1 unpassed. Held: head, eye and lid geometry, skin, brows, lashes, mouth, hair, costume, palette, rig, actions,
socket. Native renderer behaviour is UNKNOWN until Codex imports the material.

## Files

| File | What | sha256 |
|---|---|---|
| `simm_eye_e1_albedo.png` | 512 x 512, 8-bit RGB PNG, sRGB-encoded eye albedo. No emissive map. | `ec3932b9716ecc34f82c27994e1efbcf48509fe81f86406d0410948b0e34e8a6` |
| `simm_eye_e1_carrier.glb` | ONLY `SCULPT_EYE_L` and `SCULPT_EYE_R`, unchanged from v012, with the E1 `SCULPT_MAT_EYE`. No rig, animation, camera, light or other mesh. 127,412 bytes. | `61c34fc958d437fbbcf72b50101af2e3c8820bc5434bd3418a356cb211e3d61f` |
| `eye_e1_manifest.json` | Identity checks, exported glTF material fields, parameters, sample colours, checksums | |
| `eye_e1_comparison.png` | Reference face; held v012, the reviewed demo and the delivered packet at ref and alt; the albedo; a game-scale check | |

Source:
- `../build_scripts/eye_e1_build.py` builds the packet.
- `../build_scripts/eye_e1_apply.py` applies it in memory for review renders.
- `../build_scripts/eye_e1_demo.py` is the critique demo, kept as reviewed.

Rebuild (the output folder must be empty; the builder refuses otherwise):
```
blender -b art_source/handoff/claude_simm/inbox/head_candidate_v012.blend --python art_source/handoff/claude_production/ART-005/build_scripts/eye_e1_build.py -- <absolute empty dir> <absolute path to head_candidate_v012.glb>
```
Two builds gave byte-identical PNG and GLB.

## A colour-encoding finding (fixed in this packet, evidence in row 2 vs row 3 of the sheet)

`stage3_finish.py` (head v009 to v012) paints the eye in linear light and writes those linear values straight into an
8-bit sRGB image without encoding them. The held eye texture is therefore darker than authored:

| Authored sRGB | Stored in `textures_v012/simm_head_eye_basecolor.png` |
|---|---|
| sclera 236, 227, 215 | 214, 196, 173 |
| warm lower iris 92, 56, 32 | about 27, 10, 4 (nearly black) |
| pupil 18, 11, 9 | 2, 1, 1 |

This is part of why the held eyes read black. The critique demo Codex reviewed had the same bug, so its iris rendered
nearly black too. The packet encodes to sRGB before writing. Its PNG holds the proposed values exactly, sampled from
the file:
- iris top 58, 34, 22
- iris bottom 122, 78, 46
- pupil 30, 18, 12
- sclera 214, 190, 168
- catchlight centre 205, 195, 181 (225, 215, 200 at 80 percent over the iris)

The held skin and hair maps are baked, not painted from raw pixels, so they are not affected. The held eye texture is
not changed here.

## Material (Blender values and what the glTF carries)

| | Held v012 | E1 |
|---|---|---|
| Base colour | eye albedo (unencoded) | `simm_eye_e1_albedo.png` (sRGB) |
| Emission | emissive texture, factor 1, 1, 1 | none: no emissive texture, no emissive factor (asserted on export) |
| Roughness | 0.42 | 0.55 (`roughnessFactor` 0.55) |
| Blender specular | 0.35 (glTF `KHR_materials_specular` 0.83) | 0.25 (glTF `KHR_materials_specular` 0.593) |
| IOR | 1.45 | 1.45 |
| Metallic | 0 | 0 |

Codex measured the held material natively at `metallic_specular` 0.5. Blender specular, the glTF specular factor and
Godot's `metallic_specular` are different representations. I make no claim that 0.593 imports as a particular Godot
value; Codex checks the imported mapping.

## Identity (re-imported carrier against re-imported `head_candidate_v012.glb`)

Both eyes:
- 922 vertices and 1,840 triangles each, one UV set;
- position+UV corner records identical, and triangles identical as sets;
- bounds L (0.026, -0.104, 1.116) to (0.098, -0.032, 1.188), R mirrored.

Triangle order inside the eye meshes is not stable between exports, as documented since v010, so identity is checked
as sets, not as bytes.

## Blender evidence (`eye_e1_comparison.png`, not native)

- **Ref view:** the eyes read warm brown with a darker pupil and one lit highlight; no pale ring, no glow.
- **Alt view:** the near eye still shows a small highlight; the far eye is mostly hidden by the cheek.
- **Game scale (170 px):** the eyes still read as two dark eyes.

## Known risks (for R1 to R5 and the one value-only follow-up)

1. **R2:** at the alt angle the highlight is small and depends on the light. A lit albedo highlight can vanish in
   shade by design. If the native eyes read as flat holes, the follow-up is catchlight value or size.
2. The lower iris (122, 78, 46) may read lighter than the reference's dark ovals. The other follow-up lever is the
   iris bottom value.
3. The iris now covers the lid opening. If native lid geometry differs from Blender's, a sclera sliver could still
   show (R1).
4. The native specular mapping is unverified (see above).

After R1 to R5 and at most one value-only follow-up, stop. A remaining failure points at eye-opening geometry; no
geometry change is inferred from this packet.
