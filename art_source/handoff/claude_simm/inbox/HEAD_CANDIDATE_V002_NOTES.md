# Simm head_candidate_v002: delivery notes

Status: second head-only candidate. Not a parity claim. Not tested in Godot by Claude: the engine comparison is Codex's.
v001 files are kept unchanged next to this version.

## What changed the inputs

- The full 2048 x 1270 `APPROVED_REFERENCE.png` (from `codex/simm-art-handoff`, commit `b143f31`) was used for the first time. v001 was judged against a 55 px copy.
- Codex's native Godot review of v001 (`coordination/reviews/claude-v001-godot-colour.png` and `-clay.png`, commit `8ffedf9`) was read and each priority is answered below.

## Files (under `art_source/handoff/claude_simm/inbox/`)

| File | What |
|---|---|
| `head_candidate_v002.blend` | Editable file, Blender 3.5.1. Starter scene plus new `SCULPT_*` objects. Textures packed. |
| `head_candidate_v002.glb` | Static head only. Identity root `SCULPT_HEAD_ROOT`, metres, Y-up, base-colour textures embedded. |
| `renders_v002/head_v002_reference_comparison.png` | Unaltered crop of the approved reference beside the new model, colour and clay. |
| `renders_v002/head_v002_clay_sheet.png`, `head_v002_colour_sheet.png` | Reference angle, front, both sides, back. Labelled. |
| `renders_v002/head_v002_{clay,colour}_{ref,front,side,sideL,back}.png` | Single 1000 px views. |
| `renders_v002/head_v002_fit_on_frozen_body.png` | Scale check on the frozen body. Body is not exported. |
| `textures_v002/*.png` | The three base-colour maps, also packed in the .blend and embedded in the GLB. |
| `build_scripts/` | Updated in place for v002. The exact v001 scripts are at commit `ae9c859`. New: `make_sheets.py`. |

## Counts (measured by re-importing the GLB into an empty scene)

| Mesh | Vertices | Triangles | Material |
|---|---|---|---|
| SCULPT_HEAD | 21,673 | 33,000 | SCULPT_MAT_SKIN (2048 px base colour) |
| SCULPT_HAIR | 31,466 | 41,973 | SCULPT_MAT_HAIR (1024 px base colour) |
| SCULPT_EYE_L / _R | 922 each | 1,840 each | SCULPT_MAT_EYE (512 px base colour) |
| SCULPT_BROWS | 304 | 480 | SCULPT_MAT_BROW (flat colour) |
| SCULPT_LASHES | 656 | 1,120 | SCULPT_MAT_LASH (flat colour) |
| **Total** | **55,943** | **80,253** | **5 materials, 3 textures** |

GLB contains 0 armatures, 0 actions, 0 cameras, 0 lights. Root: location 0, rotation 0, scale 1.
Bounds in Blender axes: X -0.259 to 0.237, Y -0.144 to 0.276, Z 0.936 to 1.496.
The hair mass now tops out near Z 1.44 and the tuft tip at 1.496. That is above the 1.42 guide in the handover. The
reference's own head-to-body ratio (head with hair about one third of the figure) supports the bigger hair; the guide
was written as subordinate to the silhouette. Flag it if the engine framing disagrees.
Still review density, not a game budget.

## Frozen reference: verified unchanged

`build_scripts/verify_candidate.py` against the starter (sha256 `1157d3201b16be71e51323fcb7abfbeae78e5b3d388f1b35e417cbdfb52b9db4`):
`PROTECTED_BODY`, `REFERENCE_FAILED_OLD_HEAD`, `SimmRig` (17 bone rest matrices), `hand_r_socket` and the actions
`gather`, `idle`, `walk` all unchanged.

## Answer to Codex's five priorities

1. **Hair silhouette.** Rebuilt from the full reference. 55 authored clumps instead of 64, most of them 9 to 12 cm wide
   instead of 5 to 10. The fringe is parted above Simm's right eye and swept diagonally toward his left, a heavy
   mass sits over his right temple and ear with tips kicking out, three flicks point out and up on his left, one
   tall tuft leans toward his left with a second spike beyond it. Hair mass is 3 to 5 cm thick instead of 2 to 3.
   Clump undersides now sink into the mass, which closed the pits Codex saw near the fringe roots. One pit remains
   at the tuft root (see issues).
2. **Eyes.** Opening reduced from 45 x 60 mm to 35 x 53 mm. The iris now fills the opening, so the eye is one dark
   oval with no white ring. Roughness raised from 0.14 to 0.30. Lid edge thinned (upper 3.4 mm, lower 1.2 mm) and the
   lash strip cut to 2.2 mm wide, so the hard rim is gone. Eyeballs are still separate meshes with fitted lids.
   Eyeball radius reduced from 43 to 36 mm because the larger sphere broke through the skin at the temples.
3. **Forehead and lower face.** The fringe now reaches the brows, with one point between them and a small window
   above each eye. Jaw filled, chin widened and rounded, cheek inflation halved, face about 5 percent narrower.
4. **Mouth and nostrils.** Both rebuilt. The cause of the "beak" was the base's adult overbite: the area under the
   nose sat about 9 mm ahead of the mouth and chin. Mouth and chin were brought forward, then the whole lip zone was
   laid onto a surface fitted to the skin around the mouth, and the seam was seated on it as a 41 mm closed arc with
   a crease under 1 mm deep. The nose was replaced by a single soft upturned bump on the same fitted surface. No
   nostril pits remain. The mouth is closed: the "subtle opening" Codex reads in the reference is not modelled.
5. **Colour.** Hair base colour moved to a warmer chestnut (root 98,54,33 to tip 164,102,60 sRGB). Skin slightly
   warmer. Still albedo only. Final colour judgement belongs in Godot under the warm key.

## Remaining likeness issues (honest list)

1. **Fringe edge is still a row of teeth.** The lower edge of the fringe has about seven similar points across the
   forehead. The reference has fewer, broader, softer clumps with one or two clear gaps.
2. **Hair is still smoother and tidier than the reference.** The reference hair is ragged, with deep separations
   between clumps and strong flicks on Simm's left at eye level. Mine is one well-merged mass; the left flicks are
   present but modest.
3. **Tuft.** Direction and size are closer, but from the front it reads as a knot, and there is a visible pit at
   its root from Simm's left side.
4. **Eyes.** Size and darkness are now close. The thin dark upper-lid line is my addition; the reference does not
   clearly show one. Eye spacing is my estimate from a foreshortened view.
5. **Face outline.** Rounder than v001. It may still be wider at the cheeks than the reference; this needs the
   Godot perspective view to judge.
6. **Brows** are almost fully under the fringe, as in the reference, so they contribute little.
7. **Back, nape, Simm's left profile and both ear surrounds are invented.** The under-layer edge beside the ears is
   still a clean line.
8. **Small dark flecks in the hair texture** from the baked root-to-tip tone. Cosmetic.
9. **Neck** is visible above the collar; the reference hides it with a hood and scarf the frozen body lacks.
10. **No engine evidence yet for v002.** All views here are Blender Cycles under neutral light.

## Request to Codex

A perspective Godot render of `head_candidate_v002.glb` at the camera Claude uses for the reference angle:
target (0, 1.215, 0), position (-0.829, 1.659, 1.435) in Godot axes, FOV about 18.6 degrees, square frame. Clay
first, then base colour, then the planned skin-only subsurface test at 0.20 with everything else fixed.
