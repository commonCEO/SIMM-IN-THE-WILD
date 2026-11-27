# Head candidate v012: round-section construction on four locks (Codex brief at cc6e2a8)

Status: review candidate for Codex's native check against held v011 + m001-B. Reversible: v011 is archived and
rebuilds with `HAIR_ROUND=` (set, empty). Not a parity claim, no A1 approval.

## What changed, and only this

The accepted round section (`hairkit.sweep(section="round")`, from the D2 method gate) is applied to exactly four
locks, the stage 2 default now: `D1_arc_body`, `D2_temple_arc`, `D4_fringe_sweep`, `S_fringe_right`. All four use the
default width factor 0.78. No per-lock adjustment was needed: in clay at both held cameras, plus front, side and top,
there were no gaps, no exposed scalp, roots stayed seated and the D1 tips and D2/D4 split tips stayed attached.
Guide paths, width profiles, channels and roll are unchanged. Every other lock is held, including the `top_*` masses,
the tuft, D1's tips and rear piece, D2/D4's split tips and the v011 crown map. The face, eyes, lids, brows, lashes,
jaw, neck and root are held, as are clothing, rig and actions.

The hair is one fused, re-unwrapped surface, so its UVs are new. The hair texture was re-baked through them with the
EXACT m001-B recipe (`build_scripts/hair_material_m001.py`, same palette and drift) at roughness 0.70, as a build step.
That is mapping upkeep, not a colour change: covered-texel median sRGB is unchanged at 112, 64, 37. Face, eye and skin
textures are byte-identical to v011.

## Evidence

Sections at 25, 50 and 75 percent of each changed lock, on the fused hair (`renders_v012/head_v012_four_lock_sections.png`,
grey v011, orange v012). Share of the +-25 mm window flatter than 12 degrees:

| Lock | 25% | 50% | 75% |
|---|---|---|---|
| D1_arc_body | 0.92 to 0.53 | 0.85 to 0.88 | 0.91 to 0.56 |
| D2_temple_arc | 0.53 to 0.40 | 0.41 to 0.21 | 0.48 to 0.25 |
| D4_fringe_sweep | 0.75 to 0.50 | 0.56 to 0.53 | 0.50 to 0.23 |
| S_fringe_right | 0.25 to 0.25 | 0.50 to 0.29 | 0.27 to 0.29 |

D1 at mid-length stays flat. There its guide sits about 2 mm above the held under-mass, so the flat surface in that
window is mostly the held primary mass, not the lock's own section. That is my reading of the guide offsets; it was
not separated by measurement. D4 at 75 percent rises less (30 to 14 mm across the window) because the narrower lock
leaves more of the neighbouring surface in the window. S_fringe_right was already the least flat lock.

Held envelope and silhouette:
- Crown: silhouette height above the eye line over eye-to-chin is unchanged at both cameras (full 2.27 / main 2.12 at
  `ref`, 2.45 / 2.34 at `alt`). The silhouette is 6 px narrower in `alt`, and its area changes by -0.1 percent (`ref`)
  and -0.4 percent (`alt`).
- Fringe tips: the lowest front hair at seven points across the forehead is identical to v011.
- Displacement against v011: 2,080 of 21,387 hair vertices moved more than 1 mm, at most 17.2 mm. 95 percent of them
  lie within 46 mm of the four guides; nothing farther than 70 mm from them moved more than 3 mm (elsewhere only 1 to
  3 mm of remesh noise).

Visual (my reading): in clay at the reference camera, D1's arc and D4's sweep read as rounded clumps instead of one
broad shelf. At the alternate camera the large top-left panel breaks into more separate rounded locks. The change is
modest at whole-figure scale.

## Files

| Path | What |
|---|---|
| `head_candidate_v012.glb` | Static head only. sha256 `e5a47d01d203f1438226850632b58a2c7b1e657eaec05d4a6c4faf8019e1e2de`, 3,174,964 bytes, 80,344 tris. Root `SCULPT_HEAD_ROOT` at the origin, identity. Bounds (Blender Z-up after re-import) (-0.251, -0.134, 0.936) to (0.225, 0.274, 1.409), the same as v011. Materials as v011; `SCULPT_MAT_HAIR` exports metallic 0, roughness 0.7, `KHR_materials_specular` 0.5928, `KHR_materials_ior` 1.45 (identical to v011's block). No rig, animation, camera or light. |
| `head_candidate_v012.blend` | Editable source, rebuilt from `starter_copy/START_HERE_v02.blend`: stages 1 to 3 with default environment settings, but stage 2 with the arguments `0.0021 42000` (not its defaults), then `hair_material_m001.py` with its third argument (installs the bake), then stage 4. Correction added 27 Nov (ART-012): the whole chain is now `build_scripts/build_head_v012.sh`, verified by a cold rebuild (identical geometry, byte-identical textures). |
| `textures_v012/hair_bake_record.json` | The bake's record: hair UV and position checksums, UVs unchanged by the bake, palette, 1024 px, 10 px margin. |
| `textures_v012/` | Hair base colour (new bake, sha `135bec5768a6ce8990b959b79fbb7f0e781b1a1187be75b6c6b6a2c8b53f181d`, also the exact image embedded in the GLB); eye, emissive and skin images byte-identical to v011. |
| `renders_v012/head_v011_vs_v012_comparison.png` | v011 against v012: close clay and clay at `ref` and `alt`, colour with m001-B, and a whole-figure pair. |
| `renders_v012/head_v012_four_lock_sections.png` | The twelve sections. |
| `renders_v012/head_v011_top_v012_bottom_coverage_clay.png` | Front, side and top coverage check. |
| `renders_v012/head_v012_{colour,clay}_*.png` | Single frames. Blender Cycles, review only. |

`verify_candidate.py`: `FROZEN_ALL_UNCHANGED True`. Against v011's GLB: `SCULPT_HEAD`, `SCULPT_EYE_L/R`,
`SCULPT_BROWS` and `SCULPT_LASHES` have 0 vertices moved. `SCULPT_HAIR` is 31,223 vertices in the GLB (41,984 tris),
remeshed. A second rebuild from the starter gave identical geometry in all six meshes and a byte-identical hair
texture; GLB bytes differ only by the eye meshes' triangle order, as with v010 and v011.

Provenance: as v011 (Blender Studio CC0 base head; hair, eyes and textures scripted here). No generators, purchases
or outside services.

## Honest issue list

1. Remaining scope, not changed here: the `top_*` crown masses and D1's under-mass still present broad surfaces
   (visible from the top and in the alternate camera). They use the same plate section.
2. D1 at mid-length is still flat in the measured window, for the reason above.
3. The flat-share metric is a Blender measurement in a fixed window, not a likeness score. Nothing native.

## Proposed next action

Codex checks v012 natively against v011 + m001-B. If it holds, the next decision is whether the remaining crown masses
get the same treatment.
