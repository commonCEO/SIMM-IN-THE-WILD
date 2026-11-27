# SIMM production board

Canonical board maintained by Codex. Fable updates only its own delivery/proposal files; Codex reconciles them here at the next check. Links to commits/evidence are required before DONE. Forecast in PRODUCTION_PLAN.md. Initial board25November2026; historical implementations below are PARTIAL/REVIEW, not newly verified DONE.

| ID | Priority | Owner | Status | Depends | Deliverable / acceptance |
|---|---|---|---|---|---|
| PROD-001 | P0 | Codex | DONE | none | Publish plan/board/dispatch + GDD context; Fable acknowledges next check |
| PROD-002 | P0 | Codex | BLOCKED | PROD-001 | Local allowlisted74source-file packet prepared; automatic approval review blocked branch publication pending explicit user approval of source export |
| PROD-003 | P0 | Codex | DONE | eight-slice producer-reviewed discovery baseline | PARITY_TRACEABILITY.md covers GDD families, actual subset evidence and owned missing work; audit completion only, NOT runtime/browser parity |
| ART-001 | P0 | Fable | DOING | D1 diagnostic39e2270 reviewed | Stop per-lock tweaking: neither lever visibly helps; v012+m001-B held, no v013; consolidated A1 gaps ranked, hair frozen during clothing finish |
| ART-002 | P0 | Codex | DONE | ART-001 delivered | v007 native review/held meshes verified; codex_deliveries.md ART-002 evidence; A1 still pending |
| ART-003 | P0 | Codex | REVIEW | held headv010/jacketv004/collarv004/bootsv002 |168frame native idle/walk/corrected-study-gather video and socket/rest checks delivered; full playback/camp motion/controller/performance acceptance pending; no live swap |
| ART-004 | P0 | Fable | REVIEW | p001 native review970029d held | f002+m002+p001 working finish/material baselines; geometry/palette freeze; full motion/contact depth/game-scale acceptance pending |
| ART-005 | P0 | Codex | TODO | ART-003/004 | Simm user checkpoint A1 with side-by-side and motion evidence; integrate only after validated fit/quality |
| ART-006 | P1 | Fable | REVIEW | L2 native controls e909d36 evaluated | L2 improves directional read/friendly face but occlusion/leak and floor wash remain; no accepted preset or automatic L3; hold assets pending native softness/occlusion evidence |
| RENDER-001 | P1 | Codex | DOING | local camera64 integration +fresh-instance travel/cave check | Current camp defaults64m locally after360step/26checkpoint PASS; live game not restarted. Baseline register updated; fitted actor/camp, torch/foliage/performance pending |
| ART-007 | P1 | Fable | TODO | A1 | Leina then Bronkings, rig-compatible idle/talk packets; approved identity refs, review per character |
| ART-008 | P1 | Fable | TODO | A1,ART-006 | Tent/workbench/forest/ground asset batches; one style family per packet; no collision/layout changes |
| RENDER-002 | P1 | Codex | TODO | ART-007/008 | Matched clearing camera/material/light integration, day/torch/readability; A2 user checkpoint |
| CORE-001 | P1 | Codex | DOING | PROD-003 baseline reviewed | Isolated foundation +2496actual-frame gate checks PASS; outer pause/death semantics and duplicate-clock risks mapped; single-owner orchestration/sleep-drop adapter/live integration pending |
| CORE-002 | P1 | Codex | TODO | PROD-003 | Quest data/journal/NPC six identities and one-time exchange rewards; atomic full-bag behavior |
| CORE-003 | P1 | Codex | TODO | CORE-001/002 | Bronkings home order/upgrade/three-day-or-rest/interiors, preserve furnishings/clear doors; B1 controller journey |
| CORE-004 | P1 | Codex | TODO | PROD-003 | Audit all48recipes/context gates and ingredient reachability; baseline25nonbuilding already reported locally, revalidate gaps only |
| CORE-005 | P1 | Codex | TODO | CORE-003 | Full biome/height/scene/world transitions, cave+dungeon+volcano and scene-local saves; campaign map |
| CORE-006 | P1 | Codex | TODO | CORE-005 | Combat/AI/Nups campaign interactions, fishing/boat/whale/rainbow, journal/ending; B2 full journey |
| ART-009 | P1 | Fable | TODO | A2,CORE-005 spec | Remaining NPCs, enemies/animals/biomes/interior/boat/ending assets in dependency order; manifest packets |
| UX-001 | P1 | Codex | TODO | PROD-003 | Complete quest/build/map tabs; exact controller context/focus/scroll; UI parity and EN/ET at3resolutions |
| ART-010 | P2 | Fable | TODO | A2,UX-001 spec | Approved icon/UI illustration and world feedback art; source/license/export evidence |
| AUDIO-001 | P2 | Codex | TODO | B1 | Baseline sound behavior and volume/mute, gather/craft/damage cues; no unlicensed external audio |
| SAVE-001 | P0 | Codex | DOING | local sources; remote snapshot approval pending | Migration/save compatibility matrix and isolated test harness across supported local versions; no native save publish |
| ADD-001 | P2 | Fable | TODO | A2 | Bucket/penguin/boss design proposals grounded in Mattias's drawings; separate assumptions/questions from approved facts |
| ADD-002 | P2 | Codex | BLOCKED | ADD-001 design gate | Size user additions for beta, assign implementation/art packets; no invented combat mechanics; record deferrals explicitly |
| QA-001 | P1 | Codex | TODO | B2 | Fresh-start through ending with physical controller and save/reload, no injected progression; Mattias playtest |
| PERF-001 | P1 | Codex | TODO | A2 | Profile representative clearing/campaign, set lower-spec target and asset budgets; LOD/streaming as measured |
| REL-001 | P1 | Codex | TODO | C1 | Windows export on clean environment/offline; licenses, version, save upgrade, recovery and package checksums |
| REL-002 | P0 | Codex+user | TODO | REL-001,QA-001 | RC triage zero critical/high, user acceptance, tagged reproducible1.0 build and release notes |

## Pull policy

Current active: local camera64 integrated for new camp instances; use work/simm-runtime-baseline-camera64.json (old baseline intentionally differs for camp.gd only). Next Codex fitted actor in non-saving camp; Fable ART-012 readiness ledger, ART-006 REVIEW. A1 unpassed; no fitted live asset swap or wider art production. PROD-002 publication awaits approval.

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
| ART-012 | P1 | Fable | DOING | ledger87e6989 +PC evidence supplement reviewed | Three source blob hashes verified; native textures byte-identical procedural scratch rebuilds. Pin cold-helper env/refuse nonempty output and update ledger; selected v1 licence text/source transport still open |
| EVID-001 | P1 | Codex | DONE | none |3current native clearing frames: reference, alternate, gameplay zoom; no saving or live game disruption; unblock ART-006 |


## Scheduler scope resolved; source snapshot approval pending

Claude3b2a1bee777ebf0576ae3add1afeb144f04bf7cb reports direct user scheduler scope authorization at21:07UTC. Broader unattended Fable tickets now enabled. PROD-002 publication blocked by automatic approval review: broad local source export needs explicit approval. No workaround. ART-003 and EVID-001 remain independent READY tasks; local SAVE-001/PROD-003 audit may proceed without remote snapshot.


## SAVE-001 first evidence packet

Local isolated-project audit: progression, inventory(after stale37->38bucket expectation fix), companion129checks and bucket save tests PASS. v3dedicated fixture, malformed-file/IO-failure suite and campaign migration remain TODO. See SAVE_COMPATIBILITY_AUDIT.md. Native user save never opened or written; runtime unchanged, one local test correction only. PROD-002 source publication still blocked pending user approval; no retry/workaround.


## ART-003 initial fit delivered; ART-004 first packet READY

Native full-body v007 fit confirms exposed neck, short boxy jacket and tall trouser/low shoe silhouette. Fable optionB allowed for hood/scarf ONLY in first packet, new geometry chest-bound100%, no existing weight/rest/action edits. Full body mesh/boot changes not yet assigned. A1 still pending. ART-003 REVIEW until continuous motion/socket/game-scale/performance evidence. Evidence in codex_deliveries.md. Source snapshot approval still pending; no retry.


## EVID-001 native clearing packet delivered

Three checksum-verified frames in coordination/reviews/: current reference composition study, its alternate, and non-saving fresh-state camp at gameplay zoom. ART-006 READY for evidence-based re-ranking. Study and gameplay placements differ; screenshots are correctly labelled. Current runtime assets shown, NOTv007head or upcoming hood. No player save loaded/written. See latest receipt. Broader art mesh gate unchanged.


## SAVE-001 synthetic boundary coverage advanced

295explicit checks PASS in separate audit project: validv3->v4roundtrip without rewriting original, pre-bucketv4, transactional malformed/oversize/future rejection and failed-write preservation. Harness setup error corrected before successful run. Expected malformed-JSON diagnostic documented; no clean-log overclaim. See SAVE_COMPATIBILITY_AUDIT.md. OS crash/disk-full/permission faults and campaign migrations remain untested. No production gameplay/save writes; source publication still pending.


## PROD-003 first-loop audit slice

PARITY_TRACEABILITY.md maps8active flows to browser source, local Godot functions and concrete missing evidence. Confirmed automatic day/survival/rest, NPC exchange/home service and map/localization gaps. No implementation/test pass claimed; code inspection only. CORE-001 then CORE-002/003 is the functional critical path. Remaining recipes/world/combat/controller audit still queued. Source publication approval remains pending; report contains findings only.


## Jacketv001 native review

Original17bone rests matched and candidate skin bound to original animated skeleton in memory. Rounder shape but raw cuffs/front, floating button, reported hand intersection/strap gaps remain. Partial26vertex weight-comparison gap must close. Bounded v002 brief published; ART-004 DOING, no live integration. All41runtime files unchanged.


## PROD-003 crafting slice verified

25non-building oracle/source-hash check PASS;651crafting assertions PASS in isolated audit project. Full building-context mapping and real unaccelerated ingredient journey remain. PARITY_TRACEABILITY.md distinguishes seeded transaction tests and historical accelerated supply coverage from native player-flow proof. No implementation change.


## Jacket method review before v003

Nativev002 shows high side vents/split-tail silhouette and detached cuff rings. Fable must propose shorter original-weight hem vs explicitly localized candidate hem-weight exception; no master-rig/weight change authorized yet. Keep protected source, rest/actions/socket exact. ART-004 DOING method proposal; no further full export until reviewed. No user decision required for proposal preparation.
