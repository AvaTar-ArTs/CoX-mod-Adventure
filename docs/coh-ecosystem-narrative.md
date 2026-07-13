# The City of Heroes Mod Adventure Ecosystem

## Concept

CoX Mod Adventure represents a bridge between the nostalgia of City of Heroes—once a beloved superhero MMORPG that defined a generation—and the modern era of streamlined gaming experiences on macOS. This project transforms the technical complexity of Wine-based game management into an accessible, personalized superhero experience. At its heart, it connects a legacy game running under emulation (Homecoming server, Issue 24 assets) with a vibrant community of creators who continue to enhance the game years after its official closure.

The ecosystem functions as both a personal toolkit and a community resource. On one side, it provides automated scripts and documentation to help players install mods—custom enhancements ranging from map overlays showing badge locations to sound replacements for power effects. On the other side, it preserves knowledge about managing Wine environments on modern macOS hardware, helping fellow CoH enthusiasts keep this classic alive. The architecture spans multiple tools: LaunchCat (the Wine wrapper), the official Mod Installer (which converts community downloads into native `.pigg` format), and the game itself, which loads these mods as first-class assets rather than loose file overrides.

## Monetization

This ecosystem creates value through preservation and accessibility rather than direct financial return. The primary value flows come from:

**Personal Utility**: Instead of manually downloading dozens of mods from cityofheroes.dev, organizing them, and figuring out the correct asset paths, players can run a script or use the provided GUI tools. This saves hours of technical troubleshooting—time better spent flying through Paragon City.

**Knowledge Preservation**: The CoX-mod-Adventure project documents workflows that could otherwise be lost. When macOS updates break Wine compatibility or file paths shift, this repository serves as a reference for solutions. The `coh-setup.txt` file alone contains hours of debugging insights about MoltenVK graphics, Wine drive mappings, and performance optimization.

**Community Contribution**: Through scripts like `download-mods.sh` and `README.md` guides, players contribute back to the small but dedicated community. The project already catalogs 291 mods across 8 categories—from the essential Vidiotmaps pack (31,000+ downloads) to niche audio replacements and cursor themes.

**Skill Development Cross-Pollination**: The techniques learned here—managing Wine prefixes, converting file formats, handling cross-platform asset paths—apply to other retro gaming preservation projects. The `.pigg` archive format, for instance, is a custom container that any emulator-focused tool could learn to parse.

## Workflow

The mod installation journey follows a clear path from discovery to gameplay:

1. **Mod Discovery** — Scripts read mod listings from cityofheroes.dev/mods/ and prepare download URLs. The Mod Installer (GUI tool by Michiyo) provides an alternative entry point with one-click browsing.

2. **Automated Download** — Python or Bash scripts fetch mods in parallel, saving to the local `Mods/` directory. The game's Mod Installer handles format conversion automatically.

3. **Format Conversion** — Community mods are transformed from raw packages into `.pigg` files. This native format is crucial: it loads faster than loose file overrides and integrates seamlessly with the game's asset system.

4. **Installation** — Converted `.pigg` files are placed in `~/Library/Application Support/LaunchCat/coh/assets/mods/`. The game reads them automatically when launched with `-assetpath assets/issue24;assets/live;assets/mods`.

5. **Game Launch** — LaunchCat loads the modded client through Wine 9.0 on Intel macOS. The game presents installed mods highlighted in red in the UI, with an "Update" button available for each.

The ecosystem architecture separates concerns cleanly: base game assets in `issue24/` (4.2 GB) remain untouched, live server updates in `live/` (584 MB) are managed by Homecoming, and community creations live in `mods/` (currently 32 MB from three installed packages). This separation ensures updates don't break custom content, while the `.pigg` format ensures performance doesn't suffer from customization.

---

## Technical Deep Dive: The Pigg Architecture

### What Are Pigg Files?

`.pigg` files are custom archive containers used by City of Heroes. Each file packs multiple assets—textures, sounds, geometry—into a single package the game can stream efficiently. A typical mod like `BetterIcons.pigg` (881 KB) contains hundreds of texture overrides that replace the game's enhancement icons, while `PocketDAssemblage23.pigg` (32 MB) bundles entire music tracks for the Pocket D social hub.

### Override Priority System

The game loads assets in a specific order:
```
issue24/ → live/ → mods/
```
Any file in `mods/` with the same path as one in `issue24/` or `live/` takes precedence. This is how a 3 KB file like `accolade_lrt.pigg` can change just one icon—the Long Range Teleport accolade—without touching megabytes of base assets.

### Audio Mod Structure Example

```
PocketDAssemblage23.pigg contains:
├── sound/
│   └── Ogg/
│       ├── music/
│       │   └── Rave_AE_loop.ogg
│       └── Music_Source/
│           └── Rave/
│               ├── NewRave1_loop.ogg
│               ├── NewRave2_loop.ogg
│               └── ... (6 total)
```

These `.ogg` files replace the original Rave music that plays in Pocket D, giving players a refreshed audio experience in the game's most popular social zone.

### GUI/Icon Override Structure

```
BetterIcons.pigg contains:
├── texture_library/
│   └── GUI/
│       └── Icons/
│           ├── inspirations/
│           │   ├── Inspiration_Accuracy_Lvl_1.texture
│           │   ├── Inspiration_Accuracy_Lvl_1.dds
│           │   └── ... (dozens of inspiration icons)
│           └── Powers/
│               └── ... (power icon replacements)
```

Each `.texture` file points to a corresponding `.dds` image file, the format the game uses for its UI elements.

## The Homecoming Tool Ecosystem

| Tool | Creator | Function |
|------|---------|----------|
| **City Mod Installer** | Michiyo | Primary mod manager, converts to .pigg format |
| **Vidiotmaps** | AboveTheChemist | Map overlay mod (31k+ downloads) |
| **BindControl** | emersonrp | Keybind/macro/popmenu editor |
| **Mids' Reborn** | Felis Noctu | Character build planner |
| **ATC Badge Popmenu** | AboveTheChemist | In-game badge tracking |

These tools represent years of community innovation, keeping the game fresh with quality-of-life improvements that weren't possible in 2012.

## Current State & Next Steps

The ecosystem is partially operational:
- ✅ **Game assets installed** (4.8 GB total across issue24/live)
- ✅ **Mods directory ready** (`assets/mods/` exists but was empty until now)
- ✅ **Three mods installed** (BetterIcons, accolade_lrt, PocketDAssemblage23)
- ⏳ **291 mods catalogued** in `coh-mods-list.txt` (ready for batch install)
- ⏳ **Web interface** prepared in `pages/v1-v5/` (5 design variations)

The next natural step would be either expanding the mod collection through the Mod Installer or using the web interface to let players browse and select mods through a visual catalog.