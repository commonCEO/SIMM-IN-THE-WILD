# SIMM production plan through 1.0

Owner: Codex (producer/integration). Art lead: Claude/Fable. Updated 25 November 2026.
Working baseline, not a promised release date. User requested a hands-off two-agent production plan.

## Product and scope

1.0 is a complete offline single-player Windows adventure: the browser 0.6 campaign and controller/UI behavior rebuilt in Godot, with a coherent reference-led 3D art style, durable saves, EN/ET, and a tested downloadable build. It is not merely a prettier clearing. GDD document version1.0 is NOT the game's release version.

Sources: [GDD](../docs/GAME-DESIGN-DOCUMENT.md), [data](../docs/GAME-DESIGN-DATA.md), browser src/game.js and src/model.js, approved original reference, NPC references and explicit user decisions. Browser behavior wins over accidental prototype simplifications. Record intentional 3D exceptions.

Committed scope: 48 baseline model recipes with context restrictions; 13 skills; 37 baseline item types; six quest NPCs; three home plans; gathering/crafting/stations/storage/farming; survival/day/night/sleep/defeat; bow/melee/fishing; Nups; campaign regions/dungeon/volcano; boats/whale/rainbow; journal and star-beacon journey. These counts describe the browser baseline, not proof of completed Godot systems.

User additions: bucket recipe (1wood+10iron ore, already locally implemented), penguin, Mattias's three bosses. Track explicitly outside browser parity. Bucket use, penguin behavior and boss encounters need a design specification; do not silently invent their rules. Reserve a late content lane, estimate after design. No multiplayer, live service, console/mobile ports, monetization or paid generators in this plan. Storefront launch is separate from a Windows1.0 build.

## Honest starting point

Local Windows prototype has gathering, inventory/crafting, skills, charged bow, stations/crops and Nups subsets plus authored placeholder-quality art. Verification reports and fixtures exist; campaign-wide parity is unverified. GDD parity register is dated20Nov and must be refreshed against code. Most local Godot development is uncommitted and absent from Claude's checkout. Read-only access to Git does not expose it.

Art: Claude v006 head imported in isolated Godot studies; still changes_requested. Live Simm remains the earlier rigged model. Rig and save remain protected. Camp/NPC/environment assets are unapproved for final art parity. A clean parser or a high triangle count is not visual acceptance.

## Gates and deliverables

| Gate | Result | Exit evidence | Depends |
|---|---|---|---|
| P0 production foundation | Shared board, readable source baseline, scoped collaboration | Both owners acknowledge packets; current Godot inventory recorded; safe scoped code snapshot accessible remotely | none |
| A1 Simm benchmark | Head, body/clothes and original animations read as the approved child character | Native reference/clay/alternate views, game-scale fit, idle/walk/gather/socket, performance measurement; user visual checkpoint | P0 |
| A2 approved clearing | Simm, Leina, Bronkings, tent/workbench, forest/ground/UI read as one scene | Reference-camera full clearing plus playable route, calm camera, soft clean shadows day/torch, readable UI; user visual checkpoint | A1 |
| B1 complete first loop | Fresh start -> gather -> craft -> station -> Leina delivery -> order home -> enter/furnish -> save/reload | Physical controller journey without injected materials/time/XP, pause-safe clock, no resource softlocks, old-save migration fixtures | P0; A2 for visual acceptance |
| B2 browser campaign alpha | All baseline systems/regions and ending reachable | Traceability matrix covers every GDD flow; normal-time full journey; blocked actions atomic; scene-local drops/Nups and transitions correct | B1 |
| C1 content complete beta | Campaign art/audio/UI consistent; agreed additions implemented or explicitly deferred | Every encounter readable; EN/ET full menus; 720p/1080p/4K; performance budgets met; license inventory | B2, A2 |
| R1 release candidate | Feature freeze, installable Windows build | Clean-machine launch offline; save upgrade/recovery; controller-only completion; zero open critical/high bugs; export/package checksum | C1 |
| 1.0 | Versioned release package and recovery instructions | User accepts RC playthrough; tagged source/assets, reproducible build, release notes, local rollback backup | R1 |

No downstream art mass production until A1 establishes the reusable character/material standard. Gameplay audit and export/save infrastructure may run in parallel without changing visible art. Completing a task does not approve the entire gate.

## Gantt-style forecast (relative weeks)

W1 starts with production-plan acknowledgement. This is a capacity hypothesis, not a calendar commitment. Reforecast after two accepted art packets and the parity audit. One review cycle can be an hour or several revisions; elapsed hourly checks are not productive hours. Initial planning envelope16-24weeks, low confidence, including rework; dates follow measured throughput.

| Lane / owner | W1-2 | W3-4 | W5-6 | W7-8 | W9-10 | W11-12 | W13-14 | W15-16 | W17-24 |
|---|---|---|---|---|---|---|---|---|---|
| P0 baseline/audit / Codex | ACTIVE | close | | | | | | | |
| A1 Simm / Fable+Codex | ACTIVE | gate/rework | | | | | | | reserve |
| A2 clearing art / Fable | research | build | build/gate | | | | | | reserve |
| B1 first loop / Codex | audit | build | build/gate | | | | | | reserve |
| Campaign systems / Codex | | | spec | build | build | alpha gate | | | reserve |
| Campaign assets / Fable | | | packets | build | build | build | content gate | | reserve |
| UI/audio/localization / both | inventory | style | | implement | implement | review | beta gate | | reserve |
| Agreed additions / both | design queue | | | | spec gate | build if sized | review | | reserve |
| QA/performance/save / Codex | baseline | continuous | continuous | continuous | continuous | full journey | beta | RC | rework |
| Release / Codex+user | | | | | | | | package | 1.0 after gates |

Critical path: A1 -> A2 -> coherent campaign assets -> C1 -> R1 ->1.0. Parallel functional path P0 -> B1 -> B2 must also reach C1. Neither branch can substitute for the other. If A1 slips, do audits/tooling/asset specifications, not ten uncalibrated NPC sculpts. Reserve rework capacity rather than promising fixed dates.

## Staffing and throughput

Fable owns Blender sculpt/model/UV/material/rig-compatible asset production, reference analysis, art packet manifests, and visual-method proposals. It should take the larger production volume because the user has more plan capacity there. Codex owns Windows/Godot integration, gameplay parity, save migration, controller journeys, renderer experiments, performance, packaging and producer board. Fable can draft data/tests/specs from committed browser sources, but cannot attest to the native PC or edit shared live gameplay without a dedicated assignment.

Each owner has max1 active implementation task plus1 review/preparation task. Fable queues art specifications while Codex integrates; Codex audits/save-tests while Fable sculpts. Avoid duplicate same-asset production. Each scheduled check consumes a changed peer delivery or advances an unblocked owned ticket. No-op checks are cheap and quiet. Codex30min; Fable hourly at minute06UTC, confirmed from its receipt. Do not reconfigure Fable's scheduler from Git.

## Quality, safety and release policy

Done means source + export + checks + native evidence + board acceptance. Statuses: TODO, READY, DOING, REVIEW, BLOCKED, DONE; art may be READY_FOR_USER_REVIEW but never USER_APPROVED without the user. Every ticket states owner, dependency, deliverable, test and scope fence. Reviewer returns one prioritized brief. Three cycles without visible improvement trigger a construction/method review rather than more cosmetic iterations.

Latest native save is never overwritten by a fixture or old backup. New-game tests use isolated user data/persist=false. Migrations are additive and tested with copied legacy fixtures. Preserve original rig/rest/actions/socket; file-level backup and rollback for each integration. Native user save is never published. Dirty main is never reset/switched/staged wholesale. Publish intentional code/assets only after scoped review.

Provisional performance target: stable60fps at1080p on this RTX4080 PC, with measured CPU/GPU frame time and peak memory; this is not a minimum-spec promise. Record a representative lower-spec target during B1. Set per-asset budgets after A1 captures; no invented poly budget before measuring the scene. No paid service usage or reference uploads without explicit authorization.

User only needs high-value checkpoints: Simm benchmark, clearing, first-loop playtest, campaign beta, RC. Batch other design questions in the decision log; proceed on reversible technical choices. Do not call an automated test a child's usability approval.

## Risks and change control

| Risk | Action / owner |
|---|---|
| Endless art micro-iterations | Compare matched views, freeze accepted components, change construction after3stalled rounds / both |
| Local-only code means blind peer planning | Scoped remote snapshot of relevant code/docs, no saves/vendor caches / Codex |
| GDD outdated or prototype treated as parity | Per-system code-to-fixture-to-journey matrix / Codex |
| User's active save harmed | Isolated test state, migration fixtures, backups/rollback / Codex |
| Scope grows faster than production | Baseline vs additions labels, design/estimate gate before scheduling / producer |
| Platform/plan limits or cloud reset | Versioned sources + receipts; pause dependent ticket, advance other READY work / both |
| Soft shadows hide geometry problems | Clay/alternate shape gate, separate renderer and material A/B / Codex |

Release blockers: lost/corrupted save, campaign softlock, controller-only dead end, unrecoverable crash. High bugs break a required system; medium bugs have safe workarounds; low bugs are cosmetic. RC permits no critical/high, and no medium that blocks the intended fresh-start journey. Known low issues documented. User approval required for material scope cuts, final artistic acceptance and release publication; routine local fixes and delegated peer deliveries proceed.
