# PROD-003 parity audit: first-loop blockers

26November2026. Code inspection of current LOCAL Godot source against browser0.6
and GDD sections4,7,8,11-14. First bounded slice, not the complete parity audit.
No gameplay code or save schema changed; no tests run in this audit turn.
The blocked remote source snapshot is still unpublished, so peer readers should
not assume their old cloud godot/ matches the local locations cited below.

## Status vocabulary

PRESENT means inspected implementation exists, not end-to-end acceptance.
PARTIAL means a working subset differs materially. MISSING means the reviewed
active flow lacks the required operation; not merely an unsuccessful keyword
search. UNVERIFIED means outside this slice. Planned tests below are not passes.

## Traceability

| Flow / GDD | Browser source of truth | Inspected Godot active path | Status / consequence | Ticket / required evidence |
|---|---|---|---|---|
| Day/night and hunger,8 | model.js advanceTime; game.js update | camp.gd _tick_inventory_state increments world_age; set_evening changes lights; progression has no day/time/nights fields | PARTIAL: regrowth/effect world time exists, automatic day clock/hunger drain do not. Light toggle is a test aid, not parity | CORE-001: exact300day+60night boundaries, pause/menu freeze, wrap/multiple-day dt, hunger rate and old-save defaults |
| Sleep,8 | game.js sleepUntilMorning/extraInteract | camp interactions and progression serialization reviewed; no sleep/time-transition operation | MISSING: no normal rest advancing day, night count, home completion and regrowth together | CORE-001: rest preserves stock, max-health restore, hunger/thirst floors, elapsed-time and order completion once |
| Defeat,8-9 | game.js damagePlayer -> beginDeath; GDD defeat flow | camp.gd damage_player resets health/hunger/thirst, exits cave, moves to camp, resets hostile states | PARTIAL: supplies retained and hostile reset exist; complete browser day/defeat flow not restored | CORE-001: compare actual beginDeath/recovery flow before implementing; no repeated attack lock, scene-local drops/Nups retained |
| Quest journal,7-8 | model.js questSteps; active browser journal UI | camp_menu.gd _build_other journal branch has fixed first-pickaxe objective | PARTIAL: one static objective, not campaign journal or six NPC exchange statuses | CORE-002/UX-001: dynamic stages/details/focus, rewards and state after reload |
| NPC exchange,8 | model.js finishNPCQuest; game.js NPC modal | camp.gd try_interact branches for Leina/Bronkings play talk and show hints; progression serialized fields have no npcQuests | MISSING in active NPC path: no delivery transaction, one-time reward or six-character quest state | CORE-002: full-bag refusal atomic, requested items deducted once, rewards/35XP once, migration and reload |
| Bronkings home service,8 | model.js housePlans/orderHouse/completeHouse; game.js houseServiceRecipe | active Bronkings interaction is pickaxe hint; no home/order/day/interior state in progression serializer | MISSING: recipe data alone would not implement ordered prefab home | CORE-003 after CORE-001/002: one payment,3days/rests, all3plans, blocked plot reason, clear door, upgrade preserves furnishings |
| Map tab,7 | browser active map flow and0.6world | camp_menu.gd _build_other non-journal branch explicitly says not ported | MISSING active content, despite six-tab frame existing | UX-001/CORE-005: region/position/scene information and controller interaction; needs full world contract |
| EN/ET,7 | src/i18n.js and language preference flow | TAB_NAMES/CATEGORY_NAMES plus active item descriptions and hints are hardcoded ET | PARTIAL UI text; no complete language preference/translation system | UX-001: ENdefault, independent persisted preference, no clipping at720p/1080p/4K, controller focus stable |

Code anchors inspected: camp.gd170(_tick_inventory_state),509(menu gate),
653(test evening input),733(NPC hint branches),804(set_evening),1336(damage_player);
camp_menu.gd14/20(text),1019(_build_other); progression.gd425(_valid_save),
600(save_game),615(load_game). Line numbers describe today's local source,
not old remote runtime. Inspect functions again if the code changes.

## Concrete contract findings

- Browser advanceTime reduces hunger by0.045per active second, advances worldAge,
  and wraps time at360seconds. Night begins at300. Godot's resource clock must
  not be deleted or reset when introducing the day clock.
- Browser sleep consumes the remainder of the day cycle, increments day/nights,
  restores health and applies hunger>=25/thirst>=50. It also advances completion
  and regrowth. This differs from Godot's current defeat full-hunger/thirst reset.
- NPC exchange is a transaction: payment and all rewards fit before committing,
  then one completion bit and35XP. Merely displaying a task does not meet it.
- House plans are services with full base cost, not discounted normal crafting:
  level1=25wood/15stone/6fiber; level2=45wood/12slab/4iron;
  level3=60wood/20slab/8glass/3crystal; each3days. No old modular exterior-house
  system should be resurrected because its recipes remain in the data model.
- Current v4 save validation rejects unknown fields. Adding quest/day/home state
  without a deliberate version/default/validation strategy would break loads.
  Preserve current optional fields and stable IDs; use synthetic fixtures first.

## Implementation order and scope

1. Define a single active-time contract for CORE-001. Reuse existing world_age,
   add day/time defaults without altering old quantities/skills/Nups. Specify
   exactly how historical saves seed the clock; do not infer actual past days
   from a prototype light toggle. Local migration design/test first.
2. Implement day/survival/rest/defeat as one bounded rules slice plus UI feedback,
   not a map/NPC expansion. Check current browser recovery before choosing values.
3. CORE-002 uses immutable NPC data and atomic transactions. UI can display
   locked/complete tasks without accidental activation by focus.
4. CORE-003 consumes the real day/quest contracts and handles homes/interiors.
5. QA first-loop fresh journey without injected stock/time/XP; then expand map.

The new source-publication approval remains pending. This audit is prose findings
only; it is not a workaround publishing the blocked code payload. Existing local
implementations of inventory/crafting/skills/bow/Nups remain unchanged.

## Coverage still queued

Recipes/station reachability; gathering/targeting/heights; inventory/chest edges;
charged bow/melee/wildlife; skills/Nups; crop/fuel placement; scenes/world events;
boats/whale/rainbow/volcano; save migration across the full campaign; controller
and localization journeys. Their prior fixtures/reports must be mapped to exact
requirements and remaining native tests before PROD-003 can be DONE.

## Second bounded slice: crafting/stations and ingredient evidence

26November2026. Revalidated current source fixture and executed existing
crafting_parity.gd in the separate minimal audit project/user-data namespace.
No production code/fixtures changed; player save never accessed. Native4.7.2.

| Requirement | Evidence actually checked now | Result / limit |
|---|---|---|
| Browser non-building recipe catalogue | node godot/tests/export-crafting-fixture.mjs --check | PASS:25recipes plus current model/game source hashes match stored oracle |
| Costs/output/flags and skill discount | crafting_parity.gd compares browser-derived fixture to Progression | PASS within651total assertions: all25non-building recipes and craft levels0..3 |
| XP/equip/ownership | Same suite | PASS:8XP, no autoequip, ownership/upgrade conditions |
| Cooking/smelting/fuel | Same suite using synthetic station context | PASS fuel transaction/gates; does not prove native menu feel or world station reachability |
| Capacity/nearby chest/failure rollback | Same suite | PASS rules within the suite; inventory seeded for isolated transactional tests |
| Crafting/world-object save state | Same suite | PASS current schema roundtrip and invalid fuel rejection; no native player save used |
| Remaining building and home service | camp_menu.gd _visible_recipes and camp.gd _begin_station_build inspected | Only fire/furnace/chest/garden/nest have active placement support; data presence is not playable home/interior/boat/beacon completion |
| Ingredient gathering journey | resource_journey.gd read only, prior report reviewed | Historical automated coverage; test relocates player directly and advances world_age for crops/regrowth. NOT a normal-time controller-only journey |

Actual output: `PASS:651 browser recipe, station, transaction, XP and save
assertions.` Exit0, no runtime errors in work/crafting-audit-current.log.
Independent oracle check also exit0. Counts include internal assertions, not
651distinct player flows. This slice does not re-run resource_journey or
station_menu/stations_world; their historical reports remain historical.

The approved bucket is an extra recipe outside the25browser non-building
records. Its isolated recipe/save test was exercised in SAVE-001, not silently
added to the browser oracle. Existing crafting suite prepares inventory for
each recipe; it cannot certify that all ingredients can be gathered in the
campaign or that the starting resource budget is sufficient.

### Remaining CORE-004 work

Map every building record to its intended0.6UI context, active placement
operation and actual world constraints. Keep obsolete modular-house data
hidden as required; implement Bronkings service separately. Trace each
ingredient to a real source in each intended region, plus bootstrap/capacity
and depletion cases. Then run an unaccelerated first-loop controller journey.
The25recipe rules are validated; entire crafting/world parity is still partial.


## Third bounded slice: skill purchases versus playable skill effects

26 November 2026, 08:58 UTC check. Peer art tip unchanged at 883d0b4; advanced independent PROD-003 audit rather than duplicating art work. No production source/schema changes.

- Browser fixture/source check: `node godot/tests/export-skills-fixture.mjs --check` PASS: 13 skill records and 456 browser purchase cases match current model/game source hashes.
- Existing `skills_parity.gd` executed in the separate save-audit project, without its optional real-save-backup argument. Its Progression and recipe_catalog copies were SHA256-identical to current local production sources.
- PASS: 2,339 catalogue, prerequisite, rank/point mutation, health/charm, earned-point and synthetic save assertions. Exit 0; no errors in `work/skills-parity-audit-current.log`. Counts are assertions, not player journeys. Temporary skill saves were created/deleted only under the isolated application's user-data namespace.

| Requirement | Inspected evidence | Current conclusion / missing proof |
|---|---|---|
| Four branches, 13 nodes, 22 total ranks; prerequisite and one-point costs | Current browser-derived purchase oracle and passing native suite | Rules validated within these cases; not physical-controller acceptance |
| Injury-preserving combat/guardian health increases and charm stacking | Same suite, including injured states | Validated purchase behavior and synthetic roundtrip |
| Skill selection versus purchase | camp_menu _build_skills, _skill_mouse, select_skill, upgrade_action and _input read | Single click selects, double click learns; A/Enter activates once per press with release latch; source path PRESENT, not newly exercised here |
| Menu focus/scroll/layout | skills_controls.gd read only | Historical scripted event/geometry checks at 720p/1080p/4K; not rerun, not visual QA or actual controller proof |
| Earn points, buy combat/quickdraw, craft bow | skills_journey.gd read only | Historical automated integration: teleports to harvest positions and directly ticks bow charge; not an unaccelerated physical-controller journey |
| Quickdraw/combat bow effects | bow_combat.get_stats and skills_rules.gd read | Present formula: 0.78s versus 1.2s full charge, combat/quickdraw damage additions. This slice does not execute projectile/combat effects |
| Craft/mason/smelter | progression recipe_cost/craft/add_fuel; preceding crafting audit | Implemented and transactional craft slice already validated; skill purchase alone is not station/world reachability |
| Gather/logger and angler | resource_rules.collect and camp fishing completion | Present yield/damage and two-fish branch; no fishing world journey newly verified |
| Star/frost/helper | camp_companion follow/work/slow functions | Present implementation paths; dedicated companion behavior audit still queued |
| Leap, two ranks | Browser model canStep and game jump; complete local scripts search and active movement paths | MISSING active effect: local leap is in catalogue/purchasing, but local scripts have no jump/height traversal implementation consuming it. A point can buy a rank whose promised movement effect is absent |

The leap gap belongs to CORE-005's terrain/height/jump contract and UX-001's honest skill availability/feedback. Preserve the exact browser definition (one additional terrain step per rank during jump); do not silently substitute speed or invent a new 3D bonus. Purchasing metadata parity does not mean all 13 skill effects are playable. Before B2, require both ranks to cross the appropriate terrain boundaries, ordinary movement and no-jump rejection, boat/interior/context constraints and save/reload state.

Still queued: companion and combat effect parity; full terrain traversal; normal-time controller journey; EN/ET and visual menu QA. PROD-003 remains DOING. No native user save opened; no optional backup fixture supplied. This publication contains audit findings only, not the still-blocked local source payload.


## Fourth bounded slice: Nups state, skill effects and world contexts

26 November 2026, 10:01 UTC check. No new peer delivery after 5c59b7a; Fable's collar seating packet remains assigned. This is an independent code/oracle audit, not a fresh native companion integration test.

`node godot/tests/export-nups-fixture.mjs --check` PASS: 151 companion oracle cases match current browser sources. The oracle executes browser slowed/updateAlien in a VM and checks selected source tokens; it covers aura boundaries, unobstructed following and successful nest output. Its blocked function always returns false and its addOrDrop stub always succeeds: it does not prove obstacle handling or failure transactions. It does not execute the entire browser game.

| Contract | Local path inspected | Result / limit |
|---|---|---|
| Arrival | camp_companion.tick, camp._tick_inventory_state | Local persisted companion_clock >55 active seconds; browser arrival is time>55 OR day>1. PARTIAL while day/sleep is absent; a future sleep/day migration must preserve first-arrival semantics |
| Greeting | camp_companion.greet | Surface/strict55px range, 6 star and 35 XP once, follow enabled; fallback drop present. Ordinary path PRESENT; exhausted drop capacity differs as below |
| Follow/wait and contexts | command, move_scene, tick; camp input/build/menu routing | B/T waits; resume only same cave flag and strictly within95px. Build cancel and open-menu handling precede world command. Surface/cave subset PRESENT; interiors and multiple campaign region identities missing |
| Follow movement | tick and camp.companion_blocked | 28px trailing offset, >10px dead zone, 105px/s, axis-separated blocking through shared arrow/world obstruction helper, all at32px/m. Needs real-world navigation and doors/height/region tests |
| Frost/Star aura | slowed and enemy_speed_factor | Strict100/160px radius; same-scene/friend/follow gates; enemy factor max(.25,.6-.08*Star), predator factor .45. Implementation PRESENT; historical nups_parity script tests these but was not rerun now |
| Nest/Helper | tick waiting surface branch | Strict120px proximity, interval35/(1+.5*Star), yield2/4, one payout per tick, partial counter retained when leaving range. Existing tests and journey accelerate ticks; not normal-time play proof |
| Persistence | progression companion fields, nups_save and prior SAVE-001 audit | Companion129-check save suite passed previously; current turn does not repeat it or claim fresh runtime behavior proof |

### Differences and explicit exceptions to resolve

- Browser updateAlien returns immediately inside a house. Local camp has no interior context; when CORE-003 adds interiors, it must suspend companion follow/work as in the browser, not accidentally let an outside nest produce during an indoor menu/room stay. Surface Nups working while player is in a cave is a separate existing browser behavior.
- Local greeting aborts if both inventory and world-drop creation fail (drop cap4096 or exhausted ID space); browser marks friendship and grants XP before calling addOrDrop. Local work resets its counter only after successful add/drop; browser resets it before addOrDrop even if that fails. These are transactional safety differences under exhausted-capacity conditions, not covered by the151-case successful-output oracle. Record and decide intentionally before claiming exact parity; no behavior changed here.
- Existing nups_parity.gd explicitly documents a deliberate browser bug fix: waiting surface Nups overflow is assigned to the surface even when the player is in a cave. The browser helper inherited the player's scene and could strand berries. Treat this as a tracked exception, not an unnoticed exact match.
- Native companion scene identity is only alien_in_cave plus outside/cave drop tags. CORE-005/006 must define campaign region/room identities so a waiting companion cannot appear in every region sharing the same boolean.
- nups_journey.gd directly advances55.01seconds, relocates the player to resource slots and advances nest production by a large tick; nups_controls injects events. Useful historical integration coverage, not an unaccelerated physical-controller journey. These scripts were read, not executed this turn.

Next evidence: day/rest arrival migration, interior suppression, scene-local companion/drop transitions, both capacity-failure branches, real obstacles and controller-only recruitment/nest work without injected time or positioning. Coordinate CORE-001/003/005/006 and UX-001; do not rebuild Nups art before A1. PROD-003 remains DOING. No production source, rig, animation or native save changed. Only prose audit findings published; pending source-export approval was not bypassed.

## Fifth bounded slice: charged bow, combat contexts and fishing

Audited26November2026,18:59UTC. Browser sources: model.js bowStats; game.js beginAction/endAction/attack/hitEntity/updateArrows/blocked/shorePoint/beginFishing and active update/menu flow. Native sources: bow_combat.gd, camp_wildlife.gd and camp.gd action/input/fishing/scene paths. Existing native tests were inspected before execution.

### Evidence actually run

- `node godot/tests/export-bow-fixture.mjs --check`: PASS144bow-stat cases and current model/game source hashes. Formula cases execute browser model.js; seven game.js token guards detect selected controller/projectile contract changes. These token checks are NOT execution of the whole browser combat simulation.
- Native headless `tests/bow_parity.gd`: PASS602assertions. Covers the formula grid plus charge cap/cancellation/no-ammo behavior, shot edge counting, substepped hits/range, fractional damage, current-aim knockback, strict20px impact boundary, zombie-first overlapping projectile hits, chest blocking, decorative-tree exception and real loot/XP.
- Native headless `tests/bow_controls.gd`: PASS41assertions. Synthetic keyboard/mouse/pad events, RT>.25 and radial stick>.2 thresholds, R3zoom reservation, instantX versus heldRT/Space/mouse, menu-held trigger edges, pause, tool/focus/scene/defeat cancellation.
- Both suites instantiate current camp with persist_enabled=false BEFORE tree insertion. They relocate/seed targets and tools and tick charge directly. No physical controller, normal-time gathering/combat journey or rendered UI acceptance is inferred.
- Both processes exit0; both log a root-certificate-store error. They are not clean-log passes. No script/assertion failure reported. Engine logs redirected into work/. All41runtime baseline hashes unchanged; native player save not opened/written.

### Active-flow traceability

| Contract | Reviewed current behavior / evidence | Status and next dependency |
|---|---|---|
| Charge/full power |1.2s base /0.78s quickdraw; time capped1.5s; range120+300power, speed220+220power, damage1+3power+upgrade/combat/quickdraw;32px/m conversion | Formula and selected native effects validated in suites; physical timing/feedback remains UX-001/QA-001 |
| Fire input and cancellation | X fires an immediate tap; RT/Space/mouse hold-release; menu/tool/focus/scene/defeat cancel transient charge |41injected-event checks PASS; no hardware/visual/audio sign-off |
| Projectile collision and targets |7px substeps and20px impact radius; zombie-first outdoor order; current aim supplies knockback | Selected outdoor cases PASS. Geometry, scene identity and complete target populations remain partial |
| Cave / campaign combat | Browser attacks and arrows hit living bats in the selected dungeon; native wildlife.attack/hit_projectile return false in_cave and there is no native bat combat route in these active paths | MISSING cave enemy interaction; CORE-005/006 must add dungeon/room identity and actual target/loot route before campaign claims |
| Blocking contexts | Browser blocked resolves interiors, dungeon map, world-water/prefabs/solid buildings and boat context; native arrow_blocked uses small outside/cave bounds, one pond and chests | PARTIAL layout substitute, not full collision parity; CORE-003/005/006 |
| Melee target selection | Browser stable nearest target list begins zombies then animals; native nearest iteration follows fixed actors dictionary (animals before zombies) | Equal-distance melee tie can select a different target. Projectile ordering is tested/fixed separately; do not generalize that pass to melee. Add explicit tie fixture in CORE-006 |
| Wall chopping / shelter immunity | Browser axe can demolish nearby walls before targeting an enemy; shelter suppresses appropriate enemy damage | Full building/shelter context absent from reviewed prototype; CORE-003/006, not covered by bow suite |
| Wildlife / night returns | Native outdoor types,720s wildlife return, torch/fire fear, Nups slow hooks, damage/invulnerability/XP/loot exist | PARTIAL sample population and layout; automatic night/spawn cadence and survival/defeat depend CORE-001; full AI oracle/journey still unverified |
| Fishing shore/duration/yield | Same discrete20..70px shore rays (16angles),3active seconds, cancel when movement>12px,1fish or2with angler,8XP; native shore is the prototype pond | Present flat-camp subset. Historical resource_journey teleports to shore and ticks2.99+.01s; read only this turn. Full water/boat/interior contexts and normal-time controller route pending |
| Menu while fishing | Browser openModal clears fishing. Native menu opened signal cancels bow only; _physics_process pauses while open and retains fishing state | DIFFERENCE: native cast resumes after closing instead of being cancelled. UX-001/CORE-006 require an explicit menu/context regression |
| Fishing capacity failure | Native tries inventory then a world drop; it always announces +fish afterward. Browser only shows catch-success notification when addOrDrop succeeds (8XP occurs either way) | Misleading success message if both storage and drop capacity reject. Verify both full-capacity branches in CORE-006/UX-001; do not silently change reward rules |
| Vertical movement and fishing | Native cancellation uses Vector3 distance, browser planar2D distance | Currently flat-player subset. CORE-005's future jump/height contract must deliberately choose planar equivalence or record a3D exception |

The native existing bow tests verify useful rules and a selected outdoor route, not complete combat/browser/world parity. No bow_save suite was rerun here; previous synthetic save audit is separate. No live combat/source changes made in this slice. Sound cues remain AUDIO-001; launch/charge/hit visual feedback still needs native controller play at the target resolutions.

Next PROD-003 slices: active world/height/boat/dungeon/volcano and ending reachability; crop/fuel placement and complete UI context coverage. CORE-001 clock/survival then CORE-002/003 remain the first-loop functional critical path. Audit remains DOING. Publication includes findings only; blocked production-source export was not retried or split into smaller code uploads.

## Sixth bounded slice: world, height and campaign reachability

Audited26November2026,20:02UTC. Sources: GDD8/12; browser model.js WORLD/biomeAt/heightAt/canStep/dungeon definitions/eruptionPhase/whaleStep/tickRainbow/claimRainbow/questSteps; game.js jump/getTarget/interact/blocked/place/update and whale modal; native camp.gd movement/portals/interactions/placement, camp_menu.gd build filter, progression.gd strict schema/save/load.

### Browser contract inspected directly

A read-only local Node probe imported the existing pure model functions, sampled ALL27,648tile centres and wrote a diagnostic under work/ only. Browser model SHA256:05a567570aea4735a062aec91a8ab87e70667cd0a21821aecb7b70aeb5ac028a. WORLD is192x144; sampled biomes are forest11,078, jungle5,745, sea3,921, snow3,483, desert2,236 and volcano1,185. Sampled height levels are0through10, with5,467tile centres above0. These are browser data/function observations, NOT a Godot port, path-connectivity proof or performance result.

Six dungeon rooms and six corridor rectangles are exported, with a spawn and distant crystal. Eight journal steps culminate in beaconBuilt. Pure eruptionPhase boundaries observed: quiet below215s, warning215..<225, erupting225..<240, quiet again at240. No native campaign test is claimed; existing unrelated crafting/bow passes were not repeated.

### Active native path and resulting gaps

| Flow | Browser contract | Inspected native active path | Status / consequence |
|---|---|---|---|
| World regions/water | Shared192x144 biome/coast/water model drives movement, boats, encounters and placement | camp builds one clearing/pond and clamps player outside to+-18.8m; separate sample mine clamp; no active biome/world router | PARTIAL clearing. CORE-005 must establish shared region/terrain/water geometry, not expand a decorative backdrop and call it a world |
| Height/jump/Leap | game.jump starts0.65s jump; model.canStep permits origin-height+1+leap while jumping, otherwise current height | Native movement applies gravity/floor settling only. No jump action or terrain-height/canStep consumer; leap appears only in skill data | Purchasable skill lacks traversal effect. CORE-005/UX-001 require exact action priority, permitted climbs, landing/blocked edges and3D projection tests |
| Cave gates and return | Pickaxe+torch gate, forest/volcano cave identities, room corridors and remembered exit | enter_cave checks tools, remembers runtime cave_return, teleports to one small mine; leave restores that runtime position | Gate/return PRESENT subset; no full dungeon, room map, volcano entrance or persistent scene-location identity |
| Dungeon encounters/rewards | Cave-kind-filtered bats, persistent chests, crystal interaction grants3crystal/55XP and crystalFound | Sample mine contains resource gathering and portal interaction. No corresponding bat/chest/crystal-quest interaction path in try_interact | MISSING campaign journey. Finding a crystal item through another source does not satisfy crystalFound/event progression |
| Volcano | Terrain, lava cracks and240s world-age eruption warnings/damage, separate cave and return | No active region/hazard/cave-kind branch in reviewed camp movement/tick/interaction route | MISSING CORE-005/006; do not invent base destruction or boss mechanics from the old ambiguous request |
| Boat placement/boarding | Place in eligible sea water; board sets boatId; boat movement/shore exit share water and height rules | Recipe exists in catalog/order, but build menu AND _begin_station_build allow only fire/furnace/chest/garden/nest; no boarding/sea movement/shore-exit route | MISSING active boat, despite catalog data. Must test rejected placement/payment atomically and stranded-shore recovery |
| Friendly whale | Sea target opens timing modal; RT/Space hold raises marker, release lowers; successful release gives pearl+20XP and whalesReleased | No corresponding interaction/modal/state route in current camp/menu/progression | MISSING CORE-006/UX-001, not ordinary bow combat. Preserve friendly/no-harm premise |
| Rainbow | Deterministic day>=2 eligibility; check after90day seconds;120active-second event;45px claim;3gold/25XP if bag fits; checked-day/event/claim saved | No active event tick/claim route and no corresponding supported schema fields | MISSING CORE-001/005/006/SAVE-001. Must preserve one-time checked-day/claim state and capacity rejection; never reroll on reload |
| Journal culmination/beacon | Eight actual progress predicates; beacon placement sets beaconBuilt | Native fixed journal objective and five-type build gate exclude beacon; save has no beaconBuilt/crystalFound/nights/home completion fields | Full browser journey cannot currently reach the beacon culmination. Recipe text alone is not implementation; no new credits/win cinematic is assumed |

### Scene and save contract before implementation

Current camp.in_cave/cave_return/player.position are runtime values, not persisted player location/scene state. progression.gd serializes inventory, world objects and sample resource/wildlife/Nups state, but no player transform/region/caveKind/interior/boat/rainbow/campaign predicates. The strict allowlist rejects unknown top-level keys; world-object validation also allows only the five station types. Adding boat/beacon UI alone would leave save validation incompatible.

CORE-005 must first define stable region+cave+room/level identity and coordinate origins, then bind player, resources, wildlife, drops, Nups, buildings and return points to those identities. Existing centred native camp coordinates must remain a named legacy anchor or be migrated through a tested mapping; never reinterpret old coordinates directly as browser positive world coordinates. SAVE-001 needs additive versioned defaults and roundtrip fixtures for the existing nativev3/v4 states, including a waiting companion and drops in the sample cave. No player save was used as a fixture.

Implement in dependency order: CORE-001 clock/survival and CORE-002/003 first-loop/home contract; shared CORE-005 scene/water/height model and migration; forest cave return/map/chests/crystal/combat; other biomes/volcano; boat/shore/whale and deterministic rainbow; then the actual journal/beacon path. Art remains gated by A1; these are behavioral dependencies, not permission to mass-produce all assets now.

Required future proof: normal-time/controller routes with no teleports or injected progression, save/reload in each scene and at transition boundaries, local-only drops/companion/chests, blocked/failed placement with no payment loss, height/Leap limits, safe boat exit and one-time rewards. Current read-only probe establishes none of those native passes. PROD-003 remains DOING; next bounded audit is crop/fuel/storage/placement atomicity and remaining complete UI context coverage. No production source/rig/animation/native save modified; only prose findings published while source-export approval remains pending.

## Seventh bounded slice: crop, fuel, storage and placement transactions

Audited26November2026,21:01UTC. Browser model.js crops/plantCrop/cropProgress/harvestCrop/transferItem/craftItem and game.js fuel/craft/placement/place/chest/garden UI; native progression.gd equivalents, camp.gd station/build/tick and camp_menu.gd station/storage/garden routes.

### Executed evidence and a corrected weak test

- Reviewed existing stations_world.gd before using it. It writes a synthetic fixture to user:// and disables automatic camp physics, then merely waits a frame to assert fuel is paused. That wait alone does not test menu pausing.
- Ran a LOCAL work/ derivative with the fixture redirected to an exact work/ path, preserving the native save. Replaced that weak wait with an explicit camp._physics_process(1.0) while the station menu is open; fuel stayed unchanged. Also compared both inventory and world-object count before/after occupied-square rejection. Result: PASS28station assertions, including fuel use/proximity/cooking/storage/roundtrip and the strengthened checks. Test fixture deleted only at its explicit work/ path.
- Ran current station_menu.gd unchanged: PASS station-specific menu/source-order, injected controller A fuel/craft and X chest stack behavior, water/base-tool/bag gates and construction-selection-without-early-payment checks. It uses seeded stock and persist=false, not a natural gathering journey or physical pad/visual test.
- New local pure-state crop boundary audit: PASS45assertions across the five CURRENT browser crop definitions. Tested free planting, occupied rejection, duration-minus0.001 rejection, exact readiness boundary, full-bag rejection preserving crop/inventory/XP/counter, then freeing one slot and retrying with exact yield/10XP/bed reset.
- All three native processes exit0; root-certificate-store errors remain, so no clean-log claim. No script/assertion failure reported. All41runtime baseline hashes unchanged. The live player save was neither opened nor written; no active game process stopped.

### Rules currently supported in the clearing subset

| Rule | Evidence / limit |
|---|---|
| Crop data | Carrot180s/3, potato240/4, berries210/3, herbs180/3, magicFlower300/2 matched against browser model table in the boundary test |
| Plant/harvest | No seed/payment requirement; occupied/immature/full-bag failures preserve bed and progression; successful harvest resets bed and gives10XP once. These pure transaction boundaries passed; crop visuals and unaccelerated route are separate |
| Fuel | One nearby-paid wood adds120s or240s with smelter. Any strictly positive station fuel permits a craft, then deduct5s clamped to0; not a5second wait. Seeded station/menu tests passed |
| Active time / pause | Explicit menu-open physics call returns before fuel tick; closed-menu direct inventory tick burns1fuel second per simulated second. No offline-time growth was inferred |
| Recipe/station separation | Fire cooking and furnace smelting lists/context gates exercised; nearby chest/bench/water distances covered within the existing sample clearing |
| Storage | Model transfers validate the full requested amount; menu caps stacks at20/available stock and reduces withdrawal amount until it fits. Injected A-one/X-twenty cases passed. Partial-fit fallback was source-inspected, not separately executed in this slice |
| Placement | Selection does not pay; successful placement creates unlit station at absolute cursor cell and retains build selection. Explicit rejected-duplicate stock/world comparison passed. Cost/proximity/storage/save roundtrip validated in seeded sample |
| Harvest/build overflow atomicity | Crop full-capacity failure tested directly. Cooking output-capacity rollback was covered by the earlier crafting slice. Do not generalize these to every UI/world failure combination |

### Remaining scope and required evidence

The active build filter, _begin_station_build and strict save validator still support ONLY fire/furnace/chest/garden/nest. Browser layer-aware floor/roof/ceiling/lamp/object coexistence, walls/doors/windows, furniture, stairs/interiors, boats/beacon and home plot/entrance reservations are not supplied by the five-type placement pass. Browser placement also has full water/sea, house footprint, resource and room rules; native _build_reason is a clearing approximation. CORE-003/004/005 must share geometry and validation rather than duplicating visually plausible but different blockers.

Browser and native use a145px strict placement reach boundary and nearby chest120px inclusion; representative moving-player absolute cursor behavior, all rejected-payment cases and real approach paths still need controller journeys. No new resolution/layout/art acceptance was performed. Station UI tests inject events against prepared contexts, and the local crop test advances world_age explicitly; neither establishes a child's normal-time play flow.

No production tests/source were edited or published. The reviewed test derivative and new boundary harness remain work-only while broad source export approval is pending. Only prose findings published. PROD-003 remains DOING, now narrowed to remaining menu/inventory use/action contexts, feedback/audio and verification of the full traceability inventory before opening implementation tickets. A1 art work continues independently.

## Eighth bounded slice: shared menu, inventory actions and feedback

Audited26November2026,22:00UTC. Browser game.js openMain/openModal/keyboard/pad/explicit bag actions, model.js useInventoryItem/usePotion/foodValues, audio.js; native camp_menu.gd frame/actions/input, progression.gd use_item/drop/claim and camp.gd world input/pause/drop simulation.

### Evidence actually executed

- Current native headless menu_parity.gd PASS: explicit inspect/use/drop, opening-press guard, one-shot controller crafting, bench rejection, retained tab/recipe selection, stick/category navigation, over-capacity legacy stacks/scroll and native-size shared-frame geometry at720p/1080p/4K.
- Current native headless inventory_world.gd PASS: drop beside player, pause lifetime in menus, reclaim/expiry/full-bag reward on ground, and retry after freeing capacity. This test injects stock, places the player at targets and advances expiry directly; not an unaccelerated physical-controller route.
- Both create throwaway state with persistence disabled before scene insertion, exit0 and report no script/assertion failure. Root-certificate-store errors remain; not clean-log passes. Engine logs are work-only. All41runtime baseline hashes unchanged, no player save read/write and no running user game stopped.

Headless geometry assertions establish layout bounds, NOT visual fidelity, font/icon rendering or human usability. The three requested viewport sizes were actually set by the test; there is no new screenshot or physical display/controller acceptance in this slice.

### Supported subset versus remaining UX work

| Flow | Finding / evidence |
|---|---|
| Shared six-tab frame | Bag/journal/craft/build/skills/map frame and contextual navigation exist; menu test covers bounds/focus subset. Journal is still a fixed first-pickaxe panel, map explicitly unported. Empty tab framing is not campaign UI |
| Explicit inventory actions | Inspecting does not consume; use/drop are separate confirm actions. Water restores up to60thirst and reduces heat35, full-state water is retained. Food values and healing/speed/peace branches are present and source-inspected; no new all-consumable boundary sweep is claimed |
| Capacity/legacy drops | Visible saved stacks are retained even above current capacity; no auto-truncation. Native drop/reclaim/expiry subset passed. Full region/room identity remains the CORE-005/SAVE-001 gap from earlier slices |
| C/I/J/K shortcuts | IMPORTANT source reconciliation: CURRENT browser maps C/I/J/K through openMain(), which always opens bag. Native routing all four to bag matches that code. Do not implement separate shortcut tabs from an older/general GDD description without an intentional change |
| World pause versus modal back | Browser world Escape and padStart open pause; modal Escape/Start close/back. Native menu has back handling, but camp world input has no corresponding pause-menu opening flow (Escape is handled only while building). MISSING full pause shell, not fixed by modal pausing |
| Pause/help/language/new-game | Browser pause offers resume/help/skills/new game/journal/language/zoom with safe existing-adventure default on reset confirmation. Native shared menu is not this complete pause/settings/start/reset flow. UX-001/SAVE-001 need safe confirmation/default and independent preferences |
| World camera and controls | Native calm follow, wheel/R3zoom, quickbar LB/RB and world action subset exist. Browser Z/V and pad left/right camera rotation are absent from the inspected native world-input route; menu/build context direction handling does not supply world rotation. Preserve the user-approved calm follow while restoring requested context behavior deliberately |
| EN/ET | Native names/descriptions/actions/hints are hardcoded ET; no complete language preference/path. Browser uses i18n and explicit language menu. UX-001 requires both languages, stable IDs and resolution/controller checks |
| Feedback | Native labels, held tools, charge bar/reticle, primitive loot/animations/lights exist. Browser also has sound/particles/damage flash/event notices; selected action tests do not establish matched feel/clarity |
| Audio/mute/volume | Browser audio.js synthesizes original cue/music/footstep/bird/fire sounds and exposes toggle/volume. Inspected native active scripts/scenes/config do not implement the corresponding audio subsystem/settings. AUDIO-001 remains MISSING implementation and auditory acceptance, not a licensing blocker requiring downloaded samples |

### Producer review: discovery baseline complete, implementation is not

Codex reviewed this eight-slice register against the current GDD families: initial state/economy/recipes/stations/storage/farming; world/height/scenes/events/campaign; NPC/quests/home; time/survival/defeat; combat/skills/Nups/fishing; inventory/menu/controller/language/feedback/audio; durable save migration and art gates. Every family now has an active-code assessment, available evidence boundaries and an owning board ticket. No remaining system family is silently treated as complete because data, a filename or a green subset test exists.

**PROD-003 DONE means this initial discovery/traceability baseline is reviewed and actionable. It does not mean browser parity, QA, A1 or B1 is complete.** Detailed edge cases stay in their implementation tickets, which require new targeted tests and normal-time physical journeys. The separate SAVE-001 audit remains DOING for OS fault/campaign migration evidence. Reopen/refresh affected traceability rows as implementation changes.

Release implementations remain explicitly TODO/PARTIAL: CORE-001 clock/survival, CORE-002 NPC/quests, CORE-003 homes, CORE-004 full reachability/context, CORE-005 world/height/scenes, CORE-006 campaign, UX-001 and AUDIO-001. ART-001 and A1 still gate broader art production. User additions (bucket use, penguin, Mattias bosses) retain their separate design gates; the browser baseline does not authorize invented mechanics.

Next owned READY pull is CORE-001: prepare a bounded local isolated clock/survival/state-migration contract and fixtures before integrating anything into the live camp. Use the existing strict nativev3/v4 schema as legacy input; preserve original runtime/save and do not publish source while PROD-002 export approval is pending. No automatic upgrade of the user's real save and no broad live gameplay rewrite is part of this audit closure.
