# ReShade vs `.ini` — What Each One Actually Is

---

## ReShade Itself

ReShade is a **DLL injector**. When you run the installer, it drops a file called `d3d9.dll` (for DX9 games like CoH) into the game folder. When CoH launches and tries to load DirectX 9, Windows finds ReShade's DLL first — ReShade intercepts every frame the game renders, runs its shader passes over it, and hands the modified frame to the display.

The game has no idea this is happening. ReShade sits between the game's output and your monitor.

ReShade ships with a library of **effect shaders** written in HLSL (High-Level Shader Language) — files like `Cartoon.fx`, `Bloom.fx`, `Vignette.fx`. These are the actual programs that process pixels. Each one takes the rendered frame as input and outputs a modified version.

---

## The `.ini` File

The `.ini` is just a **saved configuration** — it doesn't contain any shader code. It's a plain text key-value file that tells ReShade:

1. **Which shaders to activate** — the `Techniques=` line
2. **In what order to run them** — the `TechniqueSorting=` line
3. **What parameter values to use** — every `[ShaderName.fx]` block with its slider values

So `Cartoon.fx` is the program. `Power=2.80` in your `.ini` is the dial setting for that program.

```ini
[Cartoon.fx]       ← which shader
Power=2.80         ← parameter passed into it
EdgeSlope=2.20     ← another parameter
```

When you move a slider in the ReShade overlay in-game, it's writing new numbers into the `.ini` in real time.

---

## The Difference in a Single Sentence

> **ReShade is the engine. The `.ini` is the settings file. The `.fx` files are the effects. You only distribute the `.ini` — players already have the engine and effects after running the installer.**

---

## Why the Same Shader Produces Wildly Different Results

`Cartoon.fx` with `Power=0.80` (RetroTV) vs `Power=3.20` (InkLines) runs the exact same Sobel convolution code — the `Power` parameter just controls how aggressively the detected edges are darkened. Same shader, radically different look.

This is why 11 presets can exist as 11 tiny text files sharing the same 13 installed shaders — the shader library is fixed, the parameter space is enormous.

---

## The Execution Order Matters

`TechniqueSorting=` is significant. In `CoX_SplashPage.ini`:

```
Cartoon → ColorMatrix → Levels → Curves → Vibrance → Tonemap → Clarity → Bloom → Vignette
```

Cartoon runs **first** — it draws ink edges on the fully-colored frame. Then ColorMatrix desaturates. If you swapped those, Cartoon would draw edges on the grey frame and the ink lines would be grey too instead of black. Order changes the result even with identical parameters.
