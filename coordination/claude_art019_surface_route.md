# ART-019 authored surface route R3: connected hair cages (Fable, 27 Nov 2026, run 49; answers Codex `fd3a745`)

Proposal and capability report only. No sculpt or export of a head. The method evidence sheet is at
`art_source/handoff/claude_production/ART-005/surface_route_r3/r3_mass_method_evidence.png`. Held v012 stays the
control; A1 is unpassed.

## Short answer

- The route Codex describes can be represented and edited in the Blender I have: a connected low-resolution cage per
  hair mass, hand-edited loops, local thickness, creased grooves, tucked secondary tips and subdivision.
- I can NOT author it to the needed quality here. The container has no 3D viewport, so brush sculpting fails, and
  every shape is placed by coordinates from a script and judged afterwards from a render. That is the same blind
  placement that sank R2.
- In the evidence sheet, three passes on ONE abstract mass gave a thin drape, then thick drips, then pointed drips with
  grooves. Never hair.
- I recommend the user choose who sculpts the hair (options below) before anyone builds R3. I am not proposing another
  scripted build.

## What I looked at

- Codex's native rejection (`reviews/r2a-native-two-view.png`) and the 18:31 receipt.
- My Stage A source and sheets, and the reference as read for ART-017 and ART-018.
- A capability test in this container (`surface_route_r3/r3_capability_check.py`) and the abstract mass demo
  (`r3_mass_diagram.py`, `r3_sheet.py`).
- Not looked at: Godot, the PC, or any other Blender than 3.5.1 headless.

## Why R2 failed (agreeing with Codex)

- Every visible piece came from the same section and taper family, so the hair read as repeated leaves. Moving the
  guides would not change that.
- The under-surface showed as a smooth band at the hairline.
- The crown tuft stood alone, like an antenna.
- The deeper cause is that the shapes were placed by numbers without seeing them. The B1 and v012 constructions had the
  same weakness.

## The route, as specified

**Representation.** Five masses, each one closed quad cage of about 150 to 400 vertices, kept in a .blend as editable
meshes:
- the back and nape;
- Simm's right side, the heavier one;
- Simm's left side;
- the top and crown;
- the fringe.

Each cage has named loops: a root loop, groove loops and tip loops. The only smoothing is a Subdivision Surface modifier
(level 2 in the viewport, 3 for review) with edge creases. No voxel remesh, metaballs or fusion.

**Mass to tips** (shown on one mass in the sheet):
- **Volume.** At the root the section is D-shaped: flat against the skull and domed outward, 15 to 25 mm thick.
- **Grooves.** Creased valley loops with local thinning run from each notch up into the mass. They split its lower
  part into 2 to 4 UNEQUAL tips that share the mass's topology, so there is no separate root and no root bulb.
- **Tucked tips.** Secondary tips are separate small cages with their roots buried inside the mass's volume. The overlap
  gives each one its own shadow edge.
- **Tips.** The tips should turn triangular with a creased ridge. In my demo they turned round (see the 48 mm section),
  which is the tube failure.

**Assembly:**
- Masses overlap in layers: back, then sides, then top, then fringe, then crown tufts.
- Each root loop tucks under the mass above it, so no scalp shell is needed and there is no band.
- The crown is two or three unequal tufts growing from the top mass, not one isolated piece.

**Blender operations:**
- vertex and loop placement (bmesh);
- local "grab" offsets with a smooth falloff, which is what a grab brush does;
- lattices for bending a whole mass;
- one shape key per edit pass, so every change stays reversible;
- edge creases and subdivision;
- multires only for a final detail pass, if one is ever approved.

**Inspection:**
- clay renders at the agreed ref and alt views plus front, back and top;
- the eye-aligned silhouette against the reference envelope with its uncertainty band;
- cross-sections at fixed heights through each mass (root, mid, tip);
- a per-mass checklist: no flat leaf, no tube, no root bulb, no visible band, tips unequal.

## Capability, plainly

| Operation in this container | Result |
|---|---|
| Sculpt brush stroke (`bpy.ops.sculpt.brush_stroke`) | FAILS: needs a 3D viewport, which headless Blender does not have |
| Sculpt mesh filter | Runs but does nothing (no effect without a viewport) |
| Cage editing by coordinates and loops, creases, subdivision, multires subdivide, shape keys, hooks, lattices | Work |
| Renders, silhouette masks, cross-sections | Work, about 1 to 2 minutes per look |

The tools are not the bottleneck. The bottleneck is authoring by numbers without seeing the shape while placing it.
The sheet shows the result: a correct structure (one volume, unequal tips, grooves, a buried tucked tip) that still
reads as wax, not hair. I expect a full head built this way would be a fourth rejected variant. I will not claim
otherwise, and I am not offering another script as the answer.

## What would work: a decision for the user

These need the user's choice. Fable has not started any of them.

1. **A person sculpts the hair in interactive Blender** (Mattias, or a hired 3D artist), on the held v012 head.
   - Fable prepares the start file: head, rough mass cages, the two agreed cameras, the reference as a local camera
     background (not uploaded anywhere) and the checklist above.
   - Fable then runs QA, sections, export and the provenance record; Codex runs the native gate.
   - This is the most reliable route to the concept's cute, tousled read.
2. **Claude edits the cages in Blender on the user's own computer through computer use.**
   - This gives live viewport feedback and real brushes.
   - It is slow and imprecise with a mouse driven by screenshots, so quality is uncertain. It is a cheap test, not a
     promise.
3. **A licensed stylised hair asset, or a paid generator, adapted to the head.**
   - This needs the user's explicit approval for purchase or generation, and a licence check.
   - The earlier Meshy review was set aside by the user.

Codex is right that the visible silhouette already differs strongly. More reference of the hidden side is NOT the
blocker and is not asked for.

## Stop rule

No R3 build, sculpt or export until Codex has reviewed this and the user has chosen a route. If the user chooses 1 or
2, Fable's first deliverable is the start file and one mass, judged natively before any full head.
