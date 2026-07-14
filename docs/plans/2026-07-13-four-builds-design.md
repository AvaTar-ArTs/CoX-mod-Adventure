# CoX Mod Browser — Four Builds Design

**Date:** 2026-07-13
**Status:** Approved
**Scope:** Upgraded/ four-build expansion from mod-browser-v2.html

---

## Summary

Expand the existing mod browser prototype into four purpose-built surfaces, each serving a distinct user persona, all sharing a common `core/` layer. No build tooling. No npm install. Pure HTML/CSS/JS + Python for the server build + Electron for the native build.

---

## Folder Structure

```
Upgraded/
  core/
    mods.js         ← const MODS = [...] (291 mods with art field)
    render.js       ← makeCard(), fmtDl(), badgeClass(), renderBento(), renderTabs()
    style.css       ← CSS custom properties, card/grid/masonry, three themes
  a-static/
    index.html      ← polished static browser with mod detail drawer + install link
  b-server/
    server.py       ← Flask on :7777 with /api/install route
    index.html      ← same UI, install button calls server endpoint
    requirements.txt
  c-electron/
    main.js         ← Electron main process + ipcMain handlers
    index.html      ← renderer with direct filesystem install via ipc
    package.json
  d-launcher/
    index.html      ← Loadout builder UI
    loadout.js      ← conflict detection, apply loadout, save/load
    loadout.json    ← persisted user loadout state
```

---

## Core Layer

Three shared files. Each build includes:

```html
<link rel="stylesheet" href="../core/style.css">
<script src="../core/mods.js"></script>
<script src="../core/render.js"></script>
```

**core/mods.js** — the single source of truth for mod data. 291 mods with id, name, author, category, downloads, description, download_url, page_url, art fields.

**core/render.js** — all card-rendering logic: `makeCard(mod)`, `renderBento(el)`, `renderTabs(el, cats, active, onClick)`, `fmtDl(n)`, `badgeClass(cat)`. Stateless functions — each build wires up its own state and event handlers.

**core/style.css** — CSS custom properties for all three themes (terminal/HUD/comic), card styles, masonry/bento/list layout classes, bento strip, controls bar, category tabs. Each build can override tokens in its own `<style>` block without touching core.

---

## Build A — Static

**Persona:** Casual browser. Wants to find and download a mod without any setup.

**What's new over v2:**
- Mod detail drawer: clicking a card slides in a right-panel drawer with full description, category, download count, direct download + page links
- Install link: download button triggers direct `.pigg` download to browser Downloads folder
- Installed state: localStorage tracks which mod IDs have been downloaded; cards show a subtle "↓ saved" badge

**Entry point:** `a-static/index.html` — open directly in browser, no server needed.

---

## Build B — Server

**Persona:** Power user. Wants one-click install directly into CoH data dir, no manual file moving.

**Server:** Python Flask on `http://localhost:7777`

Routes:
- `GET /` — serves index.html
- `GET /api/mods` — returns mods.json (for dynamic reload)
- `POST /api/install` — body: `{id, download_url}` — downloads the .pigg to a temp location, then moves it to `/Applications/coh/data/` (or user-configured path)
- `GET /api/installed` — returns list of installed mod IDs from disk

**Frontend:** Same card/filter/bento UI as A-static. Install button calls `fetch('/api/install', ...)` instead of direct link. Cards show live install status: idle → installing → installed → error.

**Entry point:** `python3 b-server/server.py` then open `http://localhost:7777`

---

## Build C — Electron

**Persona:** Dedicated modder. Wants a native app that works offline and has direct filesystem access.

**Architecture:**
- `main.js` — BrowserWindow, ipcMain handlers for `install-mod` (download + fs.copyFile to CoH dir) and `get-installed` (read CoH data dir for .pigg files)
- `index.html` — renderer, uses `window.electronAPI.installMod(url, id)` preload bridge
- `preload.js` — contextBridge exposing `electronAPI` to renderer safely

**What it adds over A-static:**
- No browser file:// restrictions
- Can read `/Applications/coh/data/` to show which mods are currently active
- Native window title + dock icon
- Drag-to-install: drop a .pigg onto the window to register it

**Entry point:** `npm start` from `c-electron/`

---

## Build D — Launcher (The Loadout Builder)

**Persona:** Theorycraftier. Wants to manage their mod set like a hero build — curated, shareable, conflict-aware.

**The metaphor:** Your active mods are a *loadout*, like a City of Heroes power build. Categories are power pools. Conflicts are incompatible powers. Apply Loadout = slot your build.

**UI Layout:**
```
┌─────────────────────────┬────────────────────────┐
│  MOD BROWSER (left)     │  ACTIVE LOADOUT (right) │
│  search + filter        │  slotted by category    │
│  mod cards (compact)    │  conflict badges        │
│  [+ ADD TO LOADOUT]     │  [APPLY LOADOUT]        │
└─────────────────────────┴────────────────────────┘
```

**Features:**
- **Loadout slots** — one slot per category (Audio, Graphics, Maps, GUI/Icons, Popmenus, Cursors, Languages, Other). Multiple mods can fill a slot but conflicts are flagged.
- **Conflict detection** — two mods with overlapping file coverage (same category + same subcategory heuristic) → amber ⚠ warning on both. User decides which to keep.
- **Apply Loadout** — writes `loadout.json` with selected mod IDs, then (optionally) triggers download of each.
- **Save/Load** — `loadout.json` persists to localStorage; can also export as a `.json` file for sharing on Homecoming forums.
- **Featured Builds** — three curated starter loadouts baked in:
  - *The Completionist* — top Maps + all Popmenus
  - *Ears Only* — top 10 Audio mods by downloads
  - *Clean UI* — top GUI/Icons + Cursors

**Entry point:** `d-launcher/index.html` — open directly in browser.

---

## Build Order (Studio Producer)

Dependencies flow: `core/` must be extracted from v2 first. Then all four builds run in parallel since they share but don't depend on each other.

1. Extract `core/mods.js`, `core/render.js`, `core/style.css` from v2
2. Build A (static) — fastest, validates core works
3. Build B (server) — Python Flask, needs A's HTML as base
4. Build D (launcher) — creative, builds on A's card components
5. Build C (electron) — last, wraps A's HTML in native shell

---

## Success Criteria

- A: Opens in Safari/Chrome with no server, all 291 mods visible, mod drawer works, download triggers
- B: `python3 server.py` serves on :7777, install button moves a .pigg to CoH data dir
- C: `npm start` opens native window, installed mods shown as active
- D: Loadout saves/loads from localStorage, conflicts flagged, Featured Builds populate correctly
