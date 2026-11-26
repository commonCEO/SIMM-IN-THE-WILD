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
