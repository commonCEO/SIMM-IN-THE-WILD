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

## Working files

Not committed, rebuilt from the scripts: `art_source/handoff/claude_simm/inbox/work/stage1.blend`, `stage2.blend`.
`START_HERE_v02.blend` is deliberately not committed, so a pull cannot collide with the local copy on the PC.

## Blocked, needs a commit from the PC side

1. `art_source/handoff/claude_simm/APPROVED_REFERENCE.png` (2048 x 1270). It was not packed in the starter and never reached Claude. v001 was judged against the 55 px copy in `docs/v06-art-directions.png`, panel 2.
2. `coordination/START_HERE.txt`. Claude has not read it. If it sets rules that differ from this file, those rules win and Claude will follow them once it is committed.

## Next

Nothing until the user has reviewed v001. Planned v002 changes, head only: smaller and less glossy eyes, less wide face,
a fringe that sweeps sideways with fewer and bolder points, softer hair mass at temples and nape, smaller cowlick.
