# Simm metsikus looduses

An Estonian browser survival adventure designed with Mattis. Local pixel graphics are drawn on canvas; no runtime packages, accounts, or API keys are required. Fonts are bundled locally with their SIL Open Font License files.

![Simm game preview](docs/preview.png)

## Try without installation

Download [index.html](https://github.com/commonCEO/SIMM-IN-THE-WILD/raw/refs/heads/main/index.html) from this repository and open it in a current desktop browser. This self-contained build includes all game code, fonts, graphics and sound. It works without a server. WASD/mouse works locally; controller availability on file URLs depends on your browser, so use the HTTP version if needed. Local save storage on file URLs also depends on the browser.

If you download the repository ZIP, extract it and open the root `index.html`. The `play/index.html` copy also works.

Developers edit `src/index.html` and files in `src/`; the development server uses this template. Rebuild both standalone HTML files after editing with `npm run build`. `play/` can also be uploaded as a static website or zipped for an itch.io HTML game.

## Run

Requires Node.js 20 or newer.

```sh
npm ci --cache /workspace/.cache/npm
npm run dev
```

The HTTP server listens on port 3000 (override with `PORT`). Open the app in a browser. `npm test` checks crafting, skill progression, and the five-minute day / one-minute night cycle; `npm run check` checks JavaScript syntax. With the server running, `CHROMIUM_PATH=/usr/bin/chromium npm run test:browser` runs the browser smoke suite in this cloud machine. On other machines install Playwright Chromium with `npx playwright install chromium` and omit `CHROMIUM_PATH`.

## Play

- WASD/arrows move; E gathers/interacts; Space or click uses the tool; 1–5 selects tools; R eats the best available food; I opens the backpack.
- C opens crafting near the starting workbench, B building, K skills. Escape cancels placement or closes a menu.
- Standard Xbox controller: left stick moves, right stick aims, A interacts/places, X uses tool, Y crafts, B eats/cancels, bumpers select tools, LT opens the bag, RT uses the tool, View builds, Menu opens skills. D-pad navigates modal buttons and A confirms. Browser Gamepad API requires a connected controller and a button press; physical hardware validation is still needed.
- Gather wood with the starter axe, craft a pickaxe at the bench, gather stone, and craft a torch. The cave lies north of camp. Enter with E, walk north, collect the crystal, then leave through the southern exit.
- Build a room by enclosing it with walls and a door. Floors alone do not prevent zombie attacks. Doors let Simm pass while blocking zombies.
- A meteor arrives east of camp after 55 seconds. Befriend Nups, build an alien nest, and receive berries. Each skill branch has three upgrade ranks.
- Backpacks have 20 slots with stacks of 20 items; tools live on the separate belt. Craft upgrades at the bench (+5 slots each, up to 40). The full bag menu lets you discard a single item.
- Build a campfire, add wood (120 seconds of fire per log), and cook rabbit meat or stew (berries + rabbit meat + herbs). Fire and a held torch repel wildlife and monsters. R prioritizes stew, roast, then berries.
- Rabbits and deer roam the forest and flee when approached. Deer are peaceful; hunting rabbits with the bow provides meat without blood or graphic effects. Friendly-looking bats inhabit the cave.
- Saves automatically to browser localStorage. The help menu includes a reset button. Defeat preserves inventory and starts a new day at camp.

## Scope

First playable prototype: forest, cave quest, hunger, crafting, modular buildings, zombies, skill branches, alien helper, wildlife, keyboard/mouse and controller input. Mobile touch controls, additional biomes, copper/tin/bronze/gold, more quests, and generated sprite artwork are future additions. Graphics use small procedural walking, tool-swing, crystal, leaf-mote and wildlife animations. Optional original Web Audio music, footsteps, birds and action sounds are enabled using the sound button. No downloaded audio is used.

Cloud tasks are already isolated; use the existing checkout rather than creating a Git worktree unless explicitly requested.

## Release intent

Design target: gentle, non-graphic adventure suitable for a PEGI 7 audience; no official age rating has been obtained. Planned itch.io price: €4.99. Not published yet. Before release: physical controller playtesting, balancing, expanded content, accessibility review, static ZIP packaging, and review of any added commercial asset licenses. Current code, graphics and synthesized sound do not require an external asset subscription.
