# Claude (Fable) production file: acknowledgements, ticket updates, proposals

Written by Claude only. Codex reconciles this into `PRODUCTION_BOARD.md`. Updated 25 November 2026, about 21:00 UTC.

## Acknowledgement of PROD-001

Read on `codex/simm-art-handoff` at commit `a403661`: `PRODUCTION_PLAN.md`, `PRODUCTION_BOARD.md`,
`FABLE_NEXT_CHECK.md`, `DECISIONS_AND_RISKS.md`, the `START_HERE.txt` addition, the v006 review, the art direction
guide, the boss and new-idea notes, and the section list of the game design document (not yet the full text).

Accepted as written:

- **Roles.** Fable: Blender asset production and QA, art research, materials and textures, art packet specs,
  later UI illustration and design proposals. Codex: board, Godot runtime and renderer, browser parity, saves,
  controller verification, packaging.
- **Gates.** A1 before any NPC, body or world mesh. Audits, specs and proposals may run now.
- **Fable's tickets.** ART-001 (active), ART-004, ART-006 (started), ART-007, ART-008, ART-009, ART-010, ADD-001.
- **Fences.** Fable writes only its own files; never Codex's files, the runtime, saves, rigs or actions. No paid
  generators. No force-push. One active asset revision at a time.
- **File homes.** Proposals here; deliveries in `claude_deliveries.md`; the ART-006 audit in
  `coordination/claude_art_audit.md`; head packets in `art_source/handoff/claude_simm/inbox/`; later families in
  `art_source/handoff/claude_production/<ticket-id>/`.

## Ticket updates (board format)

**ART-012 / Fable / REVIEW (build helper hardening, 27 Nov, run 39, answers `e01071e`)**
- Trigger: Codex reviewed the ledger and asked for ONE bounded follow-up: pin the v012 settings inside the head build
  helper, refuse a non-empty output folder, prove it from a contaminated environment, and update the ledger with
  Codex's PC evidence.
- Files: `art_source/handoff/claude_simm/inbox/build_scripts/build_head_v012.sh` (hardened);
  `coordination/claude_art_provenance.md` (run 39 update).
- Checks actually run (scratch only, nothing exported to the branch):
  - rebuild from a shell with all six switches and PYTHONPATH contaminated: six meshes with identical position+UV
    records and vertex order; four textures byte-identical; no diagnostic object; FROZEN_ALL_UNCHANGED True; GLB bytes
    differ by the known eye triangle order;
  - refusal on the non-empty folder: exit 3, 15 files untouched;
  - negative control without the helper: different hair, 21,502 against 21,387 vertices.
- Open, not resolved here: the v1.0.0 licence text; publishing the PC-only textures and generators (PROD-002).
- Next dependency: Codex reconciles ART-012.

**ART-012 / Fable / REVIEW (provenance and cold-rebuild ledger, 27 Nov, run 38, answers `dd8e50c`)**
- Trigger: Codex assigned ONE Fable-owned source-readiness ledger for the held Simm art, with no asset revision.
- Files: `coordination/claude_art_provenance.md`; new `art_source/handoff/claude_production/ART-004/sources/`
  (collar_packet_v004, boot_candidate_v002, jacket_candidate_v004 `.blend`, compressed, mesh positions and actions
  identical to the working files); new `art_source/handoff/claude_simm/inbox/build_scripts/build_head_v012.sh`;
  correction line in `HEAD_CANDIDATE_V012_NOTES.md`.
- Result: deliverables and editable sources READY for every held packet. Head v012 cold rebuild verified (33 s, six
  meshes 0.00 mm, four textures byte-identical). m002 rebuild verified earlier (run 33).
- Open items needing the user or Codex: base-face licence record (only an in-file "Blender Studio CC0" label);
  `cloth_tone.png`, `leather_tone.png`, `simm_eye.png` (PC only); origin of the starter's body, rig and actions; runtime
  `simm.glb` (PC only); the reference's own terms. Not resolved here, no workaround.
- Next dependency: Codex reconciles the ledger into the board; source publication stays behind PROD-002 approval.

**ART-006 / Fable / REVIEW (A1 look-method L2, 27 Nov, run 36, answers `4097e24`)**
- Trigger: Codex's native L1 run rejected the side key (hard shadow across lower cheek, mouth and chin; hard strap and
  hand shadows); asked for ONE L2 fill method that keeps a friendly face and gives a directional read.
- Files: `coordination/claude_art006_look_method.md` (L2 section on top, L1 kept below);
  `art_source/handoff/claude_production/ART-006/look_method_l2/` (labelled Blender demo, metrics);
  `ART-006/build_scripts/look_method_l2_demo.py` (review only, never saves).
- Method: keep the native key and all its shadows; add one DirectionalLight3D from the L1 side direction, shadows off,
  energy 0.3, #ffe6c8, light_specular 0. Cast shadows, strap/hand silhouettes and boot contact unchanged by design.
- Evidence actually used: Codex's native L1 selected controls; a Blender demo with the native key and side directions
  converted from Codex's values (the rejected side key reproduces the native lower-face shadow there). Missing tone
  textures stood in by 0.5. Nothing native run by Fable.
- Next dependency: Codex's native base versus base + SimmFormFill test.

**ART-006 / Fable / REVIEW (A1 look-method note L1, 27 Nov, run 35, answers `e91d3bd`)**
- Trigger: Codex held p001 and asked for ONE A1 look-method note: at most three ranked rendering gaps and one controlled
  lighting/material method with per-variable changes, predicted result and failure criteria. No asset revision.
- Files: `coordination/claude_art006_look_method.md`; `art_source/handoff/claude_production/ART-006/look_method_l1/`
  (labelled Blender demo sheet, metrics JSON); `ART-006/build_scripts/look_method_demo.py` (review only, never saves).
- Content: gaps ranked (1) fill colour and key-to-fill balance, (2) fabric/skin/hair response, deferred, (3) contact and
  cast-shadow quality, Codex's RENDER-001. Method L1: A ambient #b7c9d2 to #d9c7a8; C ambient 0.35 to 0.25; B key about
  45 deg off the ref camera, 45 deg elevation, 0.8 to 1.0. Run order base, A, A+C, A+C+B, B alone. Failure criteria:
  shaded hue under 34 deg or lemon highlight lost, face shadow under 0.6x lit cheek or fringe band over the eyes, more
  shadow stepping, flattened value range, any grading.
- Evidence actually used: Codex's native p001 frames and the full reference (jacket hue and value measured); a Blender
  demonstration with no bounce light and a 0.5 stand-in for the missing tone textures. Nothing native run by Fable.
- Next dependency: Codex's native RENDER-001 test of L1.

**ART-004 / Fable / REVIEW (supporting palette p001, 27 Nov, run 34, answers `2625b68`)**
- Trigger: Codex held m002 and asked for ONE whole-Simm supporting palette as a JSON material override, geometry held.
- Files: `art_source/handoff/claude_production/ART-004/support_palette_p001/` (`simm_support_palette_p001.json`,
  `palette_shared_use_check.json`, comparison and game-scale sheets, notes); new `build_scripts/support_palette_apply.py`
  (review only, never saves).
- What changed: only the multiply factors (glTF baseColorFactor) of Simm charcoal olive trousers, Simm olive canvas,
  Simm woven olive straps and Simm canvas seams; cloth_tone texture, roughness and specular kept. Linear and sRGB for
  current and proposed are in the JSON.
- Checks actually run: each target material exists once and colours only its intended body region; the hidden old head
  holds the slots on 0 faces. Control and candidate rendered from the same file, lights and cameras (ref, alt, back,
  150 px game scale). cloth_tone.png is not in Git, so both use a flat 0.5 stand-in. Nothing native.
- Next dependency: Codex applies the four overrides in the native study with the real cloth_tone texture.

**ART-004 / Fable / REVIEW (jacket material m002, 27 Nov, run 33, answers `68e1524`)**
- Trigger: Codex held f002 as the working clothing-finish candidate and asked for ONE material-only packet, geometry frozen.
- Files: `art_source/handoff/claude_production/ART-004/jacket_material_m002/` (GLB sha `ab0d800f...`, albedo `49f81dd1...`,
  roughness `9cf43b68...`, manifest, materials JSON with proposed Godot settings, build record, comparison, game-scale and
  neutral texture preview sheets, notes); new `jacket_material_m002.py`, `jacket_material_m002_export.py`,
  `jacket_m002_neutral_preview.py`; f002 editable source committed as `ART-004/jacket_finish_f002/jacket_finish_f002.blend`.
- What changed: the unused, overlapping f002 UV layers replaced by one shared unwrap; flat colours replaced by one 1024
  albedo and one 1024 roughness atlas baked as emission from per-vertex values. Front panels keep the f002 colour, sleeves
  lighter and slightly lemon, back and lower band deeper ochre, low-frequency dye noise, trim deeper ochre, canvas
  roughness about 0.88, trim 0.80. No normal map, no occlusion, curvature, seams or grunge. Neck layer, head and all other
  materials unchanged.
- Checks actually run: Blender before/after (positions, weights, faces, modifiers identical); raw GLB against the f002
  GLB (same position/joint/weight records bit for bit, same triangles, normals within 1e-4); re-import accounting;
  `verify_candidate.py` FROZEN_ALL_UNCHANGED True; clay renders match control; rebuild from the committed f002 blend gives
  byte-identical maps. A bake bug found and fixed in this run (one part's margin painted over another's islands). Nothing
  native.
- Next dependency: Codex's native import, shader and light evaluation of m002 against the flat f002 control.

**ART-004 / Fable / REVIEW (jacket finish repair f002, 27 Nov, run 32, answers `9de793b`)**
- Trigger: Codex's native f001 review: scalloped placket, notched wrist cuff and periodic sleeve rings; one f002 repair.
- Files: `art_source/handoff/claude_production/ART-004/jacket_finish_f002/` (GLB sha `4cbac9ba...`, manifest, surface
  contact sets, materials, comparison, boundary close-ups, step diagnostic, notes); new `jacket_finish_f002_build.py`,
  `jacket_contact_check.py`, `close_render.py`; `jacket_finish_build.py` gained `FIN_STEPS` (default still f001).
- Cause found: f001's per-vertex nearest-normal trim flatten (subdivision and folds create neither defect); cuff
  widening magnified the wrist.
- What changed: rolls flattened about their own centre along a smoothed direction (cuffs: forearm radial); no cuff
  widening; hem roll not flattened; folds faded near plackets and cuffs; three unequal inner-elbow folds replace the
  rings; inward hem waves keep 3 mm from the trousers. Pockets and neck colour as f001.
- Checks actually run: density-independent surface contacts at 97 poses per clip against unchanged partner meshes,
  collar carried by the chest bone: no new hand, strap or collar crossings; trouser crossings (all from the hem roll,
  pre-existing) shift within v004's band. Vertex checks, GLB accounting, original weights identical,
  `verify_candidate.py` FROZEN_ALL_UNCHANGED True, rebuild identical. Nothing native.
- Next dependency: Codex's non-saving native study of f002 against held v004 and f001.

**ART-004 / Fable / REVIEW (jacket + neck finish candidate f001, 27 Nov, run 31, answers `b87f56a`)**
- Trigger: Codex's consolidated A1 review ranked clothing finish first and assigned one jacket + neck candidate on the
  held v004 fit; hair frozen at v012 + m001-B.
- Files: `art_source/handoff/claude_production/ART-004/jacket_finish_f001/` (GLB sha `832b42fc...`, manifest, held
  baseline checks, materials JSON, comparison sheet, notes); `build_scripts/jacket_finish_build.py`,
  `build_scripts/jacket_finish_check.py`.
- What changed: soft folds (elbows, below the shoulder, hem band; none where the hands hang); jacket subdivided once to
  carry them, original weights identical; trim flattened into a facing, cuffs doubled toward the elbow; two low patch
  pockets as a separate part (interpretation); scarf colour cream to warm brown (the "white ring"). No rig, body,
  head, boots or length changes.
- Checks actually run: 97 samples per clip on f001 and, with the same script, on held v004. Straps unchanged (4 at
  gather frame 10 in both); trousers sub-millimetre as before; the 6 "cloth in hand" points are subdivision points on
  v004's own sleeve-end caps (0.0000 mm from the held surface), not new geometry; collar overlap at rest identical for
  original vertices (38 hood, 10 scarf). GLB accounted for; `verify_candidate.py` FROZEN_ALL_UNCHANGED True. Nothing
  native.
- Next dependency: Codex's non-saving native study of f001 against held v004.

**ART-001 / Fable / REVIEW (D1 lever test, diagnostic only, 27 Nov, run 30, answers `3bb0d3a`)**
- Trigger: Codex rejected the crown variant, accepted the metric correction, and asked for one last D1-only test
  (A width 0.62; B keep 0.78 and compensate D1's section locally after the crown map).
- Files: `art_source/handoff/claude_simm/inbox/diagnostics_d1_levers/` (sections with raw support and empty bins,
  clay sheets, front/top, JSON, notes); `hairkit.py` (`round_t`), `stage2_hair.py` (`name:width:thickness:inward`),
  `lock_sections.py` (bin support and empty bins). Defaults unchanged; v012 still rebuilds.
- Checks actually run: D1 sections control/A/B (rise 6.4/3.6/6.2, A 10.6/5.9/10.2, B 6.8/4.6/7.8 mm); crown envelope
  identical in all three at both cameras; pixel change over 8/255 against control under 2 percent in close views,
  under 0.6 percent at head framing; no gaps or detached tips. Colour check not run (no candidate). Nothing native.
- Result and recommendation: neither lever visibly improves either view. Stop D1 and hair-geometry tweaking at v012 +
  m001-B; next is Codex's consolidated A1 gap review.

**ART-001 / Fable / REVIEW (crown family and D1 isolation, diagnostics only, 26 Nov, run 29, answers `0f7f741`)**
- Trigger: Codex held v012 and assigned the five named crown guides (one v013 at most) plus a read-only D1 isolation.
- Files: `art_source/handoff/claude_simm/inbox/diagnostics_crown_family/` and `diagnostics_d1_flat_middle/` (sheets,
  JSON, notes); `stage2_hair.py` (diagnostic `HAIR_SKIP` and `HAIR_SOURCE_COPY`, off by default), new
  `lock_sources.py`, fixed `lock_sections.py`.
- D1 result: leaving the held under-mass out changes D1's outer top by at most 0.6 mm and its flat share little; the
  v011 crown map halves the mid-length rise (8.4 to 3.6 mm). Cause: crown compression on a very wide lock. My v012 note
  blaming the under-mass was wrong and is corrected.
- Crown result: round section on the five guides at width 0.78 and 0.88; coverage and silhouette fine, flat share
  mostly lower, but close views at both held cameras are practically unchanged. No v013 exported, per the brief.
- Metric fix: empty 2 mm bins fell through to inner shells and faked slopes; now outer shell only, 3 mm bins.
  Earlier D2-gate and v012 flat-share numbers used the old version.
- Default build reproduces v012. Nothing native.
- Next dependency: Codex's decision on D1 (a crown map that spares lock tops, or a narrower D1), or to stop hair
  geometry here.

**ART-001 / Fable / REVIEW (head candidate v012, four round-section locks, 26 Nov, run 28, answers `cc6e2a8`)**
- Trigger: Codex accepted the round-section method for one v012 on D1_arc_body, D2_temple_arc, D4_fringe_sweep and
  S_fringe_right only.
- Files: `art_source/handoff/claude_simm/inbox/head_candidate_v012.glb` (sha `e5a47d01...`) and `.blend`,
  `textures_v012/` (hair bake sha `135bec57...` plus record), `renders_v012/`, `HEAD_CANDIDATE_V012_NOTES.md`;
  `stage2_hair.py` (four locks by default; `HAIR_ROUND=` rebuilds v011), `hairkit.py` (per-lock width factor),
  `hair_material_m001.py` (install mode), `lock_displacement.py` (several guides).
- Checks actually run: sections at 25/50/75 percent for each lock (flat share down at 9 of 12 stations; D1 mid stays
  flat over the held under-mass; S_fringe_right 25 percent unchanged); crown ratios unchanged at both cameras; fringe
  tips identical; 2,080 vertices moved over 1 mm, 95 percent within 46 mm of the four guides; coverage, roots and
  split tips checked front, side and top; `verify_candidate.py` FROZEN_ALL_UNCHANGED True; face, eyes, brows, lashes 0
  vertices moved; face/eye/skin textures byte-identical; rebuild identical. Nothing native.
- Remaining scope (labelled, not done): the `top_*` crown masses and D1's under-mass.
- Next dependency: Codex's native check against v011 + m001-B.

**ART-001 / Fable / REVIEW (hair construction method gate, one lock D2, 26 Nov, run 27, answers `d6b9555`)**
- Trigger: Codex held m001-B at roughness 0.70, rejected C, and asked for a one-cluster construction proof before
  any v012.
- Files: `art_source/handoff/claude_simm/inbox/hair_lock_method_d2/` (sheet, section JSONs, displacement JSON,
  notes); `hairkit.py` (`section="round"`), `stage2_hair.py` (`HAIR_ROUND`, default off), new `lock_sections.py` and
  `lock_displacement.py`.
- Evidence: the authored plate section is about 3.5:1 with a `sin^0.55` flat top; on the fused v011 hair it measures
  as a 40 to 45 mm shelf ending in a roughly 20 mm vertical wall. Round prototype on D2: flat share 0.53/0.41/0.48 to
  0.35/0.22/0.29 at 25/50/75 percent; 748 vertices moved over 1 mm (max 11.4 mm), 95 percent within 36 mm of D2,
  none far from D2 over 3 mm. Default build reproduces v011 exactly. Colour check with the m001-B recipe. Nothing
  native.
- Finding: visible change is modest at head scale because D2 is partly covered; the other broad panels (D1 body, D4
  sweep, top masses) share the plate section (judgement from renders).
- Next dependency: Codex's method decision and lock list for v012.

**ART-001 / Fable / REVIEW (hair material test m001 on frozen v011, 26 Nov, run 26, answers `4f9ac05`)**
- Trigger: Codex held v011 as the working head geometry and isolated a hair-only albedo/roughness test.
- Files: `art_source/handoff/claude_simm/inbox/hair_material_m001/` (albedo PNG sha `c5f4549b...`, parameters JSON,
  comparison sheet, notes); `build_scripts/hair_material_m001.py`, `hair_material_apply.py`, `hair_material_probe.py`.
- What changed: nothing in v011's files. A new albedo for `SCULPT_MAT_HAIR`, baked through the existing UVs: deeper
  warm-brown roots and body, restrained amber on broad up-facing lock surfaces, one soft broad drift, no grooves.
  Covered-texel median sRGB 140, 81, 39 (v011) to 112, 64, 37.
- Checks actually run: three settings rendered with fixed cameras, lights and geometry; exported material blocks
  read from hair-only probe exports (metallic 0; roughness 0.7 / 0.7 / 0.5; specularColorFactor 0.5928; ior 1.45);
  TEXCOORD_0 and POSITION byte-identical to the v011 GLB; texel coverage matches; PNG rebuild byte-identical; v011
  .blend and GLB re-hashed unchanged. Nothing native; Godot's handling of the specular/IOR extensions not checked.
- Next dependency: Codex's isolated native override of `SCULPT_MAT_HAIR` (A against B and C).

**ART-001 / Fable / REVIEW (head candidate v011, crown-height study, 26 Nov, run 25, answers `eb48d10`)**
- Trigger: Codex rejected the wider-eye hypothesis and assigned a bounded crown/hair height study (-8% and -12%), one
  v011 at most if it survives both cameras and the full figure.
- Files: `art_source/handoff/claude_simm/inbox/head_candidate_v011.glb` (sha `3c0d0d2c...`) and `.blend`,
  `textures_v011/`, `renders_v011/` (study sheet, coverage sheet, frames, measurements JSON),
  `HEAD_CANDIDATE_V011_NOTES.md`; `stage3_finish.py` (`CROWN_CUT`, default 0.12; 0 rebuilds v010); new
  `head_silhouette.py`.
- Checks actually run: silhouette heights above the eye line over eye-to-chin, full top and main crown mass (31 px
  opening) separately: reference camera v010 2.57 / 2.38, -8% 2.37 / 2.21, -12% 2.27 / 2.12, reference about 2.2
  (2.05 to 2.35) / 1.8 (1.67 to 2.0); alternate camera 2.77 / 2.63 to 2.45 / 2.34. Only vertices at Z 1.235 or above
  moved (hair 12,779, scalp 254); eyes, brows, lashes, textures identical; front, side and back coverage checked;
  `verify_candidate.py` FROZEN_ALL_UNCHANGED True. Nothing native.
- Open: the main crown mass is still above the reference's estimated range; crown hair layer about 18 percent thinner.
- Next dependency: Codex's native check of v011 against v010; then hair material and lock-surface refinement.

**ART-001 / Fable / REVIEW (eye-spacing diagnostic, no v011, 26 Nov, run 24, answers `9243be2`)**
- Trigger: Codex held v010 as the working head baseline and asked for a bounded eye-spacing study (+6% and +10%),
  with one v011 only if both views improve.
- Files: `art_source/handoff/claude_simm/inbox/diagnostics_eye_spacing/` (sheet, measurements JSON, notes);
  `stage1_head.py` (`EYE_SPREAD`, default off), `stage3_finish.py` (brows follow the spread), `head_landmarks.py`
  (visible head width on the eye-line row).
- Checks actually run: eye spacing over visible head width at the reference camera: reference about 0.31 (0.29 to
  0.34, read from the blurred crop), v010 0.336, +6% 0.353, +10% 0.365; front camera 0.378 / 0.400 / 0.415. Height
  above the eyes over eye-to-chin: reference about 2.2 (2.05 to 2.35), v010 2.57. Default rebuild reproduces v010
  exactly. Nothing native.
- Result: wider eyes are not justified and neither variant clearly improves both views; no v011 exported. Evidence
  points to hair and crown height above the eyes as the head-proportion gap.
- Next dependency: Codex's decision on a bounded hair/crown-height study (sequenced after this decision in the brief).

**ART-001 / Fable / REVIEW (head candidate v010, bounded likeness pass, 26 Nov, run 23, answers `7234913`)**
- Trigger: Codex's native whole-figure review at jacket v004: narrow lower face with a small pointed chin, high bare
  forehead, large glossy eyes.
- Files: `art_source/handoff/claude_simm/inbox/head_candidate_v010.glb` (sha `26721da8...`) and `.blend`,
  `textures_v010/`, `renders_v010/`, `HEAD_CANDIDATE_V010_NOTES.md`, stage 1 to 3 scripts, new `head_landmarks.py`.
- What changed: `SCULPT_HEAD` lower face only (Z 1.020 to 1.126): broader, rounder chin and fuller jaw; four fringe
  locks lengthened to the brows; eye texture darker with less white, catchlights kept, eye material less glassy.
  Brows, lashes, eye meshes, head scale, root and bounds unchanged.
- Checks actually run: eye-normalised comparison against the reference (eye centres detected in the image);
  eye-to-chin over eye spacing v009 1.131, v010 1.091, reference about 1.13 (1.08 to 1.18); lower-face width at
  Z 1.05 202.7 to 222.5 mm, cheeks held; `verify_candidate.py` FROZEN_ALL_UNCHANGED True; rebuild identical except
  eye index order. Nothing native.
- Finding for the next decision (evidence, not done): eye-normalised, the model's head and hair are larger than the
  reference's, i.e. the eyes sit close for the head size. Changing it touches whole-head proportion, which the brief
  held; it needs Codex's or the user's go-ahead.
- Next dependency: Codex's native matched-camera check.

**ART-004 / Fable / REVIEW (jacket v004 held as working fit baseline by Codex at `7234913`)**
- Codex accepted the rest-pose hand contact for the study and asked for no more micro-fixes. Nothing to do.

**ART-004 / Fable / REVIEW (jacket candidate v004, 26 Nov, run 22, answers `6532120`)**
- Trigger: Codex verified the corrected gather calibration natively and assigned one unified longer-jacket candidate.
- Files: `art_source/handoff/claude_production/ART-004/jacket_candidate_v004.glb` (sha `2b73bba6...`), manifest
  JSON, `build_scripts/jacket_long_build.py`, `build_scripts/jacket_long_check.py`, `renders_jacket_v004/`,
  `JACKET_CANDIDATE_V004_NOTES.md`. v003 archived unchanged.
- What changed: v003's torso cut once at Z 0.655 and continued as the same thick shell down to Z 0.48 (no second
  layer, no scalloped join, 0 non-manifold edges); plackets continued down the new front edges; hem roll; new
  hips/thigh weights on new vertices only. 1,778 jacket and 1,596 trim v003 vertices kept with identical positions
  and weights (sleeves, cuffs, chest, neckline, strap seating, upper plackets).
- Checks actually run (Blender, 97 samples per clip): idle 0 trouser points and 0 hand contacts; walk one trouser
  graze per half-cycle (body vertex 1174, 0.18 mm, frame 6; 1183, 0.07 mm, frame 18); corrected gather 0 and 0;
  original gather 35 cloth vertices in the hand (negative control); new-edge stretch at most 1.36. Hand margin at the
  left hip at rest is about zero (0.01 mm). GLB re-imported, every vertex and weight accounted for;
  `verify_candidate.py` FROZEN_ALL_UNCHANGED True; held GLBs re-hashed unchanged; rebuild identical. Nothing native.
- Next dependency: Codex's native fit check. Decision for Codex or the user: the rest-pose hand margin at the left
  hip (accept a graze, thin the cloth to about 1 mm there, or a rest-arm change, which is protected and outside
  Fable's fence).

**ART-004 / Fable / DONE (gather calibration v001 verified natively by Codex at `6532120`)**
- Codex reproduced 2.25 / 4.50 / 2.25 deg and applied it as a relative change onto the current native gather. The
  defective `gather_handclear_rig_only.glb` is superseded.

**ART-004 / Fable / REVIEW (gather calibration packet v001, 26 Nov, run 21, answers `d3f3a94`)**
- Trigger: Codex measured only 0.67 deg natively between `gather` and `gather_handclear` at 0.4 s, and an exact match
  at 0.2 s, and asked for one paired calibration GLB.
- Cause (evidence, reproduced byte for byte): Fable's export used `export_nla_strips=False`, which in Blender 3.5
  merges every action into one clip and kept the ORIGINAL gather curve for `upper_arm_l`. The first GLB was the
  original under a new name, with no Z offset. Fable's mistake, not a Godot or axis issue. The 0.67 deg is the gap
  between the starter's original (9.17 deg at 0.4 s) and the native 11-key original (8.50 deg); its cause is not
  established because the native `simm.glb` is not on this branch.
- Files: `art_source/handoff/claude_production/ART-004/gather_adjust/gather_calibration_v001.glb` (sha `7caf4ab7...`),
  `gather_calibration_v001_manifest.json`, `calibration_export.py`, `GATHER_CALIBRATION_V001_NOTES.md`. The defective
  file stays for the record, marked; `gather_handclear.py` no longer exports.
- Checks actually run, on the RE-IMPORTED GLB: 17 bones, clips `gather` and `gather_handclear`, one mesh (the panel);
  delta 2.250 / 4.500 / 2.250 deg at 0.2 / 0.4 / 0.6 s, as authored; hand_l moves (-19.8, +3.3, +8.1) mm in glTF
  axes at 0.4 s, equal to the Blender authoring value; other 16 bones identical between the clips (1.8e-7). Starter
  `gather` fingerprint unchanged. Rebuilt twice, identical. Nothing native.
- Panel still unfinished (join visible, 3 trouser points up to 1.3 mm, stretch 1.37 in walk); not a production
  candidate.
- Next dependency: Codex binds the panel and compares both clips natively; optionally lists the native gather
  upper_arm_l keys so Fable can say whether the native original is a resample of the starter's curve.

**ART-004 / Fable / REVIEW (`gather_handclear` delivered, 26 Nov, at the user's decision)**
- Trigger: the user's choice of option 1, recorded below.
- Files: `art_source/handoff/claude_production/ART-004/gather_adjust/` (rig-only GLB with the new clip, key JSON,
  build script, frame-12 comparison, notes); long-jacket prototype v2 scripts and measurements.
- What changed: a NEW action, a copy of `gather` with one channel (`upper_arm_l` Z rotation) offset by up to
  4.5 degrees at mid-clip, zero at both ends. The original actions are unchanged key for key.
- Checks actually run: panel-in-hand 0 for `gather_handclear` (58 with the original clip), idle and walk 0, at
  49 samples per clip; GLB re-imported; rebuild reproduces the same GLB; originals compared against the starter.
  Nothing native.
- Next dependency: Codex validates it natively and, if accepted, applies the one-channel change to the master
  `gather`; then the long jacket can go to a production candidate.

**User decision, 26 Nov 2026, typed directly in Fable's session: "1 adjust".** The user chose option 1 of the
long-jacket proposal below: adjust the `gather` clip so the hand stays clear of the hip. Fable is preparing it as a
separate candidate action (a copy, `gather_handclear`); the original `gather` action, rig, rest pose and socket stay
untouched until Codex validates and integrates it natively.

**ART-004 / Fable / PROPOSAL: longer-jacket deformation method, clay prototype (26 Nov, run 20, answers `6a7da65`)**

A method prototype on a throwaway copy; no export, nothing delivered as an asset. Scripts, frames and measurements:
`art_source/handoff/claude_production/ART-004/jacket_long_proposal/`. Built on the current fit file (head v009, collar
v004, jacket v003, boots v002), all unchanged. Not done: anything native.

**Method: a new lower panel, not new weights on the old hem.** Jacket v003 stays exactly as delivered: its
vertices, faces and weights are untouched and it keeps its own hem. A new part, `SCULPT_JACKET_SKIRT`, is its own
topology: 15 rows from Z 0.665 down to Z 0.480 and 96 columns round the body, open at the front (plus or minus 19
degrees, matching jacket v003's front edges). It is 7 mm thick, subdivided once, 20,384 triangles at prototype density.
- **Fit:** its top band sits 4 mm inside jacket v003's lower band, so the join is hidden. Below that it flares
  gently and keeps 20 mm clear of the trousers at rest.
- **Rollback:** remove that one part.

**Weights, candidate only, existing bones only (`hips`, `thigh_l`, `thigh_r`).**
- Above Z 0.655 the panel is 100 percent `hips`, like the jacket hem it hides under.
- Below that, the thigh share rises to 0.6 at the hem along a 0.7-power curve, so the middle rows follow the legs too.
- The same-side thigh takes it at the sides and front. At the back centre the two thighs share it, softened by
  45 percent, which stops the back hem tearing.
- Every vertex sums to 1. Nothing on `PROTECTED_BODY`, the rig, rest pose, actions or socket changes.

**Evidence.**
- `long_jacket_full_figure.png`: clay, same figure height in every panel. The hem moves from 0.40 of figure height
  to the reference's 0.33 line, and bare trouser from 0.20 to about 0.13, which is the reference.
- `long_jacket_walk_gather_close.png`: walk at 25 and 75 percent and gather at 50 percent, from the reference camera,
  side and back. One coherent hem, with no vents and no split tail; the back hem stays smooth.
- `long_jacket_measurements_49_samples.txt`, 49 samples per clip, sampled not continuous:

| Clip | Trouser points outside the panel (within 30 mm of it) | Panel vertices inside a hand (hand-only triangles) | Largest edge stretch |
|---|---|---|---|
| idle | 0 | 7, at one sample | 1.00 |
| walk | 3, up to 5.7 mm, at frame 6 | 0 | 1.37, at frame 6 |
| gather | 0 | **101, at frame 12** | 1.00 |

An earlier pass with 12 mm of trouser clearance and a later thigh blend showed dark trouser wedges through the panel
in walk. Moving to 20 mm and blending earlier removed them in the frames.

**The limit: the gather hand.** This is the precise limitation you asked for, not a disguised view. In `gather` the
clip presses the right hand into the hip. The frozen trousers themselves take up to 4.4 mm of hand there, and the
original jacket only avoided it by ending above the hand. Any cloth that covers the hip down to Z 0.48 is in the
hand's path. On `hips` and thigh weights alone that cannot be fixed (`long_jacket_gather_hand_contact.png`).
Options, all needing a decision I cannot make inside the current fences:
1. **Adjust the gather clip** so the hand stays about 2 cm further out at frames 7 to 17. It removes the
   contact for every jacket length and the existing trouser contact too. It changes a protected animation, so it
   needs your decision and probably the user's.
2. **Candidate-only weight from the hand onto the small panel patch** in its path, so the cloth is pushed rather
   than pierced. It is local and reversible, but goes beyond "existing hips and thigh bones".
3. **A pocket opening at that spot**, so the hand reads as going into a pocket. It is a design change, and it only
   works if the hand's path lines up with a plausible pocket.

**Recommendation.** Take the lower-panel method forward. It reaches the reference length with a coherent hem, and
walk is close: 3 small trouser points and one stretched frame to clean up. Pair it with option 1 if you and the user
accept a small gather-clip change, otherwise option 2. Without one of them, a long jacket keeps a visible hand
contact in gather, and I would not export it as finished.


**ART-004 / Fable / REVIEW (boot candidate v002 delivered, 26 Nov, run 19)**
- Peer commit consumed: `f5a51de` (boot v001 native review and v002 brief at `f98e519`).
- Files changed: `art_source/handoff/claude_production/ART-004/boot_candidate_v002.glb`,
  `BOOT_CANDIDATE_V002_NOTES.md`, six frames in `renders/`, `build_scripts/boot_build.py` (v002).
- Checks actually run: rocker fitted against 147 foot-bone samples per foot; 97 samples per clip for trousers,
  ankle seam and floor contact (0, 0, and -1 mm worst against the original's -1 mm); manifest; GLB re-import;
  `verify_candidate.py` (`FROZEN_ALL_UNCHANGED True`); held files re-hashed. Nothing native.
- Remaining gaps: even, ring-like shaft folds; plain toe; flat working material; trouser and jacket-length gap.
- Next dependency: Codex's native fit, then its separate jacket/leg deformation proposal.

**ART-004 / Fable / REVIEW (boot candidate v001 delivered, 26 Nov, run 18)**
- Peer commit consumed: `0ff622e` (rigid boot method accepted and v001 contract at `465ccf1`).
- Files changed: `art_source/handoff/claude_production/ART-004/boot_candidate_v001.glb`,
  `BOOT_CANDIDATE_V001_NOTES.md`, five frames in `renders/`, new `build_scripts/boot_build.py`,
  `boot_check.py`, `boot_review_prep.py`.
- Checks actually run: four-part manifest and single-bone binding asserts; ownership of every face of the three
  original shoe materials; 97 samples per clip for trouser containment, the shaft's lower edge inside the boot
  foot, and floor contact against the original soles; GLB re-imported; `verify_candidate.py`
  (`FROZEN_ALL_UNCHANGED True`); held head, collar and jacket files re-hashed (unchanged). Nothing native.
- Correction to the contract: `Simm brown boot leather` includes 376 `chest` triangles (the pack straps). The study
  should hide only the 1,784 foot-owned triangles, not all 2,160.
- Remaining gaps: sole up to 7 mm below the floor in walk (original 1 mm); flat leather lighter than the reference;
  plain heel and toe; trouser and jacket-length gap unchanged.
- Next dependency: Codex's native boot fit.

**ART-004 / Fable / PROPOSAL: boot and leg silhouette method, with a clay blockout (26 Nov, run 17, answers `508f813`)**

A throwaway clay blockout made to test the method. No production asset, no export, no weight change anywhere.
Scripts and frames: `art_source/handoff/claude_production/ART-004/boot_proposal/`. The blockout was built on the
current fit file (head v009, collar v004, jacket v003); those files are unchanged.

Looked at directly: the approved reference at full resolution (with a pixel ruler), the original shoe and trouser
geometry and weights, the 17-bone rig, and the clips. Not done: anything native.

**1. What the original shoes are (evidence).** Three materials, all 100 percent on `foot_l` / `foot_r`:
`Simm dark soles` (744 tris), `Simm brown boot leather` (1,160 tris; 784 of them under Z 0.30) and `Simm worn
jacket edges` (256 tris, all on the feet: the yellow lace-line trim). Each shoe is about 177 mm wide and 275 mm
long, Z 0 to 0.24, with the trousers hanging over it to about Z 0.17. That is the low, bulbous slipper read.

**2. Proportions, as fractions of figure height, hair top to sole (approximate: the reference is a soft three-quarter view).**

| | Reference | Current | With the blockout |
|---|---|---|---|
| Top of boot | 0.20 | 0.12 | 0.20 (cuff at Z 0.29) |
| Jacket hem | 0.33 | 0.40 | 0.40 (unchanged) |
| Bare trouser between them | 0.13 | 0.28 | 0.20 |
| Chin | 0.69 | 0.71 | 0.71 |

`boot_blockout_full_figure.png` shows the reference and the clay before and after at the reference camera and from
the side, each scaled to the same figure height, with the 0.20 and 0.33 lines drawn.

**3. The blockout.** Per leg, two parts:
- `SCULPT_BOOT_SHAFT_L/R`: a closed leather shaft round the trouser leg from Z 0.13 to 0.29, about 62 to 66 mm
  radius, with a turned-over cuff at the top. Bound 100 percent to `shin_l` / `shin_r`. The trouser leg inside it is
  hidden and is also on `shin`.
- `SCULPT_BOOT_FOOT_L/R`: heel, ankle collar, instep, rounded toe box and a 26 mm rounded sole, fused. It is narrower
  and flatter than the original shoe (128 mm wide). Bound 100 percent to `foot_l` / `foot_r`. Its ankle collar is
  wider than the shaft, so it wraps the shaft's bottom edge.
- A native study would hide `Simm dark soles`, `Simm brown boot leather` and `Simm worn jacket edges`, plus
  `Simm folded hood canvas` as now. Trousers, body pose, rig, rest, actions, socket, head, collar, jacket and pack
  stay as they are. Rollback is showing those three materials again and removing the four boot parts.

**4. Bending evidence.** The shin-to-foot angle is 62.8 degrees at rest and in idle and gather, and peaks at 69.6
degrees in walk (frame 6). The ankle only flexes about 7 degrees in these clips.
- `boot_blockout_ankle_bend.png`: close clay frames at rest, at the two worst walk frames and at gather, for both
  bindings. `boot_blockout_walk_worst.png`: the whole leg at the worst walk frame.
- Rigid parts read as one continuous boot in every frame: the foot's ankle roll covers the shaft's lower edge,
  with no visible gap or poke-through.
- A candidate-only blend (the lowest 40 mm of the shaft up to 50 percent on `foot`) looks the same. It brings
  nothing at this range of motion.
- Trouser vertices outside the shaft, 97 samples per clip: 0 in idle, walk and gather.
- The numeric seam counts in `boot_bend_check_97_samples.txt` are not a pass or fail. They count the shaft's
  outside layer as "outside the foot" by design, and are kept only for the record.

**Recommendation: rigid two-part boots.** Shaft on `shin`, foot on `foot`, each part 100 percent on one existing
bone. No weight exception, no blend, no change to the master rig or the trousers.

**5. What boots cannot fix (opinion, for the consolidated brief).** With boots at the reference height, 0.20 of
the figure is still bare trouser against the reference's 0.13. The rest of that difference is the jacket length: the
hem is at 0.40 against 0.33. Reaching it means a hem at about Z 0.47 to 0.50, which method A ruled out under
exact weights, because the thighs swing through the hem. I am documenting it as a later proposal, not changing
anything: a longer jacket would need either the narrow hem-band weight exception Codex has not granted, or an
accepted shorter-jacket design. The legs also read longer and thinner than the reference's; fuller trousers above
the boot would help, again a later item.

**Next, if accepted:** one boot packet, with smoother shaping than this lumpy blockout, leather colour from
the current boot material, one 256 px texture or flat colours, the same 97-sample checks and a named-part manifest.

**ART-004 / Fable / REVIEW (collar packet v004 delivered, 26 Nov, run 16)**
- Peer commit consumed: `a92c4da` (jacket v003 kept as working baseline and collar v004 brief at `bdf4942`).
- Files changed: `art_source/handoff/claude_production/ART-004/collar_packet_v004.glb`,
  `COLLAR_PACKET_V004_NOTES.md`, fourteen frames in `renders/`, `build_scripts/collar_build.py` (v004), new
  `build_scripts/collar_seat_check.py`.
- Checks actually run: jacket weights under the collar inspected (100 percent `chest` except a few shoulder-point
  vertices); seat gap in 32 directions at 25 and 97 samples per clip (largest 5.0 mm); jaw, nape and hair
  clearance over 39 poses; pack contact; closed-mesh and thin-wall check; manifest and export;
  `verify_candidate.py` (`FROZEN_ALL_UNCHANGED True`); held candidate files re-hashed (unchanged). Nothing native.
- Remaining gaps: 5 mm seat gap at Simm's left front side; the frozen folded-hood piece still shows (proposal:
  hide it in the study); hood to hair 5.6 mm in gather.
- Next dependency: Codex's native test and the combined silhouette review.

**ART-004 / Fable / REVIEW (jacket candidate v003 delivered, 26 Nov, run 15, method A)**
- Peer commit consumed: `e947b22` (combined native review at `19ec210`, method A and v003 brief at `94cb54b`).
- Files changed: `art_source/handoff/claude_production/ART-004/jacket_candidate_v003.glb`,
  `jacket_candidate_v003_vertex_map.json`, `JACKET_CANDIDATE_V003_NOTES.md`, seven frames in `renders/`,
  `build_scripts/jacket_build.py` (v003), `build_scripts/jacket_export_check.py` (hand-only test, `SAMPLES`).
- Checks actually run: hem at the original height with exact weights; hand-only contact test at 25 and 97
  samples per clip (0 contacts); the original body measured in `gather` (its trousers take up to 4.4 mm of hand,
  its jacket none); full GLB accounting (5,606 of 5,606 matched, weights identical); `verify_candidate.py`
  (`FROZEN_ALL_UNCHANGED True`). Nothing native.
- Remaining gaps: a small fold on each sleeve just above the cuff; thin cuff roll; strap gap up to 12.9 mm;
  jacket length still the original 0.58 m against the reference's 0.47 to 0.50 m.
- Collar: seating correction proposed in the notes (bunch merged into the stand, base seated on the jacket
  surface with a skirt); collar v003 not edited.
- Next dependency: Codex's native fit of v009 + collar v003 + jacket v003.

**ART-004 / Fable / PROPOSAL: hem and cuff method before jacket v003 (26 Nov, run 14, answers `906cdaf`)**

No geometry delivered. Evidence was made on throwaway copies: two test jackets built from the v002 script with
changed constants, and, for option B, hem weights changed on the candidate copy in memory only. Nothing was
saved, exported or written to `PROTECTED_BODY`, the rig, the actions or the socket. Frames and scripts are in
`art_source/handoff/claude_production/ART-004/method_proposal/`.

Options tested, same camera and light, walk at 25 and 75 percent, gather at 50 percent (`hem_options_walk_gather.png`):

| Option | Hem lowest Z | Weights | What the frames show |
|---|---|---|---|
| v002 as delivered | 0.545 | original | side vents, split-tail silhouette (as you found) |
| **A** | **0.585** | **original, exact** | **one coherent hem, no vents; no trouser showing through in any of the frames** |
| B0 | 0.545, no vents | original | a small dark trouser corner pokes through the side of the hem in walk |
| B1 | 0.545, no vents | 186 hem-band vertices (Z under 0.635, now 100 percent `hips`) blended toward the same-side thigh, up to 0.5 at the hem | the same corner, slightly smaller |
| B2 | 0.545, no vents | same band, up to 0.8 | smaller again, still there, and the back hem starts to separate into a torn edge (`hem_option_B_weight_strength.png`) |

Numbers I tried and do not rely on: a nearest-surface "inside the trousers" count, which flips sign near thin
cloth and gave nonsense values, and a ray test that also counted the open front of the jacket. The frames are
the evidence. Cloth more than 2 mm into a hand, 25 samples per clip: A 0 / 0 / 4 vertices up to 5.7 mm (idle,
walk, gather); B0 to B2 0 / 0 / 4 up to 4.7 mm; v002 0 / 0 / 0.

**Recommendation: A.** A coherent hem at the original height, every weight exact, no vents. The 0.47 to 0.50 m
reference length is given up here; the shorter-legged read comes later from taller boots and a fuller lower
jacket, as you suggested. B would need per-vertex weight tuning to remove the corner and would still tear at the
back. If you want B anyway, the band, bones and blend are in `hem_method_test_weights.py`: affected vertices
are the jacket vertices under Z 0.635 that are 100 percent `hips` today, inside |X| 0.215; same-side thigh
weight `fz*W*(0.35 + 0.65*s)`, other thigh `fz*W*0.35*(1 - s)`, `hips` the remainder, so each sums to 1;
`fz` rises from 0 at Z 0.635 to 1 at the hem, `s` from 0 at the centre line to 1 at |X| 0.10. Rollback is the
original weights, which the export check already compares vertex by vertex.

Open item for A: the gather hand. 4 vertices reach up to 5.7 mm into a hand at the hip side. v003 would draw the
hem in locally where the measured hand path passes, with a gentle rise of at most 10 mm at the sides (a curve,
not a vent), and report the measured result.

**Cuffs: a continuous rolled lip, not a bracelet.** The original cuff rings sat at a mean radius of about
47 mm and never touched a hand in any clip (measured on the original body). v002 moved them to about 51 mm and
opened the sleeve to 43 mm to clear the hand, which is what made them float. v003: the cuff roll goes back to
the original ring radius and height, and the sleeve end is shaped to meet it, with the roll overlapping the
sleeve by 2 to 3 mm so it reads as one turned-back edge. No flare, no widening past the original ring.

Next: on your go, jacket v003 with option A and these cuffs, one export, the same checks as v002.

**User feedback, 26 Nov 2026, on a native side view of head v007 + collar v002 + jacket: "IMO we're still 30% off."**
Fable's read of that frame against the approved reference, measured in Blender where possible:
1. Bare neck (largest gap). 44 mm of skin shows at the nape between the hood top (Z 1.017) and the lowest hair
   (Z 1.061), and 30 mm at the throat between the scarf (Z 0.990) and the chin (Z 1.020). The reference head sits
   down in a full, bunched hood with almost no neck visible. Collar v002 was shrunk on purpose to clear the pack.
2. Hair. Glossy, uniform brown with deep dark grooves; the back ends in a hard shelf of pointed locks above a pale
   nape. The reference hair is softer, lighter at the tips, and comes down to meet the hood.
3. Skin and light. Pale, grey on the shadow side of the face and neck; the reference is warm and peachy. Mostly
   lighting (audit hypotheses L5, L9), partly the skin bake.
4. Face profile. Lower face long and flat, eyes read as flat discs from the side. Smaller than 1 to 3.
Proposed: reopen collar first (a real hood behind the nape, scarf up to the chin), then the hair's back and nape.
Head v007 and collar v002 are on hold by Codex's call; reopening them needs the user's go-ahead.
User's answer, typed directly: "Yes, this needs to have full parity, for Mattias to be happy". Collar and hair
are reopened on the user's authority, overriding the hold for these two items only.

**ART-004 / Fable / REVIEW (collar packet v003 delivered, 26 Nov 07:45 UTC, user-approved reopen)**
- Trigger: user review of a native side view, not a Codex brief.
- Files changed: `art_source/handoff/claude_production/ART-004/collar_packet_v003.glb`,
  `COLLAR_PACKET_V003_NOTES.md`, eight frames in `renders/`, `build_scripts/collar_build.py` (v003).
- Checks actually run: bare neck measured by direction round the neck; hood fitted to the head mesh; 39 sampled
  poses for jaw, nape and hair clearance; collar against pack; manifest and binding asserts; GLB export;
  `verify_candidate.py` (`FROZEN_ALL_UNCHANGED True`). Nothing native.
- Evidence: notes, frames, GLB sha256 `f233e2693f5060e234f4741f62c0acad0f9855298b78379ee540f46c96878961`.
- Remaining gaps: 2.8 mm hood to hair tip in gather; the back bunch reads as a lump from the side; not seen with
  jacket v002 or in Godot.
- Next: ART-001 head v008 (hair only), then Codex's combined native study.

**ART-001 / Fable / REVIEW (head v009 delivered, 26 Nov, at the user's request)**
- Trigger: the user, typed directly: "your version looks like it's from Silent Hill or from some horror cartoon,
  and what's on the concept is very cute ... you should fix it." This lifts the face hold for the expression.
- Files changed: `art_source/handoff/claude_simm/inbox/head_candidate_v009.glb`, `.blend`, `textures_v009/`,
  `renders_v009/`, `HEAD_CANDIDATE_V009_NOTES.md`, `build_scripts/stage3_finish.py` (eyes, brows, smile, skin).
- Cause found in the build: the iris was wider than the eye opening, so the eyes were solid dark ovals with no
  white and no highlight; brows thin, pale and 36 mm above the eyes.
- Checks actually run: rebuild; meshes compared with v008 after re-import (only brows changed); emissive eye
  texture confirmed in the GLB; `verify_candidate.py` (`FROZEN_ALL_UNCHANGED True`). Nothing native.
- Next dependency: Codex's combined native study of head v009 + collar v003 + jacket v002.

**ART-001 earlier entry (head v008, hair colour and gloss)**
- Trigger: the same user review.
- Files changed: `art_source/handoff/claude_simm/inbox/head_candidate_v008.glb`, `.blend`, `textures_v008/`,
  `renders_v008/`, `HEAD_CANDIDATE_V008_NOTES.md`, `build_scripts/stage3_finish.py` (hair palette and material).
- Checks actually run: full rebuild from the starter; every mesh compared with v007 after re-import (identical);
  skin and eye textures byte-identical; `verify_candidate.py` (`FROZEN_ALL_UNCHANGED True`). Nothing native.
- Evidence: hair colour measured in the reference and in the user's native frame; numbers in the notes.
- Next dependency: Codex's combined native study of head v008 + collar v003 + jacket v002, ideally including the
  side view the user reviewed.

**ART-001 / Fable / REVIEW (delivered, waiting on ART-002)**
- Peer commit consumed: `7ef4a5e` (v006 review and v007 brief).
- Files changed: `inbox/head_candidate_v007.blend`, `.glb`, `renders_v007/`, `textures_v007/`,
  `HEAD_CANDIDATE_V007_NOTES.md`, `build_scripts/stage2_hair.py`.
- Checks actually run: full rebuild from the starter copy in headless Blender 3.5.1; GLB re-imported into an empty
  scene for counts and bounds; `verify_candidate.py` (frozen body, old head, 17 bone rest matrices, socket, three
  actions unchanged); skin texture compared byte for byte with v003; both agreed clay cameras judged before export.
- Evidence: `inbox/renders_v007/`, GLB sha256 `9a296dd846e3fba327f6270cc41c9f25c4864a513b2436218cd39e754d6328d9`.
- Remaining gaps: hair still heavier and tidier than the reference; face held, not approved; no engine evidence.
- Correction: v006 was delivered with two fringe locks missing because of a patch bug. Restored in v007. Details
  in the v007 notes.
- Next dependency: Codex's native review (ART-002).

**ART-006 / Fable / DOING (first pass delivered)**
- Peer commit consumed: `a403661`.
- Files changed: `coordination/claude_art_audit.md`.
- Checks actually run: none native. Reference and concept images read directly; current scene state taken from
  Codex's guide only.
- Remaining gaps: no current native clearing frames in Git, so the gap ranking is second hand.
- Next dependency: Codex commits three native clearing frames; then Claude re-ranks and details per-asset defects.

**PROD-001 / Codex / acknowledged by Fable** at this commit.

**ART-004 / Fable / REVIEW (jacket candidate v002 delivered, 26 Nov 07:28 UTC)**
- Peer commit consumed: `bfd7ce4` (jacket v001 native review and six-point v002 brief at `367f484`).
- Files changed: `art_source/handoff/claude_production/ART-004/jacket_candidate_v002.glb`,
  `jacket_candidate_v002_vertex_map.json`, `JACKET_CANDIDATE_V002_NOTES.md`, six frames in `renders/`,
  `build_scripts/jacket_build.py` (v002), `jacket_export_check.py` (rewritten), `jacket_review_prep.py`,
  new `jacket_hand_sweep.py` and `jacket_hand_sweep.json`.
- Checks actually run: deterministic build; per-part asserts that every vertex is an original vertex with its
  original faces, groups and weights; hand and thigh travel measured over 17 samples per clip; 9 samples per clip
  for cloth against thighs and hands, before and after; GLB re-imported and all 5,606 vertices matched to source
  vertices within 20 micrometres with identical weights, failing on any miss; skeleton names, parents and rest
  joints compared; `verify_candidate.py` (`FROZEN_ALL_UNCHANGED True`). Nothing native.
- Evidence: notes file, frames, GLB sha256 `c985517f0f8519e8f4e56d599a8ef99dd25bf6eb39c96ecb0ef8d67e314f2e61`.
- Remaining gaps: a side vent of up to 80 mm in the hem at each hip; 3 trim vertices in the thigh in gather;
  cuff roll is a ring wider than the sleeve end; hem height unchanged; old topology; not seen in Godot.
- Correction: my v001 note that no thigh broke through the hem was wrong. It did, in walk.
- Next dependency: Codex's in-memory native study. If the vents are rejected, a decision on which of three
  faults is least bad, or leave to propose a weighting exception for the hem band.

**ART-004 earlier entry (jacket candidate v001, 26 Nov 01:22 UTC; reviewed, changes requested)**
- Peer commit consumed: `e5e7105` (collar v002 held as working baseline and jacket brief at `193b661`).
- Files changed: `art_source/handoff/claude_production/ART-004/jacket_candidate_v001.glb`,
  `jacket_candidate_v001_vertex_map.json`, `JACKET_CANDIDATE_V001_NOTES.md`, six frames in `renders/`,
  new `build_scripts/jacket_build.py`, `jacket_export_check.py`, `jacket_review_prep.py`;
  `collar_packet_v002.blend` (the baseline source Codex asked for).
- Checks actually run: deterministic build on the collar v002 file; asserts that the candidate is exactly the
  original jacket vertex set with identical connectivity, groups and weights; 9 samples in each of `idle`, `walk`,
  `gather` for cloth against thighs and hands, before and after; GLB re-imported for bones, counts, bounds and
  weights; `verify_candidate.py` (`FROZEN_ALL_UNCHANGED True`). Nothing native.
- Evidence: notes file, frames, GLB sha256 `1ecc5240f497a55f5f7133048cb9f484582318cdae269e3305f420ce317bddcc`.
- Remaining gaps: not seen in Godot; hem lowered 37 mm only; 10 vertices touch a hand in `gather`; straps up to
  14.5 mm above the new surface; one frozen button without a placket; roundness limited by the old topology.
- Next dependency: Codex's in-memory native study. Head, collar, trousers, boots, hands and pack stay closed.

**ART-006 / Fable / REVIEW (second pass delivered, 26 Nov 02:10 UTC)**
- Peer commit consumed: none new. Tip unchanged at `e5e7105`. Evidence used: the three native frames from `98c1777`.
- Files changed: `coordination/claude_art_audit.md` (sections 1, 3 and 6).
- Checks actually run: all three native frames and the approved reference viewed at full size; pixel statistics
  and one lit and shaded floor sample pair per image; character and tent heights measured in pixels. Nothing native.
- Evidence: section 3.1 of the audit. Opinion is separated in 3.2.
- Result: light and shadow is now rank 1 (was 4); foliage stays 2; ground stays 3; characters rank 4 on screen
  but remain the A1 gate; camp layout and scale is a new rank 5 (tent about twice its study size in the playable
  camp); props 6; UI 7.
- Remaining gaps: three stills, one light setup, no motion; grass and foliage colour samples were not reliable
  enough to quote; Simm in the frames is the old runtime model.
- Next dependency: Codex to test L9 and L10 natively if it agrees, and to accept or change the oak pilot as the
  first world packet after A1. The tent scale question in the playable camp needs Codex or the user.

**ART-004 earlier entry (collar packet v002, 26 Nov 00:20 UTC; now held as working baseline)**
- Peer commit consumed: `fad6b7a` (collar v001 review, changes requested, at `65387e5`).
- Files changed: `art_source/handoff/claude_production/ART-004/collar_packet_v002.glb`,
  `COLLAR_PACKET_V002_NOTES.md`, seven frames in `renders/`, `build_scripts/collar_build.py` (v002 shapes),
  new `build_scripts/collar_pose_clearance.py`. No `.blend` (lighter delivery rule).
- Checks actually run: deterministic build on `head_candidate_v007.blend`; manifest and single-bone asserts;
  front, side and back inspected in clay and colour; 39 sampled poses across `idle`, `walk`, `gather` for
  distance to the visible head; rigid collar-against-pack measurement; `verify_candidate.py`
  (`FROZEN_ALL_UNCHANGED True`). Nothing native.
- Evidence: notes file, frames, GLB sha256 `a3146c83dca0b95d31d96f328091df899dc6bca5c53cfa4776ea825766349e73`.
- Remaining gaps: not seen in Godot or in motion; scarf may now be too thin; hood has little volume from the
  back; 4 hidden hood vertices under the pack lip; neck contact at the nape to be checked in `gather`.
- Next dependency: Codex's native attach and the same three clips. Jacket and boots stay closed until then.

**ART-006 / Fable / READY, not started (run 6).** The collar correction took this run. Re-rank from the three
native clearing frames is the next run's one task.

**ART-004 earlier entry (first packet: hood roll and scarf v001, superseded)**
- Peer commit consumed: `98c1777` (ART-003 first fit and the scoped collar assignment at `7a939fd`; clearing frames at `98c1777`).
- Files changed: `art_source/handoff/claude_production/ART-004/collar_packet_v001.glb`, `.blend`,
  `COLLAR_PACKET_V001_NOTES.md`, `renders/`, `build_scripts/collar_build.py`, `collar_export_check.py`;
  `claude_simm/inbox/build_scripts/render_views.py` (review-only handling of the body's missing textures).
- Checks actually run: deterministic build on `head_candidate_v007.blend`; part manifest and single-bone binding
  asserts; rest-pose clearance to jaw, skull base and hair; GLB re-imported for counts and bounds;
  `verify_candidate.py` (body, old head, 17 bone rest matrices, socket, three actions unchanged). Nothing native.
- Evidence: notes file, six frames, GLB sha256 `e8ba5af258a416629d2de4559d3b81e62138ffdb495201607583fb3f20d9ee39`.
- Remaining gaps: not seen in motion; hood colour match to the textured jacket unverified; lapel ends overlap the
  untouched jacket and straps.
- Next dependency: Codex's native attach to `chest` and sampled clips.

**ART-006 / Fable / READY, not started this run.** The three native clearing frames arrived at `98c1777`. One
ticket per run: the P0 collar packet went first. The evidence-based re-rank is next.

**ART-004 proposal (earlier entry)**
- Peer commit consumed: `757c52d` (no new art feedback in it; proposal cleared at `1f7d6a8`).
- Files changed: `coordination/claude_art004_proposal.md`,
  `art_source/handoff/claude_production/ART-004/frozen_body_with_v007_head_clay.png`.
- Checks actually run: read-only inspection of `PROTECTED_BODY` in the starter (counts, islands, materials, vertex
  groups, collar zone); one Blender clay render of the frozen body with head v007. Nothing native. The frozen
  body was not modified.
- Evidence: the measurements table in the proposal; the clay frame.
- Remaining gaps: no observation of the body in Godot or in motion; body textures are not in Git.
- Next dependency: ART-003 results; Codex's answer on single-bone parts (option B); the two body textures.

## Proposed corrections to the plan

Each item says whether it rests on evidence or on opinion.

### 1. Fable's schedule is hourly (evidence). RESOLVED 21:07 UTC: scope widened by the user

Update: the user typed the request directly and the stored check now follows Fable's tickets on the board, one
bounded step per run, with the same fences. The three bullets below describe the situation before that.

- The platform minimum is one hour. `trig_01RTVFoanSgc82QmxWinsxYg` fires at minute 6 UTC.
- Its stored instructions still say "head only". Claude tried to widen them to follow Fable's board tickets and
  the session's permission layer refused, as it did for the original schedule until the user typed the request
  directly. Claude has not worked around it.
- Effect until the user widens it: unattended runs will keep doing head revisions and writing `claude_*.md`
  files. They will not advance ART-006 or later tickets on their own. Those move when the user prompts the session.
- Proposed board note: treat Fable's unattended capacity as "ART-001 only" until the receipt here says otherwise.

### 2. Measured throughput so far (evidence), and what it implies (opinion)

- Evidence: seven head versions between 15:34 and about 21:00 UTC on 25 November. Six Codex review rounds. Each
  Claude revision took 20 to 45 minutes of work once the brief was read. The head is still `changes_requested`.
- Evidence: the first three rounds were spent finding the right inputs and proportions (no reference, then a
  55 px reference, then the real one and the first Godot view). Rounds four to seven converged on one topic, hair
  construction.
- Opinion: a hero character part needs 5 to 8 rounds; a prop or tree kit probably 2 to 4 once section 2 of the
  audit is agreed. The clearing is 13 manifest assets plus ground. That puts A2 at very roughly 40 to 70 review
  rounds. At one round an hour that fits weeks 3 to 6 only if both loops run most of the day. Reforecast after two
  accepted packets, as the plan already says.

### 3. New ticket proposed: ART-011, game-resolution Simm head (opinion, with one fact)

- Fact: the head is 80,265 triangles in five meshes with auto-unwrapped hair. That is review density.
- A1's exit evidence includes a performance measurement and game-scale readability. Measuring the 80k head would
  measure the wrong thing.
- Proposal: once the head shape is accepted, Fable makes a reduced head and hair with a normal map baked from the
  sculpt, before ART-003's game-scale study or in parallel with it. Depends on ART-002 stable. Feeds ART-003,
  ART-005 and PERF-001.

### 4. ART-004 should start as a scoped proposal now (opinion)

- Fact: the reference hides Simm's neck behind a raised hood and scarf; the frozen body has neither at that
  height, and Codex has listed the exposed neck as a known mismatch since v002.
- Fact: `PROTECTED_BODY` is 7,444 vertices and 14,144 polygons with 20 material slots and one armature modifier.
- Proposal: Fable writes the ART-004 approach now (which parts change, on the existing skinned topology, with what
  evidence), so the mesh work can begin the moment ART-003 reports. No body mesh before that.

### 5. Repository growth (evidence) and a lighter delivery rule (proposal)

- Evidence: each head version adds about 38 MB (renders 20, `.blend` 15, `.glb` 3). Seven versions are about
  265 MB on Fable's branch.
- Proposal from v008: every revision commits the GLB, the notes and five renders (reference and alternate in clay
  and colour, plus the comparison sheet). The `.blend` and the full render set are committed only for versions
  Codex marks as a new baseline. Everything stays rebuildable from the committed scripts and starter copy.
  Codex, say if you need the full set every time.

### 6. Turnaround of invented surfaces (opinion)

- Fact: the back, nape and Simm's left side have never been seen by the user; they are Claude's invention.
- Proposal: A1's user checkpoint (ART-005) explicitly shows back and both sides, so an objection lands once,
  before the same hair logic is reused on Leina and others.

### 7. Inputs Fable needs before later tickets (evidence)

- ART-006: three native clearing frames (see the audit).
- ART-007: starter `.blend` files for Leina and Bronkings with frozen rigs, prepared like Simm's starter, and the
  approved identity picture for each.
- ADD-001: `docs/concepts/mattias-bosses-20261125.png` is referenced by the boss notes but is not on the branch.
- PROD-002: the scoped code snapshot, before Fable drafts any data or test specs.

### 8. A process safeguard Fable has added (evidence)

- The v006 omission happened because a text patch removed two lock statements without any error.
- From v007 the hair build prints the lock count and fails on duplicate names, and each notes file states the count
  (v007: 67 locks). Codex may want the same kind of manifest check on its side for multi-part assets.

## Decisions log items Fable can help close

- D07, D08 (penguin, bosses, bucket): Fable will write ADD-001 proposals when the ticket opens and the drawing is
  readable. Nothing is assumed about mechanics.
- D11 (budgets): see proposal 3; provisional planning ranges are in the audit, marked as opinion.
