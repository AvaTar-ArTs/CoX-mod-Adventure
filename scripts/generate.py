#!/usr/bin/env python3
"""Generate all three mod browser HTML variations from mods.json."""
import json, re
from pathlib import Path

HERE = Path(__file__).parent
MODS_JSON = HERE / "mods.json"
FONTS_DIR = Path.home() / "Library/Fonts"
IMG_DIR   = Path.home() / "Pictures/CoH-ComicArt"

mods = json.loads(MODS_JSON.read_text())
MODS_JS = "const MODS=" + json.dumps(mods, separators=(',',':')) + ";"
CATS = ["ALL","Audio","Graphics","GUI / Icons","Popmenus","Maps","Cursors","Languages","Other"]

def font(name, file, weight="normal", style="normal"):
    p = FONTS_DIR / file
    return f"@font-face{{font-family:'{name}';src:url('file://{p}');font-weight:{weight};font-style:{style};}}"

def img(file):
    return f"file://{IMG_DIR / file}"

# ── Shared JS logic (filter / search / sort) ──────────────────────────────────
SHARED_JS = """
let filtered = [...MODS];
let activeCategory = 'ALL';
let searchQuery = '';
let sortKey = 'downloads';
let searchTimer;

function applyFilters() {
  filtered = MODS.filter(m => {
    const catMatch = activeCategory === 'ALL' || m.category === activeCategory;
    const q = searchQuery.toLowerCase();
    const textMatch = !q || m.name.toLowerCase().includes(q) || (m.description||'').toLowerCase().includes(q) || (m.author||'').toLowerCase().includes(q);
    return catMatch && textMatch;
  });
  if (sortKey === 'downloads') filtered.sort((a,b) => b.downloads - a.downloads);
  else if (sortKey === 'name') filtered.sort((a,b) => a.name.localeCompare(b.name));
  else if (sortKey === 'author') filtered.sort((a,b) => (a.author||'').localeCompare(b.author||''));
  renderCards();
  document.getElementById('count').textContent = filtered.length + ' mods';
}

document.getElementById('search').addEventListener('input', e => {
  clearTimeout(searchTimer);
  searchTimer = setTimeout(() => { searchQuery = e.target.value; applyFilters(); }, 200);
});
document.getElementById('sort').addEventListener('change', e => {
  sortKey = e.target.value; applyFilters();
});
document.querySelectorAll('.cat-tab').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.cat-tab').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    activeCategory = btn.dataset.cat;
    applyFilters();
  });
});
applyFilters();
"""

CAT_TABS = "".join(f'<button class="cat-tab" data-cat="{c}">{c}</button>' for c in CATS)

# ─────────────────────────────────────────────────────────────────────────────
# VARIATION 1 · MISSION BRIEFING TERMINAL
# ─────────────────────────────────────────────────────────────────────────────
def build_terminal():
    fonts_css = "\n".join([
        font("BirthOfAHero",    "BIRTH_OF_A_HERO.ttf"),
        font("SuperSquad",      "Super Squad.ttf"),
        font("HeroLight",       "Hero-Light.ttf"),
        font("HeroBold",        "Hero-Bold.ttf",        weight="bold"),
        font("Gobold",          "Gobold.ttf"),
        font("FiraCode",        "FiraCode-Bold.ttf",    weight="bold"),
    ])

    cat_colors = {
        "Audio":"#f59e0b","Graphics":"#38bdf8","GUI / Icons":"#a78bfa",
        "Popmenus":"#34d399","Maps":"#fb923c","Cursors":"#f472b6",
        "Languages":"#60a5fa","Other":"#94a3b8",
    }

    render_js = """
function fmtDownloads(n) {
  if (n >= 1000) return (n/1000).toFixed(1).replace(/\\.0$/,'') + 'k';
  return n.toString();
}
const CAT_COLORS = """ + json.dumps(cat_colors) + """;
function renderCards() {
  const grid = document.getElementById('grid');
  if (!filtered.length) {
    grid.innerHTML = '<div class="no-results">NO MODS FOUND — ADJUST FILTERS</div>';
    return;
  }
  grid.innerHTML = filtered.map(m => `
    <div class="mod-card">
      <div class="card-badge" style="color:${CAT_COLORS[m.category]||'#94a3b8'}">${m.category.toUpperCase()}</div>
      <h3 class="card-name">${m.name}</h3>
      <div class="card-meta">
        <span class="card-author">${m.author||'Unknown'}</span>
        <span class="card-dl">⬇ ${fmtDownloads(m.downloads)}</span>
      </div>
      ${m.description ? `<p class="card-desc">${m.description.slice(0,120)}${m.description.length>120?'…':''}</p>` : ''}
      <a class="card-btn" href="${m.download_url}" target="_blank">DOWNLOAD .PIGG</a>
    </div>
  `).join('');
}
"""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>CoX Mod Terminal</title>
<style>
{fonts_css}

*, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

:root {{
  --bg:       #05050f;
  --surface:  #0d0d1a;
  --border:   #1e2040;
  --gold:     #f59e0b;
  --blue:     #38bdf8;
  --red:      #ef4444;
  --text:     #e2e8f0;
  --muted:    #64748b;
}}

body {{
  background: var(--bg);
  color: var(--text);
  font-family: 'HeroLight', sans-serif;
  min-height: 100vh;
}}

/* scanline overlay */
body::after {{
  content: '';
  position: fixed; inset: 0; pointer-events: none; z-index: 9999;
  background: repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(0,0,0,.08) 2px, rgba(0,0,0,.08) 4px);
}}

/* ── HERO ── */
.hero {{
  position: relative;
  min-height: 260px;
  display: flex; align-items: flex-end;
  padding: 2.5rem 2rem 2rem;
  background: url('{img("KingsRow.jpeg")}') center/cover no-repeat;
  overflow: hidden;
}}
.hero::before {{
  content: '';
  position: absolute; inset: 0;
  background: linear-gradient(180deg, rgba(5,5,15,.55) 0%, rgba(5,5,15,.92) 100%);
}}
.hero-content {{ position: relative; z-index: 1; }}
.hero-eyebrow {{
  font-family: 'Gobold', monospace;
  font-size: .7rem; letter-spacing: .25em;
  color: var(--gold); margin-bottom: .5rem;
}}
.hero-title {{
  font-family: 'BirthOfAHero', sans-serif;
  font-size: clamp(2.4rem, 6vw, 4.5rem);
  color: #fff; line-height: 1;
  text-shadow: 0 0 40px rgba(245,158,11,.35);
}}
.hero-sub {{
  font-family: 'FiraCode', monospace;
  font-size: .8rem; color: var(--muted);
  margin-top: .6rem; letter-spacing: .08em;
}}

/* ── CONTROLS ── */
.controls {{
  background: var(--surface);
  border-bottom: 1px solid var(--border);
  padding: 1rem 2rem;
  display: flex; gap: 1rem; align-items: center; flex-wrap: wrap;
}}
#search {{
  flex: 1; min-width: 200px;
  background: var(--bg); border: 1px solid var(--border);
  color: var(--text); padding: .5rem .75rem;
  font-family: 'FiraCode', monospace; font-size: .85rem;
  outline: none;
}}
#search:focus {{ border-color: var(--gold); }}
#search::placeholder {{ color: var(--muted); }}
#sort {{
  background: var(--bg); border: 1px solid var(--border);
  color: var(--text); padding: .5rem .75rem;
  font-family: 'FiraCode', monospace; font-size: .8rem;
  cursor: pointer; outline: none;
}}
#count {{
  font-family: 'FiraCode', monospace;
  font-size: .75rem; color: var(--gold); white-space: nowrap;
}}

/* ── CATEGORY TABS ── */
.tabs {{
  background: var(--surface);
  border-bottom: 1px solid var(--border);
  padding: 0 2rem;
  display: flex; gap: 0; overflow-x: auto;
  scrollbar-width: none;
}}
.cat-tab {{
  background: none; border: none; cursor: pointer;
  font-family: 'Gobold', monospace; font-size: .7rem;
  letter-spacing: .12em; color: var(--muted);
  padding: .75rem 1.1rem;
  border-bottom: 2px solid transparent;
  transition: color .15s, border-color .15s;
  white-space: nowrap;
}}
.cat-tab:hover {{ color: var(--text); }}
.cat-tab.active {{ color: var(--gold); border-bottom-color: var(--gold); }}

/* ── GRID ── */
.grid-wrap {{ padding: 1.5rem 2rem; }}
#grid {{
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 1rem;
}}

.mod-card {{
  background: var(--surface);
  border: 1px solid var(--border);
  padding: 1.25rem;
  display: flex; flex-direction: column; gap: .5rem;
  transition: border-color .15s, box-shadow .15s;
}}
.mod-card:hover {{
  border-color: var(--gold);
  box-shadow: 0 0 16px rgba(245,158,11,.12);
}}
.card-badge {{
  font-family: 'Gobold', monospace;
  font-size: .6rem; letter-spacing: .2em;
}}
.card-name {{
  font-family: 'SuperSquad', sans-serif;
  font-size: 1rem; color: #fff; line-height: 1.25;
}}
.card-meta {{
  display: flex; justify-content: space-between; align-items: center;
}}
.card-author {{
  font-family: 'FiraCode', monospace;
  font-size: .7rem; color: var(--muted);
}}
.card-dl {{
  font-family: 'FiraCode', monospace;
  font-size: .75rem; color: var(--blue); font-weight: bold;
}}
.card-desc {{
  font-family: 'HeroLight', sans-serif;
  font-size: .8rem; color: var(--muted); line-height: 1.5;
  flex: 1;
}}
.card-btn {{
  display: block; text-align: center;
  background: transparent; border: 1px solid var(--gold);
  color: var(--gold);
  font-family: 'Gobold', monospace; font-size: .65rem; letter-spacing: .15em;
  padding: .5rem; margin-top: .5rem;
  text-decoration: none;
  transition: background .15s, color .15s;
}}
.card-btn:hover {{ background: var(--gold); color: var(--bg); }}

.no-results {{
  grid-column: 1/-1; text-align: center;
  font-family: 'Gobold', monospace; font-size: .8rem;
  letter-spacing: .2em; color: var(--muted); padding: 4rem 0;
}}
</style>
</head>
<body>

<section class="hero">
  <div class="hero-content">
    <div class="hero-eyebrow">// PARAGON CITY · MOD INTELLIGENCE TERMINAL</div>
    <h1 class="hero-title">COX MOD ARCHIVE</h1>
    <p class="hero-sub">291 MODS · HOMECOMING SERVER · PIGG FORMAT</p>
  </div>
</section>

<div class="controls">
  <input id="search" type="search" placeholder="Search mods, authors, descriptions…">
  <select id="sort">
    <option value="downloads">Sort: Most Downloaded</option>
    <option value="name">Sort: Name A–Z</option>
    <option value="author">Sort: Author A–Z</option>
  </select>
  <span id="count"></span>
</div>

<div class="tabs">{CAT_TABS}</div>

<div class="grid-wrap">
  <div id="grid"></div>
</div>

<script>
{MODS_JS}
{render_js}
{SHARED_JS}
</script>
</body>
</html>"""

# ─────────────────────────────────────────────────────────────────────────────
# VARIATION 2 · COMIC BOOK
# ─────────────────────────────────────────────────────────────────────────────
def build_comic():
    fonts_css = "\n".join([
        font("SonicComic",  "sonic_comic.ttf"),
        font("SuperSquad",  "Super Squad.ttf"),
        font("HeroLight",   "Hero-Light.ttf"),
        font("ComicLovers", "COMIC LOVERS.ttf"),
        font("FiraCode",    "FiraCode-Bold.ttf", weight="bold"),
    ])

    cat_colors = {
        "Audio":"#e63946","Graphics":"#2b9348","GUI / Icons":"#7209b7",
        "Popmenus":"#f77f00","Maps":"#023e8a","Cursors":"#d62828",
        "Languages":"#3a0ca3","Other":"#555555",
    }

    render_js = """
function fmtDownloads(n) {
  if (n >= 1000) return (n/1000).toFixed(1).replace(/\\.0$/,'') + 'k';
  return n.toString();
}
const CAT_COLORS = """ + json.dumps(cat_colors) + """;
function renderCards() {
  const grid = document.getElementById('grid');
  if (!filtered.length) {
    grid.innerHTML = '<div class="no-results">NO MODS FOUND!</div>';
    return;
  }
  grid.innerHTML = filtered.map(m => `
    <div class="mod-card">
      <div class="card-badge" style="background:${CAT_COLORS[m.category]||'#555'}">${m.category.toUpperCase()}</div>
      <h3 class="card-name">${m.name}</h3>
      <div class="card-meta">
        <span class="card-author">by ${m.author||'Unknown'}</span>
        <span class="card-dl">${fmtDownloads(m.downloads)} DL</span>
      </div>
      ${m.description ? `<p class="card-desc">${m.description.slice(0,120)}${m.description.length>120?'…':''}</p>` : ''}
      <a class="card-btn" href="${m.download_url}" target="_blank">⚡ GET IT!</a>
    </div>
  `).join('');
}
"""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>CoX Mod Comics</title>
<style>
{fonts_css}

*, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

:root {{
  --ink:    #1a1a1a;
  --paper:  #fdf6e3;
  --red:    #e63946;
  --yellow: #ffbe0b;
  --blue:   #023e8a;
}}

body {{
  background: var(--paper);
  background-image: radial-gradient(circle, #c8b89a 1px, transparent 1px);
  background-size: 8px 8px;
  color: var(--ink);
  font-family: 'HeroLight', sans-serif;
  min-height: 100vh;
}}

/* ── HERO ── */
.hero {{
  background: var(--red);
  border-bottom: 4px solid var(--ink);
  padding: 2.5rem 2rem;
  position: relative;
  overflow: hidden;
}}
.hero::before {{
  content: '';
  position: absolute; inset: 0;
  background: radial-gradient(circle at 80% 50%, rgba(255,190,11,.25), transparent 60%);
}}
.hero-eyebrow {{
  font-family: 'SonicComic', sans-serif;
  font-size: .85rem; color: var(--yellow);
  text-shadow: 2px 2px 0 var(--ink);
  margin-bottom: .4rem;
}}
.hero-title {{
  font-family: 'SonicComic', sans-serif;
  font-size: clamp(2.8rem, 7vw, 5rem);
  color: var(--yellow);
  text-shadow: 3px 3px 0 var(--ink), 6px 6px 0 rgba(0,0,0,.2);
  line-height: 1; position: relative;
}}
.hero-sub {{
  font-family: 'FiraCode', monospace;
  font-size: .75rem; color: rgba(255,255,255,.8);
  margin-top: .6rem;
}}
.hero-bang {{
  position: absolute; right: 2rem; top: 50%; transform: translateY(-50%);
  font-family: 'SonicComic', sans-serif;
  font-size: 5rem; color: var(--yellow);
  text-shadow: 4px 4px 0 var(--ink);
  opacity: .4; pointer-events: none;
}}

/* ── CONTROLS ── */
.controls {{
  background: var(--yellow);
  border-bottom: 3px solid var(--ink);
  padding: .75rem 2rem;
  display: flex; gap: .75rem; align-items: center; flex-wrap: wrap;
}}
#search {{
  flex: 1; min-width: 200px;
  background: #fff; border: 2px solid var(--ink);
  color: var(--ink); padding: .45rem .75rem;
  font-family: 'FiraCode', monospace; font-size: .85rem;
  box-shadow: 3px 3px 0 var(--ink);
  outline: none;
}}
#sort {{
  background: #fff; border: 2px solid var(--ink);
  color: var(--ink); padding: .45rem .75rem;
  font-family: 'FiraCode', monospace; font-size: .8rem;
  box-shadow: 3px 3px 0 var(--ink);
  cursor: pointer; outline: none;
}}
#count {{
  font-family: 'SonicComic', sans-serif;
  font-size: .9rem; color: var(--ink); white-space: nowrap;
}}

/* ── TABS ── */
.tabs {{
  background: var(--ink);
  padding: 0 2rem;
  display: flex; gap: 0; overflow-x: auto;
  scrollbar-width: none;
}}
.cat-tab {{
  background: none; border: none; cursor: pointer;
  font-family: 'SonicComic', sans-serif; font-size: .75rem;
  color: rgba(255,255,255,.5); padding: .65rem 1rem;
  border-bottom: 3px solid transparent;
  transition: color .15s, border-color .15s;
  white-space: nowrap;
}}
.cat-tab:hover {{ color: var(--yellow); }}
.cat-tab.active {{ color: var(--yellow); border-bottom-color: var(--yellow); }}

/* ── GRID ── */
.grid-wrap {{ padding: 1.5rem 2rem; }}
#grid {{
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 1.25rem;
}}

.mod-card {{
  background: #fff;
  border: 3px solid var(--ink);
  box-shadow: 5px 5px 0 var(--ink);
  padding: 1.25rem;
  display: flex; flex-direction: column; gap: .5rem;
  transition: transform .1s, box-shadow .1s;
}}
.mod-card:hover {{
  transform: translate(-2px, -2px);
  box-shadow: 7px 7px 0 var(--ink);
}}
.card-badge {{
  display: inline-block;
  color: #fff; font-family: 'ComicLovers', sans-serif;
  font-size: .65rem; letter-spacing: .1em;
  padding: .2rem .5rem;
  border: 2px solid var(--ink);
  align-self: flex-start;
}}
.card-name {{
  font-family: 'SuperSquad', sans-serif;
  font-size: 1.05rem; color: var(--ink); line-height: 1.2;
}}
.card-meta {{
  display: flex; justify-content: space-between;
  border-top: 1px dashed #ccc; padding-top: .4rem;
}}
.card-author {{
  font-family: 'FiraCode', monospace;
  font-size: .7rem; color: #666; font-style: italic;
}}
.card-dl {{
  font-family: 'SonicComic', sans-serif;
  font-size: .85rem; color: var(--red);
}}
.card-desc {{
  font-family: 'HeroLight', sans-serif;
  font-size: .8rem; color: #444; line-height: 1.5; flex: 1;
}}
.card-btn {{
  display: block; text-align: center;
  background: var(--red); border: 2px solid var(--ink);
  color: #fff; box-shadow: 3px 3px 0 var(--ink);
  font-family: 'SonicComic', sans-serif; font-size: .8rem;
  padding: .5rem; margin-top: .5rem;
  text-decoration: none;
  transition: transform .1s, box-shadow .1s;
}}
.card-btn:hover {{
  transform: translate(-1px,-1px);
  box-shadow: 4px 4px 0 var(--ink);
  background: var(--yellow); color: var(--ink);
}}

.no-results {{
  grid-column: 1/-1; text-align: center;
  font-family: 'SonicComic', sans-serif; font-size: 1.5rem;
  color: var(--red); padding: 4rem 0;
  text-shadow: 2px 2px 0 var(--ink);
}}
</style>
</head>
<body>

<section class="hero">
  <div class="hero-eyebrow">★ ISSUE #291 · THE HOMECOMING COLLECTION ★</div>
  <h1 class="hero-title">COX MOD COMICS</h1>
  <p class="hero-sub">YOUR ULTIMATE GUIDE TO CITY OF HEROES MODS</p>
  <div class="hero-bang">POW!</div>
</section>

<div class="controls">
  <input id="search" type="search" placeholder="Search mods…">
  <select id="sort">
    <option value="downloads">Most Downloaded</option>
    <option value="name">Name A–Z</option>
    <option value="author">Author A–Z</option>
  </select>
  <span id="count"></span>
</div>

<div class="tabs">{CAT_TABS}</div>

<div class="grid-wrap">
  <div id="grid"></div>
</div>

<script>
{MODS_JS}
{render_js}
{SHARED_JS}
</script>
</body>
</html>"""

# ─────────────────────────────────────────────────────────────────────────────
# VARIATION 3 · POWER HUD
# ─────────────────────────────────────────────────────────────────────────────
def build_hud():
    fonts_css = "\n".join([
        font("SpaceMono",   "SpaceMono-Bold.ttf",       weight="bold"),
        font("SpaceMonoR",  "SpaceMono-BoldItalic.ttf", weight="bold", style="italic"),
        font("Gobold",      "Gobold.ttf"),
        font("HeroLight",   "Hero-Light.ttf"),
        font("HeroBold",    "Hero-Bold.ttf",            weight="bold"),
        font("FiraCode",    "FiraCode-Bold.ttf",        weight="bold"),
    ])

    cat_colors = {
        "Audio":"#00d4ff","Graphics":"#7c3aed","GUI / Icons":"#06d6a0",
        "Popmenus":"#f72585","Maps":"#4cc9f0","Cursors":"#b5179e",
        "Languages":"#3a86ff","Other":"#6b7280",
    }

    render_js = """
function fmtDownloads(n) {
  if (n >= 1000) return (n/1000).toFixed(1).replace(/\\.0$/,'') + 'k';
  return n.toString();
}
const CAT_COLORS = """ + json.dumps(cat_colors) + """;
function renderCards() {
  const grid = document.getElementById('grid');
  if (!filtered.length) {
    grid.innerHTML = '<div class="no-results">[ NO TARGETS FOUND ]</div>';
    return;
  }
  grid.innerHTML = filtered.map(m => `
    <div class="mod-card">
      <div class="card-header">
        <div class="card-badge" style="--cc:${CAT_COLORS[m.category]||'#6b7280'}">${m.category.toUpperCase()}</div>
        <div class="card-dl">${fmtDownloads(m.downloads)}<span class="dl-label">DL</span></div>
      </div>
      <h3 class="card-name">${m.name}</h3>
      <div class="card-author">${m.author||'UNKNOWN AGENT'}</div>
      ${m.description ? `<p class="card-desc">${m.description.slice(0,120)}${m.description.length>120?'…':''}</p>` : ''}
      <a class="card-btn" href="${m.download_url}" target="_blank">
        <span class="btn-icon">▶</span> ACQUIRE MODULE
      </a>
    </div>
  `).join('');
}
"""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>CoX Power HUD</title>
<style>
{fonts_css}

*, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

:root {{
  --bg:     #050510;
  --panel:  #080820;
  --border: #0d1030;
  --cyan:   #00d4ff;
  --purple: #7c3aed;
  --glow:   rgba(0,212,255,.15);
  --text:   #c8d8f0;
  --muted:  #4a5580;
}}

body {{
  background: var(--bg);
  background-image:
    linear-gradient(rgba(0,212,255,.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0,212,255,.03) 1px, transparent 1px);
  background-size: 40px 40px;
  color: var(--text);
  font-family: 'HeroLight', sans-serif;
  min-height: 100vh;
}}

/* ── HERO ── */
.hero {{
  position: relative;
  min-height: 220px;
  display: flex; align-items: center;
  padding: 2.5rem 2rem;
  background: url('{img("FuturCityScape.jpeg")}') center/cover no-repeat;
  overflow: hidden;
}}
.hero::before {{
  content: '';
  position: absolute; inset: 0;
  background: linear-gradient(180deg, rgba(5,5,16,.4) 0%, rgba(5,5,16,.95) 100%);
}}
.hero::after {{
  content: '';
  position: absolute; bottom: 0; left: 0; right: 0;
  height: 2px;
  background: linear-gradient(90deg, transparent, var(--cyan), transparent);
  box-shadow: 0 0 20px var(--cyan);
}}
.hero-content {{ position: relative; z-index: 1; }}
.hero-id {{
  font-family: 'SpaceMono', monospace;
  font-size: .65rem; letter-spacing: .3em;
  color: var(--cyan); margin-bottom: .5rem;
  text-shadow: 0 0 12px var(--cyan);
}}
.hero-title {{
  font-family: 'Gobold', sans-serif;
  font-size: clamp(2.5rem, 6vw, 4.5rem);
  color: #fff; line-height: 1;
  text-shadow: 0 0 40px rgba(0,212,255,.5);
  letter-spacing: .05em;
}}
.hero-sub {{
  font-family: 'SpaceMono', monospace;
  font-size: .7rem; color: var(--muted);
  margin-top: .6rem; letter-spacing: .12em;
}}

/* ── CONTROLS ── */
.controls {{
  background: var(--panel);
  border-bottom: 1px solid var(--border);
  border-top: 1px solid rgba(0,212,255,.1);
  padding: 1rem 2rem;
  display: flex; gap: 1rem; align-items: center; flex-wrap: wrap;
}}
#search {{
  flex: 1; min-width: 200px;
  background: var(--bg); border: 1px solid rgba(0,212,255,.25);
  color: var(--text); padding: .5rem .75rem;
  font-family: 'SpaceMono', monospace; font-size: .78rem;
  outline: none; letter-spacing: .05em;
}}
#search:focus {{ border-color: var(--cyan); box-shadow: 0 0 12px rgba(0,212,255,.15); }}
#search::placeholder {{ color: var(--muted); }}
#sort {{
  background: var(--bg); border: 1px solid rgba(0,212,255,.2);
  color: var(--text); padding: .5rem .75rem;
  font-family: 'SpaceMono', monospace; font-size: .75rem;
  cursor: pointer; outline: none;
}}
#count {{
  font-family: 'SpaceMono', monospace;
  font-size: .7rem; color: var(--cyan);
  text-shadow: 0 0 10px var(--cyan); white-space: nowrap;
}}

/* ── TABS ── */
.tabs {{
  background: var(--panel);
  border-bottom: 1px solid var(--border);
  padding: 0 2rem;
  display: flex; gap: 0; overflow-x: auto;
  scrollbar-width: none;
}}
.cat-tab {{
  background: none; border: none; cursor: pointer;
  font-family: 'SpaceMono', monospace; font-size: .65rem;
  letter-spacing: .1em; color: var(--muted);
  padding: .7rem 1rem;
  border-bottom: 2px solid transparent;
  transition: color .15s, border-color .15s, text-shadow .15s;
  white-space: nowrap;
}}
.cat-tab:hover {{ color: var(--text); }}
.cat-tab.active {{
  color: var(--cyan); border-bottom-color: var(--cyan);
  text-shadow: 0 0 10px var(--cyan);
}}

/* ── GRID ── */
.grid-wrap {{ padding: 1.5rem 2rem; }}
#grid {{
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(270px, 1fr));
  gap: 1rem;
}}

.mod-card {{
  background: var(--panel);
  border: 1px solid var(--border);
  clip-path: polygon(0 0, calc(100% - 14px) 0, 100% 14px, 100% 100%, 0 100%);
  padding: 1.25rem;
  display: flex; flex-direction: column; gap: .5rem;
  transition: border-color .15s, box-shadow .15s;
  position: relative;
}}
.mod-card:hover {{
  border-color: rgba(0,212,255,.4);
  box-shadow: 0 0 20px var(--glow), inset 0 0 20px rgba(0,212,255,.04);
}}
.card-header {{
  display: flex; justify-content: space-between; align-items: flex-start;
}}
.card-badge {{
  font-family: 'SpaceMono', monospace;
  font-size: .6rem; letter-spacing: .12em;
  color: var(--cc, var(--cyan));
  text-shadow: 0 0 8px var(--cc, var(--cyan));
}}
.card-dl {{
  font-family: 'SpaceMono', monospace; font-weight: bold;
  font-size: .9rem; color: var(--cyan);
  text-shadow: 0 0 12px var(--cyan);
}}
.dl-label {{
  font-size: .55rem; opacity: .6; margin-left: .2rem;
}}
.card-name {{
  font-family: 'HeroBold', sans-serif;
  font-size: 1rem; color: #e0ecff; line-height: 1.25;
}}
.card-author {{
  font-family: 'SpaceMono', monospace;
  font-size: .65rem; color: var(--muted); letter-spacing: .08em;
}}
.card-desc {{
  font-family: 'HeroLight', sans-serif;
  font-size: .78rem; color: var(--muted); line-height: 1.5; flex: 1;
}}
.card-btn {{
  display: flex; align-items: center; gap: .5rem;
  justify-content: center;
  background: transparent;
  border: 1px solid rgba(0,212,255,.3);
  color: var(--cyan);
  font-family: 'SpaceMono', monospace; font-size: .65rem; letter-spacing: .12em;
  padding: .55rem; margin-top: .5rem;
  text-decoration: none;
  clip-path: polygon(0 0, calc(100% - 8px) 0, 100% 8px, 100% 100%, 0 100%);
  transition: background .15s, border-color .15s, text-shadow .15s;
}}
.card-btn:hover {{
  background: rgba(0,212,255,.1);
  border-color: var(--cyan);
  text-shadow: 0 0 8px var(--cyan);
}}
.btn-icon {{ opacity: .7; }}

.no-results {{
  grid-column: 1/-1; text-align: center;
  font-family: 'SpaceMono', monospace; font-size: .8rem;
  letter-spacing: .2em; color: var(--muted); padding: 4rem 0;
}}
</style>
</head>
<body>

<section class="hero">
  <div class="hero-content">
    <div class="hero-id">[ PARAGON CITY · MOD ACQUISITION SYSTEM · HC-291 ]</div>
    <h1 class="hero-title">COX POWER HUD</h1>
    <p class="hero-sub">HOMECOMING MOD DATABASE · ALL MODULES AVAILABLE</p>
  </div>
</section>

<div class="controls">
  <input id="search" type="search" placeholder="[ SEARCH MODULES… ]">
  <select id="sort">
    <option value="downloads">SORT: ACQUISITION COUNT</option>
    <option value="name">SORT: DESIGNATION A–Z</option>
    <option value="author">SORT: AGENT A–Z</option>
  </select>
  <span id="count"></span>
</div>

<div class="tabs">{CAT_TABS}</div>

<div class="grid-wrap">
  <div id="grid"></div>
</div>

<script>
{MODS_JS}
{render_js}
{SHARED_JS}
</script>
</body>
</html>"""

# ── Write all three ───────────────────────────────────────────────────────────
variants = [
    ("mod-browser.html",       build_terminal, "Variation 1: Mission Briefing Terminal"),
    ("mod-browser-comic.html", build_comic,    "Variation 2: Comic Book"),
    ("mod-browser-hud.html",   build_hud,      "Variation 3: Power HUD"),
]

for fname, builder, label in variants:
    html = builder()
    path = HERE / fname
    path.write_text(html, encoding="utf-8")
    print(f"✓ {fname}  ({len(html)//1024}KB)  — {label}")

print("\nDone. Open with:")
for fname, _, _ in variants:
    print(f"  open Upgraded/{fname}")
