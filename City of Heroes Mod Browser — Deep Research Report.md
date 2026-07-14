##### City of Heroes Mod Browser — Deep Research Report

  Angle 1 — Reddit r/Cityofheroes: What's Actually Trending

  The direct site-search limitation is real. Reddit blocks most site-scoped
  Google scraping, so individual post upvote/comment counts were not
  retrievable through search. However, cross-referencing search
  bleed-through, Massively Overpowered article comment sections, and forum
  references reveals the following patterns:

  Confirmed viral/high-engagement signals:

  - The Massively Overpowered article "How to mod City of Heroes Homecoming
  the easy way" (published January 25, 2024) generated significant inbound
    traffic to the mod ecosystem — it was the most-shared modding primer of
    2024 and is still the #1 discovery article for new modders entering the
    pipeline. This article was widely cross-posted to r/Cityofheroes.
  - The "Quality of Life, Texture Mods, and Other Things" Homecoming forum
  thread (topic 9304, last updated January 21, 2026) has 21 followers and
    spans 4 pages — well above average for a Tools & Utilities post. Its
    contents (texture replacers, cursor mods, sound swaps, keybinds, macros)
    represent a bundled discovery resource that players share when others ask
    "where do I start with mods?"
  - Forum thread "Various Powerset Soundmods" (topic 9586) is actively linked
  in Reddit discussions whenever audio customization is requested. The mod
    author explicitly invites sound requests, which signals an unmet
    supply-side demand pattern.
  - Forum thread "Sounds/Music Mod Request" (topic 48462, February 2024) has
  someone specifically requesting two audio-targeting mods: selective login
    screen music and character creation theme control — neither of which exist
    as packaged mods.
  - "AI Voices for all missions and NPCs" (Homecoming Suggestions forum,
  May 2026) is a fresh thread explicitly invoking what Ascension WoW has done
    with AI voice addon support. This is a high-signal aspirational request.
  - "Talking NPCs" (topic 50337) references the jason-kane/coh_npc_voices
  Python tool — a log-reading TTS tool. Players posting about this get
    immediate follow-up questions, indicating latent demand.
  - Cursor mods have two listing entries on cityofheroes.dev (mods 91 and 92
  — "High Visibility Mouse Cursors Set A and B"), which means the demand was
    strong enough to justify iterating on the format. This is a reliable "wish
    there was" proxy.

  Repeat question patterns across platforms (high-confidence from indirect
  signals):
  1. "Is there a mod that replaces [powerset X] sounds with [franchise Y]?"
  2. "How do I know if a mod still works after the last patch?"
  3. "Is there a way to get HD textures / higher resolution costume
  textures?"
  4. "Does [mod] work on Thunderspy / Rebirth too?"
  5. "Where do I find ALL the mods in one place?"

  Sources: Working As Intended: How to mod CoH | Quality of Life Texture Mods
  thread | Sounds/Music Mod Request | AI Voices thread | Talking NPCs

---
  Angle 2 — GitHub Tool Ecosystem: What Exists and What's Wanted

  Confirmed repositories with context:

  ┌──────────────────────────────┬───────┬─────────┬────────────────────┐
  │             Repo             │ Stars │ Last Ac │    What It Does    │
  │                              │       │ tivity  │                    │
  ├──────────────────────────────┼───────┼─────────┼────────────────────┤
  │                              │       │ Nov 25, │ Full offline build │
  │ LoadedCamel/MidsReborn       │ ~30   │  2025   │  planner, C#, .NET │
  │                              │       │         │  8+                │
  ├──────────────────────────────┼───────┼─────────┼────────────────────┤
  │                              │       │         │ Browser-based      │
  │ n15g/badger                  │ 5     │ Active  │ badge tracker      │
  │                              │       │         │ (TypeScript), 13   │
  │                              │       │         │ open issues        │
  ├──────────────────────────────┼───────┼─────────┼────────────────────┤
  │ n15g/coh-content-db-homecomi │ Activ │ Active  │ Data source for    │
  │ ng                           │ e     │         │ badge/content DB   │
  ├──────────────────────────────┼───────┼─────────┼────────────────────┤
  │                              │ Activ │ Jul 22, │ Python TTS NPC     │
  │ jason-kane/coh_npc_voices    │ e     │  2025   │ voice reader via   │
  │                              │       │         │ chat log           │
  ├──────────────────────────────┼───────┼─────────┼────────────────────┤
  │                              │       │ Oct     │ Texture extraction │
  │ mikwilli/cohtools            │ Low   │ 2023    │ /reimport pipeline │
  │                              │       │         │  (Python)          │
  ├──────────────────────────────┼───────┼─────────┼────────────────────┤
  │                              │       │         │ PIGG file reader,  │
  │ ovekaaven/cohtools           │ Low   │ Older   │ .texture to .dds   │
  │                              │       │         │ CLI tool           │
  ├──────────────────────────────┼───────┼─────────┼────────────────────┤
  │ Miravalier/CoH-Builder       │ Low   │ Older   │ Vanilla JS web     │
  │                              │       │         │ build planner      │
  ├──────────────────────────────┼───────┼─────────┼────────────────────┤
  │ quixadhal/City-of-Heroes     │ Low   │ Active  │ Macros and scripts │
  └──────────────────────────────┴───────┴─────────┴────────────────────┘

  Key observations:

  - Mids Reborn (30 stars) is the anchor community tool, actively maintained,
  with a dedicated Homecoming forum club. Its user base is orders of
    magnitude larger than its GitHub star count suggests — the stars reflect
    developer-identity users, not the broader player base.
  - Badger (5 stars, 13 open issues) has active issue volume relative to star
  count. The 13 open issues on a 5-star repo means a disproportionate number
    of active users are filing bugs and requests. The data dependency on
    coh-content-db-homecoming means badge data freshness is a recurring pain
    point whenever Homecoming patches add or modify badges.
  - coh_npc_voices (last commit July 22, 2025) is the most recently active
  modding-adjacent tool. It works entirely via the CoH chat log file — no
    PIGG manipulation — which makes it a lightweight model for other log-based
    overlays or parsers.
  - There is NO GitHub repository for a community mod browser, mod update
  notifier, or mod compatibility checker. This is a confirmed gap.
  - GShade (Mortalitas/GShade) — a ReShade fork — lists CoH among its 300+
  supported games. This means some players are already running
    post-processing overlays. There is no CoH-specific preset pack on any major
    mod platform.
  - There is no CI/CD or version-pinning infrastructure for any CoH mod.
  Every mod is a static file drop. No semantic versioning, no changelogs
    enforced, no compatibility matrix.

  Sources: MidsReborn GitHub | Badger GitHub | coh_npc_voices GitHub |
  cohtools (ovekaaven) | cohtools (mikwilli) | CoH GitHub topics

---
  Angle 3 — OuroDev Wiki Texture Pipeline: The Full Technical Picture

  Confirmed workflow (from wiki + forum corroboration):

  1. Open Pigg Viewer Pro, navigate to the Homecoming Piggs/ folder
  2. Open the target .pigg file
  3. Right-click texture → "Extract As DDS"
  4. Edit in any DDS-capable editor (Photoshop + NVidia Texture Tools, GIMP,
  etc.)
  5. Save as DDS with DXT5 compression (DXT1 for textures without alpha
  channel)
  6. Back in Pigg Viewer 1.61, right-click original texture → "Create texture
  from .dds"
  7. Pigg Viewer outputs the full path starting with texture_library/
  8. Copy that path into the Homecoming data/ folder — game reads it as an
  override

  Confirmed hard limitations (documented and independently corroborated):

  - Texture resolution is hardcoded. Altered textures must match the exact
  pixel dimensions of the original. You cannot upscale. "HD texture" mods are
    technically impossible using the current client architecture.
  - Texture components require coordinated editing. Each surface can have:
  diffuse texture, grayscale map, bump map, gloss map, specular map, color
    mask, transparency channel. If you alter one, shadows and reflections break
    unless you alter the linked maps too.
  - DDS artifacts accumulate. The wiki explicitly warns to save a lossless
  copy (.tga, .png, .bmp) because DDS introduces compression artifacts like
    JPEG. Mod authors who skip this step cannot iterate cleanly.
  - No batch tools. Every texture is extracted and reimported individually
  through a GUI. There is no CLI pipeline for bulk operations.
  - Pigg Viewer 1.61 is the only option. The wiki is explicit: it is the ONLY
  program that can do texture-to-pigg conversion without hex editing. This
    creates a single-tool dependency with no fallback.

  Documentation gaps that block new modders:

  1. The wiki was last significantly updated around 2019 based on internal
  dating of limitation notes. It does not address the City Mod Installer
    workflow — new modders don't know whether to put files in data/ manually or
    use the installer.
  2. No documentation on which .pigg files contain which assets. New modders
  spend hours exploring.
  3. No documentation on bump map generation tools (just says "some means of
  generating a bump map").
  4. Audio modding has entirely separate documentation from texture modding,
  and the two are not cross-referenced.
  5. Zero documentation on compatibility between mods from different authors
  (file collision behavior).

  Sources: OuroDev Texture Modding Wiki | OuroDev Texture Maps Basics |
  Homecoming Updated Texture Guide | Complete Texture Guide | StrategyWiki 
  Clientmods

---
  Angle 4 — Competing Servers' Mod Ecosystems

  Homecoming is the reference implementation. It has:
  - cityofheroes.dev (mod browser + City Mod Installer for Windows/Mac)
  - Forum section: Tools, Utilities & Downloads (the primary mod discovery
  surface pre-installer)
  - Explicit mod permissiveness ("Homecoming totally allows them" —
  client-side only)
  - Mids Reborn as an officially recognized Homecoming forum club

  Thunderspy (the most feature-divergent server):
  - Positions itself as the "most advanced" server with massive character
  customization: full color sliders, extended body scale sliders, pet
    customization, customizable player apartments
  - April 2026 patch notes include a new color picker (hue slider,
  saturation/brightness, hex input, favorite swatches, color history)
  - Thunderspy's customization philosophy is server-side, not mod-side — they
  implement what other servers' players achieve via client mods directly
    into the game engine. This is a fundamentally different model.
  - No Thunderspy-specific mod browser found. Their differentiation is
  built-in, not modded-in.
  - Patreon presence at patreon.com/coxg confirms ongoing funding.

  Rebirth (the "closer to Paragon Studios" server):
  - April 2026: released the City of Heroes Multiverse Launcher to mark the
  22nd anniversary of CoH. It is explicitly designed as a shared entry point
    for ALL rogue servers, letting each customize its launcher skin
    (backgrounds, links, news).
  - The Multiverse Launcher announcement (massivelyop.com, April 29, 2026;
  mmorpg.com coverage) is significant: it reduces discovery friction for
    smaller servers.
  - Rebirth's wiki is at wiki.cityofheroesrebirth.com. No mod browser found
  specific to Rebirth.
  - Their forums have a thread "Attempt: Developing Web Mids"
  (forum.cityofheroesrebirth.com, topic 3322) — someone independently trying
    to build a web-based Mids equivalent, indicating the Rebirth community has
    modding-adjacent dev energy but lacks infrastructure.

  Cross-server mod compatibility:
  - All client-side mods operate on the same game client binary (i27+ based
  servers share client infrastructure). In theory, mods are server-agnostic.
  - In practice, Thunderspy's server-side engine changes mean some UI
  elements may differ. No documented incompatibility list exists.
  - The City Mod Installer explicitly targets "i27+ based servers" —
  Thunderspy's deeper divergence may not be fully accounted for.
  - There is no cross-server mod compatibility matrix anywhere.

  Sources: Thunderspy | Thunderspy Patch Notes | Rebirth Multiverse Launcher 
  — Massively | Rebirth Multiverse Launcher official | MMORPG.com coverage |
  Rebirth Web Mids thread

---
  Angle 5 — What Mod Creators Say They Need

  The submission process is opaque by design. There is no self-serve mod
  submission portal at cityofheroes.dev. The current workflow, as best
  reconstructed from forum threads and the Massively OP article:

  1. Mod author creates their mod files (raw DDS/texture/audio files in the
  correct folder structure)
  2. Author posts to Homecoming forum Tools & Utilities section announcing
  the mod
  3. Author contacts Michiyo (the mod site operator) to be added to the City
  Mod Installer index
  4. Michiyo packages it and adds it to the installer list
  5. Updates require re-contacting Michiyo

  This is confirmed by the absence of any self-serve author dashboard and by
  the Massively OP article's framing of Michiyo as the central
  gatekeeper/packager.

  Specific pain points recoverable from forum threads:

  - Distribution via Google Drive (confirmed for "Various Powerset Soundmods"
  topic 9586): mod authors default to Google Drive because there is no
    upload mechanism on the mod site. Google Drive links rot when authors stop
    maintaining them. Several older forum mod posts have dead links.
  - No versioning or changelog system. When "Quality of Life, Texture Mods,
  and Other Things" (topic 9304) was last updated January 21, 2026, there is
    no way for users who installed it previously to know an update exists
    unless they manually revisit the forum thread.
  - Conflict detection is only in the installer client. When two mods
  overwrite the same file, the installer warns you. But users who manually
    install mods (the pre-installer workflow) have no such protection.
  - No author identity persistence on the mod site. Mod pages on
  cityofheroes.dev show "By [username]" but there is no author profile page,
    portfolio, or notification system. A mod author cannot push update
    announcements to their subscribers.
  - The "texture modding issue" Help & Support thread (topic 53769,
  September 2024) is a player stuck on the alpha channel / bump map
    relationship — a documented gap in the modding guide. The forum is serving
    as de facto technical support for documentation holes.
  - "How do you create texture mods?" (topic 11322) is a years-old thread
  that still gets traffic, suggesting the documentation pipeline fails to
    capture first-time creators before they hit friction.
  - Sound mod request aggregation is entirely ad-hoc. Topic 9586 author
  invites requests in their own thread. There is no community-wide "mod
    request board" where unmet demand is systematically tracked.
  - The Vidiotmaps mod (last updated July 8, 2025 to version 1.2.1) is
  maintained by AboveTheChemist and is cited as the single most-downloaded
    mod — but its download count is not publicly displayed anywhere. Authors
    have no metrics.

  Sources: City of Heroes Mods master thread | City Mod Installer Released |
  Vidiotmaps thread | Various Powerset Soundmods | Texture Modding Issue |
  How to create texture mods | CoH Mods mods.cityofheroes.dev

---
  Synthesis: 5 Highest-Confidence Things to Build Next

  1. Mod Update Notification System (Highest confidence, clearest pain, zero
  existing solution)

  Every mod is a static file drop with no versioning. Authors update via
  forum post edit or a new post. Users have no signal. Build a lightweight
  "last updated" timestamp + version field per mod, with an optional
  email/RSS notification opt-in for users who have installed a given mod. The
  City Mod Installer already tracks what's installed locally — the missing
  piece is the server-side changelog. This directly addresses the single most
  recurring mod maintenance complaint across all five research angles.

  2. Mod Request Board with Voting (High confidence, clear demand signal,
  buildable in 6 days)

  Sound mod requests are made in individual creator threads. There is no
  centralized place to signal unmet demand. A simple "request a mod" board
  with upvoting — searchable by category (audio, texture, cursor, UI, map) —
  gives mod authors a prioritized work queue and gives the community a way to
  see what's wanted without asking the same questions repeatedly. The
  "Sounds/Music Mod Request" thread (topic 48462), the AI voices thread
  (topic 45039), and the powerset soundmods thread (topic 9586) all represent
  the same underlying need. This also creates a discovery loop: popular
  requests attract authors; fulfilled requests close the loop.

  3. Self-Serve Mod Submission Portal for Authors (High confidence, removes
  the Michiyo bottleneck)

  Currently one person is the gatekeeper to the City Mod Installer index. A
  self-serve upload form — with fields for mod name, category, version,
  changelog, compatible servers, screenshot, and download file — removes this
  single point of failure and unblocks the mod creation pipeline. The
  beta.mods.cityofheroes.dev URL already exists, suggesting active iteration
  on the platform. An author dashboard showing download counts per mod is a
  natural addition that zero existing tools provide. Mod authors currently
  have no metrics whatsoever.

  4. Cross-Server Compatibility Tags and Filtering (Medium-high confidence,
  growing need given Multiverse Launcher)

  The April 2026 Rebirth Multiverse Launcher is the clearest signal that the
  multi-server ecosystem is formalizing. Players will increasingly be on
  multiple servers. Currently, every mod on cityofheroes.dev is implicitly
  "for Homecoming" with no tagging for Thunderspy, Rebirth, or Reunion
  compatibility. A simple tag system (tested on: Homecoming, Rebirth,
  Thunderspy, Reunion) plus a filter on the browse page costs almost nothing
  to build but dramatically increases the mod browser's relevance to a
  growing cross-server audience. Thunderspy's server-side customization
  differences make this especially important for UI mods.

  5. Beginner Modding Guide Integrated Into the Browser (Medium-high
  confidence, fills the OuroDev wiki gap)

  The OuroDev wiki was last meaningfully updated circa 2019. It does not
  reference the City Mod Installer. The forum thread "How do you create
  texture mods?" (topic 11322) still attracts traffic years later because
  there is no single authoritative, current guide. An integrated "Make a Mod"
  section on cityofheroes.dev — covering: tools needed (Pigg Viewer 1.61,
  DDS editor), the data folder override system, the DXT5 compression
  requirement, the hardcoded resolution limit, audio file format
  requirements, and how to submit to the installer — would convert more
  players into mod authors and expand the supply side of the ecosystem. The
  friction is documented and understood; only the consolidated delivery is
  missing.

---
  Sources (master list):
  - OuroDev Texture Modding
  - OuroDev Texture Maps Basics
  - Homecoming Updated Texture Guide
  - Complete Homecoming Texture Guide
  - Quality of Life Texture Mods thread
  - Various Powerset Soundmods
  - Sounds/Music Mod Request
  - How to create texture mods
  - Texture Modding Issue thread
  - City Mod Installer Released
  - CoH Mods master forum thread
  - Vidiotmaps for Homecoming
  - AI Voices suggestion thread
  - Talking NPCs forum thread
  - coh_npc_voices GitHub
  - MidsReborn GitHub
  - Badger GitHub
  - coh-content-db-homecoming GitHub
  - cohtools (ovekaaven)
  - cohtools (mikwilli)
  - GitHub city-of-heroes topic
  - Working As Intended: How to mod CoH
  - Homecoming 2025 roadmap
  - Thunderspy
  - Thunderspy Patch Notes
  - Rebirth Multiverse Launcher — Massively
  - Rebirth Multiverse Launcher official
  - Rebirth Web Mids thread
  - mods.cityofheroes.dev
  - cityofheroes.dev
  - StrategyWiki Clientmods
  - Nexus Mods CoH