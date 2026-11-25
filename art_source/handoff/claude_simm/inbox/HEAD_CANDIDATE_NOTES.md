# Simm head_candidate_v001: delivery notes

Status: first head-only candidate for review. This is not a parity claim. Stop point reached: head, hair, eyes only.

## Read this first: two deviations from the handover

1. **The approved reference was not available.** `START_HERE_v02.blend` contains no packed image named
   `APPROVED_SIMM_REFERENCE` (its only images are three unpacked texture links to `D:/SimmInTheWild/godot/...`),
   and `APPROVED_REFERENCE.png` was not uploaded. The sculpt was judged against the only copy of that picture in
   the repository: `docs/v06-art-directions.png`, panel 2, where Simm's head is about 55 px wide instead of 145 px.
   `assets/art/simm-walk.png` and `docs/title.png` were used as secondary design cues for the hair layout.
   The comparison sheet shows that low-resolution copy, labelled as such.
2. **No interactive Blender session.** This ran in a cloud container with Blender 3.5.1 headless (same version as
   the starter), not through a Blender connection on the PC at `D:/SimmInTheWild`. Sculpt brushes need a viewport,
   so every stroke was applied as a scripted grab, inflate, scale or smooth with a soft falloff, then rendered and
   corrected by eye, pass after pass. The strokes are in `build_scripts/` in the order they were applied. Nothing
   from the earlier Codex head or hair generators was used; the hidden old head was not read.

## Files (all under `art_source/handoff/claude_simm/inbox/`)

| File | What |
|---|---|
| `head_candidate_v001.blend` | Editable file, Blender 3.5.1. Starter scene plus new `SCULPT_*` objects. Textures packed. |
| `head_candidate_v001.glb` | Static head only. Identity root, metres, Y-up, base-colour textures embedded. |
| `renders/head_v001_reference_comparison.png` | Reference (low-res repo copy) beside the new model, colour and clay. |
| `renders/head_v001_clay_sheet.png`, `head_v001_colour_sheet.png` | Reference angle, front, both sides, back. Labelled. |
| `renders/head_v001_{clay,colour}_{ref,front,side,sideL,back}.png` | Single 1000 px views. |
| `renders/head_v001_fit_on_frozen_body.png` | Scale check on the frozen body. Body is not exported. |
| `textures/*.png` | The three base-colour maps, also packed in the .blend and embedded in the GLB. |
| `build_scripts/` | Stroke-by-stroke authoring scripts, renderer, exporter, verification. |

## Objects in `10_SCULPT_NEW_HEAD`

| Object | Source and treatment | In GLB |
|---|---|---|
| `SCULPT_HEAD` | The supplied base face (Blender Studio Human Base Meshes v1.0.0, CC0), 4,118 verts / 4,134 polys, reshaped. Subdivision modifier level 1, not applied. Original UV map kept. | yes, subdivision applied |
| `SCULPT_EYE_L`, `SCULPT_EYE_R` | The supplied eye objects. Their geometry was replaced with a clean sphere: the base eye's cornea-bulge loops shaded as a visible ring once made spherical. | yes |
| `SCULPT_HAIR` | New. One fused sculpted surface. | yes |
| `SCULPT_BROWS`, `SCULPT_LASHES` | New. Thin real geometry, nothing painted. | yes |
| `SCULPT_HAIR_GUIDES` | New. The 64 authored hair guide paths as NURBS curves, for editing. | no |
| `SCULPT_HEAD_ROOT` | New. Empty at identity, parent of the meshes. | yes (root) |

## Counts (measured by re-importing the GLB into an empty scene)

| Mesh | Vertices | Triangles | Material |
|---|---|---|---|
| SCULPT_HEAD | 21,673 | 33,000 | SCULPT_MAT_SKIN (2048 px base colour) |
| SCULPT_HAIR | 30,856 | 39,986 | SCULPT_MAT_HAIR (1024 px base colour) |
| SCULPT_EYE_L / _R | 922 each | 1,840 each | SCULPT_MAT_EYE (512 px base colour) |
| SCULPT_BROWS | 304 | 480 | SCULPT_MAT_BROW (flat colour) |
| SCULPT_LASHES | 656 | 1,120 | SCULPT_MAT_LASH (flat colour) |
| **Total** | **55,333** | **78,266** | **5 materials, 3 textures** |

GLB contains 0 armatures, 0 actions, 0 cameras, 0 lights. Root: location 0, rotation 0, scale 1.
Bounds in Blender axes: X -0.208 to 0.237, Y -0.133 to 0.253, Z 0.936 to 1.469.
The skull top is near Z 1.37 and the hair mass near 1.41; the top cowlick reaches 1.469, above the 1.42 guide.
The neck runs down to Z 0.936 so it disappears inside the collar. Hair vertex count is high for its triangle
count because of split normals and UV seams on the fused surface.

This is a likeness-review density, not a game budget. 78k triangles for a head is too heavy for the playable
actor. Reduction and a bake belong after the shape is approved, as the plan already states.

## Frozen reference: verified unchanged

`build_scripts/verify_candidate.py` compares the candidate against the untouched starter
(sha256 `1157d3201b16be71e51323fcb7abfbeae78e5b3d388f1b35e417cbdfb52b9db4`, identical to the upload):

- `PROTECTED_BODY`: vertex data hash, counts, matrix, parent, visibility, materials, groups, modifiers unchanged.
- `REFERENCE_FAILED_OLD_HEAD`: same checks, unchanged, still hidden.
- `SimmRig`: object matrix and all 17 bone rest matrices and parents unchanged.
- `hand_r_socket`: transform, parent bone unchanged.
- Actions `gather`, `idle`, `walk`: every keyframe unchanged.

No file outside `art_source/handoff/claude_simm/inbox/` was created or changed. `godot/` is untouched.
One side effect to know about: the starter's scene render engine is restored to Eevee, and the three missing
texture links on the body stay missing exactly as they arrived.

## What was sculpted

Head, in order: toddler proportions (cranium enlarged and widened, lower face shortened, neck slimmed), nose reduced
to a small upturned button, adult brow ridge and glabella melted into one calm slope, cheeks filled low, jaw rounded,
chin kept small. The mouth was redesigned on the base's own three lip-seam loops as a closed, upturned line about
45 mm wide. The eyelids use the base's real lid rings: they were refitted onto 43 mm-radius eyeballs as upright
ovals (45 x 60 mm opening), upper lid carrying the thickness, lower lid flush, eyeball set about 3.5 mm behind the
surrounding skin so it does not bulge.

Hair: a thick mass over the hair-bearing scalp, then 64 individually placed clumps (back in two tiers, nape
under-clumps, heavier right side over the ear, lighter left side with outward flicks, a fringe with one central
point between the brows, top masses sweeping forward from a crown whorl, a three-part cowlick, thin accent strands).
Everything is fused into one surface and relaxed, so clumps share roots and only separate toward the tips.

Colour: albedo only. Skin base tone with cheek, nose-tip and ear warmth, a lip tint, and a faint lash-root tone.
Iris is a dark upright oval with a lighter lower half. No painted shadows, no painted highlights, no baked light.

## Invented, because the reference does not show it

- The whole back of the head: both back tiers, the nape, the crown whorl position.
- Simm's left profile and the hair behind and around both ears.
- The exact hairline under the fringe, and the ear shape.
- Eye colour detail. At 55 px the reference eyes are dark ovals and nothing more.

## Remaining likeness issues (honest list)

1. **Eyes are bigger and glossier than the reference.** Mine read slightly doll-like. The reference eyes are
   smaller, closer to matte, and sit a little higher. First thing I would change after review.
2. **Face is rounder and wider than the reference.** The lower face tapers to a narrower chin than the picture
   suggests. Cheeks are right in spirit, the outline is more chibi than the reference.
3. **Fringe hangs like a curtain.** The reference fringe sweeps sideways from a parting with a few bold points.
   Mine falls mostly straight down with too many similar small teeth. The "evenly spaced" risk in the brief is
   not fully cleared across the forehead.
4. **Hair is stiffer and less airy than the reference.** Clumps are well merged, but the mass is helmet-like at
   the temples and the under-layer edge shows as a clean line beside the ears and as two light slivers at the nape.
5. **Small pits in the hair surface** near Simm's right temple and one in the fringe, left from fusing.
6. **Cowlick is too big and reads as a comb from the front.** Direction is right, scale is not.
7. **Hair tone is cooler and darker than the reference**, which is lit by warm sun. Not comparable until Codex
   lights it in Godot.
8. **Neck is visible and thin above the collar.** The reference hides it behind a hood and scarf the frozen body
   does not have at that height. Not a head problem, but it will show in the engine render.
9. **Nostril dots** remain as two faint dimples under the nose tip.
10. **Reference resolution.** Every judgement above was made against a 55 px head. Items 1 to 3 need re-checking
    against the real 2048 x 1270 file.

## What I need for v002

`APPROVED_REFERENCE.png` uploaded into the session. With it I would fix items 1 to 6 as a head-only revision.

## Reproduce

```bash
blender -b START_HERE_v02.blend --python inbox/build_scripts/stage1_head.py -- "$PWD/inbox/work/stage1.blend"
```

```bash
blender -b inbox/work/stage1.blend --python inbox/build_scripts/stage2_hair.py -- "$PWD/inbox/work/stage2.blend" 0.0021 40000
```

```bash
blender -b inbox/work/stage2.blend --python inbox/build_scripts/stage3_finish.py -- "$PWD/inbox/head_candidate_v001.blend" "$PWD/inbox/textures"
```

```bash
blender -b inbox/head_candidate_v001.blend --python inbox/build_scripts/stage4_export.py -- "$PWD/inbox/head_candidate_v001.glb"
```

```bash
blender -b --python inbox/build_scripts/verify_candidate.py -- "$PWD/START_HERE_v02.blend" "$PWD/inbox/head_candidate_v001.blend" "$PWD/inbox/head_candidate_v001.glb"
```
