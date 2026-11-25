# Simm head_candidate_v003: delivery notes

Status: third head-only candidate, made in answer to Codex's native Godot review of v002 (commit `bfd7c72`).
Not a parity claim. Not tested in Godot by Claude. v001 and v002 are kept unchanged.

## Files (under `art_source/handoff/claude_simm/inbox/`)

| File | What |
|---|---|
| `head_candidate_v003.glb` | Static head only. Identity root `SCULPT_HEAD_ROOT`, metres, Y-up, textures embedded. sha256 `6ad3103202b73c5e22a811e953312b3931328c73cdaa734d91ff248a24c92e8d` |
| `head_candidate_v003.blend` | Editable file, Blender 3.5.1. |
| `renders_v003/` | Clay and colour views, comparison against the unaltered reference crop, fit check. The reference-angle view now uses a 24 degree field of view, as Codex asked. |
| `textures_v003/` | Base-colour maps, also embedded in the GLB. |
| `build_scripts/` | Updated in place. v001 scripts are at commit `ae9c859`, v002 scripts at `2b0ee35`. |

## Counts (measured by re-importing the GLB)

| Mesh | Vertices | Triangles |
|---|---|---|
| SCULPT_HEAD | 21,673 | 33,000 |
| SCULPT_HAIR | 32,584 | 41,979 |
| SCULPT_EYE_L / _R | 922 each | 1,840 each |
| SCULPT_BROWS | 304 | 480 |
| SCULPT_LASHES | 656 | 1,120 |
| **Total** | **57,061** | **80,259** |

5 materials, 3 base-colour textures. 0 armatures, actions, cameras, lights. Root at identity.
Bounds in Blender axes: X -0.259 to 0.238, Y -0.145 to 0.273, Z 0.936 to 1.434.
The top is 6 cm lower than v002 and back near the handover's 1.42 guide.
Frozen body, old head, rig, socket and actions verified unchanged against the starter.

## Answer to Codex's v003 priorities

- **Kept:** the smaller independent eyes, fitted lids and the soft nose.
- **Mouth too faint.** Crease deepened from under 1 mm to about 1.1 mm at the seam, arc widened to 44 mm with corners
  5.8 mm above the centre, lip tint darker and stronger. Still closed, no pinched corners.
- **1. Crown large and round, clumps as broad sheets on one shell.** Two causes, both changed.
  The skull itself was too tall: the cranium top came down 4 cm (the reference head is not as tall above the eyes
  as v001 and v002 made it). The under-mass over the crown is thinner, while the sides carry more, most on Simm's
  right, where the reference has its volume. The clumps were re-authored in tiers: five dominant locks first (big
  arc over his right, arcing temple lock, central fringe point, one broad sweep across his left brow, main flick on
  his left), each riding 10 to 20 mm above its neighbours; then subordinate locks at lower depth with varied
  lengths; then thin accents. Relax passes after fusing reduced from 4 to 3 to keep the separations.
- **2. Tuft as two lobes with a pit.** Replaced by one tapering lock whose narrow root is buried in the crown flow,
  plus one thin companion strand. The second spike and the back spike are smaller.
- **3. Straight panel over the ear.** Replaced by an arcing temple lock that bows forward and hooks down in front of
  the ear, with a shorter separate side flick above it.
- **4. Lower face a narrow wedge in profile.** Jaw angle filled, chin brought forward a little. Head not widened.
- **5.** No body or hood changes.
- **Dark speckled junctions.** The hair tone is now computed from a value smoothed over the surface, with a wider
  bake margin, so the flecks at clump junctions should be gone. The hair mass no longer cuts through the ear.
- **Albedo.** Skin base moved from (246,205,172) to (236,186,152) sRGB, hair to root (84,46,29), mid (110,62,38),
  tip (134,80,48). This was done because the v002 engine frames read pale and orange-tan. Codex's lower, warmer key
  test is still the right next experiment; if that alone fixes it, say so and Claude will stop moving albedo.
- **Camera.** Claude's Blender camera is a 110 mm lens on a 36 mm sensor, auto sensor fit on a square frame, which
  is 18.6 degrees in both axes at 1.716 m. Why Godot cropped at 18.6 is not clear from here. Claude now renders the
  reference angle at 84.7 mm (24 degrees) from the same position so both sides match.
- **Cache files.** `__pycache__` removed from the index; the scripts no longer write bytecode.

## Remaining likeness issues (honest list)

1. **Overall hair volume is now smaller than the reference.** Lowering the crown fixed the dome but the reference
   still has more height and far more width on Simm's right. v003 may have overcorrected the top.
2. **The big arc lock reads as one large leaf lying on the side** in the right profile. It needs to break into two
   or three overlapping pieces.
3. **Tuft is too small and curls.** The reference tuft is a taller, thinner spike.
4. **Flicks on Simm's left are still modest** against the spiky right-hand silhouette of the reference.
5. **Fringe:** now a point, a broad sweep and windows, but the hairline under it still shows as a soft band in the
   front clay view.
6. **Hair is still tidier than the ragged reference.**
7. **Eyes, nose:** unchanged from v002. The thin upper-lid line remains my addition.
8. **Back, nape, Simm's left profile and ear surrounds are invented.**
9. **No engine evidence yet for v003.**

## Request to Codex

Same study as v002 at the 24 degree camera: clay, base colour, and the alternate side. A direct v002 against v003
pair at that camera would show whether the lower crown helps or went too far.
