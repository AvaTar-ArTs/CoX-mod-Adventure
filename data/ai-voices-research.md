# CoH AI Voices — Full Source Audit

> Compiled 2026-07-14 from live research agent sweep across Homecoming forums, GitHub, Ascension WoW, and live-game archive.

---

## Table of Contents

- [Forum Threads](#forum-threads)
- [GitHub — coh_npc_voices (Sidekick)](#github--coh_npc_voices-sidekick)
- [GitHub — wow-voiceover (The Precedent)](#github--wow-voiceover-the-precedent)
- [External Articles](#external-articles)
- [Live Game Forum Archive](#live-game-forum-archive)
- [Issue-Level Quotes](#issue-level-quotes)
- [Key Synthesis](#key-synthesis)

---

## Forum Threads

### Primary: AI Voice Request

| Field | Value |
|---|---|
| **Title** | "AI Voices for all missions and NPCs." |
| **URL** | https://forums.homecomingservers.com/topic/45039-ai-voices-for-all-missions-and-npcs/ |
| **Section** | Suggestions & Feedback |
| **Posted** | May 3, 2026 |
| **Pages** | 3 (confirmed by search snippet) |
| **Dev response** | None confirmed |

**What was requested:** Server-integrated AI voice acting for all NPC dialogue and mission text, citing Ascension WoW's VoiceOver addon (mrthinger/wow-voiceover) as the model. Ascension distributes it through their own launcher addons tab — clicking a quest NPC causes it to read quest text aloud with a consistent AI voice.

---

### Sidekick Tool Release Thread

| Field | Value |
|---|---|
| **Title** | "Talking NPCs" |
| **URL** | https://forums.homecomingservers.com/topic/50337-talking-npcs/ |
| **Section** | Tools, Utilities & Downloads |
| **Posted** | July 22, 2025 |
| **Dev response** | None confirmed |

This is the release announcement for `coh_npc_voices` (Sidekick). Links to the GitHub repo. Each post about this tool generates immediate follow-up questions — active latent demand.

---

### Oldest Voice Request (Accessibility Framing)

| Field | Value |
|---|---|
| **Title** | "Mission Text TTS" |
| **URL** | https://forums.homecomingservers.com/topic/4458-mission-text-tts/ |
| **Section** | Suggestions & Feedback |
| **Posted** | July 7, 2022 |

Player describes manually copy-pasting mission text into an external TTS reader and suggests the game add built-in TTS for mission text. Earliest confirmed Homecoming-era voice request. No AI component — accessibility framing. Predates both the AI voice wave and coh_npc_voices.

---

### Voice / Pronoun Bug Thread

| Field | Value |
|---|---|
| **Title** | "Gender Trouble: Badge/NPC Dialog/Voice adjustment option" |
| **URL** | https://forums.homecomingservers.com/topic/64162-gender-trouble-badgenpc-dialogvoice-adjustment-option |
| **Section** | Suggestions & Feedback |
| **Posted** | May 10, 2026 |

Three identified bugs/design flaws:
1. Badges swap gender when character is in costume
2. NPC gender-sensitive dialogue uses masculine pronouns regardless of character
3. Character vocalizations default to "Huge Gruff Guy" voice category

Adjacent to TTS/AI voice space — reveals existing voice system is broken at the logic level before AI enhancement is even relevant.

---

### Dialogue Asset Request Thread

| Field | Value |
|---|---|
| **Title** | "Transcripts?" |
| **URL** | https://forums.homecomingservers.com/topic/57864-transcripts/ |
| **Section** | General Discussion |
| **Posted** | June 11, 2025 |

Player asks whether transcripts of NPC conversation blocks exist to dub for a YouTube video. Points to demand for mission text as a raw asset — relevant to pre-generating audio files for Approach B.

---

### Unrelated (Confirmed)

| Field | Value |
|---|---|
| **Title** | "Voice of the City?" |
| **URL** | https://forums.homecomingservers.com/topic/43313-voice-of-the-city/ |
| **Section** | General Discussion |
| **Posted** | June 14, 2023 |

About a hypothetical animated anthology series narrator character, not voice acting or TTS. Confirmed unrelated.

---

## GitHub — coh_npc_voices (Sidekick)

| Field | Value |
|---|---|
| **URL** | https://github.com/jason-kane/coh_npc_voices |
| **Author** | jason-kane (sole maintainer, highly responsive — often same-day) |
| **Created** | March 23, 2024 |
| **Latest version** | v4.5.3 — November 22, 2025 |
| **Stars** | 3 |
| **Forks** | 0 |
| **Watchers** | 3 |
| **Open issues** | 4 |
| **Total issues filed** | 43 |
| **Discussions** | None (not enabled) |
| **YouTube demo** | https://www.youtube.com/watch?v=Ov29c91NtYQ |

### Full Release History

| Version | Date | Key Change |
|---|---|---|
| v4.5.3 | 2025-11-22 | Externalized gamespeak abbreviations to editable `gamespeak.json` |
| v4.5.2 | 2025-11-22 | Bugfix: missing profanity filter data files |
| v4.5.1 | 2025-11-21 | Optional profanity filter + gamer abbreviation expander (afk/brb/gg/etc.) |
| v4.5.0 | 2025-11-01 | Supergroup and league chat toggles |
| v4.4.1 | 2025-08-28 | Patterns bugfixes, declared stable |
| v4.4.0 | 2025-08-17 | Full Patterns tab release |
| v4.4.0-preview | 2025-08-10 | Preview of Patterns feature |
| v4.3.0 | 2025-07-27 | Toggle categories (recharges, snark, recipes); OpenAI voice fix |
| v4.2.0 | 2025-07-26 | "Disabled" engine option |
| v4.1.1 | 2025-07-19 | Amazon Polly bugfix; verified clean Win10 install |
| v4.1.0 | 2025-07-18 | TTS engines made pluggable modules — major refactor |
| v4.0.0 | 2025-06-21 | Async audio (multiple NPCs simultaneously); terminal chat history view |
| v1.1.0 | 2024-04-06 | Sidekick UI started |
| v1.0.0 | 2024-03-31 | Full UI, unique voices per character, Google TTS, audio effects, team voices |
| v0.0.1 | 2024-03-23 | Initial release — simple Python log watcher |

### TTS Engines Supported

| Engine | Quality | Cost | Notes |
|---|---|---|---|
| Windows TTS | Low | Free | Default. Requires PowerShell unlock on Win10 (`enable_all_win10_voices.ps1` included in repo). Win11: no voices installed by default. |
| Google Cloud TTS | High | Paid | Slow generation. Requires ADC login. |
| ElevenLabs | Excellent | ~$5–$22/mo | 10k chars/mo free tier ≈ 5–15 hrs gameplay. Active user burned through free tier in 4 days. |
| OpenAI TTS | Very good | ~$4/mo | "Works best" per most active user. $1.28/week for heavy play (confirmed Issue #34). |
| Amazon Polly | Good | Paid | Bug in v4.1.0 fixed in v4.1.1. |
| Azure | Good | Paid | Supported. |
| Disabled | — | Free | Turns off TTS while keeping damage graph, XP tracker features. |

### Notable Technical Architecture

- **Log watcher:** Reads `chatlog.txt` using a file-system watcher (`watchdog`). Zero game binary access.
- **SQLite voice cache (`voices.db`):** NPC lines are cached after first generation — near-zero API cost for repeated lines. Player chat is explicitly NOT cached (privacy decision by jason-kane).
- **Async audio (v4.0.0):** Multiple NPCs can speak simultaneously via a queue between log reader and audio player threads.
- **Pluggable TTS modules (v4.1.0):** Each engine is a separate Python module — clean extension path.
- **Per-NPC audio effects:** Clockwork faction gets vocoder/pitch effect via numpy. Ring modulator available for others. VoiceBox API used (recent VoiceBox update broke `blend` param — replaced with `dry`/`wet`).
- **numpy dependency:** Largest dependency (zip release = 124MB). Used for mp3→wav conversion and vocoder math. Developer noted removing numpy would cut 2/3 of the package size.
- **Database migration system (v4.0.0):** Schema upgrades handled automatically.
- **Win10 voice unlock:** `enable_all_win10_voices.ps1` moves TTS voices from transcription-only registry path to general TTS registry path.

### Open Issues (as of latest check, Jan 2026)

| Issue # | Title | Type | Filed |
|---|---|---|---|
| #43 | MultiBox support + proc announcement | Enhancement | Jan 24, 2026 |
| #42 | `gamespeak.json` breaks if edited in Notepad | Documentation | Nov 25, 2025 |
| #36 | Announce coordinates feature | Enhancement | Nov 1, 2025 |
| #31 | Patterns tab documentation request | Documentation | Aug 19, 2025 |

Note on #42: Workaround is jsoneditoronline.org — Notepad breaks JSON encoding. jason-kane confirmed he will document this.

### Most Active Contributors in Issues

| User | Role | Notes |
|---|---|---|
| jason-kane | Author/maintainer | Sole developer. Responds same-day. |
| Orinvath | Power user | ~12 issues filed Jul 2025–Jan 2026. OpenAI engine. $4/mo heavy use. |
| Compuzak | User | Issue #13 (Nov 2024): hardcoded path to jason's username. Fixed same release. |
| josueGastelum | User | Issue #15 (Jul 2025): fresh install failure. Resolved in v4.1.1. |

---

## GitHub — wow-voiceover (The Precedent)

| Field | Value |
|---|---|
| **URL** | https://github.com/mrthinger/wow-voiceover |
| **Author** | mrthinger |
| **Used by** | Ascension WoW (classless private WoW server) |
| **Function** | Reads quest dialogue aloud via AI when interacting with quest NPCs |
| **Scope** | All Vanilla WoW playable races and all quest NPCs |
| **Distribution** | Via Ascension's own launcher addons tab — no user setup |
| **Architecture** | Reads quest text directly from WoW game memory |

**Why this matters architecturally:** VoiceOver accesses quest popup text from game memory directly — which is why it can voice content that never appears in a log file. CoH's mission briefings never enter the chat log, making the direct analog impossible for a log-watcher approach.

---

## External Articles

### Ascension WoW Announcement

| Field | Value |
|---|---|
| **URL** | https://ascension.gg/en/news/azeroth-has-a-voice-and-its-ai-generated/402 |
| **Title** | "Azeroth has a Voice: and it's AI Generated" |
| **Note** | Humorously warns against using it on Thrall specifically — voice quality is uneven across NPCs |
| **TTS provider** | Not disclosed in article |

This is the specific article the CoH forum poster was referencing. The Ascension team ships VoiceOver through their own launcher as a first-party feature — frictionless, no API key required for the player.

### Homecoming 2025 Roadmap

| Field | Value |
|---|---|
| **URL** | https://massivelyop.com/2025/01/08/city-of-heroes-homecoming-offers-a-brief-roadmap-with-two-major-updates-planned-for-2025/ |
| **Note** | No mention of voice acting, audio features, AI, or NPC improvements in any search result or snippet |

No roadmap reference to voice features found across any Homecoming official communication.

### 2025 Player Satisfaction Survey

| Field | Value |
|---|---|
| **URL** | https://forums.homecomingservers.com/topic/62877-2025-player-satisfaction-survey-responses |
| **Responses** | 2,246 |
| **Posted** | February 2026 |
| **Voice acting mention** | Not found in accessible snippets (thread is behind 403) |

---

## Live Game Forum Archive

### Original "Voices of the NPCs" Thread

| Field | Value |
|---|---|
| **URL** | https://forumarchive.cityofheroes.dev/topic/198865?page_no=4 |
| **Posted** | November 12, 2009 (by user Alasdair) |
| **Archive** | Preserved at cityofheroes.dev |

Page 4 excerpts (March 2010):
- **Lazarus** — joking about Lady Grey's voice resembling Angelina Jolie
- **RosaQuartz / @k26dp** — suggested Kathleen Turner for Sister Psyche, Eliza Dushku for Silver Mantis, Robin Williams for the Radio character
- **Red Valkyrja** — Eddie Izzard's accent for Commander Castillo
- **Sojourn_EU** — struggled to match voices to canon characters

**Significance:** The community has been requesting NPC voices since 2009 — 15+ years before the AI tools to do it cheaply existed.

---

## Issue-Level Quotes

Direct quotes pulled from GitHub issue comments:

### Issue #34 — OpenAI Cost Report (Orinvath, Oct 2025)

> "Everything has been working pretty flawlessly otherwise, been using it nonstop since my first communication. OpenAi seems to work the best for me and is very affordable, see image! A weeks worth of heavy gameplay for $1.28, and for great voices!"

### Issue #18 — ElevenLabs vs Cost (Orinvath, Jul 2025)

> "Running those powershell commands did the trick! Although I have to say the ElevenLabs voices are so much nicer. If only they were affordable. I blew through 100k credits in 4 days.. This is not bad though. Now that I have all the NPC's talking I cant go back...lol"

### Issue #7 / Release Notes — Windows TTS default (jason-kane, May 2024)

> "Default is still to use free local Windows TTS. Quality isn't very good but the price is right."

### Issue #14 / v4.0.0 — Async audio (jason-kane, Jun 2025)

> "multiple foes can talk at the same time now; this makes a big difference in allowing the narration to keep up with the action. Stability is now pretty excellent. I've gone many hours with no hints of trouble."

### Issue #34 — On addiction to the feature (jason-kane)

> "it's really hard to go back to vanilla once you've gotten used to voices."

### Issue #15 — On numpy size (jason-kane)

> "The way to make it smaller is to remove the numpy dependency. That would cut 2/3rds of it. Numpy is good at doing math fast. I'm using it to convert mp3 to wav files...It's also used for some of the voice effects, most critically the vocoder I'm using to make the clockwork sound robotic."

---

## Key Synthesis

### The Architectural Gap (Critical)

**Mission briefing popup text does not appear in the chat log.** CoH contact briefings, debriefs, clue text, and souvenir text are rendered as in-game popup windows and never flow through the chat system. coh_npc_voices is structurally blocked from voicing them. This is the core ask of thread 45039.

| Content Type | In Chat Log? | Voiced by Sidekick? |
|---|---|---|
| NPC speech bubbles in world | Yes | Yes |
| Contact greetings (world) | Yes | Yes |
| Team / SG / League chat | Yes | Yes (toggleable) |
| Badge notifications | Yes | Yes |
| **Mission briefing text** | **No** | **No** |
| **Debriefing / debrief text** | **No** | **No** |
| **Clue / souvenir text** | **No** | **No** |
| **Contact phone call text** | **No** | **No** |

### Why Ascension's Model Is Different

Ascension's VoiceOver reads quest data from WoW game memory directly. CoH access to mission popup text would require:
- A game client hook (not possible without binary modification)
- Pre-generated audio files keyed to mission text IDs (buildable, high effort)
- Server-side implementation (not a client mod path)

### What No Developer Has Addressed

No Homecoming developer has publicly responded to any voice-related suggestion thread, the coh_npc_voices tool announcement, or the 2025 Player Satisfaction Survey on this topic. Zero roadmap mention across all accessible sources.

### The Fastest Buildable Path

1. Contribute `contact_profiles.json` to jason-kane/coh_npc_voices — NPC name → voice personality mapping for the 50 most common contacts. Jason Kane is active and receptive to contributions.
2. Wrap as a PyInstaller single `.exe` — removes Python setup barrier. OpenAI engine as default at ~$4/month.
3. Ship as a City Mod Installer mod or standalone download on Homecoming forums Tools & Utilities.
