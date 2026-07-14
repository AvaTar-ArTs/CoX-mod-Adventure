# CoX Mod Adventure - Upgrade Candidate Research
**Date:** 2026-07-13
**Status:** Research and triage note

---

## Purpose

This note researches how to decide what to upscale or upgrade in the repo without only working on files that already feel "complete."

The right strategy is:

```text
inventory all artifacts
-> audit quality and completeness
-> score upgrade value
-> promote the best complete surfaces
-> mine useful incomplete/reference surfaces
-> wrap legacy behavior behind the next version
-> archive or leave non-goal material untouched
```

This keeps the project from polishing only finished HTML pages while ignoring high-value scripts, reference variants, local runtime evidence, and data contracts.

---

## Research Basis

Three outside patterns apply directly.

| Pattern | Relevant idea | CoX application |
|---|---|---|
| Content inventory and audit | Inventory answers "what exists"; audit answers "is it useful, current, complete, or removable." | Make a repo artifact map before deciding what to upgrade. |
| Progressive enhancement | Preserve baseline content/function, then layer richer behavior for capable environments. | Keep self-contained `file://` pages working while adding canvas, runtime panels, and richer interactions. |
| Strangler Fig modernization | Gradually replace pieces while old and new coexist; do not rewrite all at once. | Use current pages/scripts as reference/legacy surfaces while the Paragon Mod Terminal becomes primary. |

Sources reviewed:

- Nielsen Norman Group, "Content Inventory and Auditing 101": inventory lists what exists; audit evaluates quality, gaps, update needs, and removal readiness. `https://www.nngroup.com/articles/content-audits/`
- MDN, "Progressive enhancement": start with baseline content/functionality, then deliver richer experience when supported. `https://developer.mozilla.org/en-US/docs/Glossary/Progressive_Enhancement`
- Microsoft Azure Architecture Center, "Strangler Fig pattern": migrate incrementally by replacing specific functionality while old behavior keeps working. `https://learn.microsoft.com/en-us/azure/architecture/patterns/strangler-fig`
- Martin Fowler, "Strangler Fig": modernization should begin with small additions and move behavior gradually from legacy into new code. `https://martinfowler.com/bliki/StranglerFigApplication.html`

---

## Completion Is Not The Only Filter

Use two separate scores:

1. **Completion**
   - Does it run or open?
   - Does it use real data?
   - Does it have a clear purpose?
   - Is it documented?
   - Is it already verified?

2. **Upgrade value**
   - Does it contain a design, data, workflow, or runtime insight the next version needs?
   - Can it become a primary artifact?
   - Can it be mined into the primary artifact?
   - Does it reduce uncertainty about LaunchCat, CityModInstaller, mods, or player flow?

A complete but generic page may be lower value than an incomplete file that contains the correct runtime model.

---

## Local Candidate Map

Current local inspection suggests this triage.

| Surface | Current read | Upgrade value | Recommended action |
|---|---|---:|---|
| `Upgraded/mod-browser.html` | Complete, self-contained, real 291-mod data, live search/filter/sort. | High | Promote as structural base for the next primary browser. |
| `Upgraded/mod-browser-hud.html` | Complete variant, same data and interactions. | High | Mine HUD state language for install/runtime panels. |
| `Upgraded/mod-browser-comic.html` | Complete variant, same data and interactions. | Medium-high | Mine category color and impact styling; avoid letting comic treatment dominate UX. |
| `Upgraded/mod-browser-layout-playground.html` | Complete tuning playground, not production browser. | High | Use as decision tool for layout/density/theme before changing generator. |
| `Upgraded/generate.py` | Complete generator for three variants, embeds real data and local assets. | High | Upgrade into the main production path after deciding the next layout. |
| `mods.json` and `Upgraded/mods.json` | Valid JSON and identical. | High | Treat as canonical data contract; avoid drift. |
| `scrape-mods.py` | More complete scraper/downloader/installer than older downloader. | High | Promote as the v2 data/tooling base after review. |
| `download-mods.py` | Small older downloader with stale hardcoded IDs and weak verification. | Medium | Do not polish first; either wrap into docs as legacy or fold useful intent into `scrape-mods.py`. |
| `download-mods.sh` | Large shell downloader list. | Low-medium | Treat as historical/bulk fallback; mine only if it has URLs not covered by JSON. |
| `pages/v1-v5/` | Earlier design variations, mostly static pages. | Medium | Mine visual ideas and copy; do not make them primary. |
| `index.html` | Complete landing page but generic compared with `Upgraded/`. | Medium | Replace or redirect toward the Paragon Mod Terminal after primary browser is chosen. |
| `docs/plans/*.md` | Current product comprehension and workflow docs. | High | Keep as decision record and update as build choices become real. |
| `docs/coh-ecosystem-narrative.md` | Strong ecosystem story and runtime explanation. | High | Mine into UI copy and local-state panels. |
| transcript `.txt` exports | Raw context, not product artifacts. | Medium | Mine selectively; do not upgrade directly. |
| `coh-modders/` archives | Tool/archive payloads, large. | Medium | Catalog and reference; do not transform unless installer distribution becomes scope. |
| `docs/tmp-artifacts/` | Evidence/test payloads. | Low-medium | Preserve as evidence; avoid building on it directly. |

---

## Upgrade Lanes

### Lane 1 - Promote Complete Artifacts

These are complete enough to become foundations:

- `Upgraded/mod-browser.html`
- `Upgraded/mod-browser-layout-playground.html`
- `Upgraded/generate.py`
- `mods.json`
- `scrape-mods.py`
- `docs/plans/2026-07-13-cox-mod-adventure-context-and-direction.md`
- `docs/plans/2026-07-13-cox-research-review-and-workflow-logic.md`

Upgrade goal:

```text
Turn the terminal variant into a Paragon Mod Terminal that shows catalog state, installed state, and next actions.
```

### Lane 2 - Mine Incomplete Or Reference Artifacts

These should influence the next version without becoming the next version:

- `pages/v1-v5/`
- `pages/Comic/`
- transcript `.txt` exports
- `docs/coh-ecosystem-narrative.md`
- `docs/full-conversation-export.md`
- `download-mods.py`
- `download-mods.sh`

Mining targets:

- useful copy,
- visual treatments,
- player journey ideas,
- command examples,
- edge cases,
- historical intent.

### Lane 3 - Wrap Or Replace Legacy Behavior

The safer modernization pattern is not delete-and-rewrite. It is:

```text
legacy downloader/page remains available
-> new generator/browser becomes primary
-> docs explain what is legacy vs current
-> old files are archived only after the new path is verified
```

For this repo:

- `download-mods.py` should not be the future install base unless it is rewritten around `mods.json`.
- `scrape-mods.py` already has the better shape and should absorb downloader duties.
- `index.html` can become a launcher/landing shell for the upgraded browser rather than staying as a separate generic homepage.

### Lane 4 - Add Enhancement Layers Last

Progressive enhancement means:

1. baseline opens from `file://`,
2. all 291 mods render,
3. search/filter/sort work,
4. download/page links work,
5. runtime status panels render from reviewed local data,
6. then add p5/canvas/pixel/CRT layers.

Visual effects should never be the first upgrade if the baseline browsing task is not stable.

---

## Scoring Rubric

Use this before working on any file.

| Score | Question | Weight |
|---|---|---:|
| Data-backed | Uses real `mods.json`, real runtime paths, or verified DB/log facts. | 3 |
| User-facing | A player will directly see or use it. | 3 |
| Workflow-critical | A later artifact depends on it. | 3 |
| Complete enough | Opens/runs and has a clear purpose. | 2 |
| Unique insight | Contains design/runtime/copy not duplicated elsewhere. | 2 |
| Low-risk upgrade | Can be improved without breaking other paths. | 2 |
| Replaceable legacy | Better used as reference than as implementation. | -1 |

Priority candidates are files with high positive score, not simply the newest or most complete files.

---

## Recommended Next Upgrade Set

Work in this order:

1. **Primary browser**
   - Start from `Upgraded/mod-browser.html`.
   - Pull HUD state ideas from `Upgraded/mod-browser-hud.html`.
   - Pull restrained category impact from `Upgraded/mod-browser-comic.html`.

2. **Generator**
   - Upgrade `Upgraded/generate.py` so the next primary page can be regenerated.
   - Keep `mods.json` as the data source.

3. **Runtime-state layer**
   - Add a small reviewed data file or inline constant for installed mods:
     - `BetterIcons.pigg`
     - `PocketDAssemblage23.pigg`
     - `accolade_lrt.pigg`
   - Show these as "installed locally" markers in the browser.

4. **Downloader/tooling**
   - Promote `scrape-mods.py` over `download-mods.py`.
   - Add dry-run/install safety and verification before any broader installer automation.

5. **Landing shell**
   - Make `index.html` point clearly to the upgraded browser and local tool story.
   - Do not spend major design time there until the browser is primary.

---

## What Not To Do

- Do not only work on files that are already polished.
- Do not upgrade every page variation equally.
- Do not make `pages/v1-v5` production candidates unless one solves a specific problem better than `Upgraded/`.
- Do not rewrite downloader logic before deciding the data contract and install safety checks.
- Do not add p5/pixel effects before the core catalog and local-state view are clear.
- Do not treat raw transcript files as docs; mine them into docs.

---

## Next Concrete Action

Create an upgrade manifest with one row per repo artifact:

```text
path | type | current role | completeness | upgrade value | action | reason
```

Then use the manifest to choose exactly one upgrade slice:

```text
Paragon Mod Terminal v2:
terminal browser + HUD installed-state markers + comic category accents + regenerated from generate.py
```

That slice upgrades complete files and mines incomplete/reference files at the same time.
