# ART-004 proposal: Simm body, hood and clothes

Written by Claude (Fable), 25 November 2026, 22:10 UTC. A proposal only. No body mesh was made or changed.
Codex cleared a proposal at `1f7d6a8`; mesh work waits for the ART-003 fit study.

## 1. What this is based on

Looked at directly:

- The frozen `PROTECTED_BODY` in the starter file, read-only (numbers below are measured from it).
- The approved reference, full size, Simm's figure crop.
- A Blender clay render of the frozen body with head v007:
  `art_source/handoff/claude_production/ART-004/frozen_body_with_v007_head_clay.png`.

Not seen: the body in Godot, in motion, or with its textures. `cloth_tone.png` and `leather_tone.png` point to
`D:/SimmInTheWild/godot/assets/textures/...` and are not in Git, so Claude has only the materials' flat colours.
Everything about deformation below is expectation, not observation. ART-003 is the evidence.

## 2. The frozen body as measured

| Fact | Value |
|---|---|
| Mesh | 7,444 vertices, 14,144 triangles, no quads, no shape keys, two UV maps (`UVMap`, `SurfaceUV`) |
| Structure | 89 separate mesh islands; the largest is 1,258 vertices |
| Bounds (Blender axes) | X -0.300 to 0.300, Y -0.185 to 0.251, Z 0.000 to 0.991 |
| Skinning | 15 vertex groups in use, at most 2 bones per vertex, mean 1.17. The `head` group has no body vertices |
| Materials | 20 slots, 14 used. Six head-related slots are unused leftovers |
| Biggest material groups | jacket 4,136 triangles; seam binding 3,528; boot leather 1,160; trousers 1,080; skin 752; soles 744; fasteners 704 |
| Collar zone | 529 vertices above Z 0.955, radius 0.056 to 0.217 m, hood material only 320 triangles at Z 0.96 to 0.98 |

Two things follow from the numbers. A quarter of the triangles (seam binding, 3,528) are piping and edge trim,
which is where the stiff, panelled look comes from. And the body is an assembly of rigid-looking parts with
almost no blended weights, so it bends at joints like boxes.

## 3. Where the frozen body differs from the reference

Reading of the picture, ranked by how much each shows at game distance.

1. **Neck and collar.** Reference: no neck visible. A large soft hood roll sits behind and beside the head, up to
   about ear-lobe height, and a pale scarf or collar fills the front. Frozen body: a flat collar ring at Z 0.96 to
   0.98 and about 4 cm of bare neck below the chin.
2. **Jacket volume.** Reference: one puffy rounded form, open at the front, sleeves like soft tubes, hem at about
   0.47 m above the floor. Frozen body: boxy torso with panels and straps, hem at about 0.58 m.
3. **Leg read.** Reference: only about a quarter of the figure's height is visible leg, because of the longer
   jacket and tall boots. Frozen body: about 40 percent. The skeleton's leg length cannot change, so the fix is
   the hem and the boots, not the bones.
4. **Boots.** Reference: tall, very chunky, soft fold at the top, about 0.28 m high. Frozen body: lower and slimmer.
5. **Hands.** Reference: small rounded fists. Frozen body: small and blocky. Minor.
6. **Backpack.** Reference: a soft rounded olive-brown pack on the back with one visible strap. Frozen body: boxy
   pack with hard flap, buckles and several straps.
7. **Surface.** Reference: matte, few seams. Frozen body: 14 materials, piping, fasteners.

Known limit that this ticket cannot fix: with head v007 the figure is about 3.4 heads tall; the reference is
about 3. The skeleton and the head size are both held. If that ratio matters, it is a head-scale decision for the
A1 checkpoint, not a body edit.

## 4. Three ways to do it

| | Method | What it can reach | Risk to the rig | Needs from Codex |
|---|---|---|---|---|
| A | Reshape existing vertices only; delete trim islands | Rounder jacket, longer hem, bigger boots and hands. Still triangle soup, limited smoothness, small hood | None: surviving vertices keep their groups | Nothing beyond ART-003 |
| B | A, plus smooth subdivision before the armature, plus new parts bound to a single bone each | Everything in A, smooth forms, a real hood roll and scarf (bound 100 percent to `chest`), boot cuffs (100 percent to each `shin`) | Low: no weights are painted or transferred; new parts move rigidly with one bone | Agreement that single-bone parts are allowed; walk, idle and gather checked natively |
| C | New body mesh, weights transferred from the frozen body | Free topology and shape everywhere | Medium: transfer can smear weights at armpits and hips | An explicit ticket for weight transfer and full animation QA |

**Recommendation: B.** It fixes the two largest gaps (neck and jacket volume) without any weight painting,
and keeps the frozen skeleton, rest pose, actions and socket untouched by construction. C only if B cannot make
the sleeves and trousers read soft enough.

## 5. Proposed order of work once ART-003 reports

One bounded part per run, each delivered as a packet Codex can attach and test.

1. **Hood roll, scarf and collar.** Closes the neck. Checked against the hair at the nape: v007's nape tips
   reach about Z 1.03, and the hood roll would rise to about Z 1.06 behind the head, so they must nest, not cross.
2. **Jacket torso and sleeves.** Trim islands removed or absorbed, body inflated to one soft form, hem lowered.
3. **Boots and trousers.** Taller, chunkier boots with a soft cuff; trouser legs fuller.
4. **Hands.** Rounded fists, without moving the hand socket.
5. **Backpack and one strap pair.**
6. **Materials.** Down from 14 to about 5 (jacket, shirt and scarf, trousers, leather, skin), flat PBR, palette
   taken from the reference.

## 6. What ART-003 should tell us before any of this starts

These are the observations that would change the plan.

- How much neck shows from the gameplay camera, and from the reference camera.
- Whether a hem 10 cm lower would be crossed by the thighs in `walk` (hem vertices follow `hips`).
- Whether the head's nape hair and the collar already intersect in `idle`, `walk` or `gather`.
- Where the hand socket sits relative to the hand mesh, so larger fists do not swallow held tools.
- Whether the head reads too small or too large on this body at game scale (the 3.4 against 3 heads question).
- Frame cost of the current 14-material body, so the material reduction has a measured reason.

## 7. Inputs needed

- `cloth_tone.png` and `leather_tone.png` committed, or a decision that Claude authors replacements.
- Codex's answer on option B's single-bone parts.
- The ART-003 frames and notes.

## 8. Evidence each body packet would carry

As for the head: GLB and notes, five frames, sha256, a named part manifest that fails on missing parts, counts and
bounds from a re-imported GLB, and `verify_candidate.py` extended to prove that every surviving body vertex keeps
exactly its original groups and weights, that the skeleton, rest matrices, three actions and socket are unchanged,
and that each new part is bound to exactly one bone.
