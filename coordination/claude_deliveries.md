# Claude deliveries (character art)

Written by Claude only. Codex reads this file and writes its own file next to it.
Channel: this git repository. Claude cannot see `D:\SimmInTheWild`; it works in a cloud checkout.

## How to exchange

- Claude pushes to branch `claude/compassionate-maxwell-fagj20` and to no other branch.
- Codex pushes to `main` or to a branch of its own and names that branch here or in chat. Claude fetches it by name.
- Each side edits only its own file in `coordination/`, so pulls never conflict.
- Anything Claude must see has to be committed: it cannot read untracked files on the PC.

## Production plan

Acknowledged at Codex commit `a403661`. Fable's ticket updates, plan corrections and proposals are in
`coordination/claude_production.md`. The first pass of the ART-006 art audit is in `coordination/claude_art_audit.md`.

## Current delivery: head_candidate_v007 (board ticket ART-001)

Status: reviewed by Codex in Godot at `1f7d6a8` and frozen as the candidate for the full-body fit study (ART-003). Not art approval, not ready_for_user_review. Head work is on hold until that study reports. Hair only against v006; face geometry, palette, skull and tuft held.
Made in answer to Codex's v007 brief at `7ef4a5e`.

| Path | Purpose |
|---|---|
| `art_source/handoff/claude_simm/inbox/head_candidate_v007.glb` | For Codex. 80,265 triangles, 5 materials, 3 textures, identity root. sha256 `9a296dd846e3fba327f6270cc41c9f25c4864a513b2436218cd39e754d6328d9` |
| `art_source/handoff/claude_simm/inbox/head_candidate_v007.blend` | Editable source, Blender 3.5.1. |
| `art_source/handoff/claude_simm/inbox/HEAD_CANDIDATE_V007_NOTES.md` | Counts, answer to each point of the brief, the v006 correction, remaining issues. |
| `art_source/handoff/claude_simm/inbox/renders_v007/` | Clay and colour views at both agreed cameras, reference comparison, fit check. |
| `art_source/handoff/claude_simm/inbox/textures_v007/` | Base-colour maps. The skin map is byte-identical to v003's. |

Facts for the Godot comparison:

- Bounds in Blender axes: X -0.251 to 0.225, Y -0.134 to 0.274, Z 0.936 to 1.444. Same attach rule, same two cameras.
- Non-hair meshes are as v003. Frozen data verified unchanged again.

What changed against v006: the forehead band is removed (front hairline raised above the fringe windows, under-layer flush with the skin at its edge, three short root locks growing out over it); three broad locks got a second shorter, thinner ending in their last third (fringe sweep and far-left fringe lock on image-right, temple arc on image-left); those ends and one cluster tip are thinner in depth; back and nape use the volume construction.

Correction: v006 was delivered with two fringe locks missing (`S_fringe_left`, `S_fringe_under`) because of a patch bug on Claude's side. Both are restored in v007, and the build now checks the lock list.

## Earlier delivery: head_candidate_v006 (kept, superseded by v007)

Status: superseded. Reviewed by Codex in Godot at `7ef4a5e`: changes requested. Known defect found afterwards: two fringe locks were missing from this delivery (see v007 notes).
Made in answer to Codex's v006 brief at `8f0c2ee`.

| Path | Purpose |
|---|---|
| `art_source/handoff/claude_simm/inbox/head_candidate_v006.glb` | For Codex. 80,263 triangles, 5 materials, 3 textures, identity root. sha256 `5aa8b9bc752c554befe3be0b52358331544318208f90d5bc2c9c62f2969f5ceb` |
| `art_source/handoff/claude_simm/inbox/head_candidate_v006.blend` | Editable source, Blender 3.5.1. |
| `art_source/handoff/claude_simm/inbox/HEAD_CANDIDATE_V006_NOTES.md` | Counts, answer to each point of the brief, remaining issues. |
| `art_source/handoff/claude_simm/inbox/renders_v006/` | Clay and colour views at both agreed cameras, reference comparison, fit check. |
| `art_source/handoff/claude_simm/inbox/textures_v006/` | Base-colour maps. The skin map is byte-identical to v003's. |

Facts for the Godot comparison:

- Bounds in Blender axes: X -0.251 to 0.225, Y -0.141 to 0.272, Z 0.936 to 1.450. Same attach rule, same two cameras.
- Non-hair meshes are as v003. Frozen data verified unchanged again.

What changed against v005: cluster body 17.5 percent thinner with its root sunk into the crown flow, rear lump thinned and lowered; rounded-volume construction now on the temple arc, fringe point, fringe sweep, all left flicks and the subordinate fringe locks, each thinner than the cluster body and with its own taper start; no parallel grooves anywhere, replaced by one or two drifting shallow channels on the top and back masses; five short unequal silhouette flicks added (three on Simm's left, two low on his right).

Where Claude expects Codex to object: the hair may now be too smooth overall against the ragged reference; the under-layer band still shows at the hairline from the front; the new flicks are small.

## Earlier delivery: head_candidate_v005 (kept, superseded by v006)

Status: superseded. Reviewed by Codex in Godot at `8f0c2ee`: construction method accepted, changes requested.
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

- Last Codex commit seen: `bfd7ce4` (jacket v001 native review and the v002 brief at `367f484`; `bfd7ce4` is a crafting parity audit with no art). Collar v002 review and jacket brief were at `193b661`. Reference and protocol from `b143f31`.
- `coordination/START_HERE.txt` read. Claude follows it; nothing in it conflicts with the user's scope.
- Claude's recurring check: ACTIVE since 25 Nov 2026 18:06 UTC. The user typed the request directly in Claude's session.
  - ID: `trig_01RTVFoanSgc82QmxWinsxYg`, name "Simm art: check Codex git handoff".
  - Cadence: hourly at minute 6 (cron `6 * * * *`, UTC). 30 minutes was requested and refused by the platform: "the minimum interval is 1 hour".
  - Location: Anthropic cloud session `session_019rvqHFAG36h6kZmjmt6P4H`, same conversation and checkout each time. Model configured and last served: `claude-fable-5-2`.
  - Each run: fetch `codex/simm-art-handoff`; if the tip equals "Last Codex commit seen", stop with no commit; otherwise read the review and make one bounded head-only revision.
  - Receipt: first check run by hand at 18:06 UTC right after creation. It fetched `bfd7c72..c527d31` and found two new Codex commits (`59d7dc2`, `c527d31`). v004 was built in that same manual run.
  - Scheduled run 1 fired 19:06 UTC on time, unattended. It fetched `c527d31..bfeec78`, read the v004 review and built v005. So the schedule is confirmed working end to end.
  - Scheduled run 2 fired 20:06 UTC on time, unattended. It fetched `bfeec78..8f0c2ee`, read the v005 review and built v006.
  - About 20:45 UTC the user prompted the session with Codex's plan announcement. In that prompted turn Claude consumed `8f0c2ee..a403661`, built v007, acknowledged the plan and wrote the first ART-006 pass.
  - Scope of the stored check: still head-only. Claude's attempt to widen it to Fable's board tickets was refused by the permission layer and was not worked around. Until the user widens it directly, unattended runs do ART-001 only.
  - Scheduled run 3 fired 21:06 UTC on time, unattended. It fetched `a403661..1f7d6a8` and read the ART-002 receipt. Codex asked for no v008, so nothing was rebuilt, rendered or exported. Only this receipt was committed.
  - 21:07 UTC: the user typed the request directly and the stored check was widened. It is now named "SIMM art: follow Fable tickets on the production board", same ID, same hourly cadence at minute 6 UTC. Each run does one thing: a revision Codex has just asked for, else the highest-priority Fable ticket that is not waiting on Codex, else a proposal Codex has cleared. Fences are unchanged (Fable's files only, board gates respected, no generators, no force-push). The earlier "head-only" limitation no longer applies. Next run 22:06 UTC; with the head on hold it should pick up the ART-004 proposal.
  - Scheduled run 4 fired 22:06 UTC on time, unattended, under the widened instructions. It fetched `1f7d6a8..757c52d` (no art feedback), found the head on hold and ART-006 blocked, and took the cleared proposal: `coordination/claude_art004_proposal.md`. No mesh was made or changed.
  - Scheduled run 5 fired 23:06 UTC on time, unattended. It fetched `757c52d..98c1777`, read the ART-003 fit study and the scoped collar assignment, and delivered ART-004's first packet (hood roll and scarf v001). ART-006's re-rank was left for the next run: one ticket per run.
  - Scheduled run 6 fired 00:06 UTC on 26 Nov, on time, unattended. It fetched `98c1777..fad6b7a`, read the collar v001 review (changes requested) and delivered collar packet v002. ART-006's re-rank is still next: one ticket per run.
  - Scheduled run 7 fired 01:06 UTC on 26 Nov, on time, unattended. It fetched `fad6b7a..e5e7105`, read the collar v002 review (held as working baseline) and the jacket brief, committed the collar v002 `.blend`, and delivered jacket candidate v001. ART-006's re-rank was displaced again by a fresh P0 revision request.
  - Scheduled run 8 fired 02:06 UTC on 26 Nov, on time, unattended. Codex's tip was unchanged at `e5e7105`, so no revision was waiting. The run took ART-006: the audit was re-ranked from the three native clearing frames. No mesh, render or export.
  - Scheduled runs 9 to 12 (03:06 to 06:06 UTC, 26 Nov) fired on time and found Codex's tip unchanged at `e5e7105`. Nothing was rebuilt or committed.
  - Scheduled run 13 fired 07:06 UTC on time, unattended. It fetched `e5e7105..bfd7ce4`, read the jacket v001 native review (changes requested, six-point brief) and delivered jacket candidate v002.
  - About 07:30 UTC the user reviewed a native side view ("IMO we're still 30% off") and then typed "Yes, this needs to have full parity, for Mattias to be happy", approving reopening the collar and the hair, which Codex had on hold. Collar v003 was delivered in that prompted turn.
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

- ART-004: collar v003 delivered (user-approved reopen), see below. Jacket candidate v002 is still waiting for Codex's study. The two have not been combined yet.
- ART-001: reopened by the user. Head v008 is next: hair back and nape down to meet the hood, softer, lighter tips, less gloss.
- ART-006: second pass in REVIEW; proposals gated by A1.

## ART-004 collar packet v003: standing hood around the neck (current, user-approved reopen)

Status: delivered for Codex's native test. Not a parity claim, not ready_for_user_review.

| Path | Purpose |
|---|---|
| `art_source/handoff/claude_production/ART-004/collar_packet_v003.glb` | For Codex. Same two named parts, same root, same `chest` binding and attachment as v002. 12,998 triangles. sha256 `f233e2693f5060e234f4741f62c0acad0f9855298b78379ee540f46c96878961`. |
| `art_source/handoff/claude_production/ART-004/COLLAR_PACKET_V003_NOTES.md` | Why, what changed, clearances, known issues. |
| `art_source/handoff/claude_production/ART-004/renders/collar_v003_*.png` | The user's native frame next to v003; colour and clay views. |

Facts for the native test:

- v002 left about 9 cm of bare neck at the sides, 44 mm at the back and 30 mm at the throat. v003 stands up round the neck to just under the jaw and the hair line, 11 mm off the skin, and the scarf is raised to fill the throat.
- 39 sampled poses: nearest approach 9.5 mm to the jaw, 7.6 mm to the nape, 2.8 mm to a hair tip (all in gather). No pack contact.
- Please test it with jacket candidate v002, not the original jacket.

## ART-004 jacket candidate v002: torso, sleeves and soft trim (waiting for Codex)

Status: delivered for Codex's in-memory native study, in answer to the six-point brief at `367f484`. Not a parity claim, not ready_for_user_review, not for playable integration.

| Path | Purpose |
|---|---|
| `art_source/handoff/claude_production/ART-004/jacket_candidate_v002.glb` | For Codex. Skinned `SCULPT_JACKET` and `SCULPT_JACKET_TRIM` on a rest copy of the 17-bone skeleton, no animation. 7,376 triangles, 2 flat materials. sha256 `c985517f0f8519e8f4e56d599a8ef99dd25bf6eb39c96ecb0ef8d67e314f2e61`. |
| `art_source/handoff/claude_production/ART-004/jacket_candidate_v002_vertex_map.json` | Per part: original vertex index, original position, candidate position. |
| `art_source/handoff/claude_production/ART-004/JACKET_CANDIDATE_V002_NOTES.md` | The six points answered one by one, manifest, preservation report, clip measurements, known issues. |
| `art_source/handoff/claude_production/ART-004/renders/jacket_v002_*.png` | Before and after in the three clips with side views, and at rest; clay and colour at both agreed camera directions. |
| `art_source/handoff/claude_production/ART-004/build_scripts/jacket_hand_sweep.py` and `.json` | New read-only measurement of where the hands and thighs travel in the clips, and its data. |

Facts for the native study:

- Replace, in memory, exactly as for v001: hide body materials `Simm golden canvas jacket.001` and `Simm golden seam binding.001`, add the two parts on the live skeleton. The frozen button stays; it is now seated on the front roll.
- Every vertex of both parts is an original vertex moved, with its original weights. The trim is the original placket strips and cuff rings reshaped: front rolls 100 percent `spine`, cuff rolls 100 percent forearm.
- All 5,606 vertices in the GLB are matched to source vertices within 20 micrometres, 0 unmatched, weights identical. The run fails otherwise.
- Blender clip samples: 0 jacket or trim vertices in a hand in idle, walk and gather. No thigh through the hem in my walk frames.
- The hem is not lowered. It now has a side vent of up to 80 mm at each hip, because thigh and hand leave under 6 mm of room there. This is the main thing to judge natively.
- Correction to my v001 notes: the leading thigh did come through the v001 hem in walk. I missed it in the small clay frames.
- Body, old head, rig, socket and actions verified unchanged.

## ART-004 jacket candidate v001: torso and sleeves only (reviewed by Codex, changes requested, superseded by v002)

Status: delivered for Codex's in-memory native study, in answer to the brief at `193b661`. Not a parity claim, not ready_for_user_review, not for playable integration.

| Path | Purpose |
|---|---|
| `art_source/handoff/claude_production/ART-004/jacket_candidate_v001.glb` | For Codex. Skinned `SCULPT_JACKET` on a rest copy of the 17-bone skeleton, no animation. 4,136 triangles, 1 flat material. sha256 `1ecc5240f497a55f5f7133048cb9f484582318cdae269e3305f420ce317bddcc`. |
| `art_source/handoff/claude_production/ART-004/jacket_candidate_v001_vertex_map.json` | Alternative: original vertex index, original position, candidate position for all 2,074 vertices. |
| `art_source/handoff/claude_production/ART-004/JACKET_CANDIDATE_V001_NOTES.md` | What to replace in the study, manifest, preservation report, clip measurements, known issues. |
| `art_source/handoff/claude_production/ART-004/renders/jacket_v001_*.png` | Before and after at rest and in the three clips; clay and colour at both agreed camera directions. |
| `art_source/handoff/claude_production/ART-004/collar_packet_v002.blend` | The editable collar v002 baseline Codex asked for. sha256 `832a4bb8f686a7e09777cf52ffc1836384c3607009978810e4fe7b64d4c642d5`. |

Facts for the native study:

- Replace, in memory: hide body materials `Simm golden canvas jacket.001` and `Simm golden seam binding.001`, add `SCULPT_JACKET` on the live skeleton. Nothing else changes.
- The candidate is the original 2,074 jacket vertices moved: same connectivity, same groups, every weight identical, asserted by the export script. No auto-rig, transfer or painting.
- Shape: rounded torso with a belly, shoulders sloped outside the straps, hem 37 mm lower (Z 0.545), round fuller sleeves with a gathered cuff. All seam binding is left out.
- Blender clip samples: no added thigh crossings; 10 vertices pass up to 8.2 mm into a hand in `gather` (new).
- Known: straps sit up to 14.5 mm above the new surface; one frozen brass button has lost the placket behind it; hem still far from 0.47 to 0.50; old topology limits roundness.
- Body, old head, rig, socket and actions verified unchanged.

## ART-004 collar packet v002 (held by Codex as working baseline; superseded by v003 at the user's request)

Status: delivered for Codex's native test, in answer to the review at `65387e5`. Not a parity claim, not ready_for_user_review.

| Path | Purpose |
|---|---|
| `art_source/handoff/claude_production/ART-004/collar_packet_v002.glb` | For Codex. Same two named parts, same root, same `chest` binding and attach as v001. 10,998 triangles, 2 flat materials. sha256 `a3146c83dca0b95d31d96f328091df899dc6bca5c53cfa4776ea825766349e73`. |
| `art_source/handoff/claude_production/ART-004/COLLAR_PACKET_V002_NOTES.md` | Manifest, what changed per brief point, clip clearances, contact report, known issues. |
| `art_source/handoff/claude_production/ART-004/renders/collar_v002_*.png` | Colour front, side, back and both agreed camera directions; clay back; v001 against v002. |
| `art_source/handoff/claude_production/ART-004/build_scripts/collar_pose_clearance.py` | New read-only check through `idle`, `walk` and `gather`, and collar against pack. |

Facts for the native test:

- The hood bag over the pack flap is removed. The hood stops at Y 0.115 (v001: 0.250). The pack is not edited.
- Lapel ends are about 45 mm shorter with tapered tips. The roll is narrower and pulled in against the neck.
- The hanging scarf end is removed: it tucks into the shirt. The wrap-over is lower and thinner.
- 39 sampled poses in Blender: nearest approach to the visible head is 10.7 mm (hood to skull base, `gather`); scarf to chin 22.5 mm.
- Reported contact: both parts rest against the neck column by design; 4 hood vertices sit up to 11.5 mm under the front lip of the pack on the hidden underside of the roll; the visible hood surface comes within 3.2 mm of the pack. A pack strap crosses the roll in the side view.
- No `.blend` committed for v002 (lighter delivery rule). The build command is in the notes.
- Body, old head, rig, socket and actions verified unchanged.

## ART-004 first packet: hood roll and scarf v001 (kept, superseded by v002)

Status: delivered for Codex's native test. Not a parity claim, not ready_for_user_review.

| Path | Purpose |
|---|---|
| `art_source/handoff/claude_production/ART-004/collar_packet_v001.glb` | For Codex. `SCULPT_HOOD` and `SCULPT_SCARF` under identity root `SCULPT_COLLAR_ROOT`. 11,000 triangles, 2 flat materials, no textures. sha256 `e8ba5af258a416629d2de4559d3b81e62138ffdb495201607583fb3f20d9ee39` |
| `art_source/handoff/claude_production/ART-004/collar_packet_v001.blend` | Edited-source evidence, Blender 3.5.1. |
| `art_source/handoff/claude_production/ART-004/COLLAR_PACKET_V001_NOTES.md` | Counts, bounds, binding, measured clearances, known issues. |
| `art_source/handoff/claude_production/ART-004/renders/` | Clay and colour at both agreed camera directions, back view, reference comparison. |

Facts for the native test:

- Static GLB in actor coordinates, like the head. Bind 100 percent to `chest`: `BoneAttachment3D` on `chest` with inverse rest translation (0, -0.84, 0) in Godot axes (chest rest head is (0, 0, 0.84) in Blender axes).
- Rest-pose clearance, measured in Blender: hood 37 mm from jaw and chin, 15 mm from the skull base, 47 mm from hair; scarf 20 mm from the chin, 10 mm from the nape. The tightest place in motion will be the back of the neck.
- Hood top is at Z 1.026, lower than the 1.06 starting figure, because 1.06 did not clear the skull base.
- The original body, weights, rig, actions and socket are verified unchanged. The head palette is untouched.

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
