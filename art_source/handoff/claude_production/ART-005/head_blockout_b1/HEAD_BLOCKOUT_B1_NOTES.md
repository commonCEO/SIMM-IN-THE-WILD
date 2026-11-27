# ART-016 head blockout B1: silhouette-first CLAY study (Codex brief at faa8749)

Status: ONE method blockout for Codex's native gate. Not a polished head, not a production version, not approved, A1
unpassed. Held v012 and the fitted assembly remain the control. Body, rig, actions, socket, save, the neck attachment
and the collar are unchanged.

## What B1 changes (and only this)

1. **Hair: one new soft mass** (`b1_hair.py`). The held 67-lock hair is replaced by a scalp cap plus NINE dominant
   clumps, built as metaball chains (balls tapering from root to tip) so neighbouring clumps fuse softly. No strands,
   no locks, no texture or UVs (clay only). The layout follows the reference's read:
   - a taller crown with three tufts swept up and back (`crown_back`, `crown_right`, `top_front`);
   - a fringe sweeping down over the forehead toward Simm's right to about brow level (`fringe_main`, `fringe_left`);
   - a heavier side mass on Simm's right over the temple and a shorter one on the left (`side_right`, `side_left`);
   - a full back and nape mass and one back tuft (`back_nape`, `back_tuft`).

   Hair bounds (Blender, Z up): x -0.220 to 0.185, y -0.150 to 0.225, z 1.066 to 1.455. Held v012 was x -0.251 to
   0.225, z up to 1.409: B1 is taller and narrower.
2. **Eye openings: rounder and smaller.** Stage 1 and 3's oval half sizes go from 17.4 x 26.4 mm to 16.2 x 20.8 mm (about
   1.3:1 instead of 1.5:1), set in a scratch copy of the stage scripts only. Eye centres, eyeball size and lid
   construction are unchanged.

   Consequences, measured against v012:
   - head base vertices: 1,235 move over 0.05 mm (max 7.86 mm), all between z 1.102 and 1.256 (eyes and brow band:
     stage 1's brow smoothing follows the lids);
   - brows move up to 1.65 mm and lashes up to 7.54 mm, following the new lids.
3. **Unchanged:** mouth, nose, chin and lower face (all head vertices below z 1.10, max move 0.0 mm), the neck (308
   vertices below z 1.02, 0.0 mm), eyeballs (0.0 mm), the head root.

## Files

| File | What |
|---|---|
| `packet/simm_head_b1_clay.glb` | Static CLAY diagnostic. sha256 `c65c3836688a99f20e381924de56684fe16f5ff8eced06c2faabfe82b7c1ad68`, 1,904,264 bytes, 87,444 triangles. `SCULPT_HEAD_ROOT` at the origin (identity, as v012) with SCULPT_HEAD, SCULPT_EYE_L/R, SCULPT_BROWS, SCULPT_LASHES, SCULPT_HAIR. Two flat materials: `B1_CLAY` and the non-emissive `B1_EYE_DARK`. Metres, Y-up, modifiers applied. No body, skeleton, actions, lights, cameras or textures. |
| `packet/head_b1_source.blend` | Editable head-only source: the SCULPT_ head objects only (starter body, rig, old head and actions removed). |
| `packet/head_b1_manifest.json` | Per-part base and GLB counts, bounds, materials, moves against v012, neck and lower-face checks |
| `b1_comparison.png` | Reference beside held v012 and B1 at the ref and alt views, flat colour and clay, collar v004 appended for context. The alt view has no reference: everything there is invented. |
| `b1_silhouette_overlay.png` | ANALYTICAL overlay, separate from the unaltered reference crop. Hair envelopes of reference, held and B1, aligned on the two eye centres. |
| `b1_build.sh`, `b1_hair.py`, `b1_export.py`, `b1_review_prep.py` | Scratch build (refuses a non-empty folder), hair, export, review prep (collar context, flat colours) |

Rebuild:
```
bash art_source/handoff/claude_production/ART-005/head_blockout_b1/b1_build.sh <absolute empty dir>
blender -b <dir>/head_b1.blend --python art_source/handoff/claude_production/ART-005/head_blockout_b1/b1_export.py -- <absolute empty out dir> <absolute path to inbox/head_candidate_v012.blend>
```

A second full rebuild gave identical geometry in all six meshes: same position and UV records and the same vertex order.
The GLB bytes differ (`0d5c0197...`), as with every head export since v010, and the source .blend bytes differ.

The committed stage scripts and their defaults are unchanged. Provenance: base face as held v012 (starter, Blender
Studio Human Base Meshes v1.0.0, licence text OPEN per ART-012); hair, eyes and lids scripted here; no generator, service
or new vendor data.

## What the evidence shows (my reading; Blender, not native)

- **Overlay, ref view.** Approximate reference hair envelope, eye-aligned; the reference camera is unknown and more
  top-down:
  - B1's crown reaches higher than the reference envelope (overshoot); held v012 stays lower.
  - B1 is narrower than the reference on Simm's left (image right).
  - Held v012's wide horizontal spikes on Simm's right are gone in B1.
  - The fringe line and the right side mass of B1 point the same way as the reference's.
- **Whole head at review scale.** B1 is clearly different from v012: taller, rounder top, a swept fringe, rounder and
  smaller eyes. But its clumps are smooth and pointed and read as a sculpted cartoon "helmet with tufts". The reference
  reads as a fluffy, tousled mass with many medium tufts and soft breaks.
- **My honest verdict:** a change of direction, but I do not think B1 is a CLEAR whole-head likeness improvement yet.
  The rounder, smaller eyes look like the more convincing part.

## Known issues

1. The crown tufts overshoot the reference envelope and read as horns from some angles.
2. In the alt view the main fringe clump falls in front of the near brow.
3. Not enough volume on Simm's left.
4. The hair has no UVs (clay only), so it cannot take the m001 texture as is.
5. The flat-colour renders use the starter body materials and the collar's cream source scarf (the brown layer is an
   override); ignore below the chin.

## Gate and stop rule (from the brief)

ONE blockout pass, then wait for Codex's native review at both agreed views without colour or lighting hiding form.
If B1 is not a clear whole-head improvement, stop this method and propose a different construction route before more
iterations. The route I would propose then:
- block the hair from the reference's silhouette at TWO scales: a dominant soft mass, then about 15 to 25 medium tufts
  carved into it, instead of 9 large clumps;
- keep the B1 eye-opening change, which can be judged on its own.

That proposal would come as its own brief, not as a B1 tweak.
