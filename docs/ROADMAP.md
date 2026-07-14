# CoX Mod Adventure — Loose Plan

> A living roadmap. Phases are ordered but not rigid — revisit and reorder as the project
> evolves. Each phase names the skill/agent driving it.

---

## Phase 0 · Brainstorm First
**Skill: `brainstorming`**

Before any code touches the browser or downloader, run a brainstorm session to nail:

- What does a "mod browser" actually need to do? (search, filter, preview, one-click queue?)
- How much of the metadata lives in `coh-mods-list.txt` today vs. what's missing (names, descriptions, categories, download counts)?
- What's the minimum viable data shape a playground needs to feel useful?
- Should the playground and the production `index.html` share a data source, or stay separate tools?

**Output:** a short decision doc — `PLAN/brainstorm-notes.md` — capturing the key choices
and trade-offs agreed on before building.

---

## Phase 1 · Mod Browser Playground
**Skills: `playground` → `frontend-design`**

### 1a · Playground (exploration tool, self-contained HTML)
A single `mod-browser-playground.html` — no build step, no external deps beyond inlined CSS/JS.

Purpose: rapid exploration of how the browser should feel. Controls on the left, live mod
card preview on the right, copy-prompt output at the bottom.

Key controls to prototype:
- Category filter (Maps / Audio / GUI / Popmenus / Graphics / Cursors / Languages / Other)
- Sort order (downloads ↓, name A–Z, newest)
- Search / keyword filter
- Card density toggle (compact list vs. rich card grid)
- Theme toggle (dark retro-CoH palette vs. clean light)

Data: mock JSON of ~20 representative mods hardcoded inline. No network calls.

Deliverable: `mod-browser-playground.html` (open locally with `open`)

### 1b · Production Mod Browser (full frontend-design treatment)
Once the playground confirms the UX direction, build a production-quality
`mod-browser.html` (or fold into `index.html`) using:

- Real data from `coh-mods-list.txt` (or an enriched JSON derived from it)
- A distinctive aesthetic — the CoH aesthetic is late-90s superhero comic meets UI chrome;
  the design should feel like a *mission briefing terminal*, not a generic dark SaaS card grid
- Filter sidebar + search bar + category tabs
- Each mod card shows: name, category badge, download count, description snippet, one-click
  download button / queue button
- Responsive; works on desktop (primary) and tablet

Deliverable: `mod-browser.html` committed alongside `index.html`

---

## Phase 2 · Downloader Enhancement
**Agent: `python-expert`**

Current state of `download-mods.py`:
- Hardcoded mod IDs at the top as a literal list (stale, fragile)
- `urllib.request.urlretrieve` — no retry, no progress, no resume
- 5-worker ThreadPoolExecutor — no rate limiting or backoff
- Saves as `mod-{id}.zip` — no mod name, no category subfolder
- No post-download verification (zip integrity check)

Planned improvements (loose, not prescriptive):

| Area | What to add |
|------|-------------|
| **Data source** | Parse `coh-mods-list.txt` properly; optionally accept a `--category` flag |
| **Progress** | `tqdm` progress bar or simple `print` progress counter |
| **Retry logic** | Exponential backoff on failure (3 attempts) |
| **Resume** | Skip files already on disk (check size > 0) |
| **Naming** | Save as `{category}/{mod-name}-{id}.zip` once metadata is available |
| **Integrity** | `zipfile.is_zipfile()` check after download; log corrupt files |
| **Dry run** | `--dry-run` flag to list what would be downloaded without fetching |
| **Install step** | Optional `--install` flag to copy extracted assets to LaunchCat Wine prefix |

LaunchCat target path:
`~/Library/Application Support/LaunchCat/coh/assets/mods/`

Deliverable: updated `download-mods.py` (v2), changelog comment block at top of file.

---

## Phase 3 · QA the UI
**Skill: `dogfood`**

After `mod-browser.html` is built, run `dogfood` to:

- Open the page in a browser and exercise all interactive paths
- Test: filter by each category, search for a known mod name, sort in each direction
- Test: card hover states, download button behavior, any JS edge cases (empty results, long names)
- Test: responsiveness at 1280px, 768px widths
- Log any bugs to `PLAN/dogfood-findings.md`

---

## Phase 4 · Wire It Together (optional stretch)
- Generate a `mods.json` from the enriched mod list (name + category + download count + URL)
- Both playground and production browser read from the same `mods.json`
- `download-mods.py --from mods.json` uses it as the canonical source
- `index.html` links to `mod-browser.html` as the primary CTA

---

## Skill / Agent Map

| What | Tool |
|------|------|
| Plan features before coding | `brainstorming` skill |
| Interactive UX exploration | `playground` skill |
| Production visual quality | `frontend-design` skill |
| Downloader improvements | `python-expert` agent |
| UI bug hunting | `dogfood` skill |
| Optional: code review before commit | `code-reviewer` agent |

---

## Loose Order of Operations

```
brainstorm → playground prototype → frontend-design build
                                         ↓
                            python-expert enhances downloader
                                         ↓
                               dogfood QA pass → fix findings
                                         ↓
                                 wire together (mods.json)
```

---

*This plan is intentionally loose. Phases can overlap. Start with whatever has the most
momentum — usually the playground, since it's low-stakes and fast to iterate.*
