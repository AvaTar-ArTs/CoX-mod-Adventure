# CoX ReShade Preset Pack — Install Guide

Eleven post-processing presets for City of Heroes — the first ReShade pack ever made for CoH.
CoH runs DirectX 9; ReShade supports it fully.

---

## What's Included

| File | Look | Best For |
|---|---|---|
| `CoX_ComicVivid.ini` | High saturation, punchy contrast, subtle bloom | Screenshots, streaming, making powers pop |
| `CoX_InkLines.ini` | Heavy ink outlines, desaturated world, glowing spot-color on powers | Frank Miller meets Kirby — noir superhero |
| `CoX_SilverAge.ini` | Warm amber tones, soft outlines, flat poster colors | 1960s Fantastic Four / Kirby print aesthetic |
| `CoX_GoldenAge.ini` | Warm newsprint amber, heavy outlines, yellowed highlights | 1940s wartime comics — Captain America era |
| `CoX_Halftone.ini` | Hard posterized flat color, heavy outlines, pure primary palette | Lichtenstein / Roy Thomas Ben-Day dot print |
| `CoX_SplashPage.ini` | Near black-and-white world, vivid spot color on powers | Noir splash panel — your abilities are the only color |
| `CoX_NeonCity.ini` | Dark base, power effects burn electric, deep blue-purple shadows | Paragon City at 2am — powers as neon signs |
| `CoX_RetroTV.ini` | Warm phosphor glow, soft edges, slightly faded cartoon colors | Saturday morning Super Friends on a 1970s TV |
| `CoX_CinematicHero.ini` | Teal shadows, orange highlights, sharp and dramatic | MCU theatrical grade — actual superhero movie look |
| `CoX_DarkGritty.ini` | Desaturated, crushed blacks, film grain, vignette | Villain content, dark zones, cinematic feel |
| `CoX_CleanHD.ini` | Sharp AA, neutral color, subtle clarity | 1440p/4K play, "modern engine" look |

---

## Install Steps

### 1. Download ReShade
Go to **reshade.me** and download the latest ReShade installer.

### 2. Run the Installer
- Launch the ReShade installer executable
- Click **Browse** and navigate to your CoH install directory
  - Homecoming default: `C:\Games\Homecoming\` or wherever you installed it
  - Find `cityofheroes.exe` (or `cityofheroes64.exe`)
- When asked for rendering API: select **DirectX 9**
- When asked which shaders to install, select at minimum:
  - `Cartoon.fx` — ink edge detection (the core comic book effect)
  - `SMAA.fx` — anti-aliasing
  - `FXAA.fx` — additional AA
  - `Bloom.fx` — bloom (for Comic, NeonCity, SplashPage, RetroTV presets)
  - `Clarity.fx` — mid-tone sharpening
  - `ColorMatrix.fx` — color grading (for Gritty, SplashPage presets)
  - `Curves.fx` — contrast
  - `FilmGrain.fx` — grain effect (for Gritty, GoldenAge, RetroTV presets)
  - `Levels.fx` — black/white point
  - `LumaSharpen.fx` — sharpening (for Clean, CinematicHero presets)
  - `SplitToning.fx` — dual-tone color wash (Silver Age, Golden Age, NeonCity, RetroTV, CinematicHero presets)
  - `Tonemap.fx` — tone mapping
  - `Vibrance.fx` — saturation
  - `Vignette.fx` — vignette (for Comic and Gritty presets)
  - `Vignette.fx` — edge darkening (for InkLines, SplashPage, NeonCity presets)
- Complete the installation

### 3. Copy the Preset Files
Drop all eleven `.ini` files into your **CoH game directory** (same folder as `cityofheroes.exe`):

```
C:\Games\Homecoming\CoX_ComicVivid.ini
C:\Games\Homecoming\CoX_InkLines.ini
C:\Games\Homecoming\CoX_SilverAge.ini
C:\Games\Homecoming\CoX_GoldenAge.ini
C:\Games\Homecoming\CoX_Halftone.ini
C:\Games\Homecoming\CoX_SplashPage.ini
C:\Games\Homecoming\CoX_NeonCity.ini
C:\Games\Homecoming\CoX_RetroTV.ini
C:\Games\Homecoming\CoX_CinematicHero.ini
C:\Games\Homecoming\CoX_DarkGritty.ini
C:\Games\Homecoming\CoX_CleanHD.ini
```

### 4. Launch the Game
Start CoH normally. ReShade will inject automatically.

### 5. Open the ReShade Overlay
Press **Home** (the key above the arrow cluster) to open the ReShade UI overlay.

### 6. Select a Preset
- At the top of the ReShade overlay, click the preset dropdown
- Your presets will appear by filename
- Click one to activate it immediately — switching is instant, no restart needed

### 7. Toggle On/Off
Press **Insert** to toggle the entire ReShade effect stack on/off without closing the game.

---

## How the Comic Effects Work

**`Cartoon.fx`** runs Sobel edge detection on the rendered frame — it finds contrast boundaries between geometry, costumes, and environment, then darkens them. The result simulates ink outlines without touching the 3D mesh. Higher `Power` = heavier lines.

**`CoX_ComicVivid`** — moderate outlines (Power 1.8) + high vibrance for a bright superhero-book look. Bloom makes energy powers glow like metallic ink.

**`CoX_InkLines`** — cranks outlines to Power 3.2 and desaturates the base image, then lets `Bloom` re-saturate only the brightest regions — fire powers stay vivid while the world goes near-monochrome. Spot color on noir.

**`CoX_SilverAge`** — soft outlines (Power 1.2) with `SplitToning` pushing shadows to amber and highlights to warm cream — the paper-and-ink color cast of 1960s offset printing.

**`CoX_GoldenAge`** — warm newsprint amber via `SplitToning` + medium outlines + film grain. Like wartime comics on aged yellowed paper.

**`CoX_Halftone`** — extreme `Curves` contrast (Formula 4) posterizes the color space into flat bands. Heavy outlines draw the fill boundaries. Primary palette forced via high `Vibrance`.

**`CoX_SplashPage`** — `ColorMatrix` + `Vibrance` desaturate the world toward monochrome; extreme `Bloom` (Saturation 3.5) re-saturates only the brightest pixels (your power effects). City is ink; powers are full color.

**`CoX_NeonCity`** — `SplitToning` pushes shadows deep blue-purple; low `Exposure` darkens the world; oversaturated `Bloom` makes any bright region (powers, streetlights) bleed electric color.

**`CoX_RetroTV`** — soft outlines (Power 0.8), warm phosphor `SplitToning`, gentle `Bloom` simulating CRT phosphor glow. Film grain adds analog texture.

**`CoX_CinematicHero`** — teal shadows / orange highlights via `SplitToning` (the Hollywood complementary grade). High `LumaSharpen` for cinematic clarity.

---

## Adjusting Values

Once a preset is loaded, all shader parameters appear in the ReShade overlay as sliders.
Tweak anything — changes save automatically to the `.ini` file.

Good starting tweaks:

| Preset | Common Tweak |
|---|---|
| Comic Vivid | Reduce `Vibrance` if colors look oversaturated on your monitor |
| Ink Lines | Lower `Cartoon Power` from 3.2 if outlines are too heavy |
| Silver Age | Reduce `SplitToning HighlightBalance` if highlights look too yellow |
| Golden Age | Reduce `SplitToning ShadowBalance` if shadows are too amber |
| Halftone | Lower `Curves Contrast` if the posterization is too harsh |
| Splash Page | Lower `Bloom Amount` if power effects bleed too much color |
| Neon City | Raise `Exposure` if the base scene is too dark |
| Retro TV | Reduce `FilmGrain Intensity` if grain is too visible |
| Cinematic Hero | Adjust `SplitToning ShadowBalance` for more or less teal |
| Dark Gritty | Reduce `Vignette Amount` if the screen edges are too dark |
| Clean HD | Increase `LumaSharpen sharp_strength` for more edge clarity at 4K |

---

## Performance

ReShade adds GPU overhead (CoH is CPU-bound — GPU headroom is usually available):

| Preset | Estimated overhead |
|---|---|
| Ink Lines | ~1.0–1.5ms (heavy Cartoon pass) |
| Halftone | ~1.0–1.4ms |
| Splash Page | ~0.9–1.3ms |
| Comic Vivid | ~0.8–1.2ms |
| Silver Age / Golden Age | ~0.7–1.1ms |
| Neon City | ~0.7–1.1ms (heavy Bloom) |
| Retro TV / CinematicHero | ~0.6–1.0ms |
| Dark Gritty | ~0.5–0.9ms |
| Clean HD | ~0.2–0.5ms |

---

## Uninstall

Run the ReShade installer again, point it to your CoH directory, and select **Uninstall**.
Delete the eleven `.ini` files from your CoH directory.

---

## Compatibility

Tested concept: City of Heroes i27+ (Homecoming, Rebirth, Thunderspy, Reunion).
All rogue servers run the same client binary — these presets are server-agnostic.

If ReShade doesn't inject, check that your antivirus isn't blocking `dxgi.dll` or `d3d9.dll` in the game directory.
CoH must be run in **windowed** or **borderless windowed** mode for ReShade to function on some systems.
