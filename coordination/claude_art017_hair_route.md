# ART-017 hair construction route R2: authored layered wedges (Fable, 27 Nov 2026, run 47; answers Codex `c4b8394`)

Proposal only: no sculpt, no export, no new head. Held v012 and the fitted assembly stay the control. The sketch is at
`art_source/handoff/claude_production/ART-005/hair_route_r2/r2_silhouette_flow_sketch.png`. It has three panels: the
unaltered reference crop, an analytical sketch on a copy, and the construction schematic.

## What I looked at

- Codex's native B1 rejection (`reviews/b1-native-two-view.png`) and held v012 at both views.
- The full approved reference, read with `git cat-file`, not copied into my branch.
- My own B1 overlay.
- Not looked at: Godot itself. The reference is a blurred, sunlit 120-pixel head with an unknown camera, so the sketch
  is a reading of shapes and directions, not measurements. The back and Simm's left side are mostly invented.

## Why both earlier routes failed

| Route | Construction | What it produced natively |
|---|---|---|
| v012 | Swept locks placed radially by a crown map, flat or round sections, all fused by a voxel remesh | Flat blade tops with paper edges; a wide radial cap; per-lock edits could not change the read |
| B1 | Metaball chains, balls tapering along curves, fused by the field | Inflated lobes; the crown read as horns, the fringe as dangling lobes, the sides as a helmet wall |

Both let an automatic process decide the shape: radial placement plus voxel fusion, or metaball fields. Neither had
control over the cross-section. A flat section gives blades and a round one gives tubes. Global fusion rounds every root
and every gap, which is where the helmet comes from.

## The reference, read as construction (sketch, middle panel)

1. **Envelope:** compact and rounded; above it only a few SHORT flicks, not tall spikes.
2. **Crown whorl:** upper back, slightly toward Simm's left. The main pieces flow AWAY from it: forward and down over
   the forehead, down over Simm's right side, down and out on Simm's left.
3. **Short flicks:** two or three, pointing up and back at the crown.
4. **Forehead opening:** skin shows between the fringe tips. The fringe is a few thick pieces ending in points, sweeping
   toward Simm's right, not a straight edge.
5. **Side mass:** heavier on Simm's right, covering the temple and ending above a visible ear. Simm's left is shorter
   and flares out.
6. **Pieces:** thick at the root, a visible ridge, soft edges, and a quick taper to a point. Each overlaps the one
   behind it, so the breaks come from layering and occlusion, not grooves.

## The route: R2 authored layered wedges

1. **Scalp envelope shell.** One continuous closed surface authored from three profile curves (front, side, top) to the
   compact outline in the sketch. It is never seen on its own, because the wedges cover it. It sets the overall
   silhouette and hides the scalp in the gaps between pieces, so the outline can't swell into horns or a helmet.
2. **Wedges on authored guides.** Each piece is one guide curve placed by hand from the whorl, not by an automatic
   radial rule. A wedge is swept along its guide with:
   - **Cross-section:** a ridged lens (convex top with a ridge, flatter underside), depth to width about 0.35 to 0.6.
     That is between v012's blade and B1's tube.
   - **Width w(t):** widest in the first third, then a fast taper to a point.
   - **Depth d(t):** thickest at the root, thinning steadily to the tip. No bulb, no paper edge.
   - **Twist and curl:** per guide, small, authored.
3. **Layer order and root overlap** (schematic, bottom right). Under-layer (back, nape, behind the ears), then side
   masses, then the fringe sweep, then the crown flicks last. Every root is buried under the layer above it.
   - Pieces stay separate overlapping meshes, at most fused locally at their roots. No global voxel remesh.
   - The layering gives the natural dark breaks between pieces; there is nothing to inflate.
4. **Count follows the sketch, not a target.** As many wedges as the silhouette and flow need: roughly the six
   annotated directions, each split where the reference shows a break. If a wedge doesn't change the silhouette or a
   visible break in one of the two views, it isn't made.
5. **Hidden side:** the back and Simm's left continue the flow from the same whorl, with different shapes from the right
   (not mirrored), and are marked invented in every sheet.

**What I can reuse:** `hairkit.py`'s sweep machinery (guide curves, profiles, roll) can drive the wedges with a new lens
section and the w(t) and d(t) profiles. The radial placement, the crown map and the voxel fusion are dropped. Eyes, face,
neck, rig and actions are untouched; the B1 eye openings are NOT carried over (Codex: hypothesis only).

## What will visibly differ in BOTH native views

- **Ref view:**
  - a compact, rounded top with only short flicks;
  - a fringe of a few thick, pointed pieces sweeping toward Simm's right, with forehead showing between them;
  - a heavier right side ending above the ear.
- **Alt view:** no smooth side wall. The side reads as stacked overlapping pieces with dark breaks, and flows down and
  back from the crown; the crown shows two or three short flicks, not horns.
- **Both:** each piece has a ridge and a soft edge in clay. No flat blade tops (v012) and no tube lobes (B1).

## Early rejection gate (before any detail)

Stage A is clay only: the envelope shell plus the six largest wedges (fringe sweep, right side mass, left side, back
and nape, two crown flicks). It is compared natively at both agreed views with held v012, under the same lights and
clay.

Reject R2 and stop if ANY of these holds:
1. Anything rises above the reference envelope in the eye-aligned ref overlay. That is the horn failure.
2. The fringe ends as hanging lobes below the reference fringe line instead of pointed tips with forehead between them.
3. The alt view still reads as one smooth helmet side with no layer breaks.
4. Codex and Fable can't say the whole head is visibly closer to the reference than v012 at normal review scale, in
   both views.

Only if Stage A passes: the remaining wedges, then the m001-style material through new UVs, as a separate step.

## Stop rule for the route

- One Stage A pass, then a native review.
- If it fails, I do not iterate wedge parameters. Then the honest conclusion is that procedural construction from the
  blurred reference has reached its limit. The next useful input is clearer reference for the hair: a front, side or
  back sketch, ideally from Mattias's own drawings, or a decision by the user on which hair read matters most. That
  becomes a question for the user at A1, not another construction cycle.
