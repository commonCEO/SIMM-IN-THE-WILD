# Simm metsikus looduses · 0.3

An Estonian browser survival adventure designed with Mattis. The game fills the browser window; the toolbar, health, time and unspent skill points stay inside the game. All graphics, fonts and original synthesized sound are local.

![Simm game preview](docs/preview.png)

![Fullscreen skill tree](docs/skills.png)

## Try without installation

Download [index.html](https://github.com/commonCEO/SIMM-IN-THE-WILD/raw/refs/heads/main/index.html) and open it in a current desktop browser. Alternatively download the repository ZIP, extract it, and open the root `index.html`. `play/index.html` is an identical standalone copy. No server or asset downloads are required. Press the fullscreen button or F11 for browser fullscreen.

Saves use browser localStorage. Version 0.1 saves are migrated when available. Browsers may store file-URL saves separately when you change the downloaded filename or folder. Gamepad support and local save behavior on file URLs depend on the browser; an HTTP server provides a stable origin when needed. Physical Xbox playtesting is still needed for 0.2.

## Start a new adventure

Choose **Uus mäng** on the title screen (Xbox Y), or open Pause with Escape / Xbox Menu and choose **Uus mäng**. When replacing an existing save, the in-game confirmation starts with **Cancel** selected. Choose **Jah, alusta uut mängu** to reset the world, inventory, tools, skills, quests and creatures. No browser-native confirmation dialog is required.

## Version 0.3

- Original pixel-art forest, Simm walking frames, creatures, cave, campsite, ore, buildings, textured floors, water edges and title portraits. The art and fonts are embedded in the downloadable file.
- Large fullscreen menus scale for 720p through 4K. Crafting/building cards show available material counts.
- Controller navigation responds immediately to a new stick/D-pad direction. Hold-repeat starts after 260 ms, then repeats every 85 ms. The world renderer freezes while a menu is open; unchanged footer text is not rewritten each frame.
- Skill nodes stay selectable even when locked. Navigate in their actual directions, inspect prerequisites in a large side panel, and press A / Enter to learn. Selection stays on the same node after upgrading; bumpers switch branches.
- Right-stick scroll works in long menus and the detail panel. Keyboard/mouse remain supported.
- A brief startup readiness state decodes the embedded art and draws the title background once before enabling play, keeping early controller taps out of the initial render work.
- New Game and Pause work entirely with the controller. RS opens skills directly; Menu opens Pause.
- Adventure journal guides gathering, crafting, the crystal, Nups, building shelter, surviving nights and constructing a crystal beacon. Journal is J / D-pad Up or the quest HUD button.
- Shooting-star arrival, flickering fire, canopy visibility, cached textured terrain and water boundaries matching the collision model improve atmosphere and performance.

## Controls

| Action | Keyboard / mouse | Xbox standard mapping |
| --- | --- | --- |
| Move | WASD / arrows | Left stick |
| Aim | Mouse | Right stick |
| Interact / place | E / click to place | A |
| Tool / bow charge | Hold Space or mouse; release to shoot | Hold RT; release to shoot (X taps tool) |
| Inventory | I | View, beside the left stick |
| Building menu | B | Y |
| Craft | C while beside workbench | A while beside workbench |
| Skill tree | K | Right stick click (RS) |
| Pause / New Game | Escape | Menu |
| Adventure journal | J / quest HUD | D-pad Up |
| Eat best food | R | LT |
| Nups wait / follow | T | B |
| Rotate wall / door | Q | X while building |
| Select tool | 1–6 / toolbar | LB / RB |
| Menu selection | Arrows / Enter / mouse | Left stick / D-pad / A |
| Close / cancel building | Escape | B |

Sound starts off. Toggle it using the sound button; its louder default is adjustable with the volume slider.

## Version 0.2

- Full-window game with an internal hotbar and prominent unspent skill points. Browser fullscreen is optional.
- Controller menus manage their own visible selection and support both the stick and D-pad. RT reads analog values as well as the pressed flag.
- Interactions require proximity and highlight the eligible object. The workbench is usable within 46 world pixels.
- Buildings use a grid and green/red placement preview. Connected horizontal and vertical walls, corners and manually rotated walls/doors make the floor plan legible. Enclosing a room with walls and a door protects Simm.
- The axe removes stumps for less wood and breaks a wood wall in three hits. Half its original wood cost is dropped for pickup.
- Four skill roots each have two alternative specializations with visible prerequisites: combat, crafting, gathering and star invention.
- Holding/releasing a bow action launches a real directional projectile. Charge increases distance and damage. A facing marker and aiming guide show the direction. Rabbits and deer can be hunted without blood or graphic effects.
- Wildlife spawns on land, checks water boundaries while moving, and persists in saves.
- Night enemies are fewer, slower and weaker. Damage flashes the screen and player, with a shared period of invulnerability to prevent multiple simultaneous hits. Defeat fades out, restores Simm at camp, then fades into the next morning, retaining inventory.
- Nups follows at a distance. B/T leaves him waiting at his current position or recalls him when nearby. While following he slows nearby enemies; while waiting near a nest he brings berries. Skill specializations expand these abilities.
- Cave deposits provide iron and copper ore. A fueled furnace creates ingots and stone slabs; ingots upgrade the axe/pickaxe at the workbench and slabs make stone flooring.
- A crafted fishing rod catches fish from the shore. Campfires cook fish, meat and berry/herb stew.
- The bag has 20 slots with stacks of 20, separate from tools. Workbench upgrades add five slots each, up to 40. Dropped items remain visible, can be picked up, and expire after 10 simulated minutes. Menus pause this timer along with the game.

## Development and checks

Requires Node.js 20+. No application API keys, accounts, or external services are required. Developers edit `src/index.html`, `src/game.js`, `src/model.js`, `src/audio.js` and `src/style.css`.

```sh
npm ci
npm run dev
```

In this cloud machine use `npm ci --cache /workspace/.cache/npm` to keep the cache in a writable directory. The server listens on port 3000; `PORT` overrides it. The development server serves the source template at `/`; the generated standalone build is at `/index.html`.

```sh
npm run check
npm test
npm run build
CHROMIUM_PATH=/usr/bin/chromium npm run test:browser
CHROMIUM_PATH=/usr/bin/chromium npm run test:menus
CHROMIUM_PATH=/usr/bin/chromium npm run test:standalone
```

The gameplay and menu browser tests need the running server; the standalone suite reads the generated HTML directly. `TEST_URL` can override its address. On other machines install Chromium with `npx playwright install chromium` and omit `CHROMIUM_PATH`. Build refreshes both standalone HTML files deterministically and embeds font license text. The menu suite checks rapid stick reversal, spatial navigation, prerequisite previews, learning, retained focus, controller-only reset/cancel and fullscreen layouts. Its latency figures are browser simulations, not physical-controller measurements. The normal suite checks capacity, crafting, progression, drops/expiry, bow charge and building orientation. Browser checks exercise controller crafting/menu navigation, real gathering, building/demolition, cave quest, cooking, smelting, fishing, bow hunting, companion behavior, nighttime protection, and saves.

Cloud tasks already run in isolated environments; use the existing checkout rather than a Git worktree unless explicitly requested.

## Future release

PEGI 7 is the art/content target; no official age rating has been obtained. Intended itch.io price: €4.99. The game has not been published there. Touch controls, ice/volcano biomes, more biomes and quests, gold/tin/bronze and release balancing remain future work. Fonts include their SIL Open Font License notices; no downloaded music or commercial asset subscriptions are used.
