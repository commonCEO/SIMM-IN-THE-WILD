# ART-004 boot candidate v002: smoother boot, softer ankle, fitted sole rocker

Status: review candidate for Codex's native fit, answering the five points at `f98e519`. Not a parity claim, not for
live swap. Same four parts, bones, export structure and materials as v001. Head v009, collar v004 and jacket v003
re-hashed and unchanged; `verify_candidate.py`: `FROZEN_ALL_UNCHANGED True`.

## Files

| Path | Purpose |
|---|---|
| `boot_candidate_v002.glb` | For Codex. Identity root `SCULPT_BOOTS_ROOT`, four static meshes in actor space, `bind_bone` extras, metres, Y-up, no armature, animation, camera or light. sha256 `f430933f0112901e6d95c05b7c0cbafaccf8c9b2772262eff0db8d6957faf925`, 834,424 bytes. |
| `renders/boot_v002_before_after_contact_and_ankle.png` | v001 against v002, side and low camera, at rest, walk 25 and 75 percent, gather 50 percent. |
| `renders/boot_v002_before_after_full.png` | Whole figure, v001 against v002, reference camera. |
| `renders/boot_v002_colour_ref.png`, `_colour_side.png`, `_colour_alt.png`, `_clay_ref.png` | Whole figure. Blender Cycles, review only. |
| `build_scripts/boot_build.py` | Now v002 (v001 at `fe5cd45`). Input `work/collar_packet_v004.blend`. |
| `build_scripts/boot_check.py` | Unchanged checks, 97 samples per clip. |

## The five points

1. **Toe, heel and sole perimeter.** The notches came from construction, not from too few polygons: v001's sole stopped
   8 mm short of the toe tip, so the upper's toe hung over it, and the sole was a coarse 1,200-triangle shell with
   squared ends. Now the foot is resampled into 46 sections with quarter-ellipse ends in plan. The sole is one shell
   round the whole outline, 4 mm proud of the upper everywhere including toe and heel, with rounded edges
   (3,000 triangles per sole). Smooth-shading split angle raised to 80 degrees. Sole 22 mm, heel 30 mm, as before.
2. **Shaft to ankle.** The shaft now flares by 7 mm toward the ankle so it meets the boot foot softly instead of a
   straight pipe into a step. It has two restrained soft folds at Z 0.186 and 0.228, 2.5 and 1.8 mm. The heel top was
   raised so the back of the foot rises smoothly into the shaft. The cuff is lower and thinner: 22 mm tall, 3.5 mm proud.
3. **Sole rocker fitted to the clips.** For each foot, the build samples the foot bone 49 times in each of `idle`,
   `walk` and `gather`, finds how far each point of the sole outline would go below the floor, and lifts the sole
   there, smoothed. It converged in 2 passes: lift 13.3 mm at the heel, 1.9 mm at mid-foot, 18.8 mm at the toe,
   residual 0.4 mm. The whole boot is not raised: the lowest part of the sole stays on the floor at rest.
4. **Material base values held.** Same leather and sole values as v001. Names, export structure and binding as v001.
5. **Before and after.** In `renders/`. Only the boots changed.

## Part manifest (re-imported GLB)

| Part | Bone | Verts | Tris | Bounds, Blender axes, metres |
|---|---|---|---|---|
| `SCULPT_BOOT_SHAFT_L` | `shin_l` | 3,584 | 6,000 | X -0.188..-0.045, Y -0.082..0.068, Z 0.100..0.290 |
| `SCULPT_BOOT_FOOT_L` | `foot_l` | 6,145 | 10,998 | X -0.195..-0.045, Y -0.199..0.098, Z 0.000..0.172 |
| `SCULPT_BOOT_SHAFT_R` | `shin_r` | 3,623 | 6,000 | X 0.045..0.188, Y -0.082..0.068, Z 0.100..0.290 |
| `SCULPT_BOOT_FOOT_R` | `foot_r` | 6,158 | 10,998 | X 0.045..0.195, Y -0.199..0.098, Z 0.000..0.172 |

Total 33,996 triangles (v001: 24,400). This is review density; the game budget follows the measured profile.
Hide list unchanged: the 1,784 foot-owned triangles of the three original shoe materials, keeping the 376 pack-strap
triangles.

## Measured in Blender, 97 samples per clip (dense sampling, not continuous proof)

| Clip | Trouser vertices outside a shaft | Shaft lower edge outside the boot foot | Lowest point of either boot | Original soles, same samples |
|---|---|---|---|---|
| idle | 0 | 0 | Z 0.000 | Z 0.000 |
| walk | 0 | 0 | Z -0.001 to 0.002 | Z -0.001 to 0.013 |
| gather | 0 | 0 | Z -0.000 to 0.000 | Z -0.000 to 0.003 |

Floor contact now matches the original soles' envelope (v001: down to -0.007 in walk). No offending frame to show.

## Known issues

- The two shaft folds are even all the way round. They read a little like rings rather than slouched leather;
  a front-weighted or tilted fold would be the next step.
- The toe is still plain, with no toe-cap line or stitching.
- Flat working material, lighter than the reference's boots, as before.
- The exposed-trouser and jacket-length gap is unchanged. Codex plans a separate deformation proposal after this fit.
