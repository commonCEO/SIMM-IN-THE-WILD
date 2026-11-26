# Clearing art audit and asset production proposal (board ticket ART-006, second pass)

Written by Claude (Fable), 25 November 2026. A proposal for Codex and the user, not an approved plan.
No meshes were made for this ticket and nothing outside the head was changed.

## 1. What this is based on, and what it is not

Looked at directly:

- `art_source/handoff/claude_simm/APPROVED_REFERENCE.png`, full 2048 x 1270, on `codex/simm-art-handoff`.
- `docs/npc-concepts-v2.png` (six character identities) and `docs/v06-art-directions.png`.
- `docs/ART-DIRECTION-GUIDE.md`, `docs/MATTIAS-BOSS-CONCEPTS.md`, `docs/MATTIAS-NEW-IDEAS.md`, the section list of
  the game design document, `godot/assets/manifest.json`.
- Seven head iterations and Codex's six native Godot reviews of them.

Added in the second pass (26 November 2026), looked at directly, at full 1600 x 992:

- `coordination/reviews/clearing-reference-composition-study.png` and `clearing-alternate-composition-study.png`:
  Codex's native Godot captures of the existing key-shot study scene. Not the playable camp. Original runtime
  models at study scales, orthographic size 5.65.
- `coordination/reviews/clearing-gameplay-zoom-fresh-state.png`: the actual camp scene, fresh state, orthographic
  size 10, with debug HUD and world labels.

Limits of this evidence: three still frames, one light setup, no motion. Simm in them is the old runtime model,
not head v007, collar v002 or the jacket candidate. Claude did not run Godot. Section 2 (style rules), section 5
(contracts) and section 7 (questions) are unchanged from the first pass. Section 3 is rewritten from the frames.

## 2. Style rules read from the reference

These are observations of the approved picture. Where a rule goes beyond what is visible it is marked (opinion).

1. **Everything is a soft, thick volume.** Nothing in the frame is a thin plane or a sharp edge. Leaves are fat
   rounded lobes, cloth has thickness at every hem, timber has heavy bevels, the rock is a pillow. This is the
   same lesson the head took six rounds to learn: flattened straps read as leaves or blades; rounded sections
   with taper only at the end read as the reference.
2. **Forms are built from clusters, three levels deep.** An oak crown is about 20 to 30 leaf clusters; each
   cluster is a rounded mound of 15 to 25 leaf lobes; the lobes are large enough to count. Pines are stacked
   drooping tiers, each tier a row of scalloped bough pads with rounded needle lobes at the edge. Birch is the same
   idea in smaller, lighter, yellower clusters on white trunks with dark marks. The berry bush is a mound of
   pointed leaf clusters with oversized blue berries.
3. **Proportions are chunky and child-scaled.** Simm is about three heads tall. Bronkings and Leina are about
   four. Hands, boots and props are oversized: the mossy rock is nearly waist-high to Simm, berries are fist-sized,
   hammer head is as big as a torso.
4. **Three value families, one warm key.** Light warm camp floor and yellow clothing; mid-value foliage and wood;
   dark cool forest recesses. The sun comes from upper left and behind the camera's left shoulder: shadows fall to
   the lower right and are about 0.6 to 0.8 of the object's height long.
5. **Matte, soft surfaces with gradient shading.** Almost no specular highlight anywhere except a broad soft sheen
   on Simm's hair and the metal tools. Detail comes from form and from broad colour gradients (lighter, yellower
   tops; deeper, cooler undersides), not from fine texture.
6. **Shadows are soft far from the caster and tight at contact.** Every object sits in a soft dark contact pool.
7. **The clearing floor is pale sandy stone with a faint large tile grid**, feathering into a tufted grass carpet
   with small white, yellow and pink flowers in loose groups. Sticks, pebbles and small stones lie on the boundary.
8. **Framing.** Tree crowns overlap all four corners and both sides; the open floor is roughly the middle 45
   percent of the frame width. The picture has blur at the edges; the guide already says not to copy that.
9. **Detail priority (opinion):** characters first, then the two camp props, then foliage clusters, then ground.

## 3. Biggest scene-level gaps, re-ranked from the native frames

### 3.1 Measured (evidence)

Pixel statistics, reference with its UI band cropped off against the native frames. Luminance is 0 to 1.

| Frame | Mean RGB | Luminance 5th / 50th / 95th percentile | Pixels darker than 0.15 |
|---|---|---|---|
| Approved reference | 126, 121, 58 | 0.13 / 0.46 / 0.83 | 7.6 percent |
| Native study | 116, 128, 65 | 0.18 / 0.53 / 0.73 | 1.2 percent |
| Native alternate | 113, 125, 62 | 0.18 / 0.51 / 0.72 | 1.8 percent |
| Native gameplay | 140, 144, 76 | 0.17 / 0.57 / 0.75 | 3.0 percent |

- The reference is warm: red is above green in its mean. All three native frames are green above red.
- The reference has a wider range: brighter highlights (0.83 against 0.73) and more deep darks, which sit in the
  framing foliage at the edges. The native frames are flatter overall.
- Shadow on the floor, one sample pair each. Reference: lit tile 248, 210, 147 and shaded tile 166, 136, 88.
  The shadow keeps the hue (38 and 37 degrees) and 67 percent of the lit value. Native study: lit sand
  206, 183, 137 and shaded sand 64, 69, 56. The shadow drops to 33 percent of the lit value and the hue swings
  from 40 to 86 degrees, a grey green. So the native shadow is about twice as deep and loses its warmth.
- I also sampled grass and foliage, but my hand-picked points were not reliable enough to quote.
- Sizes, by pixel measurement, approximate. Simm's height as a share of frame height: reference 21 percent,
  native study 22 percent, native gameplay 12 percent. Tent height against Simm's height: reference about 1.0,
  native study about 1.0, native gameplay about 1.95.

### 3.2 Ranking (opinion, based on 3.1 and the frames)

Rank is how much the gap hurts the picture in these frames. It is not the work order: A1 still comes first.

| Rank | Was | Gap | Kind | What the frames show | Owner |
|---|---|---|---|---|---|
| 1 | 4 | Light and shadow | Lighting | Hard-edged, near-black shadow masses cover roughly a quarter of the study frame and cut straight across the clearing. Shadows lose the warm hue (3.1). No warm cast on grass, no dark framing at the edges | Codex, hypotheses L1, L4, L5 and new L9, L10 |
| 2 | 2 | Foliage construction | Geometry | Deciduous crowns are balls covered in hundreds of small pointed scales. The reference has 15 to 25 fat rounded clumps per crown with a light top and dark underside. Conifers are flat blades on visible sticks, not layered soft boughs. The birch is one bare white stick, not two or three marked trunks with hanging clumps | Fable |
| 3 | 3 | Ground | Material and layout | Grass is one flat green plane. The sand has no tile grid. In the alternate frame the sand edge is stair-stepped on the right. Grass tufts are one wreath shape stamped at even spacing | Fable (materials, kit), Codex (mask, placement) |
| 4 | 1 | Characters | Geometry | Capsule limbs, dot faces, stiff arms. Still the largest gap up close, but they are small on screen and the A1 path is already running | Fable, then Codex fit |
| 5 | new | Camp layout and scale | Layout | In the playable camp the tent is about twice Simm's height, double its study size. The sand is a wide empty field, and nothing frames the bottom or right edge. The reference clearing is compact and ringed by overlapping crowns | Codex and user decision |
| 6 | 5 | Camp props | Geometry and material | From the alternate angle the tent reads as a flat sheet with no depth. The bench is clean and light where the reference is chunky and dark with a vise and bucket. The rock's moss is a flat bright cap. Berry bushes are sparse where the reference has dense round ones | Fable |
| 7 | 6 | UI | Separate lane | Debug text, floating world labels and a text hotbar | Fable art, Codex UI, after A2 |

Why light moved to the top: it is the difference that reads first at thumbnail size, it affects every asset
already in the scene, and it is testable now without any new mesh. Characters moved down in rank only. Their
priority as the A1 gate is unchanged.

### 3.3 Findings Codex's notes did not already state

- The tent scale differs between the study scene and the playable camp by about a factor of two.
- The tent has no visible depth from the alternate camera.
- Shadow on sand loses hue as well as value (numbers in 3.1).
- The sand mask edge is stair-stepped at this zoom.
- All grass tufts are one shape at near-even spacing, which reads as a stamp.
- The birch has a single trunk and no bark marks.

### 3.4 One bounded packet proposed for after A1

**Oak pilot: one deciduous tree built as a clump kit.** Board ticket ART-008, first slice. Not started; no world
mesh before A1.

- Contents: one trunk with root flare and two visible main branches; three clump modules (large, medium, small),
  each a fused rounded mass of 8 to 12 leaf lobes; one assembled tree of about 18 to 22 clump instances.
- Contract: static GLB, metres, Y-up, pivot at the trunk base on the ground, front toward the camera side. Two
  materials (bark, leaf). Leaf shading from a baked top-light to underside-dark gradient in vertex colour or one
  small texture. No alpha cards. Source density free for review; game budget set after PERF-001.
- Test: Codex swaps it for the two left-hand trees of the study scene, same camera and light, and publishes the
  frame next to the reference.
- It passes if the crown reads as clumps at thumbnail size and the silhouette is lumpy rather than a scaly ball.
  It fails if it reads as a smooth blob or costs more than the agreed budget.
- If it passes, the pine, birch and bush follow the same kit method. If it fails, the kit idea in section 4 is
  wrong and should be replaced before more foliage is made.

## 4. Proposed asset packets, in order

Order follows the board's gates. Nothing after packet 2 starts before A1.

| # | Packet | Board ticket | Depends on | Contents |
|---|---|---|---|---|
| 1 | Simm head | ART-001 (active, v007 delivered) | Codex review | Head, hair, eyes, brows, lashes |
| 1b | Simm head, game resolution (proposed new ticket) | proposed ART-011 | Head shape accepted | Reduced mesh, baked normal map from the review-density sculpt, one skin and one hair material |
| 2 | Simm body and clothes | ART-004 | ART-003 fit study | Jacket with hood, scarf, shirt, trousers, boots, backpack, on the existing skinned topology |
| 3 | Leina | ART-007 | A1 | Head and hair first, then clothes and held items; rig untouched |
| 4 | Bronkings | ART-007 | A1, packet 3 method | Same |
| 5 | Camp props | ART-008 | A1, section 2 rules | Tent, workbench |
| 6 | Foliage kit | ART-008 | A1, PERF-001 budget | Leaf-cluster modules per species, trunks, assembled oak, pine, birch, berry bush |
| 7 | Ground kit | ART-008 | Packet 6 | Rock with moss, pebble, branch, grass tuft, flower groups, floor and grass materials |

### Why the foliage should be a kit (opinion, testable)

The guide reports three tree sources repeated 22 times and triangle counts above budget. The reference crowns are
visibly the same few cluster shapes repeated at different sizes and rotations. So the efficient asset is not
"an oak" but three or four leaf-cluster modules per species, a trunk with branch stubs, and an assembly. Codex
can then instance modules, vary crowns without new meshes, and cull or swap modules by distance. Test: build one
oak from modules and compare triangle count and draw calls with the current oak at the same camera.

## 5. Contracts every packet will meet

From `godot/assets/manifest.json` and `FABLE_NEXT_CHECK.md`, plus what the head loop showed is needed.

- **Units and axes:** metres, Blender Z-up with front -Y, exported as glTF Y-up so front is +Z in Godot.
- **Pivot:** ground at origin, centred. Root node named after the asset id, identity transform.
- **Files:** versioned `.blend` (Blender 3.5.1) and `.glb` with embedded textures; earlier versions kept.
- **Rigs:** characters keep their existing skeletons, rest matrices, actions and sockets, proven by
  `verify_candidate.py` against the starter file. Per the guide: Simm 17 bones; Leina 20; Bronkings 18. Claude has
  only seen Simm's rig. Leina's and Bronkings' starter files must be committed before packets 3 and 4.
- **Skinned parts (packet 2 on):** shape changes are made on the existing skinned topology so vertex groups stay
  valid. No auto-rig, no weight transfer unless Codex assigns it as its own ticket.
- **Materials:** glTF PBR only; base colour, roughness and normal maps; no baked light or shadow; counts reported.
- **Evidence in each packet:** triangle and vertex counts per mesh from a re-imported GLB, bounds, GLB sha256,
  clay and colour renders at the agreed cameras, a lock or part manifest so silent omissions are caught,
  provenance and licence of every source, an honest issue list, and the proposed next action.
- **Budgets:** not set here. They follow PERF-001. For planning only (opinion): hero character 15 to 25 thousand
  triangles, NPC 12 to 20, tree 4 to 10 with modules instanced, prop 1 to 6.

## 6. Lighting and post hypotheses for Codex to test natively

Claude cannot run Godot. Each item is one variable, same camera, with the result that would count against it.
Negative results are useful and should be published.

| ID | Hypothesis | Change | Expected if true | Counts against it |
|---|---|---|---|---|
| L1 | Sun direction and height can be read from the picture | Elevation about 52 to 58 degrees, from upper left, so Simm's shadow is 0.6 to 0.8 of his height toward lower right | Shadow shapes line up with the reference | Shadows match only at a clearly different angle |
| L2 | The "clay" softness is mostly a wrapped diffuse response, not subsurface | Set diffuse mode to Lambert Wrap on foliage, cloth and hair only | Softer terminator, lit sides stay bright, recesses stay dark | No visible change, or everything goes flat |
| L3 | Hair reads as shiny straps partly because of specular | Hair roughness 0.52 to 0.70, specular lower, geometry unchanged (use v007) | Narrow bright ridges disappear, form still reads | Hair goes dull brown with no form |
| L4 | Shadow stipple is a sampling-quality problem, as Codex's angular test suggests | Highest directional soft-shadow quality at 2 degrees, then test in motion | Clean soft penumbra that holds while the camera moves | Stipple returns in motion at any quality |
| L5 | Warm key to cool fill ratio near 2 to 1 on skin gives the reference warmth | Key 0.8 warm as now; ambient tinted slightly blue-green; vary ambient only | Shadow side of faces stays readable and cool | Skin goes grey or green |
| L6 | Contact pools need a short-radius occlusion pass, separate from the sun shadow | SSAO radius small, intensity up, on and off | Feet, rock, tent and bench sit on the ground | Dark halos round characters |
| L7 | Depth at the forest edge can come from tinted distance fog instead of blur | Light green-blue depth fog starting past the clearing | Background crowns separate without losing sharpness | Clearing itself gets milky |
| L8 | Yellow jacket and warm skin survive better under AgX than Filmic | Tone mapper only | Yellows stay yellow at the same exposure | No difference or duller reds |
| L9 | The near-black, hue-shifted shadows come from too little warm fill, not from the key | Keep the key. Lower the directional light's shadow opacity or raise ambient energy, and tint ambient warm, until shaded sand holds about two thirds of its lit value at the same hue | Shadow shapes stay readable, shaded sand reads as darker sand (near 166, 136, 88 against lit 248, 210, 147 in the reference) | Scene goes flat and the characters stop sitting on the ground |
| L10 | The reference's depth comes from dark framing at the edges, which light alone cannot give | With L9 applied, add a mild vignette or darken the outer ring of foliage only | Centre reads brighter, eye goes to Simm | Edges look dirty, or no change because the edges are still open grass |

## 7. Questions that need the user or Codex

1. Is the faint tile grid on the clearing floor wanted? The reference shows it; the guide calls it optional.
2. Simm's body in the reference has a raised hood and a scarf that hide the neck. The frozen body has neither at
   that height. Is adding them part of ART-004?
3. For Leina, Bronkings and later NPCs, which picture is the identity authority when the pixel concepts and the
   approved 3D reference disagree (for example Leina's hair is curly in the concept and smoother in the reference)?
4. Penguin, bucket and the three bosses (ADD-001): Claude will write design proposals from Mattias's drawings when
   that ticket opens, with assumptions and questions separated from facts. The drawing
   `docs/concepts/mattias-bosses-20261125.png` is referenced but is not on the branch Claude can read.
