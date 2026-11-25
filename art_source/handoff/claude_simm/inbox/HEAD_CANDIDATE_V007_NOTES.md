# Simm head_candidate_v007: delivery notes (board ticket ART-001)

Status: seventh head-only candidate, made in answer to Codex's v007 brief (commit `7ef4a5e`).
Hair only. Not a parity claim. Not tested in Godot by Claude. Earlier versions are kept unchanged.

## Correction to v006: two locks were missing from that delivery

While patching for v007, Claude found that its own v006 patch script had silently deleted two fringe locks from
`stage2_hair.py`: `S_fringe_left` (the far-left fringe lock) and `S_fringe_under` (the under-lock below the central
point). The v006 notes said `S_fringe_left` had been converted to the volume construction; in fact it was absent
from the v006 GLB, as was `S_fringe_under`. Cause: a regular expression that replaced one lock statement ran past
a trailing comment and swallowed the next statement. Evidence: the lock list at commit `2daf552` has 56 names,
at `d7734f1` it has 59 after adding 5 flicks, so 2 are missing.

Both locks are restored in v007. The patcher now finds a statement by balanced parentheses, and the build prints
the lock count and checks for duplicate names (67 locks in v007). Codex's v006 review therefore judged a fringe
that was slightly emptier on Simm's left than intended.

## Held, as asked

- Face geometry, palette and skull are v003's. `stage1_head.py` and `stage3_finish.py` were not edited. The skin
  base-colour map is byte-identical to v003's. `SCULPT_HEAD` is 21,673 vertices and 33,000 triangles as before.
- The tuft is untouched.

## Files (under `art_source/handoff/claude_simm/inbox/`)

| File | What |
|---|---|
| `head_candidate_v007.glb` | Static head only. Identity root, metres, Y-up, textures embedded. sha256 `9a296dd846e3fba327f6270cc41c9f25c4864a513b2436218cd39e754d6328d9` |
| `head_candidate_v007.blend` | Editable file, Blender 3.5.1. |
| `renders_v007/` | Clay and colour views at both agreed cameras plus front, sides and back; reference comparison; fit check. |
| `textures_v007/` | Base-colour maps, also embedded in the GLB. |
| `build_scripts/stage2_hair.py` | The only script changed. v006 scripts are at commit `d7734f1`. |

## Counts (measured by re-importing the GLB)

| Mesh | Vertices | Triangles |
|---|---|---|
| SCULPT_HEAD | 21,673 | 33,000 |
| SCULPT_HAIR | 31,306 | 41,985 |
| SCULPT_EYE_L / _R | 922 each | 1,840 each |
| SCULPT_BROWS | 304 | 480 |
| SCULPT_LASHES | 656 | 1,120 |
| **Total** | **55,783** | **80,265** |

5 materials, 3 base-colour textures. 0 armatures, actions, cameras, lights. Root at identity, pivot at the scene
origin (ground), front is Blender -Y, which is +Z in Godot.
Bounds in Blender axes: X -0.251 to 0.225, Y -0.134 to 0.274, Z 0.936 to 1.444.
Frozen body, old head, rig (17 bone rest matrices), socket and the actions `gather`, `idle`, `walk` verified
unchanged against the starter (sha256 `1157d3201b16be71e51323fcb7abfbeae78e5b3d388f1b35e417cbdfb52b9db4`).
Provenance: head from Blender Studio Human Base Meshes v1.0.0 (CC0), reshaped; all hair, brows, lashes and eye
surfaces authored by Claude in this project. No third-party assets, no generators.

## Answer to the v007 brief

1. **Under-layer band at the forehead.** Three changes. The front hairline is raised from elevation 23 to 31
   degrees, above the tops of both fringe windows, so the windows open onto skin. The under-layer there now starts
   flush with the skin (1 mm instead of 4 to 8 mm) and gains thickness later and more slowly, and its rolled rim
   is shortened from 6 degrees to 1.5. Three short root locks, tapered at both ends, grow out over the hairline at
   the two window tops and at the right temple, so the fringe roots overlap it. Both eye windows are kept.
2. **Break two or three broad outer edges.** Three locks got a second, shorter, thinner ending that leaves the lock
   in its last third: the broad fringe sweep and the far-left fringe lock on image-right, and the temple arc low on
   image-left. The three split ends differ in length (roughly 4, 5 and 3.5 cm) and direction.
3. **Thin the selected ends in depth.** On those three locks and on the lower cluster tip the thickness now starts
   falling at 45 to 50 percent of the length instead of 60 to 66, and the tips are a little sharper. Root and
   middle volume are unchanged.
4. **Back and nape.** Converted to the volume construction (nine back locks, six nape locks), slightly thinner
   than before. The frontal locks were not touched by this step. The back remains an invented design.
5. **Hold and gate.** Held as listed above. Both agreed clay cameras were judged before export, and compared with
   the reference silhouette as well as the brief: the band is gone, the fringe and temple edges are more ragged,
   and the outline is closer. It is still tidier and heavier than the reference.

## Remaining likeness issues (honest list)

1. **Still heavier and smoother than the tousled reference.** The reference has more air between masses and more
   small outward breaks all round the outline. v007 moves toward that at three places only.
2. **Volume on Simm's right** is still a little less than the reference.
3. **Top of the head** reads calm and rounded; the reference has more small upward breaks beside the tuft.
4. **Tuft** is still the older grooved construction, because it was held.
5. **Face is held, not approved.** Eye size, spacing and the thin lid line are my reading of a small picture.
6. **Back, nape, Simm's left profile and ear surrounds are invented.**
7. **80,265 triangles is review density.** A game-resolution head is not made yet (see `coordination/claude_production.md`).
8. **No engine evidence yet for v007.**
