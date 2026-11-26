# ART-001 eye-spacing diagnostic (Codex brief at 9243be2): result, no v011

Status: diagnostic only. Neither variant improved both views, and the measurement does not support wider eyes, so
no v011 was exported (as the brief allows). v010 stays the working head; nothing delivered as a new head.

## What was measured, and how

Eye-centre spacing divided by the visible head width (skin and hair, ears included) on the image row through the
eye-line midpoint. The eye spacing itself is NOT used to normalise, so it isn't hidden. Model values come from
`build_scripts/head_landmarks.py` (new: visible width on the eye-line row, from projected skin and hair vertices,
about 1 px). Reference values are read from the approved reference crop, as marked on the sheet: eye centres
detected as the two dark blobs, head edges and chin read by eye.

| | Eye spacing / visible head width, reference camera | Same, front camera | (Hair top to eye line) / (eye line to chin), reference camera |
|---|---|---|---|
| Reference | about 0.31 (0.29 to 0.34; edges +-15 px) | no front view exists | about 2.2 (2.05 to 2.35) |
| v010 (control) | 0.336 | 0.378 | 2.57 |
| +6% eye separation | 0.353 | 0.400 | (same) |
| +10% eye separation | 0.365 | 0.415 | (same) |

All values are in `eye_spacing_measurements.json`; the sheet is `eye_spacing_diagnostic.png` (reference annotated;
v010, +6% and +10% in clay at the reference and front cameras and in colour at the reference camera).

## Reading

- **Eye spacing is not the gap.** v010 already sits at the top of the reference's range; +6% and +10% move it out.
  A smaller bracket (+3%) would also move away from the reference, so it was not built. Visually both variants read
  only slightly different from v010. At +10% the far eye starts to crowd the cheek contour in the three-quarter view.
  Neither is a clear improvement in both views.
- **The larger-head read comes from height above the eyes.** From the top of the hair to the eye line, v010 measures
  about 2.6 times the eye-to-chin depth, against about 2.2 in the reference. That is the hair and crown volume, which
  matches Codex's note that the hair still reads as a broad layered sculpt. This is my measurement-based opinion; the
  reference is blurred and the camera is not solved.

## How the variants were made (kept in the scripts, off by default)

- `stage1_head.py`: `EYE_SPREAD` env (default 1.0 = v010). Moves the lid, lid-ring and orbital-skin face sets
  sideways together, fading out over the surrounding skin and to nothing within 20 mm of the midline, then refits the
  lids on eyeballs at the new centre. Eyeball size, eye height (Z 1.170) and depth unchanged. +6% = 3.7 mm and +10% =
  6.2 mm per eye. Nose, mouth and cheeks not moved.
- `stage3_finish.py`: the brows' angles scale by the same factor so they stay over the eyes (documented tracking).
- With the default, a clean rebuild from the starter reproduces v010 exactly (all six meshes: 0 vertices moved).
- The hair is rebuilt on the face, so the variants' hair remesh also differs slightly. For a real v011 I would graft
  v010's hair unchanged.

## Proposed next action (for Codex)

Hold v010. If the head-proportion gap is worth one more bounded study, measure and test the hair and crown height
above the eyes (for example a lower crown mass and shorter top locks, at two brackets) at the same two cameras.
That is hair work, which the brief sequenced after this decision.
