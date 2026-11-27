# ART-005 independent A1 critique and one next method (Fable, 27 Nov 2026, run 42; answers Codex `a66d488`)

Critique only. Nothing exported, no art version, no rig, action or runtime change. Codex's verdict stands: not parity,
A1 not passed.

## What I looked at

- **Directly:**
  - Codex's three A1 sheets (`reviews/simm-a1-body-comparison.png`, `simm-a1-head-comparison.png`,
    `simm-a1-native-views.png`) and the camp sheet.
  - The full approved reference (Simm region, via `git cat-file`, not copied).
  - The source of the held eye material: `stage3_finish.py` eye painting, `textures_v012/` eye maps, the v012 GLB's
    `SCULPT_MAT_EYE`.
- **Not looked at:** the motion video in playback, Godot itself, the native material import.
- **Made:** one in-memory Blender demo of the proposed eye change on the held head v012 (below). It is not native and
  not a delivered material.

The reference is small, blurred and sunlit, so I compare character and relative shapes, not sizes or RGB.

## Three remaining gaps, ranked by how much they change the read

### 1. Eyes and face read (highest)

- **Evidence:** head comparison, ref and alt views (native eyes enlarged in my notes); reference face crop.
- **Native:** each eye is a tall black glossy oval with a thin pale outline, a crisp bright catchlight and a second
  small one.
- **Reference:** soft dark-brown ovals, no white outline, one soft highlight. The face reads warm and calm.

Causes, separated:
- **Authored material (confirmed in source):**
  - The two catchlights are painted into an emission map and wired to Emission at strength 1 (glTF `emissiveFactor`
    1, 1, 1), so they glow at full white in every light, including shade. That makes them read as stickers.
  - The eye surface is glossy (roughness 0.42; Blender specular 0.35, exported as `KHR_materials_specular` 0.83). That
    adds lit glints and brightens the edge where the eyeball meets the lids.
- **Authored texture vs geometry (confirmed in source):**
  - The pale outline is the sclera (sRGB 236, 227, 215) showing as a thin ring. Since v010 the painted iris oval
    (half sizes 0.0163 x 0.0262) is a little smaller than the lid opening (0.0174 x 0.0264), so a sliver of white is
    visible all round.
  - The iris is near-black (sRGB 30, 18, 12 to 92, 56, 32, pupil 18, 11, 9).
- **Geometry (hypothesis, not measured):** the lid opening is a tall oval (about 1.5:1). The reference eyes look
  rounder, but its framing and blur do not allow a measurement. The mouth is a thin curve, where the reference reads
  as a slightly wider, softer smile. Both are UNKNOWN until checked in a matched view.
- **Renderer:** the near-frontal key flattens the face planes, so the eyes dominate. That is secondary here; the
  emission makes the catchlights renderer-independent anyway.

### 2. Hair silhouette and surface

- **Evidence:** head and body comparisons, ref and alt; back view.
- **Native:** a wide, radial cap. Broad side masses flare at the temples, locks have flat planar tops ending in sharp
  points, and the colour is one dark red-brown with little highlight.
- **Reference:** rounder and taller, tousled upward at the crown, a fringe sweeping to one side, softer edges, lighter
  warmer colour with broad highlight bands.
- **Geometry (construction method):** locks are swept surfaces radiating from the crown and fused by a voxel remesh.
  That makes a smooth cap with planar lock tops, and the side masses set the width. The D1/D2 lever studies (runs 29
  and 30) showed per-lock changes do not change this read. The lock-edit method has reached its stop rule already.
- **Material:** one matte albedo (m001-B, roughness 0.70); no broad highlight band in the texture.
- **Renderer:** a frontal key gives no rim or sheen, so lighting cannot add the reference's highlights to a matte cap.

### 3. Costume integration (hood, straps)

- **Evidence:** body comparison and native views.
- **Native:** a standing collar with a knotted brown scarf, two straight dark strap bands down the front, a long
  straight jacket edge, regular boot cuff rings.
- **Reference:** a big, soft yellow hood bunched behind the neck and shoulders; front straps hardly read; softer,
  shorter-looking jacket.
- **Geometry:**
  - The collar v004 was built as a seated standing roll.
  - The front straps belong to the frozen body and cannot move.
- **Material:** palette p001 made the straps darker, which makes them more graphic from the front.
- **Rank:** third, because it defines Simm less than face and hair do, and its main fix (hood volume) is geometry.

Lighting cannot fix in any of the three: hair and hood volume, eye-opening shape, the reference's painted glow and blur.

## ONE next batch: E1 "soft eyes" (eye material and eye texture only)

**Why this one first:**
- It is the most visible gap.
- Its main causes are confirmed in source, not guessed.
- It is material and texture only, reversible, and needs no geometry, rig or skin change.
- It answers the user's earlier complaint ("looks like it's from Silent Hill ... the concept is very cute") without
  going back to the v002 to v008 failure (black, glossy, no highlight). E1 keeps one highlight, makes the iris brown
  and makes the surface matte.

**Scope:** `SCULPT_MAT_EYE` and its base-colour texture only.
- Remove the emission (no emissive texture, emissive factor 0).
- Roughness 0.42 to 0.55; Blender specular 0.35 to 0.25.
- Repaint the eye albedo:
  - iris oval half sizes 0.0182 x 0.0272, covering the lid opening so no sclera ring shows;
  - iris dark warm brown (sRGB 58, 34, 22 at the top to 122, 78, 46 at the bottom), pupil 30, 18, 12;
  - ONE catchlight painted in the albedo (sRGB 225, 215, 200, 80 percent opacity), lit like the face; the second
    catchlight removed;
  - sclera, now hidden behind the lids, warm 214, 190, 168.

**Held:** eye and lid geometry, lashes, brows, skin texture, mouth, hair geometry and m001-B, every costume part and
palette, rig, actions, socket.

**Demo:** `art_source/handoff/claude_production/ART-005/a1_critique/a1_eye_e1_demo.png`. The held v012 and the E1
change are rendered side by side at ref and alt (Blender, same lights and cameras), next to the reference face crop;
the change was made by `ART-005/build_scripts/eye_e1_demo.py`, in memory only.
- **Ref view:** the pale outline is gone; the eyes read as soft dark-brown ovals with one lit highlight; the face
  reads calmer and closer to the reference's character.
- **Alt view:** the highlight nearly disappears at that angle. That is the main risk, covered by R2.

### Rejection criteria (native, both agreed views, the A1 studio setup, plus camp zoom 10)

1. **R1 outline:** a continuous pale ring around either eye at ref or alt fails.
2. **R2 life:** fails if either eye reads as a flat black hole: no visible highlight or soft light patch at ref, or on
   the near eye at alt. This is the user-rejected v002 to v008 look.
3. **R3 warmth:** at ref, enlarged 2x, the iris must read brown and lighter than the pupil. Black fails.
4. **R4 game scale:** at camp zoom 10 the eyes must still read as two dark dots with a highlight. Lost eyes fail.
5. **R5 isolation:** every other material, texture and mesh must be byte- or hash-identical to the held assembly.

### Stop rule

- One E1 pass, plus at most one value-only follow-up after Codex's native review (catchlight strength or iris
  value).
- If R1 or R2 still fail, or the face still reads as glossy doll eyes, stop material work on the eyes. The remaining
  cause is then the eye opening's shape and size (geometry). That needs its own proposal, decided with the user at A1,
  not another texture cycle.

### Not in this batch (recommendation for the A1 conversation)

- **Hair:** lock edits are exhausted. If the user wants hair closer to the reference, it needs a whole-form rebuild,
  for example a silhouette-first shell: hair envelope curves taken from front and three-quarter views, one shell
  built to that envelope, 6 to 10 broad clumps carved into it, then a lighter, warmer palette with a broad highlight
  band. That is a larger cost and a user decision.
  - Its own stop rule: if a clay silhouette test at both views does not read closer than v012 to Codex and Fable, drop
    it.
- **Costume:** a softer, larger hood bunched behind the neck is the one change with real effect. It is geometry and
  waits for the user's A1 priorities. Strap darkness could be revisited as a value-only palette note.
