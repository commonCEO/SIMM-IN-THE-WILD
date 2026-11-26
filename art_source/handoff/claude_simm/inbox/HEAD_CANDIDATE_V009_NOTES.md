# Head candidate v009: friendly face (eyes, brows, smile, skin warmth)

Status: delivered for Codex's native test. Made at the user's request, 26 Nov 2026: "your version looks like it's
from Silent Hill or from some horror cartoon, and what's on the concept is very cute ... you should fix it."
This overrides the hold on the face, palette and skull that has been in place since v003, for the face's
expression only. Not a parity claim.

## Why it read as creepy (found in the build, not guessed)

- **Eyes.** Since v002 the painted iris was wider than the lid opening (iris half width 0.026 m, opening 0.0174 m),
  so each eye was one solid dark glossy oval: no white, no visible iris, no highlight. In Godot's light they read
  as empty black holes. Every face in the concept art has white eyes, a dark iris and a highlight.
- **Brows.** Thin, pale (150, 98, 68) and about 36 mm above the top of the eye: a blank, staring expression.
- **Mouth.** A short, faint line.
- **Skin.** Pale, and grey on the shadow side in Godot.

## What changed (`build_scripts/stage3_finish.py` only)

| | v008 | v009 |
|---|---|---|
| Iris half size | 0.0260 x 0.0340 m, wider than the eye opening | 0.0140 x 0.0262 m: white shows at both sides, the iris touches both lids |
| Iris colour | 34, 20, 15 to 70, 42, 28 | 48, 27, 16 at the top to 140, 86, 44 at the bottom, darker outer ring |
| Pupil | 0.0110 x 0.0160 m | 0.0068 x 0.0118 m |
| Highlights | none | one large and one small catchlight, painted and also in a new emissive texture, so they show in any light |
| Brows | 5.2 mm wide, 1.8 mm thick, colour 150, 98, 68, about 36 mm above the eye | 7.8 mm wide, 2.6 mm thick, colour 98, 54, 30, close above the eye with an arch |
| Smile | painted line to the edge of the mouth seam | crisper, darker (150, 62, 58), about 40 percent wider than the seam, corners turned up, small dimples |
| Skin | base 236, 186, 152, cheek blush 0.42 | base 244, 186, 148, cheek blush 0.58 and a little wider |

Unchanged and checked: head, eye, hair and lash meshes are identical to v008 after re-import. Only the brows are
new geometry. The hair texture is byte-identical to v008. `verify_candidate.py`: `FROZEN_ALL_UNCHANGED True`.

## Files

| Path | Purpose |
|---|---|
| `head_candidate_v009.glb` | For Codex. Same object names, root and bounds as v007 and v008. 80,345 tris (brows +80). No rig, animation, camera or light. The eye material now has an `emissiveTexture` (`simm_head_eye_emissive`, emissive factor 1, 1, 1). sha256 `255f781e7be19dda8775b3b6f297d4f8327705eea30ef7ca12298861c2f94e7b`, 3,232,556 bytes. |
| `head_candidate_v009.blend` | Editable source, Blender 3.5.1. |
| `textures_v009/` | Embedded textures, including the new eye emissive mask. |
| `renders_v009/head_v009_reference_comparison.png` | Reference crop, v008 and v009 at the reference camera. |
| `renders_v009/` (others) | Colour at reference, alternate, front and side; clay at reference and alternate; full body at both cameras. All with collar v003 and the frozen body. Blender Cycles, review only. |

## For Codex natively

- The emissive catchlights should hold their brightness under the scene light. If they bloom too much, lower the
  emissive energy on `SCULPT_MAT_EYE` rather than removing it.
- The catchlights are mirrored between the eyes (both sit toward the outer upper side), as is usual for this style.
- Please look at the face at gameplay zoom too: the brows and the smile were sized to read there.

## Known issues

- The lower face is still a little long in three-quarter and side views. That is head geometry; not changed here.
- The smile line is wider than the mouth seam in the mesh. From the front it reads as one smile; at a steep angle
  the seam and the painted line could separate.
- Flat colours, not seen in Godot yet.
