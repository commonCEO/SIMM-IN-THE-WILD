# SIMM IN THE WILD — clearing art direction

**Visual authority:** [approved reference](ART-DIRECTION-REFERENCE.png), supplied by the user on 22 November 2026. This is the enlarged upper-right direction from `v06-art-directions.png`. The reference establishes the target; existing renders establish only the current implementation. Having thirteen GLBs is an integration milestone, not visual acceptance.

## The intended image

A small, sunlit woodland camp surrounded by a lush, sculpted forest. The scene should feel handmade, welcoming and tactile: soft rounded forms, rich plant silhouettes, believable cloth and timber, warm grazing sunlight, cool green shade. It must read as a coherent little world rather than a set of isolated toys arranged on a plain ground plane.

The reference is an illustrative target, not a texture to project or a promise of pixel-perfect reproduction. Preserve actual dimensional geometry, responsive controls and readable gameplay. Do not bake its shadows, blur or painted perspective into assets.

## What is currently wrong

| Area | Current problem | Required direction |
| --- | --- | --- |
| Composition | Wide empty oval, isolated trees and a repeated decorative ring | Interlocking forest masses around an irregular open camp; foreground, middle ground and background |
| Ground | Smooth pale sand with little local variation; grass reads as a flat green surface | Warm weathered earth with granular variation, roots, moss, grass islands and a feathered broken boundary |
| Foliage | Visible round base balls, evenly spaced blobs, oversized flat oval leaves | Nested sprays of leaves, layered conifer branchlets, crown voids and irregular silhouettes; leaves conceal construction volumes |
| Light | Washed-out yellow-green values, weak depth and speckled self-shadowing | Warm key light, restrained cool fill, deep readable green recesses and stable soft shadows |
| Materials | Uniform color and roughness; little distinction between cloth, wood, stone and leaves | Broad form first, subtle material-specific grain and roughness second; no shiny plastic or noisy universal texture |
| Characters | Stiff clothing blocks, exposed joint seams, simple eyes/hair and limited gestures | Softer anatomy and cloth transitions, shaped faces, layered hair, expressive relaxed silhouettes; preserve approved identities |
| Presentation | Oversized text and resource labels compete with the picture | Quiet gameplay framing; inspectable prompts instead of a field of permanent labels, subject to browser UX parity |

Lighting and dressing cannot repair weak silhouettes. Character sculpting, canopy rebuilding, cloth folds and material authoring remain separate art tasks even after this environment polish pass.

## Composition and camera

- Keep the stable orthographic follow camera: no bob, sway or lagged look-at. The user explicitly rejected camera wobble.
- Reference viewing pitch is roughly35–40degrees. Judge the camera using character face visibility and tent/bench readability, not a claimed exact measurement from an illustration.
- In a review view, Simm is the central warm focal point. Tent anchors left, workbench upper middle, Bronkings right, Leina upper left. Keep existing gameplay positions and reach rules unless a separate layout change is authorized.
- Forest surrounds approximately the outer third of the frame. Several overlapping crowns and trunks provide a shaded backdrop, while foreground plants partially frame the bottom corners. Avoid a visible necklace of evenly spaced planting.
- Preserve open approaches to stations, NPCs, shore and mine. Decorative planting has no collision, yields or save IDs. Visual occlusion still matters: keep decorative trunks and tall foliage off those routes.
- Do not use heavy depth of field to hide inadequate art. Gameplay interactables remain sharp and legible.

## Value, palette and illumination

Use three value families: light warm camp floor and yellow clothing; middle-value vegetation and wood; darker cool forest recesses. Highlights should remain below a broad pale-yellow wash. Blue berries, coral overalls and small white/yellow flowers are accents, not a competing rainbow.

Palette anchors (art swatches, not exact sampled pixel averages):

| Role | Suggested sRGB range |
| --- | --- |
| Sunlit leaves | `#9FAE4B` to `#C1CB66` |
| Leaf middle values | `#557539` to `#7D9440` |
| Pine/recesses | `#244A3D` to `#466C48` |
| Soil | `#9F8154` to `#C5A770` |
| Canvas | `#BDA87C` to `#D2BF91` |
| Bark | `#64452D` to `#956B3E` |
| Stone | `#7E887A` to `#A6AA94` |
| Berry bloom | `#3E5E88` to `#7392AB` |

One warm directional sun gives consistent highlights and broad soft shadows. Environment fill should retain hue and recess depth without turning shaded leaves black. Contact occlusion must ground feet, roots, cloth and rocks without dark halos or flickering dots. Torch lighting must retain the user-approved soft body shadow and evening controls.

Investigate artifacts independently: shadows on/off, SSAO on/off, full geometry versus imported LOD, material culling and overlapping surfaces. Record the actual cause and verified fix. Do not call disabling every shadow a fix, and do not conceal speckling with blur.

## Foliage construction

**Oak:** broad asymmetrical crown, multiple nested lobes, visible branch structure, leaves arranged in directional sprays. Large supporting masses should not remain naked spheres with sparse bumps. Leaves are cupped, tapered and varied, with small gaps revealing deeper darker layers.

**Pine:** a continuous tapered tree silhouette formed by overlapping descending boughs. Each bough divides into smaller needle sprays, with upward growing tips and shaded undersides. Avoid stacked cones, floating tiers, broad rubber triangles or beads on a stick.

**Birch:** slender white trunk with charcoal horizontal marks and fine branching; an airy irregular canopy with smaller lighter leaves. Avoid cotton-ball crowns and sparse isolated bunches.

**Understory:** grasses, ferns, low broadleaf plants and flowers grow in patches related to roots, shade and ground transitions. Vary density at several scales. Tall tips and occasional flowers break the contour; scattered individual stems connect patches. Do not scatter uniformly across the playable center.

All visible forms must work from a second camera angle. Grass blades and leaves need real thickness or purposeful two-sided surfaces; no whole-object cards, attached shadow discs or ground-plane sprites. Use instancing for repeated leaves/grass, and keep draw calls bounded.

## Surface treatment

- Wood: warm longitudinal grain, subtle knots and worn bevels; darker endgrain and joins. Grain follows the object, not global screen axes.
- Cloth: broad tension folds, fine low-contrast weave and matte response. Avoid a rigid triangle with a noise overlay.
- Stone: rounded broken planes, restrained mineral grain, locally clustered moss that follows the surface. Avoid evenly spaced green beads.
- Leaves: green variation by canopy depth/age, restrained roughness variation and cupped surfaces. Avoid random high-contrast freckles or a uniform shiny glaze.
- Soil: irregular low-frequency color fields plus fine grain, worn routes and embedded aggregate. Any tile marks are faint, weathered and optional; do not impose a high-contrast grid that conflicts with browser gameplay.
- Skin, eyes and hair require dedicated treatment. Do not apply the environment texture shader to characters or metal tools.

## Scope and acceptance gates

1. **Stable render:** no shadow acne, stippling, z-fighting or visible holes at normal play zoom and two closer views. Repeat in motion and under torch/evening lighting.
2. **Composition:** a dense irregular forest boundary with depth; warm open camp remains readable. No additional blockers or silent gameplay layout changes.
3. **Material pass:** ground, canvas, wood, stone and foliage separate by hue, shape and roughness. Avoid adding detail that only exists at an unusable inspection zoom.
4. **Silhouette pass:** replace visibly primitive tree crowns and stiff character/clothing forms. Lighting-only improvement does not close this gate.
5. **Gameplay preservation:** original save opens; inventory, tools, skills, resource depletion and Nups remain intact. Run the applicable regression checks without writing into the real save.
6. **User review:** show actual Godot renders beside the reference, plus the running saved game. Explicitly list remaining gaps. Only the user can approve the visual direction as achieved.

Preserve earlier `.blend` revisions, GLBs and the reference. New assets remain under `art_source/blender/` and `godot/assets/models/`, in metres, grounded at zero and with identity roots. Browser mechanics/UI/controller behavior remain the source of truth; this guide does not authorize redesigning them.

## Implemented environment pass — 22 November 2026

Directional-shadow isolation reproduced the original speckling with SSAO off, and removed it with directional shadows off. Focused28m coverage, an8192atlas and ultra soft filtering removed the visible stippling in the tested birch/workbench views while retaining soft directional shadows. Daylight, torchlight and an alternate view were inspected in Godot. This is evidence for those views, not a guarantee about every possible future asset or camera.

Blender oak/birch/pine sources now contain closed cupped leaf/needle sprays, with recessed construction cores. Grass, fern fronds and flowers use five render batches; eleven nonblocking decorative trees provide depth around the clearing. Soil has a broken grass transition and granular color, while static cloth, wood, stone and leaves have restrained object-local variation. The camera and gameplay layout remain unchanged.

The pass visibly improves density, foliage structure and shadow stability. It still falls short of the reference: character and cloth forms are stiff, leaf sprays are too pointed and repetitive, the ground lacks authored roots/stone transitions, and the forest composition needs deliberate art placement. Decorative trees currently reuse three source models. Tree counts exceed the initial budget guide and need authored LOD/material consolidation. Further technical tweaks must not be mistaken for completion of these art tasks.

### Simm iteration — 22 November 2026

Simm's v05 source now uses a tapered cheek/jaw shape, smaller inset hazel eyes, a quieter smile, swept tapered hair locks continuing around the nape, and an open golden jacket over a brown shirt. The coat has rounded sleeves, a folded hood, curved pockets and broad woven straps. The original17bone skeleton, rest matrices, animation curves and hand socket were retained and compared by hash. His playable scale, collision and controls are unchanged.

This addresses the original round-eyed face, separate hair lumps and rigid collar/pockets. The current head and hair are still stylized simplifications: further cheek/eyelid sculpting, natural hair grouping, material variation and clothing transitions need visual review against the reference. Preserve the existing motion while improving those forms; do not treat the presence of a new source revision as visual approval.

### NPC iteration — 22 November 2026

Leina and Bronkings now have v06 author files with smaller inset eyes, tapered/broader adolescent/adult face shapes, curved working clothes, flatter sewn pockets, proper back-to-front straps, folded shirt collars and rounded rolled sleeves. Leina retains auburn hair, a smoothly weighted two-bone ponytail, coral overalls, yellow shirt, flowers, a garden pouch and a cylindrical metal watering can. Bronkings remains bald and clean-shaven with ivory shirt, leather apron, tools and hammer. His hammer tilts forward from the grip so its shaft clears the sleeve, while retaining the original hand binding.

Their original20/18bone rigs, rest transforms, both hand sockets, jaw motion and idle/talk animation curves are preserved. The front/back and talk views were inspected in Godot, and both GLBs were independently reimported into Blender. Reference-level facial expression, natural curl grouping, fabric/leather surface treatment and integrated clothing anatomy still need dedicated visual refinement.

### Tent and workbench iteration — 22 November 2026

The v06 props replace the flat tent planes and sparse bench detail with broad cloth tension folds, gathered entrance flaps, thick hems and pole lashings; the bench gains pegged joinery, separate worn planks, longitudinal grain and growth rings, a vise/crank, divided tool tray, hollow metal cup, chisel/hammer/punch and draped linen. Tent vine leaves are cupped dimensional forms. Geometry, not a painted shadow or projected reference, provides the detail.

Both keep their original metric footprint and gameplay placement. The tent opening is visual: this art revision does not change its collider or add an interior gameplay system. Workbench crafting retains the existing menu, station requirements and controller behavior. Front/back views were inspected in Godot. Further material nuance, less regular wood wear and selective cloth refinement remain; both props need geometry/material optimization before broad world reuse.

### Rounded foliage and forest floor — 23 November 2026

Tree v09 sources replace long pointed sprays with closed convex leaf lenses. Oak/birch leaf faces now overlap along the crown envelope rather than sticking outward as spines; pine sprays are slimmer and rounder. Each tree uses three foliage shades. Combined tree triangle count is36% lower than the preceding sources, though it remains above the initial budget guide.

Ground grass and fern meshes use curved closed leaves and restrained per-instance tints. Small moss clumps grow around roots and fallen leaves break up the forest edge. The understory/floor remains seven nonblocking render batches; no resource identities, collisions, yields, save data or routes were changed. Daylight, torchlight and the second camera view were inspected with the existing soft-shadow settings.

This softens the previous cactus-like crowns and angular ground leaves. Remaining gaps include overly uniform leaf grouping, exposed supporting shapes at some angles, repetitive decorative trees, authored ground/root transitions and reference-level material richness. Keep using actual gameplay views and the approved image to judge the next iteration.

### Canopy grouping and ground materials — 23 November 2026

The next source iteration replaces continuous leaf shells with unequal overlapping oak lobes, smaller airy birch groups and descending pine bough pads. Leaf spacing, heading and size vary within each group; lower groups use deeper green and upper groups carry restrained highlights. Earlier v09 and intermediate v10 art remain preserved. These are dimensional closed meshes with the same metric envelope and existing trunk colliders.

The ground now has broad smooth olive/ochre fields, irregular turf fingers, pale worn routes through the camp, darker root soil and fine low-contrast aggregate. Lower, broader ferns soften the edge. A review rejected visible lattice-like ground patches and overly orderly leaf placement; subsequent artwork removes the lattice field and varies the leaves. These are surface treatments, not new paths, terrain collision or gathering rules.

Remaining art work includes more naturally interleaved birch branches, species-specific leaf sprays, less repetition among perimeter trees, richer soil/root integration and authored tree LODs. The approved reference still has more convincing sculpted foliage, character expressions and material depth. This iteration is for user review, not a claim that the target is achieved.

### Pine and birch species refinement — 23 November 2026

Birch v13 replaces the separate rounded shells with smaller tapered leaves along connected, hanging twig sprays. Overlapping sprays break up the former ball-shaped groups while retaining gaps through the fine branching. Pine v14 replaces individual oval leaves with closed scalloped bough surfaces, recessed inner foliage fans and narrower drooping outer sprays. The silhouettes are evaluated at gameplay distance as well as in the close view.

The review rejected an initially sparse birch and broad leaf-like pine pads. The delivered iteration adds birch overlap and finer pine tips with connected inner boughs. Source/export revisions remain preserved. Both retain their metric envelopes, pivots, existing colliders and final-hit wood rewards. No save or gameplay changes.

The reference remains fuller and more naturally sculpted: pine tier regularity and trunk exposure need more refinement, while birch still has a rather regular twig pattern. Geometry is above the original tree guide and requires authored LODs before broader reuse. These are remaining art tasks, not visual acceptance.

### Scene-wide audit and irregular pine — 23 November 2026

See [the visual parity plan](VISUAL-PARITY-PLAN.md) for the current scene audit,
rendering experiments, lightmap/GI strategy and remaining production order.
Pine v15 uses staggered interlocking boughs rather than horizontal rings. Default
orthographic framing is closer at size10 with the original fixed39.8° pitch.
Directional sky fill preserves shadow contrast and follows evening in both
diffuse and reflected energy. Surface grain preserves authored PBR values.

The largest gaps remain forest composition, integrated ground/root surfaces,
authored texture/normal/roughness maps and character sculpt/expression. Dynamic
lighting cannot create missing forms. This pass is not visual acceptance.

### Forest composition — 24 November 2026

Twenty-two decorative tree instances form unequal overlapping foreground and
background groups instead of an eleven-tree necklace. Species, size, proportions,
rotation and depth tint vary deliberately. Twelve gatherable woodland trees now
reuse authored oak/pine/birch art within their existing resource envelopes,
replacing the visible preview cones/balls. Their state and harvesting stay intact.

The open camp reads more clearly against the shaded forest edge. The same three
species sources still repeat, and some existing crowns obscure the player near
shore/mine viewpoints. Treat canopy occlusion/cutaway as required presentation
work. Material depth, authored surfaces, character forms and LODs remain major
gaps. Native day/torch/alternate and route views are in work/forest-composition-qa/.

### Canopy visibility and surfaces — 24 November 2026

Foreground tree foliage now opens a narrow feathered cutaway around Simm's
projected body, while bark stays solid and shadow-map geometry is retained.
This addresses the mine/shore canopy obstruction observed in the previous pass.
Five shared seamless maps add wood/endgrain, canvas weave, stone mineral and
soil aggregate variation, roughness and shallow height relief. Light is dynamic;
no shadow or reference image is baked into these maps. Actual Godot renders are
in work/canopy-materials-qa/. Dedicated prop UV/wear authoring, sculpted forms and
character expression remain below the reference and require further work.

### Simm key-shot iteration — 24 November 2026

Simm v07 has a connected wider cheek/jaw shape, shallow eye contours/lids and
larger uneven swept hair groups. A slightly raised face plane helps his eyes
read from above. The same17bone rig, socket and all animation curves remain.
The isolated shot study now has recalibrated framing and prop proportions;
its layout is not a migration of the saved camp. Sculptural integration and
close-up facial/cloth/hair refinement remain, as detailed in KEY-SHOT-PARITY.md.

### NPC and groundcover iteration — 24 November 2026

NPC v09 preserves both original rigs/actions/sockets while revising connected
faces, shallow eye/lid shapes, swept Leina fringe and clothing proportions.
Standard textured PBR clothing retains the approved palette; a white-clothing
export defect was found by native review and corrected before delivery.
Turf blades and ferns are lower, flowers smaller and grouped in white/yellow.
The wider2.2degree sun penumbra is preferred in the matched stage. SDFGI was
actually rendered and compared but left out of gameplay after excessive dark
background occlusion. Details and measured frame-cadence limits are in
KEY-SHOT-PARITY.md. More expensive rendering is not itself an art improvement.
