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

**ART-004 / Fable / proposal delivered (mesh work still TODO, waiting on ART-003)**
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
