# CoX Mod Adventure - Context and Direction
**Date:** 2026-07-13
**Status:** Working direction

---

## Concept

CoX Mod Adventure is not just a static website and not just a downloader. It is a local bridge between the City of Heroes mod ecosystem, the player's actual Mac installation, and a richer archive/control surface that makes mod discovery feel native to the game.

The current project chain is:

```text
GitHub repo bootstrap
-> local CoH tooling collection
-> scraped 291-mod catalog
-> visual mod browser prototypes
-> game-native archive/control surface
-> possible launcher/manifest/admin ideas inspired by CityVault
```

The important shift is from "files and scripts" to "operable mod cockpit." The repo should help a player understand what exists, browse by category and popularity, inspect what a mod does, download or install it, and eventually understand how the local CoH runtime is wired.

---

## Local Runtime Surfaces

These local paths are part of the project meaning:

| Surface | Role |
|---|---|
| `/Users/steven/Library/Application Support/LaunchCat/coh` | Real local City of Heroes / Homecoming runtime surface managed by LaunchCat. |
| `/Users/steven/Library/Application Support/LaunchCat/coh/assets/mods` | Real installed mod target for `.pigg` files. |
| `/Users/steven/Library/Application Support/CityModInstaller` | Real user-level CityModInstaller state: executable, Wine prefix, config, log, and installer database. |
| `/Applications/coh` | Empty marker/future convenience path, not the live runtime tree. |
| `/Applications/CoHModdingTool.app` | Local GUI modding tool. |
| `/Users/steven/CoX-mod-Adventure/Mods/` | Local holding area for downloaded tools or mod packages. |
| `/Users/steven/CoX-mod-Adventure/mods.json` | Canonical scraped catalog of 291 cityofheroes.dev mods. |
| `/Users/steven/CoX-mod-Adventure/Upgraded/` | Current creative browser prototype surface. |

The browser should eventually make these surfaces visible as part of the product story: not raw absolute paths first, but clear local state like "catalog loaded," "tool installed," "LaunchCat runtime detected," "installed mods found," and "install target ready."

### Tree Explorer Snapshot

Live inspection on 2026-07-13 showed:

| Surface | Observed state | Product implication |
|---|---:|---|
| Project root | `879M` total | Most size is installer/tool archives, not the browser prototype. |
| `Upgraded/` | `884K` | Lightweight creative prototype surface. |
| `Mods/` | `4.5M`, currently only `CoHModdingTool-Windows.zip` | The giant historical `mod-*.zip` path dump is not current live state. |
| `coh-modders/` | `862M` | Main local archive of installer/tool packages. |
| `~/Library/Application Support/LaunchCat/coh` | `5.6G` | Real local CoH/Homecoming runtime tree. |
| `~/Library/Application Support/LaunchCat/coh/assets` | `4.8G` | Main game assets tree. |
| `~/Library/Application Support/LaunchCat/coh/assets/mods` | `32M`, 3 `.pigg` files | Real installed mod target and current installed-mod inventory. |
| `~/Library/Application Support/CityModInstaller` | `334M` | User-level CityModInstaller runtime state, separate from the app bundle. |
| `/Applications/coh` | directory, `0B` | Empty marker/future convenience path, not a populated game client. |
| `/Applications/CoHModdingTool.app` | `1.1G` app bundle | Real local modding tool surface. |

The LaunchCat runtime tree contains:

- `assets/issue24`, `assets/live`, `assets/launcher`, and `assets/mods`.
- Installed mods currently visible in `assets/mods`: `PocketDAssemblage23.pigg`, `BetterIcons.pigg`, and `accolade_lrt.pigg`.
- `wine/`, `bin/`, `cache/`, `settings/`, `logs/`, `accounts/`, `data/`, and `screenshots/`.
- Launch entry files: `Homecoming.lnk`, `start-live.sh`, and `launch.sh`.
- Diagnostics and reference files: `LaunchCat-Diagnostics.txt` and `THIRDPARTYSOFTWAREREADME.txt`.

The current installed-mod baseline resolves as:

| Installed ID | Installed file | Catalog name |
|---:|---|---|
| `189` | `BetterIcons.pigg` | Better Icons - Inspirations and Powers! |
| `210` | `PocketDAssemblage23.pigg` | Pocket D New Techno music |
| `200` | `accolade_lrt.pigg` | Pocket D Long Range Teleport Icon |

`~/Library/Application Support/CityModInstaller` contains:

- `CoHModdingTool.exe` - PE32 Windows .NET GUI executable.
- `config.json` - current installer config.
- `launcher.log` - Wine/tool launch log.
- `modder.db` - SQLite database with `config`, `installedMods`, and `trackedFiles` tables.
- `wineprefix/` plus `x86/SQLite.Interop.dll` and `x64/SQLite.Interop.dll`.

`CityModInstaller/config.json` currently has `gamepath` set to `z:\Applications\coh\`, with `autoupdate` enabled and `dontCheckforData` enabled. That configured game path should be treated carefully: live game assets are under LaunchCat, while `/Applications/coh` is only an empty convenience path unless LaunchCat or Wine path mapping resolves it indirectly.

`/Applications/CoHModdingTool.app` contains:

- `Contents/Resources/CoHModdingTool.exe` - PE32 Windows .NET GUI executable.
- `Contents/Resources/modder.db` - SQLite database.
- `Contents/Resources/wineprefix/` - bundled Wine prefix.
- Bundle metadata names it `CoH Launcher`, version `1.1`, bundle id `com.powermad.coh-launcher`.

The image source folder `/Users/steven/Pictures/CoH-ComicArt/` contains usable visual assets including `KingsRow.jpeg`, `TerraVolta.jpeg`, `FuturCityScape.jpeg`, `IndepPort.jpeg`, `PerezPark.jpeg`, `SciFiBattle.jpeg`, and `StatueCity.jpeg`.

---

## Current Prototype

`Upgraded/` is the live creative prototype area. It currently contains three HTML browser variants generated from the same data:

| Variant | Existing direction | What it teaches |
|---|---|---|
| `mod-browser.html` | Mission Briefing Terminal | Strongest CoH operating-console direction. |
| `mod-browser-comic.html` | Comic Book | Best category/color energy and bold graphic identity. |
| `mod-browser-hud.html` | Power HUD | Best "in-game system UI" direction. |

The next prototype should not pick one by deleting the others. It should synthesize them:

- Mission terminal as the structural base.
- HUD panels for metadata, install state, and filter controls.
- Comic/pixel texture as surface flavor, not full-page novelty.

---

## CityVault As Adjacent Inspiration

CityVault is a Node.js City of Heroes server control panel. Its current README describes automatic launcher manifest generation, user management, character views, an admin dashboard, multi-server support, and game-file hosting/profile configuration. Source: `https://github.com/CaitlynMainer/CityVault/`

For this project, CityVault is not the thing to clone. It is a useful reference for the larger shape of a CoH control surface:

- Launcher/manifest concepts can inspire future "install profile" thinking.
- Admin/dashboard organization can inspire status panels and local checks.
- Game-file hosting docs can inspire a clear mental model for where assets live.
- Multi-profile launch settings can inspire future LaunchCat/CoH target awareness.

Immediate scope should stay smaller: mod archive, browser, local tool awareness, and install/download flow.

---

## Skill-Driven Direction

Use the local skill ecosystem deliberately, not as a bag of random effects.

Detailed workflow selection and research-review logic now lives in
`docs/plans/2026-07-13-cox-research-review-and-workflow-logic.md`.

| Skill | Use in this project |
|---|---|
| `innate-workflow` | Keep the loop: audit context, select skills, work, then preserve learning. |
| `using-superpowers` | Select the relevant skill cluster before each meaningful phase. |
| `workspace-ecosystem-audit` | Re-check live project/runtime surfaces before assuming paths or state. |
| `narrative-documentation` | Keep this direction understandable as a product, not just code. |
| `frontend-design` | Hold the UI to a distinctive CoH-native visual standard. |
| `popular-web-designs` | Borrow patterns: Pinterest masonry, Spotify media cards, Sentry density, VoltAgent terminal canvas. |
| `p5js` | Add a restrained ambient canvas: scanlines, particle fields, energy trails, city-noise atmosphere. |
| `pixel-art` | Convert CoH zone art into CRT/pixel-flavored category thumbnails or hero panels. |
| `playground` | Build a layout/density/theme tuning playground before hardening a final browser. |
| `dogfood` | Verify the browser interactively after design changes. |

---

## Agent Routing

The local agent library adds a studio workflow around the skills. Use these agents as lenses, not as separate product goals.

| Agent | Use in this project |
|---|---|
| `tree-explorer` | Map project, runtime, asset, and agent trees before making assumptions. Good for "what is actually in here?" passes. |
| `studio-producer` | Keep the work coordinated: prototype lanes, handoffs, dependencies, and what should ship next. |
| `ux-researcher` | Define player journeys: discover a mod, compare categories, decide trust, download, install, and return later. |
| `ui-designer` | Convert the CoH-native direction into buildable panels, cards, controls, states, and responsive layouts. |
| `visual-storyteller` | Make the browser tell the archive story: city map, mission briefing, mod intelligence, local install status. |
| `whimsy-injector` | Add restrained delight after core flows work: hover charge, scanline pulse, "acquire module" feedback, empty states. |
| `project-shipper` | Define the launchable artifact: which HTML is primary, what docs explain it, and what verification is required. |

Recommended routing for the next phase:

```text
tree-explorer
-> studio-producer
-> ux-researcher
-> ui-designer + visual-storyteller
-> frontend-design + p5js + pixel-art + popular-web-designs
-> whimsy-injector
-> dogfood
-> project-shipper
```

This keeps the work from collapsing into either pure code cleanup or pure visual play. The output should remain a usable mod browser that feels like a CoH surface.

---

## Next Design Move

The next version of the mod browser should become a "Paragon Mod Terminal":

1. **Bento command strip**
   - Top 5 mods by downloads become asymmetric feature panels.
   - Each panel shows category, downloads, author, and a short use-case phrase.

2. **Masonry archive grid**
   - Main archive uses variable-height cards so long descriptions and short utility mods do not create a dead uniform grid.
   - Density modes: `compact`, `standard`, `briefing`.

3. **Skill-inspired visual layer**
   - `p5js`: low-opacity background canvas for ambient city energy, scanlines, and power particles.
   - `pixel-art`: optional category art tiles derived from CoH zone imagery.
   - `popular-web-designs`: Pinterest for masonry, Sentry for dense scanning, Spotify for media-card hierarchy, VoltAgent for terminal-native depth.

4. **Local runtime awareness**
   - Status row for detected local surfaces:
     - CoH app directory
     - CoHModdingTool app
     - Mods folder
     - catalog count
   - Keep this informational first; do not overbuild installers until the browsing experience is strong.

5. **Promptable playground**
   - Add a single-file playground for tuning layout choices:
     - layout mode
     - density
     - theme accent
     - ambient canvas intensity
     - pixel-art thumbnail mode
   - The playground should output a clear prompt/instruction that can be fed back into the generator.

---

## Working Principle

Do not let incidental code defects pull the project back into a script-cleanup loop. Fix defects when they block the prototype, but keep the primary energy on product comprehension and the browser experience.

The project is trying to become a CoH-native mod archive and control surface. The code should serve that fantasy.
