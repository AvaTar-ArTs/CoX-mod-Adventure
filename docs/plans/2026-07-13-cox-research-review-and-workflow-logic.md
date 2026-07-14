# CoX Mod Adventure - Research Review and Workflow Logic
**Date:** 2026-07-13
**Status:** Comprehension pass

---

## Purpose

This note answers the current question: which skills, agents, workflows, and research logic should govern CoX Mod Adventure now that the project is understood as more than a static mod browser?

The short answer: use the skill ecosystem as an operating method, not as a pile of effects. The project should move through evidence, workflow selection, product synthesis, prototype, dogfood, and shipping.

```text
evidence surfaces
-> workflow and skill selection
-> product comprehension
-> prototype direction
-> local runtime verification
-> browser/tool build
-> dogfood and ship
```

---

## Current Research Read

CoX Mod Adventure has four live meanings:

1. **Catalog**
   - `mods.json` is the canonical 291-mod catalog.
   - The project already has category, author, download, description, page URL, and download URL data.

2. **Browser**
   - `Upgraded/` is the current creative prototype surface.
   - The strongest direction is not one existing variant alone; it is a synthesis of mission terminal structure, HUD state panels, and restrained comic/pixel flavor.

3. **Runtime Bridge**
   - LaunchCat is the actual local game runtime surface.
   - CityModInstaller is the real installer state surface.
   - `/Applications/coh` is currently an empty marker path, so it should not be treated as the populated game tree without another verification pass.

4. **Control Surface Direction**
   - CityVault confirms that the broader CoH ecosystem thinks in launcher manifests, admin dashboards, profile configuration, game file hosting, and status/control panels.
   - CoX Mod Adventure should borrow that control-surface mental model, but keep immediate scope on the mod archive, local runtime awareness, and install/download paths.

The core product thesis remains:

```text
CoX Mod Adventure should become a CoH-native mod archive and local control surface.
```

---

## Workflow Authorities

These are the highest-signal workflows for the next phase.

| Workflow / skill | Why it matters here | How to use it |
|---|---|---|
| `using-superpowers` | Prevents random action. Forces skill selection before work. | Start every meaningful phase by choosing the smallest relevant skill set. |
| `innate-workflow` | Provides the broad loop: audit, select, work, preserve. | Use as the session rhythm around `using-superpowers`. |
| `workflow-orchestrator` | Turns ambiguous multi-surface work into a clean execution path. | Use before changing browser, downloader, docs, or runtime logic. |
| `ecosystem-clarity` | Explains how the local agent/skill ecosystem fits together. | Use when choosing between `.agent-skills`, `.agents`, `.codex`, and reference trees. |
| `ecosystem-intelligence` | Useful when auditing or evolving agent/runtime surfaces. | Use for multi-tree understanding, not for direct product UI design. |
| `workspace-ecosystem-audit` | Keeps live path claims honest. | Re-run before assuming LaunchCat, CityModInstaller, or repo state. |
| `deep-research` | Provides a claim-verification pattern: scope, search, fetch, verify, synthesize. | Use for external facts or comparisons, especially CityVault or CoH tooling claims. |
| `narrative-documentation` | Keeps the project comprehensible as a product. | Convert findings into docs that guide future build work. |
| `frontend-design` | Holds the UI to a real product standard. | Use after the workflow and product thesis are clear. |
| `popular-web-designs` | Supplies pattern references: masonry, media cards, dense dashboards, terminal surfaces. | Use as layout pattern vocabulary, not as a theme copier. |
| `p5js` | Adds ambient canvas language. | Use for background motion only after the core browsing surface works. |
| `pixel-art` | Adds CoH-zone-derived thumbnails or CRT/card treatment. | Use for category identity and texture, not for reducing readability. |
| `playground` | Gives safe space for layout/density/theme tuning. | Keep the layout playground as the design laboratory. |
| `dogfood` | Verifies the browser like a user. | Run after major frontend changes. |
| `project-shipper` | Defines what actually ships. | Use to decide the primary HTML artifact and release checklist. |

---

## Recommended Agent Lenses

Use these as thinking roles, not as distractions.

| Agent lens | Best use |
|---|---|
| `tree-explorer` | Map what is actually present in repo, LaunchCat, CityModInstaller, assets, and skills. |
| `workflow-orchestrator` | Decide execution order and avoid cross-surface drift. |
| `ecosystem-analyzer` | Quantify large trees and distinguish real runtime state from reference/archive material. |
| `studio-producer` | Keep prototype lanes coordinated. |
| `ux-researcher` | Define the player journeys: discover, compare, trust, download, install, return. |
| `ui-designer` | Convert journeys into panels, controls, cards, states, and responsive rules. |
| `visual-storyteller` | Make the experience feel like a CoH mission/intel surface. |
| `whimsy-injector` | Add small interactive flavor only after core flows work. |
| `project-shipper` | Freeze the artifact and define verification. |

Lower signal for this repo phase:

| Agent lens | Why it is secondary |
|---|---|
| `studio-coach` | Mostly motivational process language. Useful only as a reminder to coordinate roles; not useful as product substance. |
| `ai-workflow-manager` | Routes across Claude/Qwen/aider/Ollama. Helpful only if we deliberately hand off to another AI tool. Codex can continue this local repo work directly. |

---

## Research Review Logic

Use this sequence when the project needs more research or external comparison.

### 1. Scope the research question

Bad:

```text
Research CoH mods.
```

Good:

```text
What launcher/manifest/control-surface patterns from CityVault or similar CoH tools should inform a local mod browser without expanding scope into server administration?
```

### 2. Split into search angles

For this project, useful angles are:

- CoH mod manager and CityModInstaller behavior.
- LaunchCat runtime layout and Wine path mapping.
- CityVault launcher/manifest/admin concepts.
- CoH `.pigg` asset loading and mod installation conventions.
- Visual product patterns for dense game archives.

### 3. Verify claims against local evidence

External claims are not enough. Every runtime claim should be checked against:

- `~/Library/Application Support/LaunchCat/coh`
- `~/Library/Application Support/LaunchCat/coh/assets/mods`
- `~/Library/Application Support/CityModInstaller`
- `/Applications/CoHModdingTool.app`
- repo `mods.json`
- repo `Upgraded/`

### 4. Synthesize into product choices

Research output must land as one of:

- a doc update,
- a prototype change,
- a data model decision,
- a verification checklist,
- or a deferred/non-goal note.

If research does not change one of those, it is not yet useful to the project.

---

## Concrete Next Workflow

The next coherent loop should be:

```text
using-superpowers
-> workflow-orchestrator
-> workspace-ecosystem-audit
-> ux-researcher + ui-designer + visual-storyteller
-> frontend-design + popular-web-designs
-> p5js + pixel-art
-> playground
-> dogfood
-> project-shipper
```

Upgrade-candidate triage for deciding which complete, partial, and reference
files should be promoted or mined lives in
`docs/plans/2026-07-13-upgrade-candidate-research.md`.

Translated into repo work:

1. **Re-check evidence**
   - Confirm `mods.json` count and category distribution.
   - Confirm installed `.pigg` files and CityModInstaller DB state.
   - Confirm the primary `Upgraded/` HTML still opens cleanly.

2. **Define the player journeys**
   - Browse the archive.
   - Filter by category.
   - Identify high-trust/popular mods.
   - Understand whether a mod is already installed.
   - Open/download/install via the right tool path.

3. **Promote the playground decision**
   - Use `Upgraded/mod-browser-layout-playground.html` to choose layout, density, theme, and texture levels.
   - Turn the chosen direction into a concrete generator change.

4. **Build the next browser version**
   - Keep self-contained HTML unless a build step becomes justified.
   - Prefer local data and local assets.
   - Add runtime-awareness panels before attempting one-click installation.

5. **Dogfood**
   - Check search, category filters, sort, empty states, long mod names, and responsive widths.
   - Record findings in `PLAN/dogfood-findings.md` or a dated plan note.

6. **Ship the working artifact**
   - Pick one primary HTML page.
   - Keep variants as references.
   - Update docs with exact current paths and caveats.

---

## Working Decisions

- Do not treat the old pasted `Mods/mod-*.zip` list as current state. It is historical context.
- Do not treat `/Applications/coh` as the populated runtime unless a future check proves that Wine or LaunchCat maps it to the real tree.
- Do not clone CityVault. Borrow its control-surface concepts selectively.
- Do not overbuild installer automation before the browser can clearly show catalog, local state, and trust signals.
- Do not let the skill ecosystem become the product. Skills are the method; CoX Mod Adventure is the product.

---

## Immediate Next Build Question

The next implementation should answer this:

```text
How does the Paragon Mod Terminal show three things at once:
1. what exists in the 291-mod archive,
2. what is currently installed locally,
3. what the player can confidently do next?
```

That is the bridge from "mod browser" to "CoH-native archive/control surface."
