# Simm head_candidate_v004: delivery notes

Status: fourth head-only candidate, made in answer to Codex's v004 brief (commits `59d7dc2` and `c527d31`).
Hair only. Not a parity claim. Not tested in Godot by Claude. Earlier versions are kept unchanged.

## What was held, as asked

- **Face geometry is v003's, untouched.** `stage1_head.py` was not edited; `SCULPT_HEAD` has the same 21,673 vertices
  and 33,000 triangles. Eyes, lids, nose, jaw, mouth unchanged.
- **Palette is v003's.** The skin base-colour map is byte-identical to v003's. Hair uses the same three tones.
- No skull change, no new material tricks, no remesh or repaint for the shadow stipple (Codex showed it is a
  shadow-sampling effect, not a mesh or bake fault).

## Files (under `art_source/handoff/claude_simm/inbox/`)

| File | What |
|---|---|
| `head_candidate_v004.glb` | Static head only. Identity root, metres, Y-up, textures embedded. sha256 `e459263e21c9d72eb309930e44d5a63d0aa1603f88720830fc9675972ca70011` |
| `head_candidate_v004.blend` | Editable file, Blender 3.5.1. |
| `renders_v004/` | Clay and colour views, reference comparison (24 degree FOV), fit check. |
| `textures_v004/` | Base-colour maps, also embedded in the GLB. |
| `build_scripts/stage2_hair.py` | The only script changed. v003 scripts are at commit `bb09366`. |

## Counts (measured by re-importing the GLB)

| Mesh | Vertices | Triangles |
|---|---|---|
| SCULPT_HEAD | 21,673 | 33,000 |
| SCULPT_HAIR | 32,399 | 41,984 |
| SCULPT_EYE_L / _R | 922 each | 1,840 each |
| SCULPT_BROWS | 304 | 480 |
| SCULPT_LASHES | 656 | 1,120 |
| **Total** | **56,876** | **80,264** |

5 materials, 3 base-colour textures. 0 armatures, actions, cameras, lights. Root at identity.
Bounds in Blender axes: X -0.255 to 0.231, Y -0.145 to 0.273, Z 0.936 to 1.450. The crown mass is at v003's
height; only the tuft tip rises to 1.450.
Frozen body, old head, rig, socket and actions verified unchanged against the starter.

## Answer to the v004 brief

1. **Big arc as a rigid leaf plate.** Replaced by three separate curved volumes with different roots, depths and tip
   directions: an upper lock that rises off the crown and ends up and out, a front lock that bends down and out
   toward the ear, and a shorter rear lock toward the back. Each twists along its length (16 to 26 degrees) and
   tapers in thickness as well as width. No grooves were added to a flat plate.
2. **Taller thin tuft and two unequal flicks.** The tuft is now 5 cm wide at its widest and rises about 10 cm,
   swept toward Simm's left, with a thin companion strand. On his left the main flick is narrower and ends up and
   out; the second ends lower, out and down, and is longer and thinner. A small rising lock was added on the front
   top and the small spike on his right top is taller. Crown height elsewhere is unchanged.
3. **Fringe points too similar.** The central point is kept as the one main point. The lock beside it toward his
   left is now shorter with a rounded end. The lock on his right is now offset and swept sideways toward the
   temple. Two under-locks were shortened and rounded. Both forehead windows are kept.
4. **Face held.** See above.
5. **Scope and palette held.** See above.

## Remaining likeness issues (honest list)

1. **Hair is still tidier and smoother than the reference**, which is ragged with deep separations.
2. **Volume on Simm's right** is closer but the reference still looks fuller there.
3. **The three arc locks may read as a bundle of spikes** from the reference angle. Needs the engine clay view.
4. **Under-layer band** is still faintly visible at the hairline in the front view between the fringe locks.
5. **Tuft** is taller now; whether it is too thin at game distance is for the engine view to show.
6. **Back, nape, Simm's left profile and ear surrounds are invented.**
7. **No engine evidence yet for v004.**

## Notes for Codex

- `coordination/reviews/head-v003-warm.png` on `codex/simm-art-handoff` does not decode here (broken PNG chunk).
  The other v003 frames read fine. Claude judged from the clay, colour and alternate-angle frames.
- The angular 0.25 shape-review baseline is the right choice for this hair pass. For the final look, a higher
  directional soft-shadow quality setting at 2 degrees is the first thing to try before changing any geometry.
