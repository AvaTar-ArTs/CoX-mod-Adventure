# CoH AI NPC Voices — Concept Brief (v1)

> Written 2026-07-14 from community-research-deep.md summary — before primary source audit.
> This is the "what we knew from snippets" state. See CONCEPT.md (v2) for what the research
> actually found. The gap between these two files is the point.

---

## What the Thread Is Asking For

Players on Homecoming are requesting AI-generated voice acting for mission text and NPC dialogue.
The thread explicitly references what Ascension WoW did with their AI voice addon in 2024–2025:
every quest text, NPC greeting, and mission briefing was AI-voiced and delivered through the
existing audio system — players could enable/disable per character or globally.

CoH has thousands of mission briefings, clue text, villain monologues, and contact NPC dialogue
that exists only as text in the client. No voice acting was ever recorded for most of them.

---

## What Already Exists: coh_npc_voices

GitHub: jason-kane/coh_npc_voices (last commit: July 22, 2025)
[NOTE v2: This date was the forum post date, not the GitHub commit date. Actual last commit: Nov 22, 2025 at v4.5.3]

This is a Python TTS (Text-to-Speech) tool that:
- Reads the CoH chat log file in real time
- Detects when NPC dialogue appears in the log
- Passes that text through a TTS engine (configurable: system TTS, ElevenLabs, etc.)
- Plays the audio output through your system audio

**Key architectural insight:** It does NOT touch any game files. Zero PIGG manipulation.
The CoH client logs NPC dialogue to a text file automatically. The tool reads that file,
not the game binary. This is the cleanest possible implementation — no install risk.

---

## The Gap Between coh_npc_voices and the Thread's Request

| coh_npc_voices (exists) | Thread request (missing) |
|---|---|
| Reads chat log → TTS on the fly | Pre-generated voices for ALL mission text |
| Voice changes every run (live TTS) | Consistent character voices per NPC |
| Requires Python + dependencies | One-click install |
| No NPC-to-voice mapping | Specific voice per contact/NPC |
| Text only from what appears in chat log | Full mission briefing text (not all in log) |
| No GUI | User-adjustable voice settings |

[NOTE v2: This table was directionally right but missed the full picture. v4.5.3 already has
a GUI, multiple TTS engines with pricing confirmed by users, SQLite caching, async audio,
per-NPC voice effects including a vocoder for Clockwork. And the "not all in log" row turned
out to be the CRITICAL gap — mission briefing popups NEVER appear in the log. That's not
a partial limitation; it's a structural block requiring a different architecture entirely.]

---

## Two Buildable Approaches

### Approach A — Extend coh_npc_voices (Low barrier, works now)

Fork or extend jason-kane/coh_npc_voices to add:
1. **NPC-to-voice mapping** — detect NPC name in log line, assign a consistent voice
2. **Voice library** — use ElevenLabs or Coqui-TTS to pre-generate audio for top 50 contacts
3. **Simple GUI** — toggle per-NPC voice on/off, volume slider, voice selection
4. **Installer wrapper** — package as a single `.exe` with Python bundled

**What you need:** The NPC name list, a TTS API key (ElevenLabs free tier), Python.
**What you don't need:** Game files, PIGG access, binary manipulation.

[NOTE v2: ElevenLabs free tier turned out to be insufficient — the most active user burned
through 100k credits in 4 days. OpenAI TTS at ~$4/month is the confirmed sweet spot.
Also: jason-kane is actively responsive and may merge a contact_profiles.json PR directly
rather than needing a fork.]

### Approach B — Pre-generated Audio Mod Pack (Harder, better result)

Generate audio files ahead of time for all mission briefing text, package as a standard
client-side audio mod using the `data/sound/` override system.

**Challenge:** Mission briefings aren't clean audio paths in the current game — they were
designed as text-only from the start. Mapping generated audio to the right trigger points
requires understanding the game's audio event system more deeply.

[NOTE v2: This challenge is harder than stated. There are no audio event paths for mission
text at all — it was never designed with audio triggers. "Understanding the audio event
system more deeply" undersells the barrier. This is essentially building new infrastructure
that doesn't exist in the client.]

---

## Recommended Path: Approach A First

The jason-kane/coh_npc_voices architecture is proven and already has community attention.
An extended fork with per-NPC voice consistency, pre-mapped voices for the 50 most common
contacts, and a one-page UI would fulfill the thread's core request and could ship without
any game file access. The ElevenLabs free tier generates enough audio for a proof-of-concept.

[NOTE v2: Recommendation stands but ElevenLabs free tier is wrong. Use OpenAI engine.]

---

## NPC Voice Mapping — Starter List

| Contact / NPC | Suggested Voice Archetype |
|---|---|
| Ms. Liberty | Professional, military, American — confident female |
| Ghost Widow | Cold, ethereal, formal — haunting female |
| Lord Recluse | Commanding, theatrical villain monologue — deep male |
| Statesman | Heroic, measured, authoritative — classic American male |
| Sister Psyche | Warm, empathetic, slightly formal — female |
| Synapse | Energetic, enthusiastic, rapid speech — young male |
| Numina | Ethereal, calm, slightly otherworldly — female |
| Back Alley Brawler | Street-tough, blunt, working-class — gruff male |
| Penny Preston | Young, eager, optimistic — younger female |
| Arbiter Sands | Bureaucratic, officious — formal male |
| Dr. Aeon | Manic, intellectual, enthusiastic — eccentric male |
| Scirocco | Weary, poetic, conflicted — accented male |

[NOTE v2: Clockwork King and Clockwork faction entries missing here — because we didn't know
Sidekick already implements a vocoder for the Clockwork faction. That's important context for
building the profile list — don't duplicate what's already done.]

---

## Connection to Community Research

- Forum topic 45039 explicitly references Ascension WoW — player-identified gap
- coh_npc_voices (Jul 2025 last commit) proves the technical path without game file access
- Each coh_npc_voices post generates "immediate follow-up questions" — active latent demand
- No packaged version exists for non-technical users — the barrier is distribution, not tech

---

## Files Needed to Start

- `npc_voice_mapper.py` — extend coh_npc_voices with NPC→voice ID mapping
- `voice_profiles.json` — NPC name → ElevenLabs voice ID mapping
- `gui.py` — simple tkinter or webview control panel
- `requirements.txt` — ElevenLabs SDK, watchdog (file watcher), pygame (audio)
- `README.md` — one-page install guide for non-technical players

[NOTE v2: These files already exist in jason-kane/coh_npc_voices — we'd be extending them,
not writing from scratch. The better path is a PR with contact_profiles.json rather than
a parallel implementation.]
