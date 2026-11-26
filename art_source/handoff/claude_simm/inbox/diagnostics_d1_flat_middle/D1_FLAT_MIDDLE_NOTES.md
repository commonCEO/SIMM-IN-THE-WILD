# ART-001 diagnostic: what makes D1_arc_body flat at mid-length (Codex brief at 0f7f741)

Read-only source isolation. Nothing here is a production change: the under-mass was not altered and no guide was
added. The isolation builds (under-mass left out, crown map off) are measuring devices only.

## Result

**The held primary under-mass does NOT explain the plateau.** This corrects my v012 note, which said it probably did;
Codex was right not to accept that cause. What does matter:

1. **The v011 crown map.** Heights above Z 1.235 are compressed to 0.815, which halves the rise of D1's top across the
   window at mid-length (8.4 mm uncompressed, 3.6 mm in v012) and raises its flat share (0.75 to 0.85).
2. **D1's own width.** Even uncompressed, its body is a broad, gently curved surface. At mid-length the 50 mm window
   sits inside a lock about 95 mm wide (122 mm authored, times 0.78), so it stays fairly flat (0.71 to 0.75 without
   the crown map).

## Evidence

The `+-25 mm` window, outer top curve, at 25, 50 and 75 percent of D1 (`lock_sections.py` with the v013 metric fix
below):

| Case | Flat share | Rise across the window (mm) |
|---|---|---|
| v012 as delivered: under-mass in, crown map on | 0.65 / 0.85 / 0.48 | 6.4 / 3.6 / 6.2 |
| Under-mass left out, crown map on | 0.71 / 0.84 / 0.57 | 6.4 / 3.6 / 5.8 |
| Under-mass in, crown map off | 0.57 / 0.75 / 0.50 | 11.1 / 8.4 / 9.9 |
| Under-mass out, crown map off | 0.59 / 0.71 / 0.52 | 10.9 / 8.4 / 9.4 |

On the bins both have, D1's outer surface with and without the under-mass differs by at most 0.6 mm.

Who forms the top in the UNFUSED source (`lock_sources.py`, stage 2 coordinates): at mid-length, D1_arc_body 42
percent, primary_mass 37 percent, D2_temple_arc 10, D1_arc_rear 10. The under-mass is outermost in places only by a
hair's breadth. After fusion the lock's surface is the outer one either way, which is why leaving the mass out changes
almost nothing.

`d1_flat_middle_isolation.png` plots the outer top curves of three cases; `d1_flat_middle_isolation.json` holds all
four cases and the ownership tallies.

## Metric correction (affects earlier reported numbers)

While isolating this I found an artefact in `lock_sections.py`. Where a 2 mm bin had no point on the lock's outer
surface, the "top" fell through to an inner shell 30 to 50 mm lower and made a false steep slope. The fix keeps only
points above the guide and uses 3 mm bins. Earlier flat-share numbers (D2 gate, v012) were made with the old version.
The v013 packet recomputes v011 and v012 with the fixed one, so every comparison there is like for like.

## Tools (in `../build_scripts/`)

- `stage2_hair.py`: diagnostic switches, both off by default. `HAIR_SKIP` leaves named source pieces out
  (`primary_mass` or lock names; guide order kept). `HAIR_SOURCE_COPY` keeps the unfused source with a per-vertex
  piece index.
- `lock_sources.py`: attributes the top of a section to its source piece.
- `lock_sections.py`: the fixed metric.

## What it implies (opinion, for Codex)

D1's mid flatness is mostly the crown compression acting on a very wide lock. Options that would address it are out
of this ticket's scope: a less uniform crown map that compresses the under-mass more than the lock tops, or a
narrower D1 width factor. Neither is done here.
