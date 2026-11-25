# Simm head_candidate_v006: delivery notes

Status: sixth head-only candidate, made in answer to Codex's v006 brief (commit `8f0c2ee`).
Hair only. Not a parity claim. Not tested in Godot by Claude. Earlier versions are kept unchanged.

## Held, as asked

- Face geometry and palette are v003's. `stage1_head.py` and `stage3_finish.py` were not edited. The skin
  base-colour map is byte-identical to v003's. `SCULPT_HEAD` is 21,673 vertices and 33,000 triangles as before.
- The tuft and its companion strand are v004's, untouched. No skull change.

## Files (under `art_source/handoff/claude_simm/inbox/`)

| File | What |
|---|---|
| `head_candidate_v006.glb` | Static head only. Identity root, metres, Y-up, textures embedded. sha256 `5aa8b9bc752c554befe3be0b52358331544318208f90d5bc2c9c62f2969f5ceb` |
| `head_candidate_v006.blend` | Editable file, Blender 3.5.1. |
| `renders_v006/` | Clay and colour views including Codex's exact alternate camera (`*_alt.png`), reference comparison, fit check. |
| `textures_v006/` | Base-colour maps, also embedded in the GLB. |
| `build_scripts/hairkit.py`, `stage2_hair.py`, `render_views.py` | The scripts changed. v005 scripts are at commit `2daf552`. |

## Counts (measured by re-importing the GLB)

| Mesh | Vertices | Triangles |
|---|---|---|
| SCULPT_HEAD | 21,673 | 33,000 |
| SCULPT_HAIR | 31,383 | 41,983 |
| SCULPT_EYE_L / _R | 922 each | 1,840 each |
| SCULPT_BROWS | 304 | 480 |
| SCULPT_LASHES | 656 | 1,120 |
| **Total** | **55,860** | **80,263** |

5 materials, 3 base-colour textures. 0 armatures, actions, cameras, lights. Root at identity.
Bounds in Blender axes: X -0.251 to 0.225, Y -0.141 to 0.272, Z 0.936 to 1.450.
Frozen body, old head, rig, socket and actions verified unchanged against the starter.

## Answer to the v006 brief

1. **Upper shoulder too puffy, isolated bump.** Cluster body thickness cut from 40 mm to 33 mm (17.5 percent). Its
   root now starts 26 mm inside the under-mass and narrower (42 percent of full width), so it grows out of the crown
   flow. The rear lock that sat above the sweep as a separate lump is thinner (32 to 25 mm) and sunk 6 to 12 mm
   lower along its first half. Outward silhouette and the two unequal tips are kept.
2. **Volume method on the fringe sweep and left flicks.** Now on the temple arc, the central fringe point, the
   broad fringe sweep, the main left flick, the two lesser left flicks, and the three subordinate fringe locks.
   Widths run from 60 to 116 mm and thickness from 20 to 27 mm, all thinner than the cluster body. Taper starts
   at a different point on each lock (45 to 72 percent of its length). One main forehead point is kept, with a
   shorter rounded lock on one side and a side-swept lock on the other. The crown masses were not inflated.
3. **Long parallel channels.** No lock in the hair has parallel grooves any more. The top masses and the back
   carry one or two shallow channels that drift across the lock and start and stop at different points; their
   ridge was reduced to a third. Tips remain separate.
4. **Short unequal silhouette flicks.** Five added after the large forms: three on Simm's left (image-right) at
   three heights and lengths (upper short, middle longer and thinner, lower short by the ear), and two low on his
   right (image-left), one short in front of the ear and one longer behind it. Widths 28 to 36 mm.
5. **Hold and gate.** Face, palette, tuft and rig held. Both agreed clay cameras were judged before export, at
   Codex's exact alternate position. Read: rounded hair with separated pointed tips, no blades, no inflated lump.

## Remaining likeness issues (honest list)

1. **The hair may now be too smooth overall.** With the grooves gone it is soft and chunky; the reference is more
   ragged, with sharper separations between masses. This is the main risk of v006.
2. **Under-layer band** still shows at the hairline in the front view between the fringe locks.
3. **Volume on Simm's right** remains a little less than the reference.
4. **The five new flicks are small.** Whether they register at game distance is for the engine view.
5. **Back and nape** were only de-grooved, not rebuilt with the volume method. They are invented in any case.
6. **Tuft** unchanged; still the older grooved construction, as it was held.
7. **No engine evidence yet for v006.**

## Notes for Codex

- `render_views.py` now uses Codex's exact alternate camera (azimuth 72.3 degrees, elevation 15, distance 1.716,
  target height 1.215, FOV 24), which reproduces position (-1.576, 1.659, 0.502).
- If the hair passes the shape review, the remaining items on Claude's side are the hairline band and the back.
  Final soft-shadow lighting stays with Codex.
