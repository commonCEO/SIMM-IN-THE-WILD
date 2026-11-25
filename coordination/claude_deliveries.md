# Claude deliveries (character art)

Written by Claude only. Codex reads this file and writes its own file next to it.
Channel: this git repository. Claude cannot see `D:\SimmInTheWild`; it works in a cloud checkout.

## How to exchange

- Claude pushes to branch `claude/compassionate-maxwell-fagj20` and to no other branch.
- Codex pushes to `main` or to a branch of its own and names that branch here or in chat. Claude fetches it by name.
- Each side edits only its own file in `coordination/`, so pulls never conflict.
- Anything Claude must see has to be committed: it cannot read untracked files on the PC.

## Current delivery: head_candidate_v005

Status: delivered for Codex's Godot review. Hair only, and only the arc cluster on Simm's right. Face geometry and palette are v003's. Not a parity claim, not ready_for_user_review.
Made in answer to Codex's v005 brief at `bfeec78`.

| Path | Purpose |
|---|---|
| `art_source/handoff/claude_simm/inbox/head_candidate_v005.glb` | For Codex. 80,268 triangles, 5 materials, 3 textures, identity root. sha256 `fcab06a5ae8b6c1d06e875585d1c646a813ebe9b3ee0dea9302cc3486bf9336b` |
| `art_source/handoff/claude_simm/inbox/head_candidate_v005.blend` | Editable source, Blender 3.5.1. |
| `art_source/handoff/claude_simm/inbox/HEAD_CANDIDATE_V005_NOTES.md` | Counts, answer to each point of the brief, remaining issues. |
| `art_source/handoff/claude_simm/inbox/renders_v005/` | Clay and colour views including the alternate angle, reference comparison, fit check. |
| `art_source/handoff/claude_simm/inbox/textures_v005/` | Base-colour maps. The skin map is byte-identical to v003's. |

Facts for the Godot comparison:

- Bounds in Blender axes: X -0.251 to 0.231, Y -0.145 to 0.273, Z 0.936 to 1.450. Same attach rule and same camera (FOV 24).
- Only the right-side arc cluster of `SCULPT_HAIR` changed against v004. Everything else in the hair, and all non-hair meshes, are as v004.
- Frozen data verified unchanged again.

What changed: the cluster is built with a new rounded-volume lock construction. One broad inflated body (12.6 cm wide, 4 cm thick, blunt rounded end), two narrower tips of different length growing out of its end in different directions, one shorter rear lock. No ridge, no parallel grooves, one shallow drifting channel on the body. Tip roots are buried in the body so joins are creases. The gate asked for was applied: two rounds of reference and alternate clay frames were judged before the full export; round one (a blob with two horns) was rejected and revised.

Open question for Codex: the hair is now built two ways, soft volume on Simm's right and v004 grooved straps elsewhere. If the cluster passes in Godot, Claude proposes applying the same construction to the fringe sweep and the left flicks in v006, then adding the short silhouette flicks from point 4 of the brief. If the cluster reads too puffy, say so first.

## Earlier delivery: head_candidate_v004 (kept, superseded by v005)

Status: superseded. Reviewed by Codex in Godot at `bfeec78`: changes requested, hair construction.
Made in answer to Codex's v004 brief at `59d7dc2` and the shadow follow-up at `c527d31`.

| Path | Purpose |
|---|---|
| `art_source/handoff/claude_simm/inbox/head_candidate_v004.glb` | For Codex. 80,264 triangles, 5 materials, 3 textures, identity root. sha256 `e459263e21c9d72eb309930e44d5a63d0aa1603f88720830fc9675972ca70011` |
| `art_source/handoff/claude_simm/inbox/head_candidate_v004.blend` | Editable source, Blender 3.5.1. |
| `art_source/handoff/claude_simm/inbox/HEAD_CANDIDATE_V004_NOTES.md` | Counts, answer to each point of the brief, remaining issues. |
| `art_source/handoff/claude_simm/inbox/renders_v004/` | Clay and colour views, reference comparison, fit check. |
| `art_source/handoff/claude_simm/inbox/textures_v004/` | Base-colour maps. The skin map is byte-identical to v003's. |

Facts for the Godot comparison:

- Bounds in Blender axes: X -0.255 to 0.231, Y -0.145 to 0.273, Z 0.936 to 1.450. Same attach rule and same camera (FOV 24).
- `SCULPT_HEAD`, eyes, brows and lashes are the same as v003. Only `SCULPT_HAIR` changed.
- Frozen data verified unchanged again.

What changed: the big arc is three overlapping curved locks with different roots, depths and tip directions; the tuft is taller and thinner with a companion strand; the two flicks on Simm's left are unequal; one rising lock added on the front top; fringe keeps one main point, with a shorter rounded lock on one side and an offset side-swept lock on the other.

Note: `coordination/reviews/head-v003-warm.png` on Codex's branch does not decode (broken PNG chunk). The other frames are fine.

## Earlier delivery: head_candidate_v003 (kept, superseded by v004; face and palette baseline)

Status: superseded. Reviewed by Codex in Godot at `59d7dc2`: changes requested, face and palette to be held.
Made in answer to Codex's v002 review at `bfd7c72`.

| Path | Purpose |
|---|---|
| `art_source/handoff/claude_simm/inbox/head_candidate_v003.glb` | For Codex. 80,259 triangles, 5 materials, 3 textures, identity root. sha256 `6ad3103202b73c5e22a811e953312b3931328c73cdaa734d91ff248a24c92e8d` |
| `art_source/handoff/claude_simm/inbox/head_candidate_v003.blend` | Editable source, Blender 3.5.1. |
| `art_source/handoff/claude_simm/inbox/HEAD_CANDIDATE_V003_NOTES.md` | Counts, point-by-point answer to the v003 priorities, remaining issues. |
| `art_source/handoff/claude_simm/inbox/renders_v003/` | Clay and colour views, reference comparison, fit check. |
| `art_source/handoff/claude_simm/inbox/textures_v003/` | Base-colour maps, also embedded in the GLB. |

Facts for the Godot comparison:

- Bounds in Blender axes: X -0.259 to 0.238, Y -0.145 to 0.273, Z 0.936 to 1.434. Same attach rule: original `head` bone, no offset, no scale.
- Camera: same position and target as before, FOV 24 degrees as Codex suggested. Claude's Blender lens details are in the notes file.
- Frozen data verified unchanged again.

What changed, in short: cranium top 4 cm lower and thinner hair over the crown; hair rebuilt as five dominant locks plus subordinate locks and accents at different depths; one tapering tuft; arcing temple lock plus a short side flick instead of the straight panel; jaw angle filled; mouth crease and tint stronger; deeper skin and hair albedo; hair flecks removed; no cache files.

Where Claude expects Codex to still object: total hair volume is now smaller than the reference and may be overcorrected on top; the big arc lock reads as one large leaf from Simm's right; the tuft is too small; left flicks are modest.

Albedo question for Codex: skin and hair base colours were deepened because the v002 engine frames read pale and orange-tan. If the lower, warmer key test fixes that without albedo help, say so and Claude will stop moving albedo.

## Earlier delivery: head_candidate_v002 (kept, superseded by v003)

Status: superseded. Reviewed by Codex in Godot at `bfd7c72`: changes requested.
Built from the full `APPROVED_REFERENCE.png` and Codex's v001 Godot review.

| Path | Purpose |
|---|---|
| `art_source/handoff/claude_simm/inbox/head_candidate_v002.glb` | For Codex. Static head, identity root `SCULPT_HEAD_ROOT`, metres, Y-up, textures embedded. 80,253 triangles, 5 materials, 3 textures. No rig, animation, camera or lights. |
| `art_source/handoff/claude_simm/inbox/head_candidate_v002.blend` | Editable source, Blender 3.5.1. |
| `art_source/handoff/claude_simm/inbox/HEAD_CANDIDATE_V002_NOTES.md` | Counts, point-by-point answer to Codex's five priorities, remaining issues. |
| `art_source/handoff/claude_simm/inbox/renders_v002/` | Clay and colour views, comparison against the unaltered reference crop, fit check. |
| `art_source/handoff/claude_simm/inbox/textures_v002/` | Base-colour maps, also embedded in the GLB. |

Facts for the Godot comparison:

- Bounds in Blender axes: X -0.259 to 0.237, Y -0.144 to 0.276, Z 0.936 to 1.496. Front is -Y. Same attach rule as v001: original `head` bone, no offset, no scale.
- Hair is bigger than v001 on purpose (reference head with hair is about one third of the figure). Tuft tip is at Z 1.496, above the 1.42 guide. Say so if the framing disagrees.
- Frozen body, old head, 17 bone rest matrices, three actions and `hand_r_socket` verified unchanged again.
- Claude's reference-angle camera in Godot axes: target (0, 1.215, 0), position (-0.829, 1.659, 1.435), FOV about 18.6 degrees, square frame. A perspective render there would let both sides compare like for like.

What changed against Codex's priorities (detail in the notes file):

1. Hair: fewer, broader clumps; fringe parted over Simm's right eye and swept toward his left; heavy right temple mass; flicks on his left; one tall tuft; fringe-root pits closed.
2. Eyes: opening 35 x 53 mm (was 45 x 60), iris fills the opening, roughness 0.30, thin lid edge, no hard rim.
3. Forehead and jaw: fringe reaches the brows; chin rounded, jaw filled, cheeks halved.
4. Mouth and nose: rebuilt. The beak was an adult overbite in the base, now corrected. Closed 41 mm smile arc with a shallow crease. Nose is a single soft bump, no nostril pits.
5. Colour: warmer chestnut hair, slightly warmer skin. Albedo only.

Where Claude expects Codex to still object: the fringe edge is a row of similar teeth, the hair is tidier than the ragged reference, the tuft reads as a knot from the front with one pit at its root, and the mouth is closed where Codex read a subtle opening.

## Earlier delivery: head_candidate_v001 (kept, superseded by v002)

Status: superseded. Reviewed by Codex in Godot at `8ffedf9`: changes requested. Head, hair and eyes only. Not a parity claim.
First commit: `ae9c859` on `claude/compassionate-maxwell-fagj20`.

| Path | Purpose |
|---|---|
| `art_source/handoff/claude_simm/inbox/head_candidate_v001.glb` | For Codex. Static head, identity root `SCULPT_HEAD_ROOT`, metres, Y-up, textures embedded. 78,266 triangles, 5 materials, 3 textures. No rig, animation, camera or lights. |
| `art_source/handoff/claude_simm/inbox/head_candidate_v001.blend` | Editable source, Blender 3.5.1. Starter scene plus new `SCULPT_*` objects. |
| `art_source/handoff/claude_simm/inbox/HEAD_CANDIDATE_NOTES.md` | Counts, base source, invented areas, full list of likeness issues. Read before importing. |
| `art_source/handoff/claude_simm/inbox/renders/` | Clay and colour views, reference comparison, fit check on the frozen body. |
| `art_source/handoff/claude_simm/inbox/textures/` | Base-colour maps, also embedded in the GLB. |
| `art_source/handoff/claude_simm/inbox/build_scripts/` | Authoring scripts, renderer, exporter, `verify_candidate.py`. |

Facts Codex needs for the Godot comparison:

- Bounds in Blender axes: X -0.208 to 0.237, Y -0.133 to 0.253, Z 0.936 to 1.469. Front is -Y.
- Geometry is in world position for the frozen actor. Attach to the original `head` bone (head at Z 0.98) with no offset or scale.
- The neck runs down to Z 0.936 so it sits inside the collar.
- Frozen body, old head, 17 bone rest matrices, actions `gather`, `idle`, `walk` and `hand_r_socket` verified unchanged against the starter (sha256 `1157d3201b16be71e51323fcb7abfbeae78e5b3d388f1b35e417cbdfb52b9db4`).
- Triangle count is review density. Reduction and bake come after the shape is approved.

## Loop state

- Last Codex commit seen: `bfeec78` (native v004 review, v005 brief, repaired v003 warm image). Reference and protocol from `b143f31`.
- `coordination/START_HERE.txt` read. Claude follows it; nothing in it conflicts with the user's scope.
- Claude's recurring check: ACTIVE since 25 Nov 2026 18:06 UTC. The user typed the request directly in Claude's session.
  - ID: `trig_01RTVFoanSgc82QmxWinsxYg`, name "Simm art: check Codex git handoff".
  - Cadence: hourly at minute 6 (cron `6 * * * *`, UTC). 30 minutes was requested and refused by the platform: "the minimum interval is 1 hour".
  - Location: Anthropic cloud session `session_019rvqHFAG36h6kZmjmt6P4H`, same conversation and checkout each time. Model configured and last served: `claude-fable-5-2`.
  - Each run: fetch `codex/simm-art-handoff`; if the tip equals "Last Codex commit seen", stop with no commit; otherwise read the review and make one bounded head-only revision.
  - Receipt: first check run by hand at 18:06 UTC right after creation. It fetched `bfd7c72..c527d31` and found two new Codex commits (`59d7dc2`, `c527d31`). v004 was built in that same manual run.
  - Scheduled run 1 fired 19:06 UTC on time, unattended. It fetched `c527d31..bfeec78`, read the v004 review and built v005. So the schedule is confirmed working end to end.
  - No GitHub event trigger is set up. If Codex needs a faster turnaround than hourly, the user can prompt Claude's session.
- Claude treats Codex's notes as peer input. Scope stays: new `SCULPT_*` head objects only, files only under `art_source/handoff/claude_simm/inbox/` and `coordination/claude_*.md`.

## Method notes for Codex: Godot lighting and post for the comparison

Suggestions to test, not measured results. Property names are Godot 4 `Environment`, `DirectionalLight3D` and `BaseMaterial3D`.

Comparison camera (matches Claude's reference-angle render): target (0, 1.205, 0), position (-0.700, 1.676, 1.374) in Godot axes,
looking at the target, FOV about 18.6 degrees on a square frame. That is azimuth 27 degrees toward Simm's right, elevation 17 degrees, distance 1.61 m.

Stage 1, shape check (keep it plain so light cannot hide form):
- One `DirectionalLight3D`, neutral white, energy about 1.5, from upper camera-left, shadows on, `light_angular_distance` 2 to 3 for a soft edge.
- Sky or flat ambient at about 0.6 so shadows stay readable. No glow, no depth of field, no fog, no colour adjustment.
- Render a grey override material first, then base colour. Same camera for both.

Stage 2, reference look (warm sunlit diorama):
- Sun colour near (1.0, 0.93, 0.80), energy 1.8 to 2.2, elevation 40 to 50 degrees, from upper camera-left as in the reference.
- Directional shadow: 4 splits, max distance only as far as the clearing needs (25 to 40 m), so the fringe shadow on the forehead stays sharp enough to read.
- Fill: sky ambient slightly cool at 0.6 to 0.9, or a second shadowless directional at 0.2 to 0.3 from the opposite side. The reference has no black shadows.
- `tonemap_mode`: AgX or Filmic. ACES tends to push the yellow jacket and warm skin toward orange.
- `ssao_enabled` with a small radius for contact shadow under the fringe, chin and ears. `ssil_enabled` at low intensity if the skin looks cut off from the warm ground bounce.
- Glow last and low (intensity around 0.2 to 0.3), only after the shape is approved.
- Mild `adjustment_saturation` 1.05 to 1.10 if the frame looks washed after tone mapping.

Materials Codex can override in Godot (the GLB carries only base colour and roughness):
- Skin: `subsurf_scatter_enabled`, strength 0.15 to 0.25, skin mode on. This is the main thing that turns flat peach into the reference's soft figurine skin. Optional `rim_enabled` at about 0.15.
- Hair: roughness 0.5 is in the file. If the reference's broad soft highlights are missing, try a small rim before touching the texture.
- Eyes: roughness 0.14. They need something bright to reflect. Prefer sky reflections. If they look dead, a small catch light restricted to the eye meshes by light cull mask is better than painting a highlight.
- Brows and lashes: turn shadow casting off, they are 2 to 3 mm thick and will cause acne or stripes.
- Import the three base-colour maps as sRGB with mipmaps; use a high-quality or lossless mode for the skin map so the cheek gradient does not band.

Known things the engine render will expose: the neck is visible above the collar (the reference hides it with a hood and scarf), and the hair mass edge beside the ears is a clean line.

## Working files

Not committed, rebuilt from the scripts: `art_source/handoff/claude_simm/inbox/work/stage1.blend`, `stage2.blend`, `stage3.blend`.
`build_scripts/` now holds the v002 state; the exact v001 scripts are at commit `ae9c859`.
A byte-identical copy of the starter is committed at `art_source/handoff/claude_simm/inbox/starter_copy/START_HERE_v02.blend` so Claude can rebuild if its container is replaced. It sits inside `inbox/`, not at the starter's own path, so a pull cannot collide with the local copy on the PC.

## Blocked

Nothing on the art side. Reference and protocol arrived. Only the schedule above is open, and it needs the user.

## Next

Wait for Codex's Godot review of v005 (the hourly check picks it up). Face and palette stay frozen at v003.

## Meshy review (user asked both agents, 25 Nov 2026; user then said to skip it for now)

Claude's read, from vendor docs and published reviews. Nothing was generated and the reference was not uploaded anywhere.

- Meshy does not replace Blender. It replaces the first hours of blocking in a shape. Its output still has to be opened in Blender, cleaned, split and attached to the frozen head bone.
- Current model is Meshy 7 (August 2026), with a 7.1 listed in the API changelog. Vendor claims better image-to-3D alignment; independent testing of version 7 on faces and hair is thin.
- Known weak spots in reviews of version 6: thin hair merges into ribbons, faces can go wrong, topology is not production ready, no facial rig. Output is one fused lump: no separate eyeballs, no fitted lids, no lip seam.
- Our input is the real limit: one view, head about 145 px. A generator will invent the same hidden sides Claude invented, with less control.
- Where it could win: overall hair volume and airiness, which is v001's weakest area.
- Cost and rights: about 20 to 25 credits per generation. Downloading version 7 models needs a paid plan (Pro listed at 20 USD per month). Free-plan output is CC BY 4.0, paid plans own the output. Plan names differ between Meshy's own pages, so check the live pricing page.
- Proposed bounded trial, only if the user selects it: one paid month, at most 4 generations (full-figure crop and head crop, with and without a cleaned front view), judged clay against clay beside Claude's current version at the same camera. Keep Meshy geometry only where its silhouette is visibly closer. Most likely outcome is a hybrid: Meshy as hair volume reference or base, Claude's head with real lids and separate eyes.
- Needs from the user before anyone runs it: explicit go-ahead to upload the reference to Meshy, and which account pays.
