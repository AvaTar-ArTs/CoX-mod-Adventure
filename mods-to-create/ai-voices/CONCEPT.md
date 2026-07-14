# CoH AI NPC Voices — Concept Brief

> Researched 2026-07-14. Sources: Homecoming forum threads 45039, 50337, 4458, 64162, 57864;
> GitHub jason-kane/coh_npc_voices (v4.5.3); GitHub mrthinger/wow-voiceover;
> Ascension WoW announcement; live forum archive 2009 thread.

---

## What the Community Is Asking For

**Thread:** "AI Voices for all missions and NPCs." — Homecoming Suggestions, topic 45039, May 3, 2026. 3 pages of replies.

The request is server-integrated AI voice acting for all NPC dialogue and mission text, similar to what Ascension WoW shipped in their launcher. The poster explicitly cites the **VoiceOver addon by mrthinger** (github.com/mrthinger/wow-voiceover), which Ascension distributes through their own addons tab. When a player clicks a quest NPC on Ascension, the NPC reads their quest text aloud with a consistent AI voice. Zero setup required — it ships as part of the launcher.

This is a 15-year-old community request in new clothes. The 2009 live-game forum archive (topic 198865) has players fantasy-casting voice actors for specific NPCs — Kathleen Turner for Sister Psyche, Eddie Izzard for Commander Castillo. The community has wanted voiced NPCs since the game launched.

**No Homecoming developer has publicly acknowledged or responded** to any voice-related suggestion thread. No roadmap mention found.

---

## What Already Exists: Sidekick (coh_npc_voices)

- **GitHub:** github.com/jason-kane/coh_npc_voices
- **Author:** Jason Kane — sole maintainer, highly responsive (often same-day replies)
- **Application name in-tool:** Sidekick
- **Created:** March 23, 2024
- **Latest version:** v4.5.3 (November 22, 2025)
- **Stars / Forks:** 3 / 0
- **Issues filed total:** 43 (indicates active use despite low star count)
- **YouTube demo:** youtube.com/watch?v=Ov29c91NtYQ

### How It Works

Sidekick watches the CoH client `chatlog.txt` file using a file-system watcher. When an NPC dialogue line appears, it:
1. Looks up the NPC name in a local SQLite database (`voices.db`)
2. If the NPC has no assigned voice yet, picks one from the configured TTS engine
3. Generates speech (or retrieves it from cache)
4. Plays audio with optional per-NPC voice effects

The SQLite cache is the key cost-saving feature: NPC lines repeat constantly, so after the first generation, subsequent plays cost nothing. Player chat is **not cached** — developer made this an explicit privacy decision.

### Supported TTS Engines (as of v4.5.3)

| Engine | Quality | Cost | Notes |
|---|---|---|---|
| Windows TTS | Low | Free | Default. "Price is right." Requires PowerShell unlock on Win10 |
| Google Cloud TTS | High | Paid | Slow generation. Requires ADC login setup |
| ElevenLabs | Excellent | ~$5–$22/mo | 10k chars/mo free tier (5–15 hrs gameplay); user burned through free tier in 4 days |
| OpenAI TTS | Very good | ~$4/mo | "Works best" per most active user (Orinvath). $1.28/week for heavy play |
| Amazon Polly | Good | Paid | Bug in v4.1.0 fixed in v4.1.1 |
| Azure | Good | Paid | Supported |
| Disabled | — | Free | Turns off TTS entirely while keeping other features (damage graph, XP tracker) |

**User report on OpenAI cost (Issue #34, Orinvath):**
> "A weeks worth of heavy gameplay for $1.28, and for great voices! Everything has been working pretty flawlessly."

**User report on ElevenLabs (Issue #18, Orinvath):**
> "I blew through 100k credits in 4 days... Now that I have all the NPC's talking I cant go back...lol"

**Developer on the experience (Issue #34):**
> "it's really hard to go back to vanilla once you've gotten used to voices."

### Notable Technical Features

- **Async audio (v4.0.0, June 2025):** Multiple NPCs can speak simultaneously — "makes a big difference in allowing narration to keep up with the action"
- **Per-NPC voice effects:** Clockwork faction gets vocoder/robotic pitch effect via numpy. Ring modulator available for others.
- **Pluggable TTS engine architecture (v4.1.0, July 2025):** Each engine is a separate module — adding new engines is clean
- **Profanity filter + gamer abbreviation expander (v4.5.x):** Expands afk/brb/gg/etc. before passing to TTS; optional filter for player chat channels
- **Supergroup and league chat toggle (v4.5.0)**
- **Patterns tab (v4.4.0):** Custom patterns for matching specific chat types
- **Win10 note:** Requires `enable_all_win10_voices.ps1` (included in repo) to unlock system TTS voices from transcription-only registry path
- **Win11 note:** No TTS voices installed by default — separate setup step

### Full Version History

| Version | Date | Key Change |
|---|---|---|
| v4.5.3 | 2025-11-22 | Externalized gamespeak abbreviations to editable `gamespeak.json` |
| v4.5.2 | 2025-11-22 | Bugfix: missing profanity filter data files |
| v4.5.1 | 2025-11-21 | Optional profanity filter + gamer abbreviation expander |
| v4.5.0 | 2025-11-01 | SG and league chat toggles |
| v4.4.1 | 2025-08-28 | Patterns bugfixes, declared stable |
| v4.4.0 | 2025-08-17 | Full Patterns tab release |
| v4.3.0 | 2025-07-27 | Category toggles (recharges, snark, recipes); OpenAI voice fix |
| v4.2.0 | 2025-07-26 | "Disabled" engine option |
| v4.1.1 | 2025-07-19 | Amazon Polly bugfix; verified clean Win10 install |
| v4.1.0 | 2025-07-18 | TTS engines made pluggable modules (major refactor) |
| v4.0.0 | 2025-06-21 | Async audio; terminal chat history view |
| v1.1.0 | 2024-04-06 | Sidekick UI started |
| v1.0.0 | 2024-03-31 | UI, unique voices per character, Google support, audio effects, team voices |
| v0.0.1 | 2024-03-23 | Initial release (simple Python log watcher) |

---

## The Critical Architectural Gap

**Mission briefing popup text does not appear in the chat log.**

CoH contact briefings, debriefs, clue text, and souvenir text are rendered as in-game popup windows — they never flow through the chat system. coh_npc_voices can only hear what appears in the log. This means:

| Content Type | In Chat Log? | Voiced by coh_npc_voices? |
|---|---|---|
| NPC speech bubbles in missions | Yes | Yes |
| Contact greetings (world dialogue) | Yes | Yes |
| Team / SG / League chat | Yes | Yes (toggleable) |
| Badge notifications | Yes | Yes |
| **Mission briefing text** | **No** | **No** |
| **Debriefing text** | **No** | **No** |
| **Clue / souvenir text** | **No** | **No** |
| **Contact phone call text** | **No** | **No** |

The Ascension WoW VoiceOver addon reads quest text directly from game memory — a fundamentally different architecture. On CoH, accessing the popup text would require either:
a) A game client hook (not possible without modifying the binary)
b) Pre-generated audio files keyed to the specific mission text IDs (Approach B below)
c) Homecoming server-side implementation (not a client mod)

---

## Related Threads

| Thread | Topic # | Date | What It Is |
|---|---|---|---|
| "Mission Text TTS" | 4458 | July 2022 | Player manually copy-pasting mission text into external TTS. Oldest confirmed voice request. Accessibility framing. |
| "Gender Trouble: Badge/NPC Dialog/Voice" | 64162 | May 2026 | Request to fix existing voice logic bugs: badges use wrong gender, NPC dialogue ignores character gender, default vocalizations are all male-coded. Different but adjacent. |
| "Transcripts?" | 57864 | June 2025 | Player wants NPC dialogue transcripts to dub for YouTube. Points to demand for mission text as a raw asset. |
| "Voice of the City?" | 43313 | June 2023 | Not voice acting — about a hypothetical animated anthology series narrator. Unrelated. |

---

## Two Buildable Approaches

### Approach A — Extend coh_npc_voices / Sidekick

**What it adds:** NPC-to-voice personality mapping, pre-configured voices for the 50 most common contacts, one-page installer for non-technical players.

**What it can't do:** Mission briefing text (not in chat log — see gap above).

**Barrier:** Low. Jason Kane is active and responsive. The engine plugin architecture (v4.1.0) makes adding a new capability clean. The codebase is well-organized Python.

**Cost for users:** OpenAI engine at ~$4/month is the sweet spot confirmed by active users.

**Steps:**
1. Fork `coh_npc_voices`
2. Add `contact_profiles.json` — maps contact name → specific voice ID + personality prompt
3. Pre-populate with the 50 most common Homecoming contacts (derived from wiki or community list)
4. Wrap in a one-page PyInstaller executable (removes Python setup requirement)
5. Submit to Homecoming forum Tools & Utilities

### Approach B — Pre-generated Audio Mod Pack

**What it adds:** Voiced mission briefings and popup text — the gap Approach A can't fill.

**What it requires:**
1. Extract all mission contact dialogue text from game data (PIGG extraction or community wiki)
2. Generate audio files via ElevenLabs / OpenAI for each unique text string
3. Map each generated file to the game's audio event path (requires understanding CoH audio event system)
4. Package as a City Mod Installer mod using the `data/sound/` override path

**Barrier:** Very high. CoH mission text was designed text-only from the start — no audio path infrastructure exists for it. This would require reverse-engineering the audio event system or creating a new trigger mechanism that doesn't exist in the client.

**Realistic scope:** Doable only for a subset of iconic contacts (Ghost Widow, Lord Recluse, the 5 Freedom Phalanx members, Statesman) where the effort is clearly worth it.

---

## NPC Voice Archetype Mapping — Starter List

Based on research into contact frequency, community recognition, and character lore:

| Contact / NPC | Voice Archetype | Rationale |
|---|---|---|
| Ms. Liberty | Professional, military, confident — American female | Freedom Phalanx leader voice |
| Ghost Widow | Cold, ethereal, formal — haunting female | Arachnos; slow cadence, precise diction |
| Lord Recluse | Commanding, theatrical villain — deep, resonant male | Monologue-heavy; needs presence |
| Statesman | Heroic, measured, authoritative — classic American male | The hero ideal archetype |
| Sister Psyche | Warm, empathetic, slightly formal — female | Counselor energy |
| Synapse | Energetic, rapid speech, enthusiastic — young male | Speed powerset personality |
| Numina | Ethereal, calm, slightly otherworldly — female | Spirit character; breathier tone |
| Back Alley Brawler | Street-tough, blunt, working-class — gruff male | Punchy, no-nonsense delivery |
| Penny Preston | Eager, optimistic, younger — female | New reporter energy |
| Arbiter Sands | Bureaucratic, officious — dry male | Villain-side, procedural |
| Dr. Aeon | Manic, intellectual, excitable — eccentric male | Mad scientist cadence |
| Scirocco | Weary, poetic, conflicted — accented male | Tragic villain register |
| Clockwork King | Fragmented, glitchy — distorted (vocoder) | Already supported by Sidekick |
| The Clockwork (faction) | Robotic, simple — low pitch (vocoder) | Already implemented in Sidekick |

---

## What This Project Should Actually Do

Given the research:

1. **Immediate:** Contribute to coh_npc_voices — submit a `contact_profiles.json` PR with personality mappings for the 50 most common contacts. Jason Kane is active and responsive. This gets proper voices to existing Sidekick users without a fork.

2. **Near-term:** Package coh_npc_voices as a one-page Windows installer (PyInstaller .exe with bundled OpenAI engine default). Drop the setup barrier from "install Python, configure API key in a config file" to "run installer, paste your OpenAI key." This is the Ascension WoW-model difference: zero-friction distribution.

3. **Long-term:** Pre-generated audio pack for the 10 most iconic contacts (Ghost Widow, Lord Recluse, Statesman, Ms. Liberty, Sister Psyche, Synapse, Back Alley Brawler, Scirocco, Dr. Aeon, Numina). Ship as a standard City Mod Installer mod with `data/sound/` overrides. Requires solving the audio event path mapping — high effort but high impact.

---

## Sources

- Homecoming Forums topic 45039 — AI Voices for all missions and NPCs (May 2026)
- Homecoming Forums topic 50337 — Talking NPCs / Sidekick release thread (July 2025)
- Homecoming Forums topic 4458 — Mission Text TTS (July 2022)
- Homecoming Forums topic 57864 — Transcripts? (June 2025)
- Homecoming Forums topic 64162 — Gender Trouble: Badge/NPC Dialog/Voice (May 2026)
- github.com/jason-kane/coh_npc_voices — all issues, releases, README
- github.com/mrthinger/wow-voiceover — the Ascension WoW precedent
- ascension.gg/en/news/azeroth-has-a-voice-and-its-ai-generated/402 — Ascension announcement
- forumarchive.cityofheroes.dev/topic/198865 — 2009 "Voices of the NPCs" thread (live game era)
