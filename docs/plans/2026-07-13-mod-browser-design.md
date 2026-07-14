# CoX Mod Browser — Design Document
**Date:** 2026-07-13  
**Status:** Approved

---

## What We're Building

`/Users/steven/CoX-mod-Adventure/Upgraded/` — a reorganized, fully aesthetic mod browser
built on the real `mods.json` (291 mods, 8 categories).

Three phases, all approved:
- **A** — Single self-contained `mod-browser.html` (no server, opens from `file://`)
- **B** — Structured project layout (`app/`, `data/`, `scripts/`)
- **C** — Two-page site: landing (`index.html`) + browser (`mods.html`)

Starting with A. Variations encouraged at every phase.

---

## Data

`mods.json` embedded as inline JS (`const MODS = [...]`) at write time.  
Schema per entry: `id, name, author, category, downloads, description, download_url, page_url`  
Categories: Audio (172), Graphics (42), GUI/Icons (28), Other (18), Popmenus (16), Cursors (6), Maps (5), Languages (4)

---

## Typography System

All fonts available locally at `~/Library/Fonts/` — used via `@font-face` from local path.

| Role | Font | File |
|------|------|------|
| Hero title | BIRTH OF A HERO | `BIRTH_OF_A_HERO.ttf` |
| Section headers | Super Squad | `Super Squad.ttf` |
| Subheadings | Hero Bold | `Hero-Bold.ttf` |
| Body / descriptions | Hero Light | `Hero-Light.ttf` |
| Metadata / counts | Fira Code Bold | `FiraCode-Bold.ttf` |
| Category badges | Gobold | `Gobold.ttf` |
| Accent / flavor | Supersonic Rocketship | `Supersonic Rocketship.ttf` |
| Comic variant | Sonic Comic | `sonic_comic.ttf` |

---

## Image Assets

All in `~/Pictures/CoH-ComicArt/`:

| File | Use |
|------|-----|
| `KingsRow.jpeg` | Hero section background (dark urban night) |
| `TerraVolta.jpeg` | Energy accent / section divider |
| `FuturCityScape.jpeg` | Secondary hero or card bg |
| `IndepPort.jpeg` | City vista / footer atmosphere |
| `SciFiBattle.jpeg` | Action accent |
| `StatueCity.jpeg` | Iconic landmark feel |

---

## Variations

Three distinct aesthetic directions, all using the same data + font assets:

### Variation 1 · Mission Briefing Terminal
Dark ops feel. CoH's late-night briefing screen.
- BG: `#0a0a14`, KingsRow.jpeg blurred + darkened overlay
- Accent: `#f59e0b` amber gold (CoH logo color)
- Secondary: `#38bdf8` power blue
- Danger: `#ef4444` villain red
- Font hierarchy: BIRTH OF A HERO → Gobold → FiraCode
- Cards: bordered amber glow on hover, scanline CSS texture overlay
- Badges: all-caps Gobold, amber on `#1a1a2e`

### Variation 2 · Comic Book
Bold, halftone, ink-on-paper energy.
- BG: `#fdf6e3` cream / `#1a1a1a` ink
- Primary: `#e63946` comic red, `#f4a261` orange, `#2b2d42` ink black
- Font: Sonic Comic / Super Squad for all headers
- Cards: thick border `3px solid black`, drop shadow offset (`4px 4px 0 #000`)
- Halftone dot pattern via CSS radial-gradient for section backgrounds
- Category badges: bold color blocks, no border-radius (sharp corners)

### Variation 3 · Power HUD
Sci-fi energy readout. CoH's in-game UI chrome translated to web.
- BG: `#050510` near-black, FuturCityScape.jpeg as blurred bg
- Primary: `#00d4ff` electric cyan (power energy)
- Secondary: `#7c3aed` void purple
- Grid: CSS clip-path hex shapes for card corners
- Font: Space Mono for all metadata, Hero Bold for names
- Animated: subtle pulse glow on download count numbers
- Cards: diagonal cut corners via clip-path, cyan border on hover

---

## Layout (all variations share this structure)

```
┌─ HERO BANNER (KingsRow bg, title font, tagline) ──────────────┐
│  CoX MOD TERMINAL          [🔍 search mods...]                 │
├─ FILTER BAR ──────────────────────────────────────────────────┤
│  ALL  AUDIO  GRAPHICS  GUI  POPMENUS  MAPS  CURSORS  OTHER    │
│  Sort: Downloads ▾                              291 results    │
├─ CARD GRID ────────────────────────────────────────────────────┤
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐     │
│  │ AUDIO    │  │ MAPS     │  │ GUI      │  │ GRAPHICS │     │
│  │ Name     │  │ Name     │  │ Name     │  │ Name     │     │
│  │ 31k ↓   │  │ 13k ↓   │  │ 6k ↓    │  │ 3k ↓    │     │
│  │ desc...  │  │ desc...  │  │ desc..  │  │ desc..  │     │
│  │[Download]│  │[Download]│  │[Download]│  │[Download]│     │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘     │
└───────────────────────────────────────────────────────────────┘
```

---

## Interactions

- Category tab click → live filter (no reload)
- Search input → filters name + description (debounced 200ms)
- Sort dropdown → downloads desc / name A-Z / author A-Z
- Download button → `window.open(mod.download_url)` (opens cityofheroes.dev download)
- Card count updates in real time

---

## File Structure (Phase A)

```
Upgraded/
  mod-browser.html          ← Variation 1 (Terminal) — primary
  mod-browser-comic.html    ← Variation 2 (Comic Book)
  mod-browser-hud.html      ← Variation 3 (Power HUD)
  mods.json                 ← copy of canonical data
  scrape-mods.py            ← consolidated scraper/installer
  README.md
```

---

## Success Criteria

- Opens directly from `file://` with no server
- All 291 mods render
- Filter + search works live
- Download buttons link correctly
- Each variation is visually distinct
