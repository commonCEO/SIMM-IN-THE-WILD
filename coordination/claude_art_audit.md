# Clearing art audit and asset production proposal (board ticket ART-006, first pass)

Written by Claude (Fable), 25 November 2026. A proposal for Codex and the user, not an approved plan.
No meshes were made for this ticket and nothing outside the head was changed.

## 1. What this is based on, and what it is not

Looked at directly:

- `art_source/handoff/claude_simm/APPROVED_REFERENCE.png`, full 2048 x 1270, on `codex/simm-art-handoff`.
- `docs/npc-concepts-v2.png` (six character identities) and `docs/v06-art-directions.png`.
- `docs/ART-DIRECTION-GUIDE.md`, `docs/MATTIAS-BOSS-CONCEPTS.md`, `docs/MATTIAS-NEW-IDEAS.md`, the section list of
  the game design document, `godot/assets/manifest.json`.
- Seven head iterations and Codex's six native Godot reviews of them.

Not seen: **any current Godot render of the clearing, the NPCs, the props or the trees.** Those live on the PC and
are not in Git. Every statement below about the *current* state of the scene is taken from Codex's art guide,
not from Claude's eyes. Statements about the *reference* are Claude's own reading of the picture.

**Request to Codex (new dependency for this ticket):** commit three current native frames to
`coordination/reviews/`: the clearing at the reference camera, one alternate angle, and one at gameplay zoom.
With those the gap list in section 3 can be made from evidence instead of second hand.

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

## 3. Biggest scene-level gaps, in the order they hurt the picture

Ranked from the guide's own descriptions and the head experience. To be re-ranked once native frames are in Git.

| Rank | Gap | Why it is first | Owner |
|---|---|---|---|
| 1 | Characters: sculpt, cloth volume, expression | The eye goes to them; A1 is the gate | Fable, then Codex fit |
| 2 | Foliage construction: crowns as counted clusters of fat rounded lobes | Covers the outer third of every frame; guide reports pointed, repetitive sprays | Fable |
| 3 | Ground: tile floor, grass carpet, feathered boundary, contact dressing | Covers the middle of every frame | Fable (materials, kit), Codex (placement) |
| 4 | Light: warm key, soft shadow without stipple, cool fill, contact pools | Decides whether good forms read as clay or as plastic | Codex, hypotheses in section 6 |
| 5 | Camp props: tent, workbench, rock, bush | Fewer and smaller on screen | Fable |
| 6 | UI frame: hearts, day badge, hotbar | Separate lane, after A2 | Fable art, Codex UI |

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

## 7. Questions that need the user or Codex

1. Is the faint tile grid on the clearing floor wanted? The reference shows it; the guide calls it optional.
2. Simm's body in the reference has a raised hood and a scarf that hide the neck. The frozen body has neither at
   that height. Is adding them part of ART-004?
3. For Leina, Bronkings and later NPCs, which picture is the identity authority when the pixel concepts and the
   approved 3D reference disagree (for example Leina's hair is curly in the concept and smoother in the reference)?
4. Penguin, bucket and the three bosses (ADD-001): Claude will write design proposals from Mattias's drawings when
   that ticket opens, with assumptions and questions separated from facts. The drawing
   `docs/concepts/mattias-bosses-20261125.png` is referenced but is not on the branch Claude can read.
