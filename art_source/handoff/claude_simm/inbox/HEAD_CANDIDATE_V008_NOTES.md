# Head candidate v008: hair colour and gloss only

Status: delivered for Codex's native test. Made at the user's request: on 26 Nov 2026 the user reviewed a native
side view, said "IMO we're still 30% off", and approved reopening the hair and the collar ("Yes, this needs to have
full parity, for Mattias to be happy"). Collar v003 is the other half of the same request. Not a parity claim.

## What changed

Only the hair material. Every mesh in the GLB is identical to v007, vertex for vertex (checked by re-importing
both files). Skin and eye textures are byte-identical to v007. Face, skull, hair shape and palette of the skin
are unchanged.

| | v007 | v008 |
|---|---|---|
| Hair root colour (sRGB) | 84, 46, 29 | 102, 52, 24 |
| Hair mid colour | 110, 62, 38 | 128, 70, 32 |
| Hair tip colour | 134, 80, 48 | 162, 100, 50 |
| Hair roughness / specular | 0.52 / 0.40 | 0.70 / 0.25 |

Why, measured: in the reference the hair's median colour is about 138, 76, 36, its shadows about 88, 37, 12 and its
highlights about 179, 111, 56. In the user's native frame of v007 the median was 120, 67, 39 and the shadows went
down to 55, 30, 17. v007 was darker, greyer and shinier than the reference. The new colours are warmer and more
saturated, the dark roots are lifted, and the gloss that made the hair read as plastic is cut (audit hypothesis L3).

## Files

| Path | Purpose |
|---|---|
| `head_candidate_v008.glb` | For Codex. Same objects, names, counts and bounds as v007: 80,265 tris, X -0.251..0.225, Y -0.134..0.274, Z 0.936..1.444. No rig, animation, camera or light. sha256 `c74a310fc198f8c28eca4de3857ce84a3563a4b5176b38c83ad5e081c7ec5116`, 3,203,764 bytes. |
| `head_candidate_v008.blend` | Editable source, Blender 3.5.1. |
| `textures_v008/` | Embedded textures. Only `simm_head_hair_basecolor.png` differs from v007 (sha256 `95495f269e5c0f10fa3ba4da91897bcbd94cc9b21107f368594fffd738a48aa8`). |
| `renders_v008/` | Colour at the reference and alternate cameras, side and back, all with collar v003 and the frozen body; the reference next to them. Blender Cycles, review only. Clay frames are not repeated: the geometry is v007's. |
| `build_scripts/stage3_finish.py` | The only script changed: hair palette and material. |

`verify_candidate.py`: `FROZEN_ALL_UNCHANGED True`. Built from `starter_copy/START_HERE_v02.blend` through stages
1 to 4 as before.

## Known issues

- Hair shape is unchanged. The back still ends in pointed locks; collar v003 now covers the nape under them.
- In my Blender light the hair reads a little orange and flat. Godot's light will differ; judge it there.
- The skin is still pale and grey on the shadow side in Godot. That is mostly lighting (audit hypotheses L5, L9).
- Not a parity claim.
