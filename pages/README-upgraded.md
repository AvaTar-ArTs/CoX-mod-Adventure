# CoX Mod Browser — Upgraded

Three aesthetic variations of the mod browser, all powered by `mods.json` (291 mods).

## Open in Browser

```bash
open mod-browser.html          # Variation 1: Mission Briefing Terminal
open mod-browser-comic.html    # Variation 2: Comic Book
open mod-browser-hud.html      # Variation 3: Power HUD
```

No server required — all open directly from `file://`.

## Files

| File | Description |
|------|-------------|
| `mod-browser.html` | Dark terminal, amber gold, KingsRow bg |
| `mod-browser-comic.html` | Halftone, ink borders, comic fonts |
| `mod-browser-hud.html` | Cyan energy, clip-path corners, pulsing counts |
| `mods.json` | 291 mods scraped from cityofheroes.dev |
| `scrape-mods.py` | Re-scrape or install mods: `python3 scrape-mods.py --install` |

## Fonts Used

Local fonts from `~/Library/Fonts/` — no CDN needed for typography.

## Refresh Data

```bash
python3 scrape-mods.py --rescrape   # re-scrape all 291 mods
cp ../mods.json mods.json           # or pull from parent
```
