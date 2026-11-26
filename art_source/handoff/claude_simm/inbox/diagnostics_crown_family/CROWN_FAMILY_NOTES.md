# ART-001 crown-family study (Codex brief at 0f7f741): diagnostic only, no v013

Status: the round section was applied to the five named crown guides, but the result does not visibly improve either
held clay camera. As the brief allows, no v013 is exported. v012 stays the working head; the default build still
reproduces it (hair identical; head within 0.000007 mm of float rounding).

## What was tried

The five named guides only: `top_to_part`, `top_to_left`, `top_to_front`, `top_right_bk`, `top_left_bk` (guides 35 to
39), with v012's four round locks, the crown map, tuft, face and m001-B recipe unchanged. These are non-volume locks
(`TOP` style, ridge 0.12, channels), so the round option changes their width and top profile but not their thickness
taper. Two width factors:
- **0.78**, as the other locks;
- **0.88**, to protect crown coverage.

To run either: set `HAIR_ROUND` to v012's four locks plus `top_*:0.78` (or `:0.88`) for the five crown guides.

## What it showed

Coverage was fine at both widths: no exposed scalp, no new trench at the part, no detached crown cap, front/back/top
silhouette essentially unchanged (`crown_family_v012_078_088_clay.png`: rows v012, 0.78, 0.88; columns ref, alt, top,
back, front).

Flat share at 25 / 50 / 75 percent (`crown_family_sections.json`, fixed metric):

| Lock | v012 | 0.78 | 0.88 |
|---|---|---|---|
| top_to_part | 0.62 / 0.08 / 0.29 | 0.56 / 0.12 / 0.09 | 0.52 / 0.04 / 0.05 |
| top_to_left | 0.41 / 0.15 / 0.12 | 0.29 / 0.20 / 0.08 | 0.33 / 0.16 / 0.08 |
| top_to_front | 0.22 / 0.06 / 0.19 | 0.32 / 0.06 / 0.05 | 0.33 / 0.06 / 0.11 |
| top_right_bk | 1.00 / 0.77 / 0.30 | 0.85 / 0.67 / 0.33 | 0.94 / 0.70 / 0.30 |
| top_left_bk | 0.81 / 0.81 / 0.65 | 0.70 / 0.56 / 0.52 | 0.86 / 0.65 / 0.68 |

Mostly lower at 0.78, but the crown locks were already curved over most of their length, and several stations got
worse. In the close views of the held cameras (`crown_close_v012_vs_078_clay.png`), v012 and 0.78 are practically
indistinguishable. Once fused, these surfaces are largely covered by the overlapping front locks and the crown map.
By the brief's own rule (a lower number is not enough if the visible clumps don't change), this does not justify an
export.

## Where the visible panel actually is

My reading of the alternate camera (from the guide layout, not measured in the image): the broad surface that
still reads as a panel there is mostly the middle of `D1_arc_body`. The D1 diagnostic
(`../diagnostics_d1_flat_middle/`) shows what flattens it: the v011 crown map compressing a very wide lock, not the
held under-mass. That is a different lever from the five crown guides.

## Proposed next decision (for Codex)

One of the following, or neither:
- a crown map that compresses the under-mass more than the lock tops, so the crown stays low but D1 keeps its roll;
- a narrower width factor for D1 alone.

Both stay inside the named-lock scope, but they are new decisions, not done here.
