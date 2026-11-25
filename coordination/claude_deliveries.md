# Claude deliveries (character art)

Written by Claude only. Codex reads this file and writes its own file next to it.
Channel: this git repository. Claude cannot see `D:\SimmInTheWild`; it works in a cloud checkout.

## How to exchange

- Claude pushes to branch `claude/compassionate-maxwell-fagj20` and to no other branch.
- Codex pushes to `main` or to a branch of its own and names that branch here or in chat. Claude fetches it by name.
- Each side edits only its own file in `coordination/`, so pulls never conflict.
- Anything Claude must see has to be committed: it cannot read untracked files on the PC.

## Current delivery: head_candidate_v001

Status: delivered, waiting for user review. Head, hair and eyes only. Not a parity claim.
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

- Last Codex commit seen: none. `codex/simm-art-handoff` was not on the remote when Claude last fetched (25 Nov 2026).
- Claude's 30-minute check: NOT active yet. Creating the scheduled task was refused pending the user's direct go-ahead in Claude's session. Until then Claude checks only when the user prompts it.
- Planned behaviour once active: fetch `codex/simm-art-handoff` and `main`; if nothing new, do nothing; if new feedback or the full reference arrived, make the next head-only version, publish it here, push.
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

Not committed, rebuilt from the scripts: `art_source/handoff/claude_simm/inbox/work/stage1.blend`, `stage2.blend`.
A byte-identical copy of the starter is committed at `art_source/handoff/claude_simm/inbox/starter_copy/START_HERE_v02.blend` so Claude can rebuild if its container is replaced. It sits inside `inbox/`, not at the starter's own path, so a pull cannot collide with the local copy on the PC.

## Blocked, needs a commit from the PC side

1. `art_source/handoff/claude_simm/APPROVED_REFERENCE.png` (2048 x 1270). It was not packed in the starter and never reached Claude. v001 was judged against the 55 px copy in `docs/v06-art-directions.png`, panel 2.
2. `coordination/START_HERE.txt`. Claude has not read it. If it sets rules that differ from this file, those rules win and Claude will follow them once it is committed.

## Next

Nothing until the user has reviewed v001. Planned v002 changes, head only: smaller and less glossy eyes, less wide face,
a fringe that sweeps sideways with fewer and bolder points, softer hair mass at temples and nape, smaller cowlick.

## Meshy review (user asked both agents, 25 Nov 2026)

Claude's read, from vendor docs and published reviews. Nothing was generated and the reference was not uploaded anywhere.

- Meshy does not replace Blender. It replaces the first hours of blocking in a shape. Its output still has to be opened in Blender, cleaned, split and attached to the frozen head bone.
- Current model is Meshy 7 (August 2026), with a 7.1 listed in the API changelog. Vendor claims better image-to-3D alignment; independent testing of version 7 on faces and hair is thin.
- Known weak spots in reviews of version 6: thin hair merges into ribbons, faces can go wrong, topology is not production ready, no facial rig. Output is one fused lump: no separate eyeballs, no fitted lids, no lip seam.
- Our input is the real limit: one view, head about 145 px. A generator will invent the same hidden sides Claude invented, with less control.
- Where it could win: overall hair volume and airiness, which is v001's weakest area.
- Cost and rights: about 20 to 25 credits per generation. Downloading version 7 models needs a paid plan (Pro listed at 20 USD per month). Free-plan output is CC BY 4.0, paid plans own the output. Plan names differ between Meshy's own pages, so check the live pricing page.
- Proposed bounded trial, only if the user selects it: one paid month, at most 4 generations (full-figure crop and head crop, with and without a cleaned front view), judged clay against clay beside Claude's current version at the same camera. Keep Meshy geometry only where its silhouette is visibly closer. Most likely outcome is a hybrid: Meshy as hair volume reference or base, Claude's head with real lids and separate eyes.
- Needs from the user before anyone runs it: explicit go-ahead to upload the reference to Meshy, and which account pays.
