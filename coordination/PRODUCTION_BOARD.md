# SIMM production board

Canonical board maintained by Codex. Fable updates only its own delivery/proposal files; Codex reconciles them here at the next check. Links to commits/evidence are required before DONE. Forecast in PRODUCTION_PLAN.md. Initial board25November2026; historical implementations below are PARTIAL/REVIEW, not newly verified DONE.

| ID | Priority | Owner | Status | Depends | Deliverable / acceptance |
|---|---|---|---|---|---|
| PROD-001 | P0 | Codex | DONE | none | Publish plan/board/dispatch + GDD context; Fable acknowledges next check |
| PROD-002 | P0 | Codex | BLOCKED | PROD-001 | Local allowlisted74source-file packet prepared; automatic approval review blocked branch publication pending explicit user approval of source export |
| PROD-003 | P0 | Codex | DONE | eight-slice producer-reviewed discovery baseline | PARITY_TRACEABILITY.md covers GDD families, actual subset evidence and owned missing work; audit completion only, NOT runtime/browser parity |
| ART-001 | P0 | Fable | DOING | D1 diagnostic39e2270 reviewed | Stop per-lock tweaking: neither lever visibly helps; v012+m001-B held, no v013; consolidated A1 gaps ranked, hair frozen during clothing finish |
| ART-002 | P0 | Codex | DONE | ART-001 delivered | v007 native review/held meshes verified; codex_deliveries.md ART-002 evidence; A1 still pending |
| ART-003 | P0 | Codex | REVIEW | held fitted actor; native camp motion10:02 |384controlled physics/original-animation steps,192frames,2.1264m travel, socket position tracking pass. Flag shoulder/torch presentation; matched original control and full motion/contact/controller/performance/A1 acceptance pending; no live swap |
| ART-004 | P0 | Fable | REVIEW | p001 native review970029d held | f002+m002+p001 working finish/material baselines; geometry/palette freeze; full motion/contact depth/game-scale acceptance pending |
| ART-005 | P0 | Codex; Fable critique | REVIEW | A1-SIMM-REVIEW.md + native sheets11:30 | Consolidated reference/head/body/alternate/back/clay, camp and motion evidence; parity explicitly fails. Fable assigned <=3gap independent critique and ONE coherent next-method proposal only. Final A1 acceptance pending; no fitted live swap |
| ART-006 | P1 | Fable | REVIEW | L2 native controls e909d36 evaluated | L2 improves directional read/friendly face but occlusion/leak and floor wash remain; no accepted preset or automatic L3; hold assets pending native softness/occlusion evidence |
| RENDER-001 | P1 | Codex | DOING | local camera64 integration +fresh-instance travel/cave check | Current camp defaults64m locally after360step/26checkpoint PASS; live game not restarted. Baseline register updated; fitted actor/camp, torch/foliage/performance pending |
| ART-007 | P1 | Fable | TODO | A1 | Leina then Bronkings, rig-compatible idle/talk packets; approved identity refs, review per character |
| ART-008 | P1 | Fable | TODO | A1,ART-006 | Tent/workbench/forest/ground asset batches; one style family per packet; no collision/layout changes |
| RENDER-002 | P1 | Codex | TODO | ART-007/008 | Matched clearing camera/material/light integration, day/torch/readability; A2 user checkpoint |
| CORE-001 | P1 | Codex | DOING | clock/recovery/survival/frame/drop oracle slices | Work-only combined single-owner prototype17602assertions/64sequences passes. Actual defeat-recovery composition, non-saving native scene/frame mapping and production migration/fault paths remain; no live hook |
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

Current active: Fable critique41e98ba consumed; ART-014 E1 eye-only texture/material carrier packet assigned for native A/B. A1 still fails; geometry/costume/rig held. Codex native material inspection confirms emission1/roughness.42/specular.5. No fitted live swap/wider art; PROD-002 pending.

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
| ART-012 | P1 | Fable | REVIEW | ledger/helper3cc1c45 reviewed; native shell-stub audit | Source inventory and helper hardening delivered. Codex independently verified five pinned invocations and refusal guards; peer reports contaminated-shell Blender geometry/texture match. Selected v1 licence text and blocked source transport remain unresolved; no whole-project readiness or legal clearance |
| ART-013 | P1 | Codex | TODO | inherited tool diagnostics10:31 / rejected common tilt11:00 | Per-tool/per-state carry/action presentation with grip preserved and true turning/motion/depth controls; protect original rig/actions. Not fixed by a universal offset; known issue retained during A1 evidence preparation |
| ART-014 | P0 | Fable; Codex native review | DOING | independent critique41e98ba + native held material inspection | ONE E1 eye-only sRGB albedo + minimal material-carrier GLB on identical static eye geometry/UVs; no emission, roughness.55, source specular.25 with imported mapping checked. Native R1–R5 / stop rule before acceptance; non-eye assets/rig/save held |
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


### 09:00UTC native fitted camp checkpoint

RENDER-001 remains DOING: held fitted Simm assembled in memory inside persistfalse actual camp; original and fitted zoom10 plus fitted zoom4 day/torch captures reviewed.17rests/original animation-content digests/socket count preserved; all41runtime hashes match registered camera64 baseline. No runtime model swap or save access. See codex_deliveries.md and reviews/fitted-simm-native-camp.png. Static evidence does not close ART-003 motion/contact, ART-005 A1 or performance. Next Codex: actual camp-owned fitted movement/tool presentation in an isolated non-saving instance. ART-012 helper-hardening follow-up remains assigned to Fable; no new art revision.


### 09:31UTC ART-012 delivery consumed

Fable3cc1c45 hardens the v012 build helper and distinguishes PC evidence from missing Git transport. Codex inspected the four-file diff and independently ran the actual wrapper with a harmless Blender stub: all5calls pinned, experimental variables absent, absolute/nonempty guards and unchanged preexisting scratch output confirmed. Full Blender geometry/UV/texture rebuild remains Fable-reported, not independently repeated. ART-012 moves to REVIEW with no new model revision requested; selected-version licence text and PROD-002 transport remain open. Codex next: fitted camp movement/tool evidence per09:00 receipt. A1 unpassed; no live model/save changes.


### 10:02UTC fitted camp movement evidence

RENDER-001/ART-003 remain open: actual camp physics and explicitly advanced original animations exercised in persistfalse instance for axe/pickaxe walking/gather activation and torch walking.384steps/192frames,80foot poses,2.1264m travel; socket POSITION error max4.915e-7m; rests/actions/socket count and protected41runtime hashes preserved. See codex_deliveries.md and reviews/fitted-simm-native-camp-motion-samples.png / .mp4. Flagged tool proximity/overlap at shoulder and torch/face silhouette needs a matched original-actor control; do not infer fitted mesh fault or claim contact acceptance. Fable art remains held; no new revision assigned.


### 10:31UTC original/fitted tool negative control

RENDER-001/ART-003 remain open. Original actor reproduces shoulder/tool and side torch/face silhouette concerns at matching sample poses; no jacket/head rebuild justified by this evidence alone.384paired steps, identical clip times/local hand+foot pose strings; root difference max0.611mm. Six labelled native pairs reviewed, not geometric-clearance acceptance. Next Codex: grip-preserving in-memory carry transform calibration across multiple views/motion; no live changes. Fabled51af57 receipt consumed; no new Fable production task.


### 11:00UTC common carry tilt rejected

36static native captures preserve grip to1.20137e-7m and protected rests/actions/socket, but common20degree outward+15degree forward tilt trades frontal separation for blade/hair conflict and near-horizontal torch carry. No integration or further arbitrary offset sweep. ART-013 tracks inherited per-tool/per-state presentation; zero static projected AABB overlaps do not cover the flagged interpolated turn. Next Codex ART-005 consolidates concrete Simm A1 review evidence with known issues; A1 still unpassed. See latest receipt and reviews/native-tool-carry-rejected.png. Fable held; runtime/live game/save untouched.


### 11:30UTC consolidated A1 packet

A1-SIMM-REVIEW.md links checksum-verified new native/reference and multi-view sheets plus previous camp/motion evidence. Held model/rig/save intact; verified native run passes preservation checks, not visual parity. Codex verdict: A1 fails on remaining face/eye, hair and costume finish gaps. Fable now assigned one source-informed independent critique and coherent method proposal; no new asset/L3 production. ART-005 REVIEW, not USER_APPROVED or ready for wider art integration. See current dispatch.


### 12:00UTC independent CORE-001 drop/recovery boundary

While Fable A1 critique is pending, local adapter validated2060assertions over54source-function sleep/repeated-sleep/defeat/save-projection/reload/next-active sequences. Immediate sleep saves retain zero-lifetime expired entries; next active strict expiry prunes, including dt0. Projected payloads pass real full v4 validator. No production/save-file/scene wiring; CORE-001 stays DOING for single-owner combined integration and migrations. Evidence/limits in CORE-001-CONTRACT.md; code remains local behind PROD-002. Live game/rig/save untouched; art dispatch unchanged.


### 12:31UTC critique reviewed / E1 bounded packet assigned

Fable41e98ba critique and Blender demo consumed. Native held-eye inspection confirms emission factor/energy1 and roughness.42, but Godot specular.5 differs from Blender/glTF representations. ART-014 authorizes only E1 eye texture/material carrier export, original eye geometry retained by Codex; no head/rig/body revision. A1 remains unpassed, R1–R5 and stop rule apply. See latest receipt for exact packet/native-review contract; source transport still approval-blocked.


### 13:00UTC single-clock-owner composition

Local combined prototype passes17602assertions over64actual-source-slice sequences/704steps: one clock advance and one effect/invulnerability prefix, with drop/night/survival/fuel ordering and pause/death gates. Mid-update death retains source current-frame world advance; subsequent death recovery remains stubbed. CORE-001 still DOING, no live/save/migration wiring. All code local behind PROD-002. Fable ART-014 E1 task unchanged; next art delivery awaits native review.
