# ART-018 hair route R2, Stage A: hair-only CLAY diagnostic (Codex brief at `634c089`)

Status: ONE Stage A packet for Codex's native gate. Clay only, not a production head, not approved, A1 unpassed.
Held v012 and the fitted assembly stay the control. Built on held v012, not on B1. Face, eyes, brows, lashes, neck,
body, rig, actions and socket are untouched; only SCULPT_HAIR is replaced (and SCULPT_HAIR_GUIDES dropped).

## What Stage A is

`r2_stage_a.py`, run on `inbox/head_candidate_v012.blend`:

1. **Under-surface.** Grown from the head's own scalp along the skin normals: 4 mm inside the skin at the hairline,
   rising to 6 mm outside it above (hairline height 1.238 m at the front, 1.182 m at the side, 1.075 m at the back). It
   is meant to hide scalp between pieces and never show a cap edge.
2. **17 authored pieces**, one hand-placed cubic guide each, in five layers from the back to the front:
   - layer 1: back_nape, back_right, back_left;
   - layer 2: side_right_back, side_right, side_left_back, side_left;
   - layer 3: temple_right, temple_left, top_cover;
   - layer 4: fringe_right, fringe_main, fringe_mid, fringe_left (sweeping toward Simm's right);
   - layer 5: crown_tuft (up and back), flick_right, flick_left.

   Each piece is swept with 48 rings of an 18-point ridged-lens section: a broad rounded top, a flatter underside, no
   razor edge. Width swells slightly, then tapers to a point; depth thins steadily. The ridge faces away from the head
   centre. Guide points before the tip are kept at least 4 to 14 mm outside the skin.
3. **Assembly.** All pieces stay separate overlapping islands in one object, with no voxel, metaball or other fusion.
   Roots are capped and buried under the next layer.

No stage script, stage default, material, UV or texture changed. No parameter sweep: two authoring passes before
delivery (the first was too narrow, with a bowl-like under-surface), then this packet.

## Files

| File | What |
|---|---|
| `packet/simm_hair_r2_stage_a_clay.glb` | Static hair-only clay GLB. sha256 `fdf6a4d8d1b59e5485a000311bfe40e89987ff58358a81d1637e9e2c64ff2e2b`, 590,008 bytes. Nodes: SCULPT_HEAD_ROOT (identity, as v012) > SCULPT_HAIR. One flat material `R2A_CLAY`. Metres, Y-up. No armature, skin, animation, texture, UV, camera or light. |
| `packet/hair_r2_stage_a_source.blend` | Minimal editable source: SCULPT_HEAD_ROOT and SCULPT_HAIR only. sha256 `a25b0849...`. |
| `packet/hair_r2_stage_a_manifest.json` | Counts, bounds, materials and checksums from the re-imported GLB. |
| `r2_stage_a.py` | Builds Stage A on held v012 (deterministic). |
| `r2a_export.py` | Hair-only export, re-import check and minimal source. Refuses a non-empty or relative output folder. |
| `r2a_invention_prep.py` | Review-only: colours each piece by how much of it the reference shows. Never exported. |
| `r2a_sheets.py` | Builds both sheets from the review renders (PIL only). |
| `r2a_comparison.png` | Two views, clay: CONTROL held v012 beside CANDIDATE Stage A at ref and alt. The unaltered reference crop sits in its own panel. |
| `r2a_overlay.png` | ANALYTICAL: the ref-view hair envelopes (reference, held, Stage A) aligned on the two eye centres, with a +-12 px edge uncertainty band; plus invention maps at both views (seen, partly seen, invented, under-surface). |

Counts from the re-imported GLB: 16,395 vertices, 32,522 triangles, 20 islands (17 pieces plus the under-surface in 3
parts). Bounds (Blender, Z up): x -0.183 to 0.194, y -0.139 to 0.222, z 1.078 to 1.432 m. Held v012 hair was x -0.251
to 0.225, z up to 1.409.

## Rebuild

```
blender -b art_source/handoff/claude_simm/inbox/head_candidate_v012.blend --python art_source/handoff/claude_production/ART-005/hair_route_r2/stage_a/r2_stage_a.py -- <abs out.blend>
blender -b <abs out.blend> --python art_source/handoff/claude_production/ART-005/hair_route_r2/stage_a/r2a_export.py -- <abs empty out dir>
```

A second build from a fresh `--factory-startup` run gave the same 16,395 vertices in the same order (max difference
7.5e-9 m).

## Preservation

`verify_candidate.py` on the built blend against the committed starter copy and v012 GLB: `FROZEN_ALL_UNCHANGED True`
(the 17 rest matrices, bones, actions, socket, protected body and the hidden old head). Nothing in `godot/`, `src/`,
saves or Codex's files was touched.

## Provenance

The guides, sections and under-surface are scripted here. The under-surface derives from the held v012 head (base face:
Blender Studio Human Base Meshes v1.0.0, licence text still OPEN per ART-012). No generator, paid service or new vendor
data. The reference was read with `git cat-file` and is not committed on this branch.

## Rejection criteria (from the brief), and my honest reading (Blender, not native)

| Criterion | My reading |
|---|---|
| Horns or inflated lobes | **Likely fail.** No lobes. But the crown tuft is a single tall curved spike well above the envelope band, so it reads as an antenna. Codex asked to keep a conspicuous tuft; this one is too tall and too lonely. |
| Flat blade or ribbon tops, paper edges | **Pass in clay.** Every piece shows a rounded ridge and a soft edge. The two flicks lie flat on top and read as stuck-on leaves. |
| Smooth exposed helmet side wall | **Partial.** The alt view shows stacked pieces with dark breaks, no wall. But the grey under-surface shows as a smooth band between the fringe and the brows and at the temples (invention map), and in clay it reads as a cap edge. |
| Dangling fringe hiding the forehead | **Fail.** The fringe is a curtain of long points reaching the brows. The gaps show under-surface, not forehead skin. |
| Root gaps or intersections | **Issue.** No visible root gaps on the front. On Simm's left, side_left_back hangs away from the head with daylight behind it in both views. |
| Clear whole-head likeness benefit | **No, in my view.** Cleaner and friendlier than v012, without the spiky "horror" read. But it reads as a neat anime bowl cut: narrower, smoother and longer at the front than the reference's wide, tousled mass with tufts flaring out at both sides. Different, not clearly closer. |

Overlay numbers (ref view, eye-aligned, 700 px): hair pixels outside the reference envelope plus band: Stage A 16,943
(nearly all above eye level: the tuft and the top), held v012 31,830 (mostly sideways spikes on Simm's right). Read
them as directions, not measurements: the reference camera is unknown and more top-down.

## Diagnosis (Codex correction 3), if the gate fails

- **Guide placement (main cause).** The fringe tips are 20 to 30 mm too low. The side pieces hug the skull instead
  of flaring out to the envelope, so the head reads narrow. The tuft is too long.
- **Section and taper.** All pieces share one taper, so they read as one repeated leaf. The reference mixes short,
  wide tufts with a few longer points.
- **Assembly.** Nothing crosses or flares outward; the under-surface sits too close to the skin at the front hairline.
- **Camera.** Some of the height gap comes from the reference's higher view, not from the model.

The route I would propose then: keep R2's construction (sections, layers, no fusion) and re-author the GUIDES only,
in one pass on this source:
- fringe tips raised to mid-forehead, so skin shows between them;
- side and back pieces flared outward to the band, Simm's right heavier;
- the crown tuft shortened into the band and paired with one or two short neighbours;
- the under-surface moved back from the front hairline.

If that still fails, the honest next input is clearer hair reference from the user (for example Mattias's drawings),
not another construction cycle.

## Next

One Stage A packet, then wait for Codex's native gate at the two agreed views. Nothing further until then.
