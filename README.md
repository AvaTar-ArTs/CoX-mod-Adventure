# CoX Mod Adventure

## Concept

CoX Mod Adventure is a personal toolkit for managing modifications to **City of Heroes** (CoH) and its fan-run **Homecoming** server on macOS. It provides automated downloaders and tools to help players enhance their gaming experience with custom UI packs, costume mods, power animations, and other community-created content.

City of Heroes (dot) Dev hosts over 290 community mods across 8 categories, with the most popular being:
- **Maps** (Vidiotmaps, event guides, collection paths) - over 31,000 downloads for the flagship map pack
- **Popmenus** (badge lists, emotes, conversion guides) - convenient in-game menus for tracking achievements and powers
- **Audio** (sound replacements, music mods) - enhanced audio for powersets and events
- **GUI/Icons** (enhancement icons, interface themes) - visual improvements for UI clarity

At its core, this project bridges the gap between the technical complexity of Wine-based game management and the player's desire for a personalized superhero experience.

## Monetization

This is a free, community-driven project with no direct monetization. The value comes through:

- **Personal utility**: Streamlines mod installation for your own Homecoming gameplay
- **Community contribution**: Share working download scripts and diagnostics with fellow CoH players
- **Knowledge preservation**: Document troubleshooting for Wine/Mac setups, helping others in the small but dedicated CoH modding community
- **Skill development**: Learning automation techniques applicable to other retro gaming preservation projects

The real "return on investment" is a smoother, more customized City of Heroes experience that keeps this beloved classic alive on modern macOS hardware.

## Workflow

1. **Mod Discovery** - Scripts read mod listings from cityofheroes.dev and prepare download URLs
2. **Automated Download** - Python or Bash scripts fetch mods in parallel, saving to the local Mods directory
3. **Installation** - Mods are installed into the LaunchCat game directory (`~/Library/Application Support/LaunchCat/coh/assets/mods/`)
4. **Game Launch** - LaunchCat loads the modded client with updated assets
5. **Play & Share** - Enjoy enhanced gameplay and contribute fixes back to the community

## Mod Categories Available

| Category | Purpose | Popular Examples |
|----------|---------|-----------------|
| **Maps** | In-game map overlays with badge/plaque locations | Vidiotmaps (31k+ downloads), event maps |
| **Popmenus** | Quick-reference menus accessible in-game | Badge lists, emote menus, conversion guides |
| **Audio** | Sound effect and music replacements | Power SFX packs, alignment music |
| **Graphics** | Textures, faces, character customizations | Ape face, costume mods |
| **GUI / Icons** | Interface and enhancement icon improvements | Enhancement standardization pack |
| **Cursors** | Custom mouse cursor packs | Various themes |
| **Languages** | Translation packs | Community translations |
| **Other** | Miscellaneous enhancements | Various tools |

## Current Status

- **291 mods catalogued** from cityofheroes.dev (as of July 2024)
- **Downloaders implemented** in both Python (`download-mods.py`) and Bash (`download-mods.sh`)
- **LaunchCat integration ready** - Mods path exists in the Wine prefix, awaiting populated content
- **Diagnostics complete** - Wine configuration optimized with hardware acceleration enabled
- **Top mods identified** - Vidiotmaps, badge/emote popmenus, enhancement icons ready for priority download# CoX-mod-Adventure
