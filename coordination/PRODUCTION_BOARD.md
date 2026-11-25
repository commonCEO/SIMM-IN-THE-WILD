# SIMM production board

Canonical board maintained by Codex. Fable updates only its own delivery/proposal files; Codex reconciles them here at the next check. Links to commits/evidence are required before DONE. Forecast in PRODUCTION_PLAN.md. Initial board25November2026; historical implementations below are PARTIAL/REVIEW, not newly verified DONE.

| ID | Priority | Owner | Status | Depends | Deliverable / acceptance |
|---|---|---|---|---|---|
| PROD-001 | P0 | Codex | DONE | none | Publish plan/board/dispatch + GDD context; Fable acknowledges next check |
| PROD-002 | P0 | Codex | READY | PROD-001 | Inventory dirty local runtime; produce allowlisted remotely readable code snapshot and provenance, excluding saves/vendor/cache; preserve main |
| PROD-003 | P0 | Codex | READY | PROD-002 | GDD section12 refreshed: every flow maps to code, fixture, native journey, missing task; no completion inferred from test filenames |
| ART-001 | P0 | Fable | REVIEW | existing v006 review | v007 delivered at58f629d; freeze as fit-study candidate, not art approval; no v008 until full-body feedback |
| ART-002 | P0 | Codex | DONE | ART-001 delivered | v007 native review/held meshes verified; codex_deliveries.md ART-002 evidence; A1 still pending |
| ART-003 | P0 | Codex | READY | ART-002 reviewed candidate | Non-saving full-body fit, original head-bone binding, idle/walk/gather/socket and game-scale comparison; no live swap |
| ART-004 | P0 | Fable | TODO | ART-003 feedback | Body/clothing benchmark packet preserving original rig, or a scoped proposal if full-body fit already works; approve head direction first |
| ART-005 | P0 | Codex | TODO | ART-003/004 | Simm user checkpoint A1 with side-by-side and motion evidence; integrate only after validated fit/quality |
| ART-006 | P1 | Fable | BLOCKED | PROD-001 | First audit delivered in claude_art_audit.md; needs3native clearing frames from Codex before evidence-based completion |
| RENDER-001 | P1 | Codex | READY | v006 available | Final soft-shadow method/motion study;2deg stipple vs samples/filter; preserve scene and provide negative results too |
| ART-007 | P1 | Fable | TODO | A1 | Leina then Bronkings, rig-compatible idle/talk packets; approved identity refs, review per character |
| ART-008 | P1 | Fable | TODO | A1,ART-006 | Tent/workbench/forest/ground asset batches; one style family per packet; no collision/layout changes |
| RENDER-002 | P1 | Codex | TODO | ART-007/008 | Matched clearing camera/material/light integration, day/torch/readability; A2 user checkpoint |
| CORE-001 | P1 | Codex | TODO | PROD-003 | Day/survival/pause/sleep/defeat browser parity, migrated time state; normal-time and defeat recovery tests |
| CORE-002 | P1 | Codex | TODO | PROD-003 | Quest data/journal/NPC six identities and one-time exchange rewards; atomic full-bag behavior |
| CORE-003 | P1 | Codex | TODO | CORE-001/002 | Bronkings home order/upgrade/three-day-or-rest/interiors, preserve furnishings/clear doors; B1 controller journey |
| CORE-004 | P1 | Codex | TODO | PROD-003 | Audit all48recipes/context gates and ingredient reachability; baseline25nonbuilding already reported locally, revalidate gaps only |
| CORE-005 | P1 | Codex | TODO | CORE-003 | Full biome/height/scene/world transitions, cave+dungeon+volcano and scene-local saves; campaign map |
| CORE-006 | P1 | Codex | TODO | CORE-005 | Combat/AI/Nups campaign interactions, fishing/boat/whale/rainbow, journal/ending; B2 full journey |
| ART-009 | P1 | Fable | TODO | A2,CORE-005 spec | Remaining NPCs, enemies/animals/biomes/interior/boat/ending assets in dependency order; manifest packets |
| UX-001 | P1 | Codex | TODO | PROD-003 | Complete quest/build/map tabs; exact controller context/focus/scroll; UI parity and EN/ET at3resolutions |
| ART-010 | P2 | Fable | TODO | A2,UX-001 spec | Approved icon/UI illustration and world feedback art; source/license/export evidence |
| AUDIO-001 | P2 | Codex | TODO | B1 | Baseline sound behavior and volume/mute, gather/craft/damage cues; no unlicensed external audio |
| SAVE-001 | P0 | Codex | READY | PROD-002 | Migration/save compatibility matrix and isolated test harness across supported local versions; no native save publish |
| ADD-001 | P2 | Fable | TODO | A2 | Bucket/penguin/boss design proposals grounded in Mattias's drawings; separate assumptions/questions from approved facts |
| ADD-002 | P2 | Codex | BLOCKED | ADD-001 design gate | Size user additions for beta, assign implementation/art packets; no invented combat mechanics; record deferrals explicitly |
| QA-001 | P1 | Codex | TODO | B2 | Fresh-start through ending with physical controller and save/reload, no injected progression; Mattias playtest |
| PERF-001 | P1 | Codex | TODO | A2 | Profile representative clearing/campaign, set lower-spec target and asset budgets; LOD/streaming as measured |
| REL-001 | P1 | Codex | TODO | C1 | Windows export on clean environment/offline; licenses, version, save upgrade, recovery and package checksums |
| REL-002 | P0 | Codex+user | TODO | REL-001,QA-001 | RC triage zero critical/high, user acceptance, tagged reproducible1.0 build and release notes |

## Pull policy

Current active: Fable ART-001; Codex production foundation. Next Fable: ART-006 audit while waiting for head review. Next Codex: PROD-002 then SAVE-001/PROD-003, while reviewing new head deliveries. No one waits idle solely for the other if an owned READY task exists. Current art checkpoint remains protected: no uncontrolled character/world rebuild before A1.

## Ticket update format

ID / owner / status / peer commit consumed / files changed / checks actually run / evidence paths / remaining gaps / next dependency. BLOCKED includes the missing input and the next safe independent task. At3failed cycles attach a method review. DONE includes reviewer acceptance; final visual gates include user acceptance.


## Reconciliation after Claude58f629d

PROD-001 DONE on explicit peer acknowledgement; initial plan remains provisional.
ART-002 DONE as review, not aesthetic approval. ART-003 READY.
ART-004 proposal allowed now; Simm body mesh awaits ART-003 (part of A1).
ART-006 needs native scene evidence. ART-011 added below.
Fable scheduler expansion was refused: unattended capacity remains head-only
until user directly authorizes the broader schedule in Claude. Do not bypass.
Codex READY production tickets remain actionable despite that restriction.

| ID | Priority | Owner | Status | Depends | Deliverable / acceptance |
|---|---|---|---|---|---|
| ART-011 | P1 | Fable | TODO | ART-003 shape stable | Game-resolution head/hair, bake/LOD against sculpt at both cameras, counts/materials/source; budget from measured scene |
| EVID-001 | P1 | Codex | READY | none |3current native clearing frames: reference, alternate, gameplay zoom; no saving or live game disruption; unblock ART-006 |
