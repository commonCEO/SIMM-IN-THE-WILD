# ART-015 inlay diagnostic carrier (Codex brief at d64a9e4)

Status: ONE static diagnostic carrier of the EXISTING reviewed composite (`../compose_inlay_demo.py`), exported once, no
retuning. Not a production head or a new version, not approved, A1 unpassed. Codex keeps held brows, hair and materials
and takes only the changed geometry in its own review assembly. Native results are UNKNOWN until Codex tests it.

## Files

| File | What |
|---|---|
| `simm_inlay_carrier.glb` | sha256 `2cb9c8c2813aa0d4de3f87520f223fcd3e9ead44d11dd4bfd5262965e8042171`, 1,383,076 bytes. Contents: `SCULPT_HEAD_ROOT` (same root transform as v012, asserted) with `SCULPT_HEAD`, `SCULPT_EYE_L`, `SCULPT_EYE_R`, `SCULPT_LASHES`. No brows, hair, body, rig, actions, lights or cameras. Exporter options as `stage4_export.py` (Y-up, metres, modifiers applied, embedded images). |
| `inlay_carrier_manifest.json` | Per-part base and exported counts, correspondence, deltas and bounds; locality; image and material identity; checksums |
| `base_vertex_moves.json` | Every moved base vertex: id, held and carrier position, move, and for the head its composite weight and oval coordinate |
| `inlay_carrier_delta_heatmap.png` | Exported head vertex moves on a front projection, with the eye opening, the mask edges and the nose and mouth boxes drawn in; held against carrier clay at ref |

## How it was made (no retuning)

1. `../run_inlay_demo.sh <empty dir>` builds the scratch inlay head from the committed starter with the patched copy of
   the stage scripts (`../inlay_method.patch`, INLAY=1, pinned v012 settings). It is only an intermediate, never the
   carrier.
2. `../compose_inlay_demo.py` takes, on the held `head_candidate_v012.blend`, the eyeballs and lashes whole and the head
   skin around the openings: weight 1 up to oval e 1.6, smoothstep to 0 at e 2.4, front half only. This is the same
   composite Codex reviewed at `5b394e7`.
3. `../inlay_carrier_export.py` exports the four parts and writes the evidence.

Full command:
```
INLAY_BLEND=<abs scratch>/head.blend blender -b art_source/handoff/claude_simm/inbox/head_candidate_v012.blend \
  --python art_source/handoff/claude_production/ART-005/face_method/compose_inlay_demo.py \
  --python art_source/handoff/claude_production/ART-005/face_method/inlay_carrier_export.py -- <abs empty dir> <abs head_candidate_v012.glb>
```

Three exports gave the identical GLB and identical manifests, one of them fed by a second, independent scratch inlay
build.

Source checksums (sha256):
- `inlay_method.patch` `1c43f97a...`
- `run_inlay_demo.sh` `1c1e953f...`
- `compose_inlay_demo.py` `f1f88460...`
- `inlay_carrier_export.py` `7cea8b5d...`

The committed stage scripts and their defaults are unchanged.

## Geometry against held v012 (exported GLB vs `head_candidate_v012.glb`, raw accessors)

| Part | Exported vertices / triangles (carrier = held) | Correspondence | Base vertices moved (> 0.05 mm), max | Exported vertices moved (> 0.05 mm), max | Normals changed |
|---|---|---|---|---|---|
| `SCULPT_HEAD` | 21,673 / 33,000 | index-wise: identical UV arrays and triangle index arrays | 1,004 (954) of 4,118, 6.99 mm | 5,843 (5,173), 6.65 mm | 5,993 |
| `SCULPT_EYE_L` | 922 / 1,840 | index-wise, identical UV and index arrays | 436 (428), 24.46 mm | 436 (428), 24.46 mm | 484 |
| `SCULPT_EYE_R` | 922 / 1,840 | index-wise, identical UV and index arrays | 436 (428), 24.46 mm | 436 (428), 24.46 mm | 484 |
| `SCULPT_LASHES` | 656 / 1,120 | index-wise, identical UV and index arrays | 564 (564), 3.32 mm | 656 (656), 3.32 mm | 656 |

Topology, UVs and material slots are unchanged; only positions and the normals that follow from them changed. The
eyes' triangle order happened to be identical this time. It is known to vary between exports, so Codex may need to
compare eyes as sets.

The eyeball move is large by design: its front half becomes the shallow cap, up to 24.5 mm at the top and bottom of the
hidden part. Changed eye bounds are glTF (0.026 to 0.098, 1.116 to 1.188, 0.082 to 0.104), mirrored for the right eye.

## Locality (exported head; this is a periorbital mask, not "eyes only")

**Head base mesh:** 868 vertices at full weight and 136 in the fade; all 1,004 moved vertices lie inside the mask.

**Exported (subdivided) head:**
- 5,843 vertices moved, within Blender x -0.118 to 0.118, y -0.113 to -0.069, z 1.085 to 1.227.
- Subdivision carries small moves past the mask edge: the furthest moved vertex is at e 3.54, and 501 vertices beyond
  e 2.4 move by at most 0.363 mm. Beyond e 3.54, 13,435 vertices are unmoved.
- **Mouth** (box |x| < 45 mm, z 1.04 to 1.10, front): 1,997 vertices, 0 moved.
- **Nose** (box |x| < 22 mm, z 1.10 to 1.165, front): 1,514 vertices, 110 moved, max 0.051 mm (6 over 0.05 mm). They are
  at the top of the bridge between the eyes, where the fade reaches. Not zero, so reported rather than called frozen.
- **Forehead above e 3.54, cheeks below it, ears, back of head:** unchanged in the export.

## Materials and textures

- Materials: held v012 materials (`SCULPT_MAT_SKIN`, `SCULPT_MAT_EYE`, `SCULPT_MAT_LASH`), field-identical to v012's
  once texture references are resolved to image names (the indices shift because the hair image is not in the carrier).
- Embedded images, byte-identical to v012's (asserted):
  - skin `d38c228a...`
  - eye base `4ad60fc3...`
  - eye emissive `3755b82c...`
- E1 is not baked in. Codex applies the E1 material (`../../eye_e1/`) or flat unlit eyes on these eye meshes, to separate
  the geometry from the texture interaction.

## Known risks, recorded rather than waived

1. With the E1 texture a thin pale arc can show under the upper lash. The shallower cap shows a little more of the
   texture's upper edge.
2. A faint line along the 0.6 mm upper-lid margin was visible in the Blender flat-eye crop.
3. In Blender the whole-face effect is small; the decisive test is native.
4. The nose-bridge top and the subdivision halo move by tiny amounts (above).

## Codex's native pass and stop rule (from the brief)

One native control/candidate at both agreed A1 views, in clay, flat and E1, plus camp zoom 10. Criteria:
- no continuous pale boundary in flat mode;
- the whole-face read visibly improves at normal comparison scale;
- no cap or lash gaps, protrusions or new dents;
- locality, rig, actions and socket held;
- small-scale eyes retained.

If the flat boundary or the whole-face criterion fails, this construction method stops, with no INLAY_EDGE or lid
thickness sweep.
