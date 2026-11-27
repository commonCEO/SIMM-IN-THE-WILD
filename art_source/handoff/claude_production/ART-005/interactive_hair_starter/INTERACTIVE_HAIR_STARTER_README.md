# ART-020 interactive hair starter (Codex dispatch `33b35d4`)

A clean head-only Blender file for a person, or an agent with a working viewport, to sculpt Simm's hair by hand.
This is preparation only:
- it contains NO new hair shape; the editable hair is an exact copy of held v012;
- it is not a candidate, not a production export, and not a likeness gate.

Held v012, A1 (unpassed) and the live game assets are unchanged.

## What is in the file

`simm_hair_starter.blend` (sha256 `ea99c9b06f939e97481749b32da27362cf9fd35eb93821bdca9ebfd36197762b`), built by
`build_starter.py` from `inbox/head_candidate_v012.blend` (sha256 `cb9f9ff1...`). The source file was not saved over.

| Collection | Objects | State |
|---|---|---|
| `00_PROTECTED_FACE_DO_NOT_EDIT` | SCULPT_HEAD_ROOT, SCULPT_HEAD (with its Subdivision modifier), SCULPT_EYE_L, SCULPT_EYE_R, SCULPT_BROWS, SCULPT_LASHES | Unselectable. Must stay unchanged. |
| `01_HELD_HAIR_CONTROL` | SCULPT_HAIR_HELD_CONTROL | The held v012 hair. Hidden and unselectable: toggle the eye icon to compare, never edit. |
| `10_WORK_HAIR` | SCULPT_HAIR_WORK | **The only object to edit.** Starts identical to the held hair (21,387 vertices, 41,983 faces, no modifiers). |
| `20_REVIEW` | CAM_REF, CAM_ALT, CAM_REF_HEAD, CAM_ALT_HEAD, KEY_REF, FILL_REF | Unselectable review setup. |

- **Frame.** Metres. Blender Z up, front -Y, Simm's right -X. SCULPT_HEAD_ROOT is an empty with an identity world
  matrix, as in v012, and all head parts are its children. The glTF export is Y up.
- **Cameras.** The agreed review views from `render_views.py`, aimed at (0, 0, 1.215) with an 84.7 mm lens:
  - CAM_REF: azimuth 30 deg toward Simm's right, elevation 15 deg;
  - CAM_ALT: azimuth 72.3 deg, elevation 15 deg;
  - both at 2.6 m (the full agreed framing). The `_HEAD` versions use the same directions at 1.43 m, the framing of
    Fable's head sheets.
- **Lights.** KEY_REF and FILL_REF are placed for the ref view, as in `render_views.py`.
- **View layers.**
  - `WORK`: the objects' own materials.
  - `CLAY_REVIEW`: everything in plain grey clay (material override REVIEW_CLAY, grey 0.55, roughness 0.6).
- **Render engine.** Eevee at 900 x 900 for local speed. Fable's sheets use Cycles.
- **Removed from this file only:** the body, rig, socket, failed old head, hair guide curves and all actions. They
  remain untouched in the held source.
- **Reference.** The image datablock `APPROVED_REFERENCE (external, not packed)` points to
  `//../../../claude_simm/APPROVED_REFERENCE.png`, which is the approved reference in a full checkout that has Codex's
  branch (git blob `2c3e04d1`, file sha256 `d2af5084...`). It is NOT packed: the .blend holds no reference pixels, and
  nothing was uploaded anywhere. On a checkout without that file it simply shows as missing.

`simm_hair_starter_manifest.json` records, for every object, the vertex and face counts, modifiers, parent, bounds and a
geometry fingerprint. The fingerprint is a sha256 over the base-mesh vertex positions, rounded to 1 micrometre, and the
face vertex indices. Every protected fingerprint equals the held source's. A second build gave the same fingerprints.

## How to work in it

1. Copy the folder somewhere outside any live project or open source work, and open the COPY of
   `simm_hair_starter.blend`.
2. Open the reference beside the 3D view: Image Editor > browse > `APPROVED_REFERENCE`. If it shows as missing, use
   Image > Open on `art_source/handoff/claude_simm/APPROVED_REFERENCE.png`. Do not pack it into the file.
3. Select `SCULPT_HAIR_WORK` (the only selectable mesh) and edit it:
   - Sculpt mode: Grab, Snake Hook, Clay Strips, Crease, Smooth. Turn on symmetry only if wanted; the reference hair is
     asymmetric.
   - Edit mode with proportional editing.
   - Or remesh the work copy first (Object Data > Remesh), or delete it and build new hair in `10_WORK_HAIR`, named
     `SCULPT_HAIR_WORK`.
4. Look through the review cameras (Numpad 0 with CAM_REF_HEAD or CAM_ALT_HEAD as the active camera). Switch to the
   `CLAY_REVIEW` view layer to judge form without colour, and toggle `SCULPT_HAIR_HELD_CONTROL` to compare with the
   held hair.
5. To keep each pass reversible, save numbered copies (File > Save Copy) or duplicate the work object, hide the old
   one and rename it out of the way. The exporter takes exactly one object named `SCULPT_HAIR_WORK`.

## Check and export

`check_and_export.py` (needs `starter_common.py` and the manifest in the same folder):

```
blender -b <your edited copy>.blend --python check_and_export.py
blender -b <your edited copy>.blend --python check_and_export.py -- <absolute new path>.glb
```

In the Blender GUI: Text Editor > Open `check_and_export.py`, set `OUT` near the top for an export, then Run Script.

- **It checks** that the five protected parts are unchanged (geometry, modifiers, parent), that the root sits at
  identity, that the held control is unchanged and that there is exactly one `SCULPT_HAIR_WORK`. It prints counts,
  bounds and whether the work hair differs from the held hair.
- **It exports** only SCULPT_HEAD_ROOT > SCULPT_HAIR (the work hair, renamed for the file): metres, Y up, modifiers
  applied, a placeholder material, no rig, actions, cameras, lights or textures. A `_check.json` with the GLB's
  sha256 is written next to it. The .blend is not saved by the script.
- **It refuses** when any protected part changed, the root moved, the work object is missing or duplicated, or the
  output file exists.

Tested here:
- an export of the unedited starter re-imports as exactly SCULPT_HEAD_ROOT > SCULPT_HAIR with no actions;
- a copy with one head vertex moved 1 mm was refused ("SCULPT_HEAD geometry changed").

Materials, UVs and textures for a new hair shape are a later, separate step: sculpting breaks the held hair's UV
layout.

## Files

| File | sha256 |
|---|---|
| `simm_hair_starter.blend` | `ea99c9b06f939e97481749b32da27362cf9fd35eb93821bdca9ebfd36197762b` |
| `simm_hair_starter_manifest.json` | `2a6d14245c5e56b093ff364b22710ef57bd58fed560f650ef3981f725c22b6c6` |
| `build_starter.py` | `aa2886a084ccab962d8870448c8650248535d105e3091cc93fcc747cae1d9373` |
| `check_and_export.py` | `86fd6b741f94efb84906b00cf10ff6faff7f15f09e2ab4dac5d0b61a5d017392` |
| `starter_common.py` | `01bd4c828420a2a54976a303e75db6c81cd2271731a484a6d37903c9473634de` |
| `starter_preview.png` | the starter through CAM_REF_HEAD and CAM_ALT_HEAD in clay (Blender, not native) |

Rebuild:
```
blender -b art_source/handoff/claude_simm/inbox/head_candidate_v012.blend --python art_source/handoff/claude_production/ART-005/interactive_hair_starter/build_starter.py -- <absolute new .blend path> [<absolute path to the reference png>]
```
The .blend bytes differ between builds; the fingerprints in the manifest do not.

## Known limits

- I could not open the 3D viewport here (headless cloud Blender 3.5.1), so viewport, sculpt-mode and Eevee behaviour
  in this file are untested. The file opens, checks, renders in Cycles and exports headless.
- The packed head textures keep their original absolute source paths as names. That is harmless, because they are
  packed.
- The work hair inherits v012's fused, UV-mapped topology, which is dense and uneven for sculpting. A remesh, or a
  fresh blockout in the same collection, may serve better.

## Next

Codex owns ART-021: checking that Windows Blender's viewport and sculpt tools work in an isolated copy, then, if they
do, a bounded hand-authoring trial on this starter. Fable does no sculpting and no export until that review.
