# Everlasting RP Toolkit — Popmenu

The first dedicated roleplay popmenu for Everlasting, CoH's RP-focused server.
Fills the confirmed gap: base location popmenu exists in the ecosystem; nothing else does.

---

## Install

1. Drop `EverlastingRP.mnu` into your CoH `data/menus/` folder:
   ```
   C:\Games\Homecoming\data\menus\EverlastingRP.mnu
   ```
2. Launch CoH. No restart required if the game is already running — type `/reloadmenus` in chat.

## Bind to a Key

In chat:
```
/bind LSHIFT+R "popmenu EverlastingRP"
```

Or any key you prefer. From that point, `Shift+R` opens the full menu anywhere in-game.

## What's Inside

| Section | Contents |
|---|---|
| Emotes — Body Language | 30+ emotes organized by Greetings / Casual / Dramatic / Seated / Dance |
| IC / OOC Status | Title presets: `[RP]`, `[LFG-RP]`, `[BUSY]`, `[AFK]`, `(( OOC ))`, `[SCENE]` |
| Scene Setters | Begin/End Scene, Time Skip, Fade to Black, Flash Forward, Flashback, OOC pause |
| RP Wrappers | Quick-insert `::` action format, `(( OOC ))` wrapper, environmental emote lines |
| Zone Locations | OOC location announcements for Atlas Park, Pocket D, Steel Canyon, Talos, Dark Astoria, Croatoa, Rogue Isles |
| SG Base Atmosphere | Enter/exit base, briefing table, mission display, training room, debrief flavor |
| Contact Info | Global handle post, LFG announcements, scene invites, SG recruiting |
| Combat RP | Threat assessment, cover, injury, victory lines, civilian protection |

## Customizing

Open `EverlastingRP.mnu` in any text editor.

**Change your global handle** in the Contact Info section — replace `@YourHandle` with your actual global.

**Add custom emotes:** Copy any `Option` line and change the label and command:
```
Option "My custom emote"    "em <emotename>"
```

Full emote list: `/emote` in chat shows all available emote names.

**Add SG base locations:** Copy a Location option and paste your base's zone name.

## Compatibility

Works on Homecoming (Everlasting), Rebirth, Thunderspy, Reunion — any i27+ server.
Popmenu syntax is client-side only; server differences don't affect it.
