# City of Heroes — Mod Ecosystem Master Reference

> Compiled 2026-07-14 from two deep research passes, OuroDev wiki audit, GitHub ecosystem scan,
> competing-server analysis, creator pain-point synthesis, and ReShade technical breakdown.
> Living document — update as ecosystem evolves.

---

## Table of Contents

- [1. Ecosystem Overview](#1-ecosystem-overview)
  - [1.1 Scale and Player Base](#11-scale-and-player-base)
  - [1.2 The Mod Stack](#12-the-mod-stack)
  - [1.3 How Mods Are Discovered](#13-how-mods-are-discovered)
- [2. Community Demand Signals](#2-community-demand-signals)
  - [2.1 Reddit and Social Platforms](#21-reddit-and-social-platforms)
  - [2.2 High-Engagement Forum Threads](#22-high-engagement-forum-threads)
  - [2.3 Repeat Question Patterns](#23-repeat-question-patterns)
  - [2.4 Download Signal Analysis](#24-download-signal-analysis)
- [3. GitHub Tool Ecosystem](#3-github-tool-ecosystem)
  - [3.1 Active Repositories](#31-active-repositories)
  - [3.2 Confirmed Gaps in GitHub Space](#32-confirmed-gaps-in-github-space)
- [4. Texture Modding — Full Technical Pipeline](#4-texture-modding--full-technical-pipeline)
  - [4.1 The Confirmed Workflow](#41-the-confirmed-workflow)
  - [4.2 Hard Limitations](#42-hard-limitations)
  - [4.3 Documentation Gaps That Block New Modders](#43-documentation-gaps-that-block-new-modders)
  - [4.4 Audio Modding — Separate Pipeline](#44-audio-modding--separate-pipeline)
- [5. Competing Servers](#5-competing-servers)
  - [5.1 Homecoming](#51-homecoming)
  - [5.2 Thunderspy](#52-thunderspy)
  - [5.3 Rebirth](#53-rebirth)
  - [5.4 Cross-Server Compatibility](#54-cross-server-compatibility)
- [6. Creator Pain Points](#6-creator-pain-points)
  - [6.1 Submission Process Bottleneck](#61-submission-process-bottleneck)
  - [6.2 Distribution Failures](#62-distribution-failures)
  - [6.3 Missing Infrastructure](#63-missing-infrastructure)
- [7. What Doesn't Exist — Confirmed Gaps](#7-what-doesnt-exist--confirmed-gaps)
- [8. What to Build — Ranked Opportunities](#8-what-to-build--ranked-opportunities)
  - [8.1 Mod Update Notification System](#81-mod-update-notification-system)
  - [8.2 Mod Request Board with Voting](#82-mod-request-board-with-voting)
  - [8.3 Self-Serve Mod Submission Portal](#83-self-serve-mod-submission-portal)
  - [8.4 Cross-Server Compatibility Tags](#84-cross-server-compatibility-tags)
  - [8.5 Beginner Modding Guide in Browser](#85-beginner-modding-guide-in-browser)
  - [8.6 ReShade Visual Preset Pack](#86-reshade-visual-preset-pack)
- [9. MMORPG Patterns That Transfer](#9-mmorpg-patterns-that-transfer)
- [10. ReShade — Technical Deep Dive](#10-reshade--technical-deep-dive)
  - [10.1 What ReShade Is](#101-what-reshade-is)
  - [10.2 What the .ini File Is](#102-what-the-ini-file-is)
  - [10.3 The Difference in One Sentence](#103-the-difference-in-one-sentence)
  - [10.4 Why the Same Shader Produces Wildly Different Results](#104-why-the-same-shader-produces-wildly-different-results)
  - [10.5 Execution Order Matters](#105-execution-order-matters)
  - [10.6 Shaders Used in This Pack](#106-shaders-used-in-this-pack)
- [11. ReShade Preset Pack — CoX Edition](#11-reshade-preset-pack--cox-edition)
  - [11.1 Comic Book Presets](#111-comic-book-presets)
  - [11.2 Atmospheric Presets](#112-atmospheric-presets)
  - [11.3 Technical Presets](#113-technical-presets)
  - [11.4 Preset Design Decisions](#114-preset-design-decisions)
- [12. AI Voices — NPC TTS Deep Dive](#12-ai-voices--npc-tts-deep-dive)
  - [12.1 What the Community Is Asking For](#121-what-the-community-is-asking-for)
  - [12.2 What Already Exists: Sidekick (coh_npc_voices)](#122-what-already-exists-sidekick-coh_npc_voices)
  - [12.3 The Critical Architectural Gap](#123-the-critical-architectural-gap)
  - [12.4 Buildable Actions](#124-buildable-actions)
- [13. Popmenu Mods Created](#13-popmenu-mods-created)
  - [13.1 EverlastingRP.mnu](#131-everlastingrpmnu)
  - [13.2 NewPlayerEssentials.mnu](#132-newplayeressentialsmnu)
- [14. Sources](#14-sources)

---

## 1. Ecosystem Overview

### 1.1 Scale and Player Base

City of Heroes returned from death in 2019 after the SCORE source leak and has maintained a stable private-server ecosystem ever since. Key numbers:

| Metric | Figure | Source |
|---|---|---|
| Monthly active players (Homecoming) | ~42,000 | March 2024 Homecoming stat |
| Peak concurrent | 4,431 | January 2024 license announcement weekend |
| Primary new-player wave | January 2024 | Massively OP coverage of license announcement |
| Largest rogue server | Homecoming | cityofheroes.dev infrastructure |

The January 2024 license announcement triggered a major new-player wave. Massively Overpowered's mod guide published the same month became the de-facto entry point for modding. That article is still the most-shared modding primer as of mid-2026.

### 1.2 The Mod Stack

```
Game Client (cityofheroes.exe, i27+ build)
    │
    ├── data/ override folder          ← where all client mods live
    │       └── texture_library/...   ← texture replacements
    │       └── sound/...             ← audio replacements
    │       └── menus/...             ← popmenu additions
    │
    ├── City Mod Installer             ← GUI tool, manages data/ folder
    │       └── mods.json index       ← catalog of available mods
    │
    └── ReShade (d3d9.dll)            ← post-process layer, DX9 intercept
            └── preset .ini files     ← parameter configs per look
```

The `data/` override system is the core: CoH reads from its own `.pigg` archives first, then checks the `data/` folder for overrides. Any file placed at the correct relative path silently replaces the game asset — no binary patching required.

### 1.3 How Mods Are Discovered

**Primary discovery path (new players, 2024–present):**
1. Massively OP article → cityofheroes.dev → City Mod Installer download → install

**Secondary path (veteran players):**
1. Homecoming forum Tools & Utilities section → individual mod threads → manual install or City Mod Installer

**Tertiary path:**
1. Reddit r/Cityofheroes thread → forum link → install

There is no search, no ratings, no "featured mods" editorial surface beyond the raw installer list. Vidiotmaps (31,344 downloads) achieved ~75% player penetration almost entirely through word-of-mouth and the Massively OP article.

---

## 2. Community Demand Signals

### 2.1 Reddit and Social Platforms

Reddit blocks most site-scoped search scraping, making direct upvote/comment count retrieval impossible. However, cross-referencing search signals, forum thread follower counts, and article comment sections reveals consistent patterns.

The Massively OP article "Working As Intended: How to mod City of Heroes Homecoming the easy way" (January 25, 2024) remains the single highest-impact modding content piece — widely cross-posted to r/Cityofheroes and still the first result for new players searching for CoH mods.

Screenshot posts of costume designs are the highest-engagement content type on r/Cityofheroes. Base-building showcases receive recurring editorial coverage from Massively OP. Both are visual content categories — a ReShade preset that improves screenshot quality has a clear virality path.

**The before/after gap:** No before/after visual quality comparison video exists for CoH. FFXIV has hundreds. A ReShade preset reveal post with side-by-side screenshots would be the first of its kind in the community.

### 2.2 High-Engagement Forum Threads

| Thread | Topic # | Signal |
|---|---|---|
| Quality of Life, Texture Mods, and Other Things | 9304 | **21 followers**, 4 pages — top discovery resource |
| Various Powerset Soundmods | 9586 | Actively linked in Reddit audio discussions; author accepts requests |
| Sounds/Music Mod Request | 48462 | Explicit demand for login screen music + character creation theme mods |
| AI Voices for all missions and NPCs | 45039 | Fresh May 2026 thread invoking Ascension WoW AI voice addon |
| Talking NPCs | 50337 | Each post on coh_npc_voices tool generates immediate follow-up questions |
| How do you create texture mods? | 11322 | Years old, still receiving traffic — documentation failure |
| Texture modding issue | 53769 | September 2024 — players stuck on alpha channel/bump map relationship |

### 2.3 Repeat Question Patterns

These questions appear across Reddit, the Homecoming forums, and Help & Support threads with enough frequency that they represent structural gaps rather than individual confusion:

1. **"Is there a mod that replaces [powerset X] sounds with [franchise Y]?"**
   — Audio per-powerset is covered but there is no discovery surface for requests. Authors don't know what's wanted.

2. **"How do I know if a mod still works after the last patch?"**
   — No versioning system exists. The only signal is whether the forum thread author has posted an update.

3. **"Is there a way to get HD textures / higher resolution costume textures?"**
   — Technically impossible: texture resolution is hardcoded in the client. Players don't know this; no FAQ addresses it.

4. **"Does [mod] work on Thunderspy / Rebirth too?"**
   — No compatibility tagging. All mods are implicitly Homecoming-centric.

5. **"Where do I find ALL the mods in one place?"**
   — cityofheroes.dev/mods exists but isn't well-indexed by search engines and isn't linked prominently from the Homecoming main site.

### 2.4 Download Signal Analysis

| Mod | Category | Downloads | Signal |
|---|---|---|---|
| Vidiotmaps for Homecoming | Maps | 31,344 | ~75% player penetration — ecosystem essential |
| Badge Set List Popmenu | Popmenus | 13,344 | Badge-hunting vertical is very strong |
| Optimal Badge/Plaque Path Maps | Maps | 6,946 | Badge second strongest vertical |
| Michiyo's Enhancement Standardization Pack | GUI/Icons | 3,003 | Base UI is confusing; anything that fixes it gets traction |
| Winter Event Gift Maps | Maps | 2,596 | Event-adjacent maps consistently downloaded |
| Banshee-themed Sonic Attack Sounds | Audio | 1,720 | Per-powerset audio has consistent long-tail demand |
| Bio Armor Effects Remover | Graphics | 1,419 | Visual clutter is a documented pain point |
| Beam Rifle Movie SFX | Audio | 1,253 | Franchise-adjacent audio replacements get traction |

**Key patterns:**
- Maps dominate by volume — Vidiotmaps alone represents a plurality of all mod downloads
- Badge-hunting is the second-strongest vertical — two of the top five mods serve this
- Audio SFX replacements per powerset are consistent long-tail performers (800–1,700 per release)
- FX removal mods attract downloads — visual overload from certain powersets is well-documented
- Enhancement UI fixes get traction despite being mundane

---

## 3. GitHub Tool Ecosystem

### 3.1 Active Repositories

| Repo | Stars | Last Commit | What It Does | Notes |
|---|---|---|---|---|
| LoadedCamel/MidsReborn | ~30 | Nov 25, 2025 | Offline build planner, C#, .NET 8+ | Official Homecoming forum club; star count understates actual user base |
| n15g/badger | 5 | Active | Browser-based badge tracker, TypeScript | 13 open issues on 5-star repo = disproportionately active user base |
| n15g/coh-content-db-homecoming | Active | Active | Badge/content DB data source | Data freshness pain point when Homecoming patches add badges |
| jason-kane/coh_npc_voices | Active | Jul 22, 2025 | Python TTS NPC voice via chat log | No PIGG manipulation — log-reading model |
| mikwilli/cohtools | Low | Oct 2023 | Texture extraction/reimport pipeline (Python) | |
| ovekaaven/cohtools | Low | Older | PIGG reader, .texture → .dds CLI | |
| Miravalier/CoH-Builder | Low | Older | Vanilla JS web build planner | |

**Important note on MidsReborn:** ~30 GitHub stars vastly understates adoption. The tool has a dedicated Homecoming forum club with active posts. Its user base is orders of magnitude larger than its star count — most players aren't developers and don't GitHub-star their tools.

**Important note on coh_npc_voices:** Last commit July 22, 2025 — the most recently active modding-adjacent repo. Works entirely via the CoH chat log file. No PIGG manipulation means no install risk. This is the lightweight model for other log-based overlays, parsers, or HUD-adjacent tools.

### 3.2 Confirmed Gaps in GitHub Space

These do not exist in any form on GitHub or any other public code repository:

- Community mod browser (web, native, or CLI)
- Mod update notifier / version checker
- Mod compatibility checker (cross-server or cross-version)
- Self-serve mod submission tool
- Mod conflict detector (CLI or web)
- Semantic versioning infrastructure for any CoH mod
- Cross-server compatibility matrix

GShade (Mortalitas/GShade) lists CoH among its 300+ supported games — meaning some players already run post-processing overlays on CoH without community awareness. No CoH-specific ReShade or GShade preset pack exists on any mod platform (cityofheroes.dev, Nexus Mods, or GitHub).

---

## 4. Texture Modding — Full Technical Pipeline

### 4.1 The Confirmed Workflow

The OuroDev wiki documents the complete texture replacement process. This is the only officially documented path as of 2026:

```
1. Open Pigg Viewer Pro
   └── Navigate to Homecoming Piggs/ folder

2. Find target texture
   └── Right-click → "Extract As DDS"
   └── Save lossless backup (.tga / .png / .bmp) ← REQUIRED

3. Edit the texture
   └── Any DDS-capable editor: Photoshop + NVidia Texture Tools, GIMP, Paint.NET
   └── Make changes to the extracted .dds

4. Save with correct compression
   └── Textures with alpha channel → DXT5 compression
   └── Textures without alpha → DXT1 compression

5. Convert back using Pigg Viewer 1.61
   └── Right-click original texture → "Create texture from .dds"
   └── Note the output path (always starts with texture_library/)

6. Place in data/ override folder
   └── Copy full path: data/texture_library/[rest of path]
   └── Game reads this as override on next launch
```

The `data/` folder override is the same mechanism used by all client-side mods regardless of category. No binary patching, no game-file modification — purely additive.

### 4.2 Hard Limitations

These are documented constraints, not bugs. Understanding them prevents hours of confusion:

**Texture resolution is hardcoded.**
The engine reads textures at their original pixel dimensions. You cannot increase resolution. A 256×256 costume texture cannot become 512×512. "HD texture pack" requests in the community are technically impossible with the current client architecture. No workaround exists.

**Texture components are linked.**
Each surface has up to seven associated maps: diffuse, grayscale, bump map, gloss map, specular map, color mask, and transparency channel. Altering the diffuse texture without updating the bump map and specular will cause lighting artifacts — shadows and reflections will appear to float incorrectly. Full replacements require coordinated edits to all linked maps.

**DDS compression artifacts accumulate.**
DDS (DirectDraw Surface) uses lossy block compression similar to JPEG. Each save-to-DDS introduces generation loss. The wiki explicitly warns: always save a lossless intermediate (.tga, .png, .bmp) before converting to DDS. Mod authors who skip this cannot iterate cleanly — their second-generation edits start from already-degraded source.

**No batch tools.**
Pigg Viewer operates through a GUI — every texture must be extracted and reimported individually. There is no CLI batch mode, no scripted pipeline, no way to export or import a folder of textures at once.

**Pigg Viewer 1.61 is the only option.**
The wiki states this explicitly. It is the only program capable of texture-to-pigg conversion without hex editing. No CLI alternative exists. No open-source equivalent. Single-tool dependency with no fallback.

### 4.3 Documentation Gaps That Block New Modders

The OuroDev wiki was last meaningfully updated around 2019. It predates City Mod Installer entirely. These gaps cause repeated forum support threads:

| Gap | Impact |
|---|---|
| No reference to City Mod Installer | New modders don't know whether to use installer or manual `data/` folder |
| No asset map (which .pigg contains which assets) | Modders spend hours searching for target textures |
| No bump map generation tool documentation | Wiki says "generate a bump map by some means" — no tool is named |
| Audio and texture docs fully separate | No cross-reference; players doing both must find two separate doc sets |
| No file collision documentation | No explanation of what happens when two mods overwrite the same file |
| No post-2019 update | Doesn't reflect current client version, server options, or community practices |

### 4.4 Audio Modding — Separate Pipeline

Audio modding is documented separately from texture modding with no cross-references. The pipeline is simpler:

- Audio files are OGG format
- Replacement files go in `data/sound/` at the matching path from the `.pigg` archives
- No specialized conversion tool required beyond a standard audio editor
- The same `data/` override mechanism applies

The lack of cross-referencing between audio and texture documentation means players doing both have to discover each independently. A unified modding guide would significantly reduce this friction.

---

## 5. Competing Servers

### 5.1 Homecoming

The reference implementation and largest rogue server. Infrastructure:
- **cityofheroes.dev** — mod browser + City Mod Installer (Windows + Mac)
- **Homecoming Forums** — Tools & Utilities section is primary pre-installer mod discovery surface
- **Mids Reborn** — officially recognized Homecoming forum club
- **Explicit mod permissiveness** — Homecoming's staff has publicly confirmed client-side mods are allowed

### 5.2 Thunderspy

The most technically divergent server. Their customization philosophy differs fundamentally:

- Implements customization **server-side** rather than via client mods
- Full color sliders, extended body scale sliders, pet customization, customizable player apartments
- April 2026 patch: new color picker with hue slider, saturation/brightness control, hex input, favorite swatches, color history
- This is a fundamentally different model: Thunderspy builds into the engine what other servers' players achieve via client mods
- No Thunderspy-specific mod browser found
- Patreon at patreon.com/coxg confirms ongoing independent funding

### 5.3 Rebirth

Positions itself as closer to the original Paragon Studios vision. Notable April 2026 development:

**City of Heroes Multiverse Launcher** (released April 29, 2026, Massively OP coverage):
- Designed as shared entry point for ALL rogue servers
- Each server can customize launcher skin (backgrounds, links, news feeds)
- Reduces discovery friction for smaller servers
- Signals formalization of the multi-server ecosystem

Their wiki (wiki.cityofheroesrebirth.com) exists but has no server-specific mod browser. A forum thread "Attempt: Developing Web Mids" (topic 3322) shows independent developer energy building web-based tools — momentum without infrastructure.

### 5.4 Cross-Server Compatibility

| Question | Answer |
|---|---|
| Do client mods work on all servers? | In principle yes — all i27+ servers share the same client binary |
| Is Thunderspy compatible? | Uncertain — their server-side engine changes may affect some UI mods |
| Is Rebirth compatible? | Yes for most mods — closer to Homecoming architecture |
| Does any compatibility matrix exist? | No. Nowhere. |
| Does City Mod Installer tag mods by server? | No. All mods are implicitly Homecoming-centric |

The April 2026 Multiverse Launcher is the strongest signal yet that cross-server compatibility tagging is becoming necessary. Players will increasingly run multiple servers from one client. The Multiverse Launcher makes server-hopping frictionless; the mod ecosystem hasn't caught up.

---

## 6. Creator Pain Points

### 6.1 Submission Process Bottleneck

The current mod submission workflow, as reconstructed from forum threads and the Massively OP article:

```
1. Author creates mod files (correct data/ folder structure)
2. Author posts to Homecoming forum Tools & Utilities section
3. Author contacts Michiyo (mod site operator) to request addition to installer
4. Michiyo packages the mod and adds it to the installer index
5. For updates: repeat from step 3 — re-contact Michiyo for each version
```

**Michiyo is a single point of failure.** There is no self-serve upload mechanism, no author dashboard, no alternative path. The absence of any self-serve submission portal on cityofheroes.dev (and the existence of a `beta.mods.cityofheroes.dev` URL) suggests active iteration is happening — but authors currently have no alternative to the gatekeeper path.

### 6.2 Distribution Failures

**Google Drive rot:** "Various Powerset Soundmods" (topic 9586) distributes via Google Drive. When mod authors stop maintaining their accounts, Drive links expire or get removed. Several older forum mod posts already have dead download links. There is no content-addressed storage, no mirroring, no archive.

**Forum thread as version history:** When a mod updates, the only signal is a post edit or a new reply in the author's forum thread. A user who installed the mod 6 months ago has no way to discover an update unless they manually revisit. No push signal, no diff, no version number in the installer UI.

### 6.3 Missing Infrastructure

Every pain point maps to a specific piece of infrastructure that doesn't exist:

| Pain Point | Missing Infrastructure |
|---|---|
| No update signal for installed mods | Server-side version tracking + changelog |
| Dead distribution links | Hosted file storage on mod platform |
| No author profile or portfolio | Author identity system with mod listing |
| Zero download metrics | Author analytics dashboard |
| No conflict warning outside installer | Conflict checker (web or CLI) |
| Manual request aggregation only | Community mod request board |
| Michiyo bottleneck | Self-serve submission portal |
| No per-server compatibility info | Compatibility tagging system |

---

## 7. What Doesn't Exist — Confirmed Gaps

These were verified absent from cityofheroes.dev, Nexus Mods, GitHub, and forum searches as of mid-2026:

| Missing Mod / Tool | Category | Why It Matters |
|---|---|---|
| ReShade / post-processing presets | Visual | FFXIV has hundreds; CoH has zero; DX9-compatible |
| Full zone ambient audio packs | Audio | Individual power SFX covered; no zone music replacements |
| Power FX texture packs (enhancement, not removal) | Visual | Only FX removal exists; reskins are absent |
| Colorblind accessibility texture pack | Accessibility | No colorblind-safe palette replacement for UI elements anywhere |
| Font scaling mod | UI | Chat size slider only; no fix for small text at 1440p/4K |
| Power recharge HUD overlay | UI | Native timer only on power tray button; no consolidated display |
| Costume preset browser | UI | Icon Catalogue is a separate site; not installer-integrated |
| IO set bonus tracker overlay | UI | Mids Reborn is offline-only; no live in-game display |
| Roleplay tools for Everlasting server | Social | Base location popmenu exists; nothing else |
| Archetype-scoped audio bundles | Audio | Individual powers only; no cohesive archetype pack |
| Community mod browser (GitHub) | Infrastructure | No open-source mod browser exists |
| Mod update notifier | Infrastructure | No versioning or push notification system exists |
| Cross-server compatibility matrix | Infrastructure | No documentation exists |
| Self-serve mod submission | Infrastructure | Gatekeeper bottleneck with no alternative |
| Beginner's modding guide (current) | Documentation | OuroDev wiki ~2019; predates City Mod Installer |

---

## 8. What to Build — Ranked Opportunities

### 8.1 Mod Update Notification System

**Confidence: Highest. Existing solutions: Zero.**

Every mod is a static file drop. No semantic versioning, no changelogs, no push notifications. City Mod Installer already tracks what's installed locally on each player's machine. The missing component is server-side:

- Per-mod `version` and `updated_date` fields in the catalog (already partially present in `core/mods.js` — 11 of 291 mods have version strings)
- Changelog entries per version
- Email / RSS opt-in per installed mod
- "Updates available" badge in the mod browser UI

This mirrors ESO Minion's update check flow exactly. The infrastructure exists for the local side; the server side needs one new API endpoint and a notification delivery mechanism.

**Buildable without game access. No binary modification. Pure web/API work.**

### 8.2 Mod Request Board with Voting

**Confidence: High. Buildable in ~6 days.**

Audio and texture mod requests currently live in individual creator threads scattered across the forum. There is no centralized place to signal unmet demand. Topics 48462 (login screen music), 45039 (AI voices), and 9586 (audio author accepting requests) all represent the same structural gap — ad-hoc, invisible, and not aggregated.

A votable request board:
- Players post mod requests by category (audio / texture / UI / map / popmenu)
- Upvoting makes demand visible
- Mod authors get a prioritized work queue
- Fulfilled requests close the loop (link to released mod)
- Creates supply→demand feedback cycle the current forum system cannot

Analog: WoW addon request boards on CurseForge. The pattern is proven.

### 8.3 Self-Serve Mod Submission Portal

**Confidence: High. Removes single-person bottleneck.**

Fields: mod name, category, version, changelog, compatible servers, description, screenshot, download file.
Author dashboard: download count per mod, version history, update push.

The `beta.mods.cityofheroes.dev` URL exists — active platform iteration is underway. This is the natural next capability. Without it, every new mod and every mod update requires manual intervention from one person.

**Secondary benefit:** Removes Google Drive as distribution layer — files hosted on platform, links permanent.

### 8.4 Cross-Server Compatibility Tags

**Confidence: Medium-high. Low effort, growing need.**

Simple tag system per mod: `tested on: Homecoming / Rebirth / Thunderspy / Reunion`. Browse filter to show only mods confirmed for a given server. With the Multiverse Launcher lowering the friction to run multiple servers, players will increasingly have this question. The current answer is "ask in the forum thread."

**Complexity: low.** Database field + UI filter. The hard part is data — it requires authors or community volunteers to actually test mods on each server.

### 8.5 Beginner Modding Guide in Browser

**Confidence: Medium-high. Fills a documented gap.**

OuroDev wiki: last updated ~2019, doesn't mention City Mod Installer, has five documented gaps (see [Section 4.3](#43-documentation-gaps-that-block-new-modders)). Topic 11322 "How do you create texture mods?" still receives traffic years later — the current documentation fails to capture first-time creators before they hit friction.

An integrated "Make a Mod" guide on cityofheroes.dev covering:
1. Tools required (Pigg Viewer 1.61, DDS-capable editor)
2. The `data/` folder override system explained
3. Texture workflow (DXT5 compression, linked maps, resolution limits)
4. Audio workflow (OGG format, sound/ path structure)
5. Popmenu syntax basics
6. How to submit to City Mod Installer

Would convert forum readers into mod creators. Expands supply side of the ecosystem.

### 8.6 ReShade Visual Preset Pack

**Confidence: High. First of its kind. Zero competition.**

No CoH ReShade presets exist anywhere. FFXIV has hundreds. CoH runs DX9 — fully ReShade-compatible. GShade already lists CoH among 300+ supported games, meaning some players run ReShade unguided with no presets.

This pack (see [Section 11](#11-reshade-preset-pack--cox-edition)) is the first-ever CoH-specific ReShade preset pack. Pure `.ini` configuration files — no game access needed, no binary manipulation, no PIGG files.

**Viral potential:** Screenshot content is the highest-engagement post type on r/Cityofheroes. A before/after ReShade comparison post would be the first visual quality comparison content ever created for CoH. FFXIV community enthusiasm for screenshot presets is well-documented. CoH's superhero aesthetics are uniquely suited to comic-book-style post-processing.

---

## 9. MMORPG Patterns That Transfer

The tools and infrastructure that exist in other MMOs map cleanly onto CoH's gaps:

| Pattern | Source Game | CoH Translation | Status |
|---|---|---|---|
| Post-processing presets | FFXIV GShade/ReShade | ReShade preset pack (DX9) | **Built — this pack** |
| Mod manager with conflict resolution | FFXIV Penumbra | City Mod Installer upgrade | Not started |
| Addon update checker | ESO Minion | Mod update notification system | Not started |
| Shareable HUD overlay strings | WoW WeakAuras | Exportable popmenu configs | Not started |
| Map pin overlay | ESO / GW2 | Vidiotmaps (exists; expand layer system) | Vidiotmaps exists |
| Mod profile switching | FFXIV Penumbra | Save/load named mod sets | Not started |
| Votable mod requests | CurseForge community | Mod request board | Not started |
| Combat log parser/overlay | GW2 ArcDPS | CoH has log; parser doesn't exist | Not started |
| Per-server launcher | WoW PTR system | Rebirth Multiverse Launcher | Rebirth built this (April 2026) |

**The closest analog for what CoH's mod ecosystem needs to become:**
- **FFXIV Penumbra** = what City Mod Installer wants to be (conflict resolver, live reload, per-character profiles)
- **ESO Minion** = what the update check system should be
- **WeakAuras** = what a CoH HUD overlay system would look like
- **Minecraft's CurseForge/Modrinth model** = the infrastructure layer CoH entirely lacks

**Key GW2 / private server advantage:** CoH has a more permissive environment than games with live commercial servers. The Homecoming team openly endorses client-side tools. This is a significant advantage — building equivalent tooling for CoH carries no ToS risk that FFXIV or WoW tools always navigate around.

---

## 10. ReShade — Technical Deep Dive

### 10.1 What ReShade Is

ReShade is a **DLL injector**. When you run the installer, it drops a file called `d3d9.dll` (for DX9 games like CoH) into the game folder. When CoH launches and tries to load DirectX 9, Windows finds ReShade's DLL first — ReShade intercepts every frame the game renders, runs its shader passes over it, and hands the modified frame to the display.

The game has no idea this is happening. ReShade sits between the game's output and your monitor.

```
Game renders frame
    │
    ▼
ReShade intercepts (d3d9.dll)
    │
    ├── Runs Cartoon.fx        (ink edge detection)
    ├── Runs Bloom.fx          (glow on bright regions)
    ├── Runs Vibrance.fx       (saturation adjustment)
    └── ... (in TechniqueSorting= order)
    │
    ▼
Modified frame reaches your monitor
```

ReShade ships with a library of **effect shaders** written in HLSL (High-Level Shader Language) — files like `Cartoon.fx`, `Bloom.fx`, `Vignette.fx`. These are the actual programs that process pixels. Each one takes the rendered frame as input and outputs a modified version.

### 10.2 What the `.ini` File Is

The `.ini` is just a **saved configuration** — it doesn't contain any shader code. It's a plain text key-value file that tells ReShade three things:

1. **Which shaders to activate** — the `Techniques=` line
2. **In what order to run them** — the `TechniqueSorting=` line
3. **What parameter values to use** — every `[ShaderName.fx]` block with its slider values

```ini
[Cartoon.fx]       ← which shader block
Power=2.80         ← parameter value passed into the shader
EdgeSlope=2.20     ← another parameter

[Bloom.fx]
BloomThreshold=0.60
BloomAmount=0.45
BloomSaturation=2.00

Techniques=SMAA,Cartoon,Bloom        ← which shaders are active
TechniqueSorting=SMAA,Cartoon,Bloom  ← order they run in
```

When you move a slider in the ReShade overlay in-game, it writes updated numbers into the `.ini` in real time. The file on disk is the live state of your preset.

### 10.3 The Difference in One Sentence

> **ReShade is the engine. The `.ini` is the settings file. The `.fx` files are the effects. You only distribute the `.ini` — players already have the engine and effects after running the installer.**

This is why sharing presets is trivial: you send an 80-line text file. The recipient already has all the shader code — they just needed someone to find the right parameter values.

### 10.4 Why the Same Shader Produces Wildly Different Results

`Cartoon.fx` with `Power=0.80` (RetroTV preset) vs `Power=3.20` (InkLines preset) runs the **exact same Sobel convolution code** — the `Power` parameter just controls how aggressively the detected edges are darkened. Same shader, radically different look.

```
Power=0.80  →  subtle ink suggestion  (RetroTV — cartoon Saturday morning look)
Power=1.80  →  clear comic outlines   (ComicVivid — standard superhero book)
Power=2.80  →  heavy borders          (Halftone — Lichtenstein flat-color print)
Power=3.20  →  stark black lines      (InkLines — Frank Miller noir)
```

This is why 11 presets can exist as 11 tiny text files sharing the same 13 installed shaders. The shader library is fixed. The parameter space is enormous.

### 10.5 Execution Order Matters

`TechniqueSorting=` is not cosmetic. The order shaders run determines what each shader "sees" as its input — which is the output of the previous shader.

**Example: `CoX_SplashPage.ini`**

```
Cartoon → ColorMatrix → Levels → Curves → Vibrance → Tonemap → Clarity → Bloom → Vignette
```

- `Cartoon` runs **first** — it draws ink edges on the **fully-colored** frame
- `ColorMatrix` then desaturates to near-monochrome
- `Bloom` runs **last** (before Vignette) — it adds glow to whatever is still bright after all the desaturation

If you swapped Cartoon and ColorMatrix:
- Cartoon would draw edges on the **already-grey** frame
- The ink lines would be grey, not black
- The comic-book edge effect would be lost

If you swapped Bloom to run before ColorMatrix:
- Bloom would re-saturate the still-colored frame
- Then ColorMatrix would desaturate everything including the bloom
- The "spot color powers only" effect would disappear

Order changes the result even with identical parameter values. This is why `TechniqueSorting=` is always explicitly set rather than left to default.

### 10.6 Shaders Used in This Pack

| Shader | Effect | Used In |
|---|---|---|
| `SMAA.fx` | Subpixel Morphological Anti-Aliasing — smooth jagged edges | All presets |
| `FXAA.fx` | Fast Approximate Anti-Aliasing — additional edge smoothing | CleanHD, CinematicHero |
| `Cartoon.fx` | Sobel edge detection → ink outline simulation | All comic/atmospheric presets |
| `Bloom.fx` | Bright-region glow expansion | ComicVivid, InkLines, SplashPage, NeonCity, RetroTV, CinematicHero |
| `Clarity.fx` | Mid-tone contrast sharpening | All presets |
| `ColorMatrix.fx` | 3×3 color matrix transformation | DarkGritty, SplashPage |
| `Curves.fx` | Tone curve adjustment (contrast, S-curve posterization) | Most presets |
| `FilmGrain.fx` | Analog noise overlay | DarkGritty, GoldenAge, RetroTV |
| `Levels.fx` | Black/white point compression | All presets |
| `LumaSharpen.fx` | Luminance-based edge sharpening | CleanHD, CinematicHero |
| `SplitToning.fx` | Independent shadow/highlight color wash | SilverAge, GoldenAge, NeonCity, RetroTV, CinematicHero |
| `Tonemap.fx` | Exposure, gamma, bleach, saturation | All presets |
| `Vibrance.fx` | Selective saturation (protects already-saturated colors) | All presets |
| `Vignette.fx` | Edge darkening | All presets |

---

## 11. ReShade Preset Pack — CoX Edition

Eleven presets organized into three categories. All are `.ini` files in `mods-to-create/reshade/`.

### 11.1 Comic Book Presets

These use `Cartoon.fx` as their core effect — Sobel edge detection that draws ink outlines on geometry and costume boundaries.

| Preset | File | Core Technique | Distinguishing Feature |
|---|---|---|---|
| **Comic Vivid** | `CoX_ComicVivid.ini` | Cartoon (Power 1.8) + Vibrance | High saturation, punchy contrast, subtle bloom. The "standard superhero comic" look. |
| **Ink Lines** | `CoX_InkLines.ini` | Cartoon (Power 3.2) + ColorMatrix desaturate + Bloom spot-color | Near-monochrome world; glowing powers stay vivid. Frank Miller noir. |
| **Silver Age** | `CoX_SilverAge.ini` | Cartoon (Power 1.2) + SplitToning amber | Soft outlines, warm paper tones. 1960s Kirby/Ditko offset printing. |
| **Golden Age** | `CoX_GoldenAge.ini` | Cartoon (Power 2.2) + SplitToning deep amber + FilmGrain | Yellowed newsprint, heavier outlines, period grain. 1940s wartime comics. |
| **Halftone** | `CoX_Halftone.ini` | Cartoon (Power 2.8) + Curves (Formula 4 posterize) | Hard contrast posterization simulates Ben-Day dot flat color. Lichtenstein aesthetic. |
| **Splash Page** | `CoX_SplashPage.ini` | Cartoon (Power 2.6) + ColorMatrix near-BW + Bloom (Saturation 3.5) | World goes near-monochrome ink; power effects burn through in vivid spot color. |

### 11.2 Atmospheric Presets

These focus on mood and environment rather than the comic-book ink-line aesthetic.

| Preset | File | Core Technique | Distinguishing Feature |
|---|---|---|---|
| **Neon City** | `CoX_NeonCity.ini` | SplitToning deep blue shadows + heavy Bloom + low Exposure | Dark base city; powers glow electric. Paragon City at 2am. |
| **Retro TV** | `CoX_RetroTV.ini` | Cartoon (Power 0.8) + SplitToning warm phosphor + FilmGrain | Soft Saturday morning cartoon on a 1970s CRT. Phosphor glow on all light sources. |
| **Cinematic Hero** | `CoX_CinematicHero.ini` | SplitToning teal shadows / orange highlights + LumaSharpen | Hollywood blockbuster color grade. MCU theatrical aesthetic. |
| **Dark Gritty** | `CoX_DarkGritty.ini` | ColorMatrix desaturate + Bleach + FilmGrain + heavy Vignette | Noir villain content. Desaturated, crushed blacks, cinematic. |

### 11.3 Technical Presets

| Preset | File | Core Technique | Distinguishing Feature |
|---|---|---|---|
| **Clean HD** | `CoX_CleanHD.ini` | SMAA + FXAA + LumaSharpen + minimal color | Strong AA, subtle sharpening, neutral grade. Makes CoH look like a modern engine at 1440p/4K. |

### 11.4 Preset Design Decisions

**Why Cartoon.fx runs first in comic presets:**
Edge detection must happen on the full-color frame to produce black ink lines. If color grading runs first and desaturates the image, Cartoon produces grey lines, not black.

**Why Bloom runs late in comic presets:**
Bloom expands bright regions. Running it late (after all color grading) means it only amplifies whatever survived the other passes — in dark/desaturated presets like SplashPage and InkLines, only the power effects remain bright enough to trigger the bloom threshold. This creates the spot-color effect without requiring any per-asset tagging.

**Why SplashPage has Bloom Saturation=3.5:**
This is intentionally extreme. The base image is already desaturated to ~20% saturation by ColorMatrix + Vibrance. A bloom saturation of 3.5× is needed to overcome that desaturation and produce vivid color only in the bloom regions. At normal saturation (0.8–1.4), the bloom would add grey-white glow, not color.

**Why CleanHD uses both SMAA and FXAA:**
SMAA (Subpixel Morphological Anti-Aliasing) is geometrically accurate but can miss fine single-pixel detail. FXAA (Fast Approximate Anti-Aliasing) catches those but can blur texture detail. Running SMAA first handles geometry, then FXAA cleans up remaining single-pixel jaggies — complementary passes rather than redundant ones.

---

## 12. AI Voices — NPC TTS Deep Dive

> Full source audit: [`data/ai-voices-research.md`](ai-voices-research.md)
> Concept docs: [`mods-to-create/ai-voices/CONCEPT-v1.md`](../mods-to-create/ai-voices/CONCEPT-v1.md) (snippet pass) → [`mods-to-create/ai-voices/CONCEPT.md`](../mods-to-create/ai-voices/CONCEPT.md) (primary source pass)
> Contact profiles: [`mods-to-create/ai-voices/contact_profiles.json`](../mods-to-create/ai-voices/contact_profiles.json)

### 12.1 What the Community Is Asking For

**Thread:** "AI Voices for all missions and NPCs." — Homecoming Suggestions, topic 45039, May 3, 2026.

Players want AI-generated voice acting for NPC dialogue and mission text, citing Ascension WoW's VoiceOver addon as the model. This is a 15-year-old request — the 2009 live-game forum archive (topic 198865) has players fantasy-casting voice actors for specific NPCs. No Homecoming developer has publicly acknowledged any voice-related suggestion thread. No roadmap mention found.

### 12.2 What Already Exists: Sidekick (coh_npc_voices)

- **GitHub:** github.com/jason-kane/coh_npc_voices — v4.5.3 (Nov 22, 2025), 43 total issues filed
- **Architecture:** File-system watcher on `chatlog.txt`. Zero game binary access. SQLite cache (`voices.db`) for near-zero API cost on repeated lines. Async audio since v4.0.0 (multiple NPCs simultaneously).
- **TTS Engines:** Windows TTS (free, low quality) → Amazon Polly / Azure / Google → **OpenAI TTS (~$4/mo, recommended)** → ElevenLabs (~$5–22/mo, burns through free tier in 4 days)
- **Per-NPC effects:** Clockwork faction already gets vocoder/robotic pitch via numpy. Ring modulator available.
- **Developer:** jason-kane — sole maintainer, often same-day response. Receptive to contributions.

### 12.3 The Critical Architectural Gap

**Mission briefing popup text does not appear in the chat log.** Contact briefings, debriefs, clue text, and souvenir text are rendered as in-game popup windows — never entering the chat system. coh_npc_voices is structurally blocked from voicing them.

| Content Type | In Chat Log? | Voiced by Sidekick? |
|---|---|---|
| NPC speech bubbles in missions | Yes | Yes |
| Contact greetings (world dialogue) | Yes | Yes |
| **Mission briefing text** | **No** | **No** |
| **Clue / souvenir text** | **No** | **No** |
| **Contact phone call text** | **No** | **No** |

Ascension WoW's VoiceOver reads quest data from game memory directly — a different architecture entirely. Equivalent CoH implementation would require binary modification or server-side support.

### 12.4 Buildable Actions

1. **Immediate:** Contribute `contact_profiles.json` to jason-kane/coh_npc_voices — NPC name → voice personality mapping for common contacts. Jason Kane is active and receptive. This gets proper voiced NPCs to existing Sidekick users without a fork. (File exists at `mods-to-create/ai-voices/contact_profiles.json` — 24 named contacts + 9 faction defaults.)

2. **Near-term:** PyInstaller one-page `.exe` installer for Sidekick — removes Python setup barrier. Bundle OpenAI engine as default. Drop setup from "install Python, configure API key in a config file" to "run installer, paste your OpenAI key."

3. **Long-term:** Pre-generated audio pack for iconic contacts (Ghost Widow, Lord Recluse, Statesman, Ms. Liberty, etc.) shipped as a City Mod Installer mod with `data/sound/` overrides. Requires solving the audio event path mapping — no infrastructure currently exists for mission text audio triggers.

---

## 13. Popmenu Mods Created

> Popmenu files: `mods-to-create/popmenus/`
> Install path: `data/menus/` in the CoH client directory

### 13.1 EverlastingRP.mnu

**Target audience:** Everlasting server roleplay community (largest RP server in Homecoming)
**Bind:** `/bind LSHIFT+R "popmenu EverlastingRP"`
**File:** `mods-to-create/popmenus/everlasting-rp/EverlastingRP.mnu`

| Submenu | Contents |
|---|---|
| Emotes | Greetings, Casual, Dramatic, Seated, Dance categories |
| IC/OOC Status | `/title` commands for roleplay availability signaling |
| Scene Setters | Emote-based ambient atmosphere narration |
| RP Wrappers | OOC markers, RP pause/resume, scene transitions |
| Zone Locations | Common RP gathering spots and IC scene locations |
| SG Base Atmosphere | Base ambience and scene framing |
| Contact Info | Global name and social channel sharing |
| Combat RP | Narration options for action sequences |

**Why a popmenu vs keybinds:** Keybind slots are finite (~100 usable) and RP emotes number in the hundreds. A popmenu is infinitely extensible and self-documenting — the player can browse rather than memorize.

### 13.2 NewPlayerEssentials.mnu

**Target audience:** Players new to City of Heroes Homecoming
**Bind:** `/bind F10 "popmenu NewPlayerEssentials"`
**File:** `mods-to-create/popmenus/essentials-bundle/NewPlayerEssentials.mnu`

| Submenu | Contents |
|---|---|
| Graphics | Quality presets, UI scale, screenshot with/without UI |
| Sound | Mute/restore all, music/effects independent control |
| Camera | Distance, first-person, mouse look, free camera |
| Combat | Auto-run, speed, targeting, follow/stay |
| Chat Channels | Say, team, league, SG, General, Help, LFG, Trade |
| Powers Display | FX detail levels, nameplate and health bar toggles |
| Team Tools | LFG panel, invite, kick, leave, sidekick |
| Badges | Badge window, count, announce, Vidiotmaps tip |
| Costume | Costume creator, slot switching, CC emote |
| UI Windows | Toggle chat, map, trays, clue, mission windows; hide-all for screenshots |
| Tips | Where to get mods, Mids Reborn, global names, cmdlist reference |

**Distribution note:** This mod directly teaches players where to find more mods (`/say City Mod Installer`) — it's self-referential marketing for the broader mod ecosystem.

---

## 14. Sources

### Community and Forum Sources
- [Working As Intended: How to mod CoH Homecoming (Massively OP, Jan 2024)](https://massivelyop.com/2024/01/25/working-as-intended-how-to-mod-city-of-heroes-homecoming-the-easy-way/)
- [Homecoming 2025 Roadmap (Massively OP)](https://massivelyop.com/2025/01/08/city-of-heroes-homecoming-offers-a-brief-roadmap-with-two-major-updates-planned-for-2025/)
- [Rebirth Multiverse Launcher (Massively OP, April 2026)](https://massivelyop.com/2026/04/29/city-of-heroes-rebirth-devs-release-a-new-launcher-to-support-the-communitys-rogue-servers/)
- Quality of Life, Texture Mods, and Other Things — Homecoming forum topic 9304
- Various Powerset Soundmods — topic 9586
- Sounds/Music Mod Request — topic 48462
- AI Voices for all missions and NPCs — topic 45039
- Talking NPCs — topic 50337
- How do you create texture mods? — topic 11322
- Texture modding issue — topic 53769
- City Mod Installer Released — topic 49175
- CoH Mods master forum thread — topic 4634
- Vidiotmaps for Homecoming — topic 37216
- Homecoming Updated Texture Guide — topic 48234
- Complete Homecoming Texture Guide — topic 64109
- Rebirth Web Mids thread — forum.cityofheroesrebirth.com topic 3322

### Technical Documentation
- [OuroDev Texture Modding Wiki](https://wiki.ourodev.com/Texture_modding)
- [OuroDev Texture Maps Basics](https://wiki.ourodev.com/view/Texture_Maps_Basics)
- [StrategyWiki CoH Clientmods](https://strategywiki.org/wiki/City_of_Heroes/Clientmods)

### GitHub Repositories
- [LoadedCamel/MidsReborn](https://github.com/LoadedCamel/MidsReborn)
- [n15g/badger](https://github.com/n15g/badger)
- [n15g/coh-content-db-homecoming](https://github.com/n15g/coh-content-db-homecoming)
- [jason-kane/coh_npc_voices](https://github.com/jason-kane/coh_npc_voices)
- [ovekaaven/cohtools](https://github.com/ovekaaven/cohtools)
- [mikwilli/cohtools](https://github.com/mikwilli/cohtools)
- [GitHub city-of-heroes topic](https://github.com/topics/city-of-heroes)

### Server and Platform Sources
- [mods.cityofheroes.dev](https://mods.cityofheroes.dev/)
- [cityofheroes.dev](https://cityofheroes.dev/)
- [Thunderspy](https://thunderspy.net/) — patch notes and server details
- [Rebirth Multiverse Launcher official](https://www.cityofheroesrebirth.com/public/multiverse_launcher.phtml)
- [Nexus Mods CoH](https://www.nexusmods.com/cityofheroes/mods/latest/)

### Related Project Files
- [`data/community-research.md`](community-research.md) — first research pass (download signals, top 10 opportunities)
- [`data/community-research-deep.md`](community-research-deep.md) — second pass (5 angles, GitHub ecosystem, texture pipeline, server comparison, creator pain points)
- [`data/ai-voices-research.md`](ai-voices-research.md) — full AI voices source audit (forum threads, GitHub coh_npc_voices, wow-voiceover comparison)
- [`mods-to-create/reshade/RESHADE-EXPLAINED.md`](../mods-to-create/reshade/RESHADE-EXPLAINED.md) — standalone ReShade/ini explainer
- [`mods-to-create/reshade/INSTALL.md`](../mods-to-create/reshade/INSTALL.md) — preset pack install guide with all 11 presets
- [`mods-to-create/ai-voices/CONCEPT-v1.md`](../mods-to-create/ai-voices/CONCEPT-v1.md) — AI voices concept (snippet-based pass)
- [`mods-to-create/ai-voices/CONCEPT.md`](../mods-to-create/ai-voices/CONCEPT.md) — AI voices concept (primary source pass, v2)
- [`mods-to-create/ai-voices/contact_profiles.json`](../mods-to-create/ai-voices/contact_profiles.json) — NPC voice personality profiles (24 contacts + 9 faction defaults)
- [`mods-to-create/popmenus/everlasting-rp/EverlastingRP.mnu`](../mods-to-create/popmenus/everlasting-rp/EverlastingRP.mnu) — RP popmenu for Everlasting server
- [`mods-to-create/popmenus/essentials-bundle/NewPlayerEssentials.mnu`](../mods-to-create/popmenus/essentials-bundle/NewPlayerEssentials.mnu) — new player reference popmenu
