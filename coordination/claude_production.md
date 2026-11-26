# Claude (Fable) production file: acknowledgements, ticket updates, proposals

Written by Claude only. Codex reconciles this into `PRODUCTION_BOARD.md`. Updated 25 November 2026, about 21:00 UTC.

## Acknowledgement of PROD-001

Read on `codex/simm-art-handoff` at commit `a403661`: `PRODUCTION_PLAN.md`, `PRODUCTION_BOARD.md`,
`FABLE_NEXT_CHECK.md`, `DECISIONS_AND_RISKS.md`, the `START_HERE.txt` addition, the v006 review, the art direction
guide, the boss and new-idea notes, and the section list of the game design document (not yet the full text).

Accepted as written:

- **Roles.** Fable: Blender asset production and QA, art research, materials and textures, art packet specs,
  later UI illustration and design proposals. Codex: board, Godot runtime and renderer, browser parity, saves,
  controller verification, packaging.
- **Gates.** A1 before any NPC, body or world mesh. Audits, specs and proposals may run now.
- **Fable's tickets.** ART-001 (active), ART-004, ART-006 (started), ART-007, ART-008, ART-009, ART-010, ADD-001.
- **Fences.** Fable writes only its own files; never Codex's files, the runtime, saves, rigs or actions. No paid
  generators. No force-push. One active asset revision at a time.
- **File homes.** Proposals here; deliveries in `claude_deliveries.md`; the ART-006 audit in
  `coordination/claude_art_audit.md`; head packets in `art_source/handoff/claude_simm/inbox/`; later families in
  `art_source/handoff/claude_production/<ticket-id>/`.

## Ticket updates (board format)

**ART-004 / Fable / PROPOSAL: hem and cuff method before jacket v003 (26 Nov, run 14, answers `906cdaf`)**

No geometry delivered. Evidence was made on throwaway copies: two test jackets built from the v002 script with
changed constants, and, for option B, hem weights changed on the candidate copy in memory only. Nothing was
saved, exported or written to `PROTECTED_BODY`, the rig, the actions or the socket. Frames and scripts are in
`art_source/handoff/claude_production/ART-004/method_proposal/`.

Options tested, same camera and light, walk at 25 and 75 percent, gather at 50 percent (`hem_options_walk_gather.png`):

| Option | Hem lowest Z | Weights | What the frames show |
|---|---|---|---|
| v002 as delivered | 0.545 | original | side vents, split-tail silhouette (as you found) |
| **A** | **0.585** | **original, exact** | **one coherent hem, no vents; no trouser showing through in any of the frames** |
| B0 | 0.545, no vents | original | a small dark trouser corner pokes through the side of the hem in walk |
| B1 | 0.545, no vents | 186 hem-band vertices (Z under 0.635, now 100 percent `hips`) blended toward the same-side thigh, up to 0.5 at the hem | the same corner, slightly smaller |
| B2 | 0.545, no vents | same band, up to 0.8 | smaller again, still there, and the back hem starts to separate into a torn edge (`hem_option_B_weight_strength.png`) |

Numbers I tried and do not rely on: a nearest-surface "inside the trousers" count, which flips sign near thin
cloth and gave nonsense values, and a ray test that also counted the open front of the jacket. The frames are
the evidence. Cloth more than 2 mm into a hand, 25 samples per clip: A 0 / 0 / 4 vertices up to 5.7 mm (idle,
walk, gather); B0 to B2 0 / 0 / 4 up to 4.7 mm; v002 0 / 0 / 0.

**Recommendation: A.** A coherent hem at the original height, every weight exact, no vents. The 0.47 to 0.50 m
reference length is given up here; the shorter-legged read comes later from taller boots and a fuller lower
jacket, as you suggested. B would need per-vertex weight tuning to remove the corner and would still tear at the
back. If you want B anyway, the band, bones and blend are in `hem_method_test_weights.py`: affected vertices
are the jacket vertices under Z 0.635 that are 100 percent `hips` today, inside |X| 0.215; same-side thigh
weight `fz*W*(0.35 + 0.65*s)`, other thigh `fz*W*0.35*(1 - s)`, `hips` the remainder, so each sums to 1;
`fz` rises from 0 at Z 0.635 to 1 at the hem, `s` from 0 at the centre line to 1 at |X| 0.10. Rollback is the
original weights, which the export check already compares vertex by vertex.

Open item for A: the gather hand. 4 vertices reach up to 5.7 mm into a hand at the hip side. v003 would draw the
hem in locally where the measured hand path passes, with a gentle rise of at most 10 mm at the sides (a curve,
not a vent), and report the measured result.

**Cuffs: a continuous rolled lip, not a bracelet.** The original cuff rings sat at a mean radius of about
47 mm and never touched a hand in any clip (measured on the original body). v002 moved them to about 51 mm and
opened the sleeve to 43 mm to clear the hand, which is what made them float. v003: the cuff roll goes back to
the original ring radius and height, and the sleeve end is shaped to meet it, with the roll overlapping the
sleeve by 2 to 3 mm so it reads as one turned-back edge. No flare, no widening past the original ring.

Next: on your go, jacket v003 with option A and these cuffs, one export, the same checks as v002.

**User feedback, 26 Nov 2026, on a native side view of head v007 + collar v002 + jacket: "IMO we're still 30% off."**
Fable's read of that frame against the approved reference, measured in Blender where possible:
1. Bare neck (largest gap). 44 mm of skin shows at the nape between the hood top (Z 1.017) and the lowest hair
   (Z 1.061), and 30 mm at the throat between the scarf (Z 0.990) and the chin (Z 1.020). The reference head sits
   down in a full, bunched hood with almost no neck visible. Collar v002 was shrunk on purpose to clear the pack.
2. Hair. Glossy, uniform brown with deep dark grooves; the back ends in a hard shelf of pointed locks above a pale
   nape. The reference hair is softer, lighter at the tips, and comes down to meet the hood.
3. Skin and light. Pale, grey on the shadow side of the face and neck; the reference is warm and peachy. Mostly
   lighting (audit hypotheses L5, L9), partly the skin bake.
4. Face profile. Lower face long and flat, eyes read as flat discs from the side. Smaller than 1 to 3.
Proposed: reopen collar first (a real hood behind the nape, scarf up to the chin), then the hair's back and nape.
Head v007 and collar v002 are on hold by Codex's call; reopening them needs the user's go-ahead.
User's answer, typed directly: "Yes, this needs to have full parity, for Mattias to be happy". Collar and hair
are reopened on the user's authority, overriding the hold for these two items only.

**ART-004 / Fable / REVIEW (collar packet v003 delivered, 26 Nov 07:45 UTC, user-approved reopen)**
- Trigger: user review of a native side view, not a Codex brief.
- Files changed: `art_source/handoff/claude_production/ART-004/collar_packet_v003.glb`,
  `COLLAR_PACKET_V003_NOTES.md`, eight frames in `renders/`, `build_scripts/collar_build.py` (v003).
- Checks actually run: bare neck measured by direction round the neck; hood fitted to the head mesh; 39 sampled
  poses for jaw, nape and hair clearance; collar against pack; manifest and binding asserts; GLB export;
  `verify_candidate.py` (`FROZEN_ALL_UNCHANGED True`). Nothing native.
- Evidence: notes, frames, GLB sha256 `f233e2693f5060e234f4741f62c0acad0f9855298b78379ee540f46c96878961`.
- Remaining gaps: 2.8 mm hood to hair tip in gather; the back bunch reads as a lump from the side; not seen with
  jacket v002 or in Godot.
- Next: ART-001 head v008 (hair only), then Codex's combined native study.

**ART-001 / Fable / REVIEW (head v009 delivered, 26 Nov, at the user's request)**
- Trigger: the user, typed directly: "your version looks like it's from Silent Hill or from some horror cartoon,
  and what's on the concept is very cute ... you should fix it." This lifts the face hold for the expression.
- Files changed: `art_source/handoff/claude_simm/inbox/head_candidate_v009.glb`, `.blend`, `textures_v009/`,
  `renders_v009/`, `HEAD_CANDIDATE_V009_NOTES.md`, `build_scripts/stage3_finish.py` (eyes, brows, smile, skin).
- Cause found in the build: the iris was wider than the eye opening, so the eyes were solid dark ovals with no
  white and no highlight; brows thin, pale and 36 mm above the eyes.
- Checks actually run: rebuild; meshes compared with v008 after re-import (only brows changed); emissive eye
  texture confirmed in the GLB; `verify_candidate.py` (`FROZEN_ALL_UNCHANGED True`). Nothing native.
- Next dependency: Codex's combined native study of head v009 + collar v003 + jacket v002.

**ART-001 earlier entry (head v008, hair colour and gloss)**
- Trigger: the same user review.
- Files changed: `art_source/handoff/claude_simm/inbox/head_candidate_v008.glb`, `.blend`, `textures_v008/`,
  `renders_v008/`, `HEAD_CANDIDATE_V008_NOTES.md`, `build_scripts/stage3_finish.py` (hair palette and material).
- Checks actually run: full rebuild from the starter; every mesh compared with v007 after re-import (identical);
  skin and eye textures byte-identical; `verify_candidate.py` (`FROZEN_ALL_UNCHANGED True`). Nothing native.
- Evidence: hair colour measured in the reference and in the user's native frame; numbers in the notes.
- Next dependency: Codex's combined native study of head v008 + collar v003 + jacket v002, ideally including the
  side view the user reviewed.

**ART-001 / Fable / REVIEW (delivered, waiting on ART-002)**
- Peer commit consumed: `7ef4a5e` (v006 review and v007 brief).
- Files changed: `inbox/head_candidate_v007.blend`, `.glb`, `renders_v007/`, `textures_v007/`,
  `HEAD_CANDIDATE_V007_NOTES.md`, `build_scripts/stage2_hair.py`.
- Checks actually run: full rebuild from the starter copy in headless Blender 3.5.1; GLB re-imported into an empty
  scene for counts and bounds; `verify_candidate.py` (frozen body, old head, 17 bone rest matrices, socket, three
  actions unchanged); skin texture compared byte for byte with v003; both agreed clay cameras judged before export.
- Evidence: `inbox/renders_v007/`, GLB sha256 `9a296dd846e3fba327f6270cc41c9f25c4864a513b2436218cd39e754d6328d9`.
- Remaining gaps: hair still heavier and tidier than the reference; face held, not approved; no engine evidence.
- Correction: v006 was delivered with two fringe locks missing because of a patch bug. Restored in v007. Details
  in the v007 notes.
- Next dependency: Codex's native review (ART-002).

**ART-006 / Fable / DOING (first pass delivered)**
- Peer commit consumed: `a403661`.
- Files changed: `coordination/claude_art_audit.md`.
- Checks actually run: none native. Reference and concept images read directly; current scene state taken from
  Codex's guide only.
- Remaining gaps: no current native clearing frames in Git, so the gap ranking is second hand.
- Next dependency: Codex commits three native clearing frames; then Claude re-ranks and details per-asset defects.

**PROD-001 / Codex / acknowledged by Fable** at this commit.

**ART-004 / Fable / REVIEW (jacket candidate v002 delivered, 26 Nov 07:28 UTC)**
- Peer commit consumed: `bfd7ce4` (jacket v001 native review and six-point v002 brief at `367f484`).
- Files changed: `art_source/handoff/claude_production/ART-004/jacket_candidate_v002.glb`,
  `jacket_candidate_v002_vertex_map.json`, `JACKET_CANDIDATE_V002_NOTES.md`, six frames in `renders/`,
  `build_scripts/jacket_build.py` (v002), `jacket_export_check.py` (rewritten), `jacket_review_prep.py`,
  new `jacket_hand_sweep.py` and `jacket_hand_sweep.json`.
- Checks actually run: deterministic build; per-part asserts that every vertex is an original vertex with its
  original faces, groups and weights; hand and thigh travel measured over 17 samples per clip; 9 samples per clip
  for cloth against thighs and hands, before and after; GLB re-imported and all 5,606 vertices matched to source
  vertices within 20 micrometres with identical weights, failing on any miss; skeleton names, parents and rest
  joints compared; `verify_candidate.py` (`FROZEN_ALL_UNCHANGED True`). Nothing native.
- Evidence: notes file, frames, GLB sha256 `c985517f0f8519e8f4e56d599a8ef99dd25bf6eb39c96ecb0ef8d67e314f2e61`.
- Remaining gaps: a side vent of up to 80 mm in the hem at each hip; 3 trim vertices in the thigh in gather;
  cuff roll is a ring wider than the sleeve end; hem height unchanged; old topology; not seen in Godot.
- Correction: my v001 note that no thigh broke through the hem was wrong. It did, in walk.
- Next dependency: Codex's in-memory native study. If the vents are rejected, a decision on which of three
  faults is least bad, or leave to propose a weighting exception for the hem band.

**ART-004 earlier entry (jacket candidate v001, 26 Nov 01:22 UTC; reviewed, changes requested)**
- Peer commit consumed: `e5e7105` (collar v002 held as working baseline and jacket brief at `193b661`).
- Files changed: `art_source/handoff/claude_production/ART-004/jacket_candidate_v001.glb`,
  `jacket_candidate_v001_vertex_map.json`, `JACKET_CANDIDATE_V001_NOTES.md`, six frames in `renders/`,
  new `build_scripts/jacket_build.py`, `jacket_export_check.py`, `jacket_review_prep.py`;
  `collar_packet_v002.blend` (the baseline source Codex asked for).
- Checks actually run: deterministic build on the collar v002 file; asserts that the candidate is exactly the
  original jacket vertex set with identical connectivity, groups and weights; 9 samples in each of `idle`, `walk`,
  `gather` for cloth against thighs and hands, before and after; GLB re-imported for bones, counts, bounds and
  weights; `verify_candidate.py` (`FROZEN_ALL_UNCHANGED True`). Nothing native.
- Evidence: notes file, frames, GLB sha256 `1ecc5240f497a55f5f7133048cb9f484582318cdae269e3305f420ce317bddcc`.
- Remaining gaps: not seen in Godot; hem lowered 37 mm only; 10 vertices touch a hand in `gather`; straps up to
  14.5 mm above the new surface; one frozen button without a placket; roundness limited by the old topology.
- Next dependency: Codex's in-memory native study. Head, collar, trousers, boots, hands and pack stay closed.

**ART-006 / Fable / REVIEW (second pass delivered, 26 Nov 02:10 UTC)**
- Peer commit consumed: none new. Tip unchanged at `e5e7105`. Evidence used: the three native frames from `98c1777`.
- Files changed: `coordination/claude_art_audit.md` (sections 1, 3 and 6).
- Checks actually run: all three native frames and the approved reference viewed at full size; pixel statistics
  and one lit and shaded floor sample pair per image; character and tent heights measured in pixels. Nothing native.
- Evidence: section 3.1 of the audit. Opinion is separated in 3.2.
- Result: light and shadow is now rank 1 (was 4); foliage stays 2; ground stays 3; characters rank 4 on screen
  but remain the A1 gate; camp layout and scale is a new rank 5 (tent about twice its study size in the playable
  camp); props 6; UI 7.
- Remaining gaps: three stills, one light setup, no motion; grass and foliage colour samples were not reliable
  enough to quote; Simm in the frames is the old runtime model.
- Next dependency: Codex to test L9 and L10 natively if it agrees, and to accept or change the oak pilot as the
  first world packet after A1. The tent scale question in the playable camp needs Codex or the user.

**ART-004 earlier entry (collar packet v002, 26 Nov 00:20 UTC; now held as working baseline)**
- Peer commit consumed: `fad6b7a` (collar v001 review, changes requested, at `65387e5`).
- Files changed: `art_source/handoff/claude_production/ART-004/collar_packet_v002.glb`,
  `COLLAR_PACKET_V002_NOTES.md`, seven frames in `renders/`, `build_scripts/collar_build.py` (v002 shapes),
  new `build_scripts/collar_pose_clearance.py`. No `.blend` (lighter delivery rule).
- Checks actually run: deterministic build on `head_candidate_v007.blend`; manifest and single-bone asserts;
  front, side and back inspected in clay and colour; 39 sampled poses across `idle`, `walk`, `gather` for
  distance to the visible head; rigid collar-against-pack measurement; `verify_candidate.py`
  (`FROZEN_ALL_UNCHANGED True`). Nothing native.
- Evidence: notes file, frames, GLB sha256 `a3146c83dca0b95d31d96f328091df899dc6bca5c53cfa4776ea825766349e73`.
- Remaining gaps: not seen in Godot or in motion; scarf may now be too thin; hood has little volume from the
  back; 4 hidden hood vertices under the pack lip; neck contact at the nape to be checked in `gather`.
- Next dependency: Codex's native attach and the same three clips. Jacket and boots stay closed until then.

**ART-006 / Fable / READY, not started (run 6).** The collar correction took this run. Re-rank from the three
native clearing frames is the next run's one task.

**ART-004 earlier entry (first packet: hood roll and scarf v001, superseded)**
- Peer commit consumed: `98c1777` (ART-003 first fit and the scoped collar assignment at `7a939fd`; clearing frames at `98c1777`).
- Files changed: `art_source/handoff/claude_production/ART-004/collar_packet_v001.glb`, `.blend`,
  `COLLAR_PACKET_V001_NOTES.md`, `renders/`, `build_scripts/collar_build.py`, `collar_export_check.py`;
  `claude_simm/inbox/build_scripts/render_views.py` (review-only handling of the body's missing textures).
- Checks actually run: deterministic build on `head_candidate_v007.blend`; part manifest and single-bone binding
  asserts; rest-pose clearance to jaw, skull base and hair; GLB re-imported for counts and bounds;
  `verify_candidate.py` (body, old head, 17 bone rest matrices, socket, three actions unchanged). Nothing native.
- Evidence: notes file, six frames, GLB sha256 `e8ba5af258a416629d2de4559d3b81e62138ffdb495201607583fb3f20d9ee39`.
- Remaining gaps: not seen in motion; hood colour match to the textured jacket unverified; lapel ends overlap the
  untouched jacket and straps.
- Next dependency: Codex's native attach to `chest` and sampled clips.

**ART-006 / Fable / READY, not started this run.** The three native clearing frames arrived at `98c1777`. One
ticket per run: the P0 collar packet went first. The evidence-based re-rank is next.

**ART-004 proposal (earlier entry)**
- Peer commit consumed: `757c52d` (no new art feedback in it; proposal cleared at `1f7d6a8`).
- Files changed: `coordination/claude_art004_proposal.md`,
  `art_source/handoff/claude_production/ART-004/frozen_body_with_v007_head_clay.png`.
- Checks actually run: read-only inspection of `PROTECTED_BODY` in the starter (counts, islands, materials, vertex
  groups, collar zone); one Blender clay render of the frozen body with head v007. Nothing native. The frozen
  body was not modified.
- Evidence: the measurements table in the proposal; the clay frame.
- Remaining gaps: no observation of the body in Godot or in motion; body textures are not in Git.
- Next dependency: ART-003 results; Codex's answer on single-bone parts (option B); the two body textures.

## Proposed corrections to the plan

Each item says whether it rests on evidence or on opinion.

### 1. Fable's schedule is hourly (evidence). RESOLVED 21:07 UTC: scope widened by the user

Update: the user typed the request directly and the stored check now follows Fable's tickets on the board, one
bounded step per run, with the same fences. The three bullets below describe the situation before that.

- The platform minimum is one hour. `trig_01RTVFoanSgc82QmxWinsxYg` fires at minute 6 UTC.
- Its stored instructions still say "head only". Claude tried to widen them to follow Fable's board tickets and
  the session's permission layer refused, as it did for the original schedule until the user typed the request
  directly. Claude has not worked around it.
- Effect until the user widens it: unattended runs will keep doing head revisions and writing `claude_*.md`
  files. They will not advance ART-006 or later tickets on their own. Those move when the user prompts the session.
- Proposed board note: treat Fable's unattended capacity as "ART-001 only" until the receipt here says otherwise.

### 2. Measured throughput so far (evidence), and what it implies (opinion)

- Evidence: seven head versions between 15:34 and about 21:00 UTC on 25 November. Six Codex review rounds. Each
  Claude revision took 20 to 45 minutes of work once the brief was read. The head is still `changes_requested`.
- Evidence: the first three rounds were spent finding the right inputs and proportions (no reference, then a
  55 px reference, then the real one and the first Godot view). Rounds four to seven converged on one topic, hair
  construction.
- Opinion: a hero character part needs 5 to 8 rounds; a prop or tree kit probably 2 to 4 once section 2 of the
  audit is agreed. The clearing is 13 manifest assets plus ground. That puts A2 at very roughly 40 to 70 review
  rounds. At one round an hour that fits weeks 3 to 6 only if both loops run most of the day. Reforecast after two
  accepted packets, as the plan already says.

### 3. New ticket proposed: ART-011, game-resolution Simm head (opinion, with one fact)

- Fact: the head is 80,265 triangles in five meshes with auto-unwrapped hair. That is review density.
- A1's exit evidence includes a performance measurement and game-scale readability. Measuring the 80k head would
  measure the wrong thing.
- Proposal: once the head shape is accepted, Fable makes a reduced head and hair with a normal map baked from the
  sculpt, before ART-003's game-scale study or in parallel with it. Depends on ART-002 stable. Feeds ART-003,
  ART-005 and PERF-001.

### 4. ART-004 should start as a scoped proposal now (opinion)

- Fact: the reference hides Simm's neck behind a raised hood and scarf; the frozen body has neither at that
  height, and Codex has listed the exposed neck as a known mismatch since v002.
- Fact: `PROTECTED_BODY` is 7,444 vertices and 14,144 polygons with 20 material slots and one armature modifier.
- Proposal: Fable writes the ART-004 approach now (which parts change, on the existing skinned topology, with what
  evidence), so the mesh work can begin the moment ART-003 reports. No body mesh before that.

### 5. Repository growth (evidence) and a lighter delivery rule (proposal)

- Evidence: each head version adds about 38 MB (renders 20, `.blend` 15, `.glb` 3). Seven versions are about
  265 MB on Fable's branch.
- Proposal from v008: every revision commits the GLB, the notes and five renders (reference and alternate in clay
  and colour, plus the comparison sheet). The `.blend` and the full render set are committed only for versions
  Codex marks as a new baseline. Everything stays rebuildable from the committed scripts and starter copy.
  Codex, say if you need the full set every time.

### 6. Turnaround of invented surfaces (opinion)

- Fact: the back, nape and Simm's left side have never been seen by the user; they are Claude's invention.
- Proposal: A1's user checkpoint (ART-005) explicitly shows back and both sides, so an objection lands once,
  before the same hair logic is reused on Leina and others.

### 7. Inputs Fable needs before later tickets (evidence)

- ART-006: three native clearing frames (see the audit).
- ART-007: starter `.blend` files for Leina and Bronkings with frozen rigs, prepared like Simm's starter, and the
  approved identity picture for each.
- ADD-001: `docs/concepts/mattias-bosses-20261125.png` is referenced by the boss notes but is not on the branch.
- PROD-002: the scoped code snapshot, before Fable drafts any data or test specs.

### 8. A process safeguard Fable has added (evidence)

- The v006 omission happened because a text patch removed two lock statements without any error.
- From v007 the hair build prints the lock count and fails on duplicate names, and each notes file states the count
  (v007: 67 locks). Codex may want the same kind of manifest check on its side for multi-part assets.

## Decisions log items Fable can help close

- D07, D08 (penguin, bosses, bucket): Fable will write ADD-001 proposals when the ticket opens and the drawing is
  readable. Nothing is assumed about mechanics.
- D11 (budgets): see proposal 3; provisional planning ranges are in the audit, marked as opinion.
