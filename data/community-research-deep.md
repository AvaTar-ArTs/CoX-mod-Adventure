# CoH Mod Ecosystem — Deep Research Report
> Generated 2026-07-14 by second-pass trend-researcher agent (5 angles)

---

## Angle 1 — Reddit r/Cityofheroes: What's Actually Trending

**Confirmed viral/high-engagement signals:**

- Massively OP "How to mod CoH Homecoming" (January 25, 2024) is the #1 new-modder discovery article — still the most-shared modding primer, widely cross-posted to r/Cityofheroes.
- "Quality of Life, Texture Mods, and Other Things" (Homecoming forum topic 9304, last updated January 21, 2026) has **21 followers**, 4 pages — well above average for Tools & Utilities. It's the bundled discovery resource players share when others ask "where do I start with mods?"
- "Various Powerset Soundmods" (topic 9586) is actively linked in Reddit discussions whenever audio customization is requested. The mod author invites sound requests — unmet supply-side demand signal.
- "Sounds/Music Mod Request" (topic 48462, February 2024) specifically requests selective login screen music and character creation theme control — neither packaged mod exists.
- "AI Voices for all missions and NPCs" (Homecoming Suggestions, May 2026) — fresh thread invoking Ascension WoW AI voice addon. High-signal aspirational request.
- "Talking NPCs" (topic 50337) references jason-kane/coh_npc_voices Python TTS tool — each post about this generates immediate follow-up questions.
- **Cursor mods have two listing entries** (mods 91 and 92 — High Visibility Mouse Cursors Set A and B) — demand strong enough to justify iterating the format. Reliable "wish there was" proxy.

**Repeat question patterns (high-confidence from indirect signals):**
1. "Is there a mod that replaces [powerset X] sounds with [franchise Y]?"
2. "How do I know if a mod still works after the last patch?"
3. "Is there a way to get HD textures / higher resolution costume textures?"
4. "Does [mod] work on Thunderspy / Rebirth too?"
5. "Where do I find ALL the mods in one place?"

---

## Angle 2 — GitHub Tool Ecosystem

| Repo | Stars | Last Activity | What It Does |
|---|---|---|---|
| LoadedCamel/MidsReborn | ~30 | Nov 25, 2025 | Full offline build planner, C#, .NET 8+ |
| n15g/badger | 5 | Active | Browser-based badge tracker (TypeScript), 13 open issues |
| n15g/coh-content-db-homecoming | Active | Active | Data source for badge/content DB |
| jason-kane/coh_npc_voices | Active | Jul 22, 2025 | Python TTS NPC voice reader via chat log |
| mikwilli/cohtools | Low | Oct 2023 | Texture extraction/reimport pipeline (Python) |
| ovekaaven/cohtools | Low | Older | PIGG file reader, .texture to .dds CLI tool |

**Key findings:**
- Badger (5 stars, 13 open issues) — disproportionate issue volume relative to star count means active user base. Data freshness a recurring pain whenever Homecoming patches add/modify badges.
- coh_npc_voices works entirely via CoH chat log — no PIGG manipulation. Lightweight model for other log-based overlays/parsers.
- **No GitHub repo exists for a community mod browser, mod update notifier, or mod compatibility checker.** Confirmed gap.
- GShade (Mortalitas/GShade) lists CoH among 300+ supported games. Some players already run post-processing overlays. No CoH-specific preset pack exists anywhere.
- No CI/CD or version-pinning infrastructure for any CoH mod. Every mod is a static file drop. No semantic versioning, no enforced changelogs, no compatibility matrix.

---

## Angle 3 — OuroDev Wiki Texture Pipeline (Full Technical Picture)

**Confirmed workflow:**
1. Open Pigg Viewer Pro → navigate to Homecoming `Piggs/` folder
2. Right-click texture → "Extract As DDS"
3. Edit in DDS-capable editor (Photoshop + NVidia Texture Tools, GIMP, etc.)
4. Save as DDS with **DXT5 compression** (DXT1 for no-alpha textures)
5. In Pigg Viewer 1.61 → right-click original → "Create texture from .dds"
6. Copy output path (starts with `texture_library/`) into Homecoming `data/` folder — game reads as override

**Hard limitations (documented):**
- **Texture resolution is hardcoded.** Must match exact pixel dimensions. HD texture mods are technically impossible with current client architecture.
- **Texture components are linked.** Diffuse texture, grayscale map, bump map, gloss map, specular map, color mask, transparency — alter one, shadows/reflections break unless linked maps are altered too.
- **DDS artifacts accumulate.** Wiki warns to save lossless copy (.tga, .png, .bmp) first.
- **No batch tools.** Every texture extracted/reimported individually through GUI.
- **Pigg Viewer 1.61 is the only option.** Explicit wiki statement — no CLI fallback exists.

**Documentation gaps that block new modders:**
1. Wiki last significantly updated ~2019. Doesn't reference City Mod Installer at all.
2. No documentation on which `.pigg` files contain which assets.
3. No documentation on bump map generation tools.
4. Audio and texture modding docs are separate with no cross-references.
5. Zero documentation on mod-to-mod file collision behavior.

---

## Angle 4 — Competing Servers' Mod Ecosystems

**Homecoming** — reference implementation. Has cityofheroes.dev + City Mod Installer + Mids Reborn forum club.

**Thunderspy** — most divergent server. Implements customization *server-side* (full color sliders, body scale, pet customization, color picker with hex input). Their model is built-in rather than modded-in. No Thunderspy-specific mod browser found.

**Rebirth** — April 2026: released **City of Heroes Multiverse Launcher** (Massively OP, April 29, 2026). Designed as shared entry point for ALL rogue servers with per-server customizable skins. "Attempt: Developing Web Mids" (Rebirth forum topic 3322) shows independent web-based Mids attempt — dev energy without infrastructure.

**Cross-server compatibility:**
- All client-side mods operate on same game client binary (i27+ based servers share client infrastructure).
- City Mod Installer explicitly targets "i27+ based servers" — Thunderspy's deeper divergence may not be accounted for.
- No cross-server mod compatibility matrix exists anywhere.

---

## Angle 5 — What Mod Creators Say They Need

**Submission process (reconstructed):**
1. Author creates mod files (correct folder structure)
2. Posts to Homecoming forum Tools & Utilities section
3. Contacts **Michiyo** (mod site operator) to be added to installer index
4. Michiyo packages and adds to installer list
5. Updates require re-contacting Michiyo

This is a single-person gatekeeper bottleneck with no self-serve alternative.

**Specific creator pain points:**
- **Distribution via Google Drive** (confirmed for topic 9586) — mod authors default to Drive because no upload mechanism exists on mod site. Drive links rot when authors stop maintaining them.
- **No versioning or changelog system.** No way for users to know updates exist without manually revisiting forum threads.
- **Conflict detection only in installer client.** Manual installers (pre-installer workflow) have no protection.
- **No author identity persistence.** Mod pages show "By [username]" but no author profile, portfolio, or notification system. Authors can't push update announcements.
- **No metrics.** Authors have zero visibility into download counts or usage patterns.
- "Texture modding issue" Help & Support thread (topic 53769, September 2024) — players stuck on alpha channel/bump map relationship. Forum serving as de-facto technical support for documentation holes.
- "How do you create texture mods?" (topic 11322) — years-old thread still getting traffic. Documentation fails to capture first-time creators before they hit friction.
- No community-wide mod request board — ad-hoc aggregation only.

---

## Synthesis: 5 Highest-Confidence Things to Build Next

**1. Mod Update Notification System** *(Highest confidence, zero existing solution)*
Every mod is a static file drop. No versioning, no changelogs. City Mod Installer tracks what's installed locally — the missing piece is server-side changelog + "last updated" timestamp + email/RSS opt-in per mod.

**2. Mod Request Board with Voting** *(High confidence, buildable in ~6 days)*
Sound/texture/UI requests made in individual creator threads with no centralized signal. A votable request board gives mod authors a prioritized work queue and creates a supply→demand feedback loop. Topics 48462, 45039, 9586 all represent the same unmet need.

**3. Self-Serve Mod Submission Portal for Authors** *(High confidence, removes Michiyo bottleneck)*
Upload form with: name, category, version, changelog, compatible servers, screenshot, file. Author dashboard with download counts. beta.mods.cityofheroes.dev URL suggests active platform iteration — this is the logical next capability.

**4. Cross-Server Compatibility Tags** *(Medium-high, growing need post-Multiverse Launcher)*
April 2026 Rebirth Multiverse Launcher signals formalization of multi-server ecosystem. Simple tag system (tested on: Homecoming / Rebirth / Thunderspy / Reunion) + browse filter costs almost nothing but dramatically increases relevance to cross-server players.

**5. Beginner Modding Guide Integrated Into Browser** *(Medium-high, fills OuroDev wiki gap)*
OuroDev wiki last meaningfully updated ~2019. Doesn't reference City Mod Installer. "How do you create texture mods?" (topic 11322) still gets traffic years later. An integrated "Make a Mod" section covering: Pigg Viewer 1.61, DXT5 requirement, hardcoded resolution limit, data folder override system, audio formats, submission process — would expand the creator supply side.

---

## Sources
- OuroDev Texture Modding wiki
- OuroDev Texture Maps Basics
- Homecoming Updated Texture Guide (topic 48234)
- Complete Homecoming Texture Guide (topic 64109)
- Quality of Life Texture Mods thread (topic 9304)
- Various Powerset Soundmods (topic 9586)
- Sounds/Music Mod Request (topic 48462)
- How to create texture mods (topic 11322)
- Texture Modding Issue thread (topic 53769)
- City Mod Installer Released (topic 49175)
- CoH Mods master forum thread (topic 4634)
- Vidiotmaps for Homecoming (topic 37216)
- AI Voices suggestion thread (topic 45039)
- Talking NPCs thread (topic 50337)
- jason-kane/coh_npc_voices, LoadedCamel/MidsReborn, n15g/badger, n15g/coh-content-db-homecoming, ovekaaven/cohtools, mikwilli/cohtools
- GitHub city-of-heroes topic
- Massively OP: Working As Intended mod guide (January 2024)
- Rebirth Multiverse Launcher (Massively OP, April 29, 2026)
- Thunderspy.net patch notes
- mods.cityofheroes.dev, cityofheroes.dev, StrategyWiki Clientmods, Nexus Mods CoH
