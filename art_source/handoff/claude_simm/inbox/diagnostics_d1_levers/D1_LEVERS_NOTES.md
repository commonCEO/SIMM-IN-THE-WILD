# ART-001 D1 lever test (Codex brief at 3bb0d3a): neither lever visibly helps, so D1 tweaking stops

Status: diagnostic only. No v013 and no candidate; v012 stays held. As the brief says, when neither alternative
visibly improves both views, D1 tweaking stops here and the next step is Codex's consolidated A1 gap review.

## What was tested (D1_arc_body only)

| Case | D1 setting | Everything else |
|---|---|---|
| Control | v012: round section, width 0.78 | v012 |
| A | width 0.62, same crown map and guide path | v012 |
| B | width 0.78; round section thickness x1.227 (= 1/0.815, the crown map's slope factor) and the guide's lift lowered by 7 mm, so the thicker section's outer top stays where it was. This pre-compensates the crown map locally; the global crown cut is untouched. | v012 |

The other three round locks, the five crown guides at their v012 settings, the primary mass, tuft, face and protected
body stay as they are. Switches: `HAIR_ROUND` entries `name:width:thickness:inward` in `stage2_hair.py`, and
`round_t` in `hairkit.py`. Both default to v012's values; the default build is unchanged.

## Evidence

Sections at 25 / 50 / 75 percent of D1 (`d1_lever_sections.png`, `d1_levers.json`). The plot shows every raw cut
point, the outer top per 3 mm bin, and red ticks at EMPTY bins (no outer point in that bin; they are left empty, not
bridged). Support is sparse: 3 to 8 of the 26 bins are empty in each section.

| Case | Rise across the +-25 mm window (mm) | Flat share |
|---|---|---|
| Control | 6.4 / 3.6 / 6.2 | 0.65 / 0.85 / 0.48 |
| A | 10.6 / 5.9 / 10.2 | 0.38 / 0.59 / 0.35 |
| B | 6.8 / 4.6 / 7.8 | 0.41 / 0.62 / 0.50 |

The section numbers move, A most. What that does to the image:

| | Reference camera | Alternate camera |
|---|---|---|
| Crown envelope (full / main height over eye-to-chin) | 2.267 / 2.118 in all three | 2.449 / 2.341 in all three |
| Close view, pixels changed by more than 8 of 255 against control | A 0.9 percent, B 0.4 percent | A 1.7 percent, B 0.5 percent |
| Held head framing, same measure | A 0.3 percent, B 0.1 percent | A 0.6 percent, B 0.2 percent |

In the clay renders (`d1_levers_clay_ref_alt.png`: control, A and B at both held cameras, close and at head
framing), I can't see a difference that would change the read. Front and top (`d1_levers_front_top.png`) show no
gaps, no exposed scalp and D1's tips still attached. The colour readability check with m001-B was not run, because
there is no candidate to check.

## Reading

D1's measurable section change is real but small in the frame. In both cameras the broad top read comes from how the
locks overlap and from the crown's overall shape, not from D1's mid-section alone. More hair micro-variants would
cost cycles without a visible return.

## Recommendation

Stop D1 and hair-geometry tweaking at v012 + m001-B, and move to Codex's consolidated A1 gap review. If hair is still
the top A1 gap there, it needs a different method decision (for example, fewer and more distinct crown masses
designed as a set), not further per-lock profile tuning.
