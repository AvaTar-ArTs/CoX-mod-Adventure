# CoH Mod Ecosystem — Community Research Report
> Generated 2026-07-14 by trend-researcher agent sweep

---

## 1. What Players Are Actively Searching For

### Download Signals — Confirmed Demand

| Mod | Category | Downloads |
|---|---|---|
| Vidiotmaps for Homecoming | Maps | 31,344 |
| Badge Set List Popmenu | Popmenus | 13,344 |
| Optimal Badge/Plaque Path Maps | Maps | 6,946 |
| Universal Emotes Popmenu | Popmenus | 3,548 |
| Michiyo's Enhancement Standardization Pack | GUI/Icons | 3,003 |
| Winter Event Gift Maps | Maps | 2,596 |
| Halloween Event GM Maps | Maps | 2,270 |
| Banshee-themed Sonic Attack Sounds | Audio | 1,720 |
| Base Teleporter Beacon Labels | Graphics | 1,554 |
| Less Annoying Sounds Mod | Audio | 1,355 |
| Bio Armor Effects Remover | Graphics | 1,419 |
| Beam Rifle Movie SFX | Audio | 1,253 |

**Key signals:**
- Vidiotmaps ~75% penetration (31K / ~42K monthly players) — most essential mod in ecosystem
- Badge-hunting content (maps + popmenus) is second-strongest vertical
- Audio SFX replacements per powerset are long-tail but consistent (800–1,400 DL each)
- FX removal mods (Bio Armor) get downloads — visual clutter is a documented pain point
- Enhancement UI fixes get traction despite being mundane — base UI is confusing

---

## 2. Pain Points & Fixable Issues

### CityModInstaller Friction
- **#1 friction**: requires manually adding `-assetpath assets\\mods` in Tequila launcher settings — no fallback for Homecoming launcher users
- No FAQ, troubleshooting, or uninstall documentation on instructions page
- No version tracking visible to users (Vidiotmaps v1.2.1 shipped July 8 2025; zero push signal)
- No user review or rating system — download count is only quality signal
- No conflict preview in browse view (only warned during install)
- No "last updated" date prominent in grid/list view
- No per-server compatibility tagging (Homecoming vs Rebirth vs Thunderspy)

### Browser-Side Gaps
- No forum/discussion thread links on mod pages (many mods originated as forum threads)
- No update notification system
- No essentials bundle / new-player onboarding path
- Post-Jan 2024 new-player wave (4,431 concurrent peak) needed a guide — Massively OP filled the void

### Confirmed Forum Demand (threads from 2021–May 2026)
- "Minimal FX for all" — Bio Armor, Stone Armor, Energy Aura still overwhelming even with in-game Minimal FX enabled
- "No pulse / no glow" requests for individual toggle powers (Electric Armor Static Shield named specifically)
- Badge tracker fragmentation — players use 4+ separate tools with no integration
- Repeated: "Is there a mod to reduce [FX]?" — no complete client-side solution exists

---

## 3. What Can Be Made — Confirmed Missing Mods

### Absent from the entire ecosystem:
- **ReShade / post-processing presets** — FFXIV has hundreds; CoH has zero (DX9-compatible)
- **Full zone ambient audio packs** — individual power SFX covered but no zone music replacements
- **Power FX texture packs** (enhancement/reskin, not just removal)
- **Colorblind accessibility mods** — no colorblind-safe palette replacement for UI elements
- **Font scaling mods** — chat slider only; no fix for small text at 1440p/4K
- **Power recharge HUD overlay** — native timer only on power tray button; no consolidated panel
- **Costume preset browser** — Icon Catalogue is a separate site, not installer-integrated
- **IO set bonus tracker overlay** — Mids Reborn is offline only; no live in-game display
- **Roleplay tools for Everlasting server** — base location popmenu exists; nothing else
- **Archetype-scoped audio bundles** — individual powers only; no cohesive archetype pack

### Top 10 Buildable Opportunities (ranked)

1. **ReShade Visual Preset Pack** — first ever for CoH; highly shareable screenshot content; 3–5 presets (Comic Book Vivid, Dark Gritty, Clean Widescreen); buildable in days
2. **CityModInstaller Update Notifier** — version metadata already in catalog; highest-utility infrastructure; mirrors ESO Minion/FFXIV Penumbra update flow
3. **FX Intensity Pack** (Bio Armor, Stone Armor, Energy Aura — 3-tier: full/reduce-60%/remove) — explicit confirmed forum demand 2021–2026; DDS texture pipeline documented on OuroDev
4. **Forum Thread Backlinks on mod pages** — pure UI/data addition; already partially done (forum_url in core/mods.js)
5. **Zone Ambient Audio Pack** (Atlas Park + Steel Canyon) — OGG replacement; Paragon Wiki maps zone music; lo-fi + cinematic variants
6. **Archetype Audio Bundle** (Scrapper melee SFX pack) — bundles per-power mods into one install; reduces decision fatigue; estimated 3–5K DL potential
7. **Colorblind Accessibility Texture Pack** — no equivalent exists; health/endurance bars + enhancement quality colors; first accessibility mod; press-worthy
8. **Mod Profile System** — save/switch named mod sets (PvE, RP, Casual); WeakAuras profile pattern; MVP = save/load installed list to config file
9. **Loading Screen Lore Texture Pack** — pure DDS swap; high visual impact; zero gameplay risk; FFXIV community enthusiasm confirms pattern
10. **Essentials Bundle** — curated one-click install for new players; Vidiotmaps + Badge Set List + Enhancement Pack + cursor + glowie; converts Massively OP guide readers into installers

---

## 4. MMORPG Overlay Patterns That Translate

| Pattern | Source | CoH Translation |
|---|---|---|
| Shareable HUD overlay strings | WoW WeakAuras | Exportable popmenu configs |
| Post-processing presets | FFXIV GShade/ReShade | ReShade preset pack (DX9-compatible) |
| Mod manager with conflict resolution + profiles | FFXIV Penumbra | CityModInstaller upgrade |
| Map pin overlay | ESO / GW2 | Vidiotmaps (exists; expand layer system) |
| Addon update checker | ESO Minion | CityModInstaller update notifications |
| Combat log parser/overlay | GW2 ArcDPS | CoH log exists; parser doesn't |
| Job gauge / cooldown bars | FFXIV JobBars | ReShade + popmenu hybrid HUD |

### Key comparisons:
- **FFXIV Penumbra** = what CityModInstaller wants to be (conflict resolver, live reload, per-character profiles)
- **ESO Minion** = what the update check system should be
- **WeakAuras** = what a CoH HUD overlay system would look like if built
- **GW2 model** = CoH has MORE permissive environment (official private servers can endorse tools)

---

## 5. Community Scale & Reddit Signals

- ~42,000 monthly active players (March 2024 Homecoming stat)
- Peak concurrent: 4,431 (January 2024 license announcement weekend)
- r/Cityofheroes active subreddit
- Massively OP January 2024 mod guide = primary new-player mod discovery source
- Screenshot posts of costume designs = highest engagement content type
- Base-building showcases = recurring editorial coverage (Massively OP covered repeatedly)
- Recurring questions: "how to reduce FX", "how to track badges", "better cursor?", "what mods should I install first?"
- Viral mod pattern: visually demonstrable in screenshot or short video (cursor, FX removal, map overlay)
- Gap: no before/after CoH visual quality video content exists — ReShade preset would fill this

---

## Sources
- cityofheroes.dev/mods (mod catalog)
- forums.homecomingservers.com (Minimal FX threads, badge tracker requests, texture mod guides)
- massivelyop.com (Jan 2024 mod guide, March 2024 player count, Jan 2026 2025 retrospective)
- wiki.ourodev.com/Texture_modding
- github.com/LoadedCamel/MidsReborn
- github.com/n15g/badger
- homecoming.wiki/wiki/Music
- thunderspy.net
- curseforge.com (WeakAuras stats)
- deltaconnected.com/arcdps (GW2 ArcDPS)
