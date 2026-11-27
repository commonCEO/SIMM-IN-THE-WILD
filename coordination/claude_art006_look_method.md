# ART-006 A1 look method (Fable)

## L2 "shadowless form light" (27 Nov 2026, run 36; answers Codex `4097e24`)

Status: ONE method proposal for Codex's native test. No asset, material or palette change. L1 below is kept for
history. Codex rejected its side key natively: hard shadow across the lower cheek, mouth and chin, and hard strap and
hand shadows. Warm ambient A stays a separate candidate.

### Why L1 failed, and what L2 changes

The L1 side key did two jobs at once: it gave a direction to the shading, and it moved every cast shadow. The hair
fringe, hood and collar then threw hard shadows onto the lower face. L2 splits those jobs:
- **Cast shadows stay where they are now.** They come only from the native key, which stays exactly as it is (rotation
  -40, -30, 0, energy 0.8, colour #fff0df, angle 0.25, far 20).
- **Directional shading comes from a second light that casts no shadows.** Its effect is a smooth Lambert falloff
  across each form (brighter on planes facing it, unchanged on planes facing away). It cannot draw a shadow edge on the
  face or the cloth, because it casts none.

It is a fixed world-space light. It does not follow the camera, and nothing is painted.

### The one parameter mapping (Godot, proposed, untested)

Add one DirectionalLight3D "SimmFormFill" to the study, with all other values unchanged:

| Property | Value |
|---|---|
| direction | source vector (-0.679067, 0.707107, 0.197149), the L1 side direction you already constructed (rotation -45, -73.81079, 0) |
| shadow_enabled | false |
| light_energy | 0.3 (= 0.375 of the key) |
| light_color | #ffe6c8 (warm, a touch warmer than the key) |
| light_specular | 0.0 (no second highlight on hair, cloth or the eyes' catchlights) |
| ambient, key, SSAO, shadows, exposure, Filmic, materials | unchanged; base = the corrected far20 study with cool ambient #b7c9d2 at 0.35 |

Run base and base + SimmFormFill at the ref, alt and back cameras, colour and clay, plus one motion check (walk) for
shading stability. A is not part of L2. If wanted, A + L2 is a separate control, already shown in the demo.

### Predicted visible result

Predictions come from the Blender demo, which uses the native key and side directions converted from Codex's values
(`look_method_l2_metrics.json`).
- **Face:** no new shadow shapes. The cheek nearest the light (Simm's right, screen left in the ref view) lifts slightly
  (demo: face half luminance 0.664 to 0.701, other half 0.697 to 0.712). A gentle sense of light from one side, not a
  dark side. For comparison, the rejected side key dropped the far half to 0.598, with hard edges.
- **Back and sides:** the clearest change. One side of the back reads lit and the other stays in shade, a soft
  gradient (demo back-view jacket value p90 115 to 160, p50 94 to 107).
- **Cast shadows, strap and hand silhouettes, boot contact:** identical to base, because SimmFormFill casts none.
- **Front ref view:** little change to the jacket's value range (demo p10 to p90 stays about 43 levels). L2 alone will
  not make the front less frontal.

### How it could fail (any one fails L2)

1. **Leak.** A shadowless light also reaches places the key's shadow and SSAO keep dark. If the inside of the hood,
   under the jacket hem, between the legs or the inner pack side brightens visibly against base, the light is too
   strong or SSAO does not cover direct light. Report which, and do not compensate with more ambient occlusion
   strength.
2. **Face.** Any new dark shape on the cheek, mouth or chin fails (none is expected). So does a lost catchlight or a
   second highlight on the eyes, which means light_specular is not 0.
3. **Flattening.** The far side's value relative to the near side at the back view does not separate (no visible
   gradient), or the whole figure only gets brighter. Then the energy is too low; the single follow-up lever is energy
   0.3 to 0.45, not a new direction.
4. **Motion.** Shading on the face or jacket pops or swims during the walk. A directional light without shadows should
   be stable, so this would point to normals or skinning, not lighting.
5. **Scope.** Fitted-Simm study only. No grade, no camera-linked light.

### Demo disclosure

`art_source/handoff/claude_production/ART-006/look_method_l2/look_method_l2_demo.png` and the metrics file, made by
`ART-006/build_scripts/look_method_l2_demo.py` (review only, never saves). The rejected B column reproduces the native
hard lower-face shadow, which is some support that the demo's light directions match.

It is Blender Cycles with one sun plus a constant world colour and no bounce light, not Godot. `cloth_tone.png` and
`leather_tone.png` are not in Git, so cloth and boots use a flat 0.5 stand-in. Absolute colours mean nothing; Codex owns
the native evaluation.

---

## L1 "warm shade, side key" (27 Nov 2026, run 35; answers Codex `e91d3bd`; side key rejected natively at `4097e24`)

One bounded method proposal for Codex's native test (RENDER-001 owns the native run). No mesh, material or palette
revision. Held assets: head v012 + m001-B, jacket f002 + m002, palette p001, collar v004 + brown neck layer, boots v002.

### What I looked at

- **Directly:**
  - Codex's native frames `reviews/support-p001-native-palette-comparison.png` (ref, alt, back) and
    `reviews/jacket-m002-native-material-comparison.png`.
  - The full approved reference, read from Codex's branch with `git cat-file`, not copied.
  - Codex's stated native baseline: key 0.8 #fff0df; ambient 0.35 #b7c9d2; Filmic; SSAO 0.45 at radius 0.20;
    directional 8192/ULTRA/TAA; angle 0.25; range 3 m.
- **Not looked at:** Godot itself, the native scene files, motion, camp occlusion, performance.
- **My own renders:** a Blender demonstration of the method on the held assets, labelled as such:
  `art_source/handoff/claude_production/ART-006/look_method_l1/`.

### Measured, not judged

Yellow-jacket pixels: HSV saturation over 0.5, hue 36 to 70 degrees (`look_method_l1_metrics.json`).

| | Hue mean (p10 to p90) | Value p10 / p50 / p90 (sRGB) |
|---|---|---|
| Reference, Simm crop (sunlit) | 42.2 (36.4 to 50.8) | 181 / 239 / 253 |
| Native p001, ref camera | 44.3 (41.5 to 46.4) | 189 / 220 / 234 |
| Native p001, back camera | 45.0 (42.9 to 47.8) | 111 / 116 / 131 |

The reference spreads the jacket over about 14 degrees of hue: warm ochre in shade, lemon in light. Native spreads it
over about 5 degrees. The reference's value spread (p10 to p90) is 72 levels; the native front view's is 45. On the
back, where the jacket is all in shade, the yellow drops to a single dull olive band. These numbers are evidence of a
lighting difference only to the extent that the materials are now similar. The reference is a painted, sunlit image, so
matching its numbers is not parity.

### Three gaps, ranked by visible effect

1. **Direct-to-fill balance and fill colour (form shadows).**
   - The cool ambient (#b7c9d2) on saturated yellow turns every shaded plane olive. The near-frontal key leaves
     the front evenly lit with little turning shadow.
   - Lighting can fix: shade hue, key-to-fill ratio, where the terminator falls.
   - Lighting cannot fix: hood and jacket bulk, head and hair volume, boot chunkiness (geometry), or the reference's
     painted glow, depth of field and warm whole-frame grade (painting; the brief rules out grading to match).
2. **Fabric, skin and hair response.**
   - The reference shows a soft, wrapped terminator on cloth and skin and a broad sheen on the hair crown. Native shows
     a harder Lambert edge and matte hair (m001-B at 0.70, held; 0.50 stays rejected as waxy).
   - Partly follows from gap 1: a side key creates the highlight shapes. Partly material (wrap, sheen, rim), which
     glTF does not carry.
   - Not proposed now. Test only after L1 settles, as one variable at a time.
3. **Contact and cast-shadow quality.**
   - The blocky floor shadow and the missing contact darkening under the boots. Codex's RENDER-001 already tests
     shadow range and cascades.
   - L1 moves the shadow, so its failure criteria include not making that worse.

### The method: L1 "warm shade, side key"

Change only the lights below, in this order, on the native fitted-Simm study. Keep the same cameras, pose, exposure,
Filmic, SSAO, shadow settings and every material. Capture each step, including the clay shape-control frame, at the ref,
alt and back cameras.

| Step | Variable (Godot, proposed, untested) | From | To |
|---|---|---|---|
| A | ambient light colour | #b7c9d2 | #d9c7a8 (warm neutral), energy unchanged 0.35 |
| C | ambient light energy | 0.35 | 0.25 (key-to-fill ratio up by 1.4x) |
| B | key DirectionalLight3D direction and energy | present direction, 0.8 | light arriving about 45 degrees off the ref camera's axis toward Simm's right (screen left in the ref view), elevation about 45 degrees; energy 1.0; colour #fff0df and angle 0.25 unchanged |

Run order: base, A, A+C, A+C+B, plus B alone as a control. Energies do not map one-to-one between engines. My demo was
calibrated in Blender, so only the ratios and directions carry over.

#### Predicted visible result (from the demo, to be checked natively)

- **A:** the shaded jacket turns warm ochre instead of olive. Demo back view: hue 45.2 to 38.5 degrees, value p50 94 to
  114. The lit side barely changes; skin and hair shade warm slightly.
- **C alone:** shade only darkens and stays olive (demo back p50 94 to 80). Hence C goes with A, not on its own.
- **B:** one lit and one shaded side on the jacket and face from the ref camera. Cast shadow falls behind-right, as in
  the reference. In the alt view the jacket becomes mostly lit (value p10 89 to 137).
- **A+C+B:** warm shade with a wider light-to-shade value range. The jacket's hue spread widens toward the reference's
  (demo ref view: p10 to p90 hue 36.9 to 49.1).

#### Failure criteria (any one fails the step)

1. **Hue.** Shaded jacket hue mean below 34 degrees (turns orange-brown and loses yellow), or lit jacket hue p90 below 44
   (lemon highlight lost).
2. **Face.** On the face, the shadow-side cheek luminance falls below 0.6x the lit cheek, a dark band from the fringe
   crosses the eyes, or catchlights disappear. This would push back toward the grim look the user rejected. It fails
   even if the jacket improves.
3. **Shadows.** Floor or hood shadow stepping or stipple becomes more visible than at base. Stop B and hand over to
   RENDER-001 shadow coverage; do not soften the light to hide it.
4. **Flattening.** The warm ambient flattens form: native front-view jacket value p90 minus p10 shrinks below base (45
   levels) after A+C.
5. **Scope.** Judged on the fitted-Simm study only. Foliage and world may need different fill. No colour grade.

### Demo disclosure

`look_method_l1_demo.png` was made with Blender Cycles: one sun, a constant world colour, no bounce light, Filmic,
fixed exposure, the held cameras.

- `cloth_tone.png` and `leather_tone.png` are not in Git: cloth and boot colours use a flat 0.5 stand-in. Trousers,
  pack, straps and boots therefore render darker than native, and absolute colours mean nothing.
- Script: `art_source/handoff/claude_production/ART-006/build_scripts/look_method_demo.py` (review only, never saves).
- Nothing native was run by Fable.
