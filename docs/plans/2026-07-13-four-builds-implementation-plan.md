# CoX Mod Browser — Four Builds Implementation Plan

> **For Hermes:** Use subagent-driven-development skill to implement this plan task-by-task.

**Goal:** Expand the mod browser prototype into four purpose-built surfaces sharing a common core layer.

**Architecture:** A `core/` folder holds mods.js, render.js, and style.css. Four build folders (a-static, b-server, c-electron, d-launcher) each include those three files via relative paths. No npm, no bundler for A/D. Flask for B, Electron for C.

**Tech Stack:** Vanilla HTML/CSS/JS (A, D), Python Flask (B), Electron (C), p5.js CDN for ambient canvas.

**Starting point:** `Upgraded/mod-browser-v2.html` exists with all 291 mods inlined — use it as the extraction source.

---

## Phase 0: Extract Core

---

### Task 0.1: Create Upgraded/core/ folder structure

**Objective:** Make the three core files that all builds will share.

**Files:**
- Create: `Upgraded/core/mods.js`
- Create: `Upgraded/core/render.js`
- Create: `Upgraded/core/style.css`

**Step 1: Extract mods.js**

Run from repo root:
```bash
python3 - <<'EOF'
import json, re

mods = json.load(open('mods.json'))
cat_art = {
    'Audio':       'TerraVolta.jpeg',
    'Graphics':    'KingsRow.jpeg',
    'GUI / Icons': 'IndepPort.jpeg',
    'Popmenus':    'PerezPark.jpeg',
    'Maps':        'AncientCity.jpeg',
    'Cursors':     'FutureCity.jpeg',
    'Languages':   'TimeCityscape.jpeg',
    'Other':       'CityscapeView.jpeg',
}
for m in mods:
    m['art'] = cat_art.get(m.get('category', 'Other'), 'KingsRow.jpeg')
    d = m.get('description', '') or ''
    d = re.sub(r'\s+', ' ', d).strip()
    m['description'] = d[:160] + ('…' if len(d) > 160 else '')

with open('Upgraded/core/mods.js', 'w') as f:
    f.write('const MODS = ')
    f.write(json.dumps(mods, separators=(',', ':')))
    f.write(';\n')
print('mods.js written:', len(mods), 'mods')
EOF
```
Expected: `mods.js written: 291 mods`

**Step 2: Create render.js**

Create `Upgraded/core/render.js` with content:
```js
const ART_BASE = 'file:///Users/steven/Pictures/CoH-ComicArt/';

function badgeClass(cat) {
  const map = {
    'Audio': 'badge-audio', 'Graphics': 'badge-graphics',
    'GUI / Icons': 'badge-gui', 'Popmenus': 'badge-popmenu',
    'Maps': 'badge-maps', 'Cursors': 'badge-cursors',
  };
  return map[cat] || 'badge-other';
}

function fmtDl(n) {
  if (!n) return '–';
  return n >= 1000 ? (n / 1000).toFixed(1) + 'k' : String(n);
}

function makeCard(m) {
  const div = document.createElement('div');
  div.className = 'mod-card';
  const desc = m.description
    ? `<div class="card-desc">${m.description}</div>` : '';
  div.innerHTML = `
    <span class="card-badge ${badgeClass(m.category)}">${m.category.toUpperCase()}</span>
    <div class="card-name">${m.name}</div>
    <div class="card-meta">
      <span>${m.author || 'Unknown'}</span>
      <span class="card-dl">↓ ${fmtDl(m.downloads)}</span>
    </div>
    ${desc}
    <div class="card-actions">
      <a class="btn btn-primary" href="${m.download_url}" target="_blank">DOWNLOAD</a>
      <a class="btn" href="${m.page_url}" target="_blank">INFO</a>
    </div>`;
  return div;
}

function renderBento(el) {
  const top5 = [...MODS].sort((a, b) => (b.downloads || 0) - (a.downloads || 0)).slice(0, 5);
  el.innerHTML = top5.map((m, i) => `
    <div class="bento-card" onclick="window.open('${m.page_url}','_blank')">
      <div class="bento-thumb" style="background-image:url('${ART_BASE}${m.art}')"></div>
      <div class="bento-inner">
        <div class="bento-rank">#${i + 1} · ${m.category.toUpperCase()}</div>
        <div class="bento-name">${m.name}</div>
        <div class="bento-dl">↓ ${fmtDl(m.downloads)} downloads</div>
      </div>
    </div>`).join('');
}

function renderTabs(el, cats, activeCat, onClick) {
  el.innerHTML = cats.map(c =>
    `<button class="cat-tab${c === activeCat ? ' active' : ''}" data-cat="${c}">${c.toUpperCase()} (${c === 'All' ? MODS.length : MODS.filter(m => m.category === c).length})</button>`
  ).join('');
  el.querySelectorAll('.cat-tab').forEach(btn =>
    btn.addEventListener('click', () => onClick(btn.dataset.cat))
  );
}
```

**Step 3: Extract style.css**

Copy the full `<style>` block from `Upgraded/mod-browser-v2.html` (lines 8–206, everything between `<style>` and `</style>`) into `Upgraded/core/style.css`. Remove the `<style>` and `</style>` wrapper tags.

**Step 4: Verify**

```bash
ls -lh Upgraded/core/
```
Expected: three files — mods.js (~130KB), render.js (~2KB), style.css (~6KB)

**Step 5: Commit**
```bash
git add Upgraded/core/
git commit -m "feat: extract shared core (mods, render, style) from v2"
```

---

## Phase 1: Build A — Static Browser

---

### Task 1.1: Scaffold a-static/index.html

**Objective:** Create a-static/ that loads from core/ and renders the full mod browser.

**Files:**
- Create: `Upgraded/a-static/index.html`

**Step 1: Create the file**

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>CoX Mod Archive</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.9.4/p5.min.js"></script>
<link rel="stylesheet" href="../core/style.css">
<style>
/* a-static overrides */
</style>
</head>
<body class="theme-terminal density-standard">
<canvas id="p5-canvas"></canvas>
<main>
  <div class="hero">
    <div class="hero-content">
      <div class="eyebrow">CITY OF HEROES · HOMECOMING</div>
      <div class="hero-title">MOD ARCHIVE</div>
      <div class="hero-sub" id="hero-sub">291 MODS · COMMUNITY CATALOG</div>
    </div>
  </div>
  <div class="bento-label">TOP DOWNLOADS</div>
  <div class="bento" id="bento"></div>
  <div class="controls">
    <input id="search" type="search" placeholder="Search mods, authors…" autocomplete="off">
    <select id="sort" class="ctrl-select">
      <option value="downloads">SORT: DOWNLOADS</option>
      <option value="name">SORT: NAME A→Z</option>
      <option value="author">SORT: AUTHOR</option>
    </select>
    <select id="layout" class="ctrl-select">
      <option value="masonry">LAYOUT: MASONRY</option>
      <option value="bento">LAYOUT: BENTO</option>
      <option value="list">LAYOUT: LIST</option>
    </select>
    <select id="density" class="ctrl-select">
      <option value="standard">DENSITY: STANDARD</option>
      <option value="compact">DENSITY: COMPACT</option>
    </select>
    <select id="theme" class="ctrl-select">
      <option value="terminal">THEME: TERMINAL</option>
      <option value="hud">THEME: HUD</option>
      <option value="comic">THEME: COMIC</option>
    </select>
    <span id="count"></span>
  </div>
  <div class="tabs" id="tabs"></div>
  <div class="archive-wrap">
    <div class="archive layout-masonry" id="archive"></div>
  </div>
</main>
<script src="../core/mods.js"></script>
<script src="../core/render.js"></script>
<script src="app.js"></script>
</body>
</html>
```

**Step 2: Verify file exists**
```bash
ls Upgraded/a-static/
```
Expected: `index.html`

---

### Task 1.2: Create a-static/app.js (filter, sort, render loop)

**Objective:** Wire up all controls and render the mod grid.

**Files:**
- Create: `Upgraded/a-static/app.js`

**Step 1: Create app.js**

```js
const CATS = ['All', ...new Set(MODS.map(m => m.category))];
let activeCat = 'All', query = '', sortBy = 'downloads';

function renderArchive() {
  const layout = document.getElementById('layout').value;
  const el = document.getElementById('archive');
  el.className = `archive layout-${layout}`;

  let list = MODS.filter(m => {
    if (activeCat !== 'All' && m.category !== activeCat) return false;
    if (!query) return true;
    const q = query.toLowerCase();
    return (m.name || '').toLowerCase().includes(q)
      || (m.author || '').toLowerCase().includes(q)
      || (m.description || '').toLowerCase().includes(q);
  });

  list = list.sort((a, b) => {
    if (sortBy === 'downloads') return (b.downloads || 0) - (a.downloads || 0);
    if (sortBy === 'name') return (a.name || '').localeCompare(b.name || '');
    return (a.author || '').localeCompare(b.author || '');
  });

  document.getElementById('count').textContent = list.length + ' mods';
  el.innerHTML = '';
  if (!list.length) {
    el.innerHTML = '<div class="empty">NO MODS MATCH · ADJUST FILTERS</div>';
    return;
  }
  list.forEach(m => el.appendChild(makeCard(m)));
}

document.getElementById('search').addEventListener('input', e => { query = e.target.value; renderArchive(); });
document.getElementById('sort').addEventListener('change', e => { sortBy = e.target.value; renderArchive(); });
document.getElementById('layout').addEventListener('change', () => renderArchive());
document.getElementById('density').addEventListener('change', e => {
  document.body.className = document.body.className.replace(/density-\S+/, '') + ' density-' + e.target.value;
});
document.getElementById('theme').addEventListener('change', e => {
  document.body.className = document.body.className.replace(/theme-\S+/, '') + ' theme-' + e.target.value;
});

renderBento(document.getElementById('bento'));
renderTabs(document.getElementById('tabs'), CATS, activeCat, cat => {
  activeCat = cat;
  renderTabs(document.getElementById('tabs'), CATS, activeCat, arguments.callee);
  renderArchive();
});
renderArchive();
```

**Step 2: Open in browser and verify**

Open `Upgraded/a-static/index.html` in Safari or Chrome.
Expected: 291 mods visible in masonry grid, bento strip shows top 5, search and filters work.

**Step 3: Commit**
```bash
git add Upgraded/a-static/
git commit -m "feat: build A static browser with core integration"
```

---

### Task 1.3: Add mod detail drawer to a-static

**Objective:** Click a card → slide-in right drawer with full mod details.

**Files:**
- Modify: `Upgraded/a-static/index.html` (add drawer HTML)
- Modify: `Upgraded/a-static/app.js` (add drawer open/close logic)
- Modify: `Upgraded/core/style.css` (add drawer CSS)

**Step 1: Add drawer CSS to core/style.css**

Append to `Upgraded/core/style.css`:
```css
/* ── MOD DETAIL DRAWER ── */
.drawer-overlay {
  position: fixed; inset: 0; z-index: 100;
  background: rgba(0,0,0,.6); opacity: 0;
  pointer-events: none; transition: opacity .2s;
}
.drawer-overlay.open { opacity: 1; pointer-events: all; }

.drawer {
  position: fixed; top: 0; right: 0; bottom: 0;
  width: min(420px, 100vw);
  background: var(--surface); border-left: 1px solid var(--border);
  padding: 1.5rem; overflow-y: auto;
  transform: translateX(100%); transition: transform .25s ease;
  z-index: 101; display: flex; flex-direction: column; gap: 1rem;
}
.drawer.open { transform: translateX(0); }
.drawer-close {
  align-self: flex-end; background: none; border: 1px solid var(--border);
  color: var(--muted); font-family: 'Gobold', monospace;
  font-size: .65rem; letter-spacing: .15em;
  padding: .3rem .6rem; cursor: pointer;
}
.drawer-close:hover { border-color: var(--gold); color: var(--gold); }
.drawer-cat {
  font-family: 'Gobold', monospace; font-size: .6rem;
  letter-spacing: .25em;
}
.drawer-name {
  font-family: 'BirthOfAHero', sans-serif;
  font-size: 1.6rem; color: #fff; line-height: 1.1;
}
.drawer-author {
  font-family: 'FiraCode', monospace; font-size: .75rem; color: var(--muted);
}
.drawer-thumb {
  width: 100%; height: 120px;
  background-size: cover; background-position: center;
  border: 1px solid var(--border); opacity: .6;
}
.drawer-dl {
  font-family: 'FiraCode', monospace; font-size: .8rem; color: var(--gold);
}
.drawer-desc {
  font-size: .8rem; color: var(--muted); line-height: 1.6;
}
.drawer-actions { display: flex; gap: .75rem; margin-top: auto; }
```

**Step 2: Add drawer HTML to a-static/index.html** (before closing `</body>`):

```html
<div class="drawer-overlay" id="overlay"></div>
<aside class="drawer" id="drawer">
  <button class="drawer-close" id="drawerClose">✕ CLOSE</button>
  <span class="drawer-cat" id="dCat"></span>
  <div class="drawer-name" id="dName"></div>
  <div class="drawer-author" id="dAuthor"></div>
  <div class="drawer-thumb" id="dThumb"></div>
  <div class="drawer-dl" id="dDl"></div>
  <div class="drawer-desc" id="dDesc"></div>
  <div class="drawer-actions" id="dActions"></div>
</aside>
```

**Step 3: Add drawer logic to a-static/app.js**

Append to `app.js`:
```js
function openDrawer(m) {
  document.getElementById('dCat').textContent = m.category.toUpperCase();
  document.getElementById('dCat').className = `drawer-cat ${badgeClass(m.category)}`;
  document.getElementById('dName').textContent = m.name;
  document.getElementById('dAuthor').textContent = 'BY ' + (m.author || 'Unknown');
  document.getElementById('dThumb').style.backgroundImage = `url('${ART_BASE}${m.art}')`;
  document.getElementById('dDl').textContent = '↓ ' + fmtDl(m.downloads) + ' downloads';
  document.getElementById('dDesc').textContent = m.description || 'No description available.';
  document.getElementById('dActions').innerHTML = `
    <a class="btn btn-primary" href="${m.download_url}" target="_blank">DOWNLOAD</a>
    <a class="btn" href="${m.page_url}" target="_blank">MOD PAGE</a>`;
  document.getElementById('drawer').classList.add('open');
  document.getElementById('overlay').classList.add('open');
}

function closeDrawer() {
  document.getElementById('drawer').classList.remove('open');
  document.getElementById('overlay').classList.remove('open');
}

document.getElementById('drawerClose').addEventListener('click', closeDrawer);
document.getElementById('overlay').addEventListener('click', closeDrawer);
```

**Step 4: Wire card click to open drawer**

In `app.js`, modify the `list.forEach` line:
```js
list.forEach(m => {
  const card = makeCard(m);
  card.addEventListener('click', e => {
    if (!e.target.closest('a')) openDrawer(m);
  });
  el.appendChild(card);
});
```

**Step 5: Verify**

Open `a-static/index.html`. Click a mod card (not the download/info buttons). Drawer should slide in from the right with full mod details. Click overlay or ✕ CLOSE to dismiss.

**Step 6: Commit**
```bash
git add Upgraded/a-static/ Upgraded/core/style.css
git commit -m "feat: add mod detail drawer to a-static build"
```

---

## Phase 2: Build B — Local Server

---

### Task 2.1: Scaffold b-server/ folder

**Objective:** Create the Flask server and its HTML entry point.

**Files:**
- Create: `Upgraded/b-server/requirements.txt`
- Create: `Upgraded/b-server/server.py`
- Create: `Upgraded/b-server/index.html`

**Step 1: Create requirements.txt**
```
flask>=3.0.0
requests>=2.31.0
```

**Step 2: Create server.py**

```python
import json, os, shutil, tempfile, subprocess
from pathlib import Path
from flask import Flask, jsonify, request, send_from_directory
import requests as req

app = Flask(__name__, static_folder='.')
ROOT = Path(__file__).parent
MODS_FILE = ROOT.parent.parent / 'mods.json'
COH_DATA = Path('/Applications/coh/data')

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/core/<path:filename>')
def core(filename):
    return send_from_directory('../core', filename)

@app.route('/api/mods')
def api_mods():
    return jsonify(json.loads(MODS_FILE.read_text()))

@app.route('/api/installed')
def api_installed():
    if not COH_DATA.exists():
        return jsonify([])
    return jsonify([f.stem for f in COH_DATA.glob('*.pigg')])

@app.route('/api/install', methods=['POST'])
def api_install():
    data = request.json
    mod_id = data.get('id')
    url = data.get('download_url')
    if not url:
        return jsonify({'ok': False, 'error': 'missing url'}), 400
    try:
        r = req.get(url, timeout=60)
        r.raise_for_status()
        fname = url.split('file=')[-1].split('/')[-1]
        dest = COH_DATA / fname if COH_DATA.exists() else ROOT / 'downloads' / fname
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(r.content)
        return jsonify({'ok': True, 'path': str(dest), 'id': mod_id})
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 500

if __name__ == '__main__':
    print('CoX Mod Server → http://localhost:7777')
    app.run(port=7777, debug=True)
```

**Step 3: Create index.html**

Same structure as `a-static/index.html` but with server-aware install logic. Copy `a-static/index.html`, change the `<script src>` paths to `/core/` and add `<script src="app.js"></script>`. The `app.js` will differ (see next task).

**Step 4: Verify structure**
```bash
ls Upgraded/b-server/
```
Expected: `index.html  requirements.txt  server.py`

**Step 5: Commit**
```bash
git add Upgraded/b-server/
git commit -m "feat: scaffold b-server Flask install server"
```

---

### Task 2.2: Create b-server/app.js with install API calls

**Objective:** Install button calls the local server instead of direct download.

**Files:**
- Create: `Upgraded/b-server/app.js`

**Step 1: Create app.js**

```js
// Same filter/sort/render as a-static, plus server install
const CATS = ['All', ...new Set(MODS.map(m => m.category))];
let activeCat = 'All', query = '', sortBy = 'downloads';
const installed = new Set();

async function fetchInstalled() {
  try {
    const r = await fetch('/api/installed');
    const list = await r.json();
    list.forEach(id => installed.add(id));
  } catch(_) {}
}

function makeServerCard(m) {
  const card = makeCard(m);
  const actions = card.querySelector('.card-actions');
  const isIn = installed.has(String(m.id));

  const installBtn = document.createElement('button');
  installBtn.className = 'btn btn-primary install-btn';
  installBtn.dataset.id = m.id;
  installBtn.textContent = isIn ? '✓ INSTALLED' : 'INSTALL';
  if (isIn) installBtn.disabled = true;

  installBtn.addEventListener('click', async e => {
    e.stopPropagation();
    installBtn.textContent = 'INSTALLING…';
    installBtn.disabled = true;
    const res = await fetch('/api/install', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({id: m.id, download_url: m.download_url}),
    });
    const json = await res.json();
    if (json.ok) {
      installBtn.textContent = '✓ INSTALLED';
      installed.add(String(m.id));
    } else {
      installBtn.textContent = 'ERROR';
      installBtn.disabled = false;
      console.error(json.error);
    }
  });

  actions.prepend(installBtn);
  return card;
}

function renderArchive() {
  const layout = document.getElementById('layout').value;
  const el = document.getElementById('archive');
  el.className = `archive layout-${layout}`;

  let list = MODS.filter(m => {
    if (activeCat !== 'All' && m.category !== activeCat) return false;
    if (!query) return true;
    const q = query.toLowerCase();
    return (m.name || '').toLowerCase().includes(q)
      || (m.author || '').toLowerCase().includes(q)
      || (m.description || '').toLowerCase().includes(q);
  }).sort((a, b) => {
    if (sortBy === 'downloads') return (b.downloads || 0) - (a.downloads || 0);
    if (sortBy === 'name') return (a.name || '').localeCompare(b.name || '');
    return (a.author || '').localeCompare(b.author || '');
  });

  document.getElementById('count').textContent = list.length + ' mods';
  el.innerHTML = '';
  list.forEach(m => el.appendChild(makeServerCard(m)));
}

document.getElementById('search').addEventListener('input', e => { query = e.target.value; renderArchive(); });
document.getElementById('sort').addEventListener('change', e => { sortBy = e.target.value; renderArchive(); });
document.getElementById('layout').addEventListener('change', () => renderArchive());
document.getElementById('density').addEventListener('change', e => {
  document.body.className = document.body.className.replace(/density-\S+/, '') + ' density-' + e.target.value;
});
document.getElementById('theme').addEventListener('change', e => {
  document.body.className = document.body.className.replace(/theme-\S+/, '') + ' theme-' + e.target.value;
});

renderBento(document.getElementById('bento'));
renderTabs(document.getElementById('tabs'), CATS, activeCat, cat => {
  activeCat = cat;
  renderTabs(document.getElementById('tabs'), CATS, activeCat, arguments.callee);
  renderArchive();
});

fetchInstalled().then(() => renderArchive());
```

**Step 2: Test the server**
```bash
cd Upgraded/b-server
pip3 install -r requirements.txt
python3 server.py
```
Expected: `CoX Mod Server → http://localhost:7777`

Open `http://localhost:7777` in browser. Expected: same mod browser as A-static, install buttons visible.

**Step 3: Commit**
```bash
git add Upgraded/b-server/app.js
git commit -m "feat: b-server install API integration with status buttons"
```

---

## Phase 3: Build D — Loadout Launcher

---

### Task 3.1: Scaffold d-launcher/index.html (split-panel layout)

**Objective:** Two-panel layout — mod browser left, active loadout right.

**Files:**
- Create: `Upgraded/d-launcher/index.html`
- Create: `Upgraded/d-launcher/loadout.js`

**Step 1: Create index.html**

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>CoX Loadout Builder</title>
<link rel="stylesheet" href="../core/style.css">
<style>
body { overflow: hidden; }
.launcher-shell {
  display: grid;
  grid-template-columns: 1fr 340px;
  height: 100vh; overflow: hidden;
}
.browser-panel { overflow-y: auto; }
.loadout-panel {
  background: var(--surface); border-left: 1px solid var(--border);
  display: flex; flex-direction: column; overflow: hidden;
}
.loadout-header {
  padding: 1rem 1.25rem .5rem;
  font-family: 'BirthOfAHero', sans-serif;
  font-size: 1.4rem; color: #fff; flex-shrink: 0;
}
.loadout-sub {
  font-family: 'Gobold', monospace; font-size: .58rem;
  letter-spacing: .2em; color: var(--muted);
  padding: 0 1.25rem .75rem; flex-shrink: 0;
}
.loadout-slots { overflow-y: auto; flex: 1; padding: .5rem 1rem; }
.slot-group { margin-bottom: .75rem; }
.slot-label {
  font-family: 'Gobold', monospace; font-size: .58rem;
  letter-spacing: .2em; color: var(--muted);
  padding: .3rem 0 .2rem;
  border-bottom: 1px solid var(--border); margin-bottom: .3rem;
}
.slot-item {
  display: flex; align-items: center; justify-content: space-between;
  padding: .35rem .5rem; font-size: .78rem;
  border: 1px solid var(--border); margin-bottom: .25rem;
  background: var(--bg);
}
.slot-item.conflict { border-color: #f59e0b; }
.slot-item-name { flex: 1; color: var(--text); font-size: .75rem; }
.slot-remove {
  background: none; border: none; color: var(--muted);
  cursor: pointer; font-size: .8rem; padding: 0 .25rem;
}
.slot-remove:hover { color: var(--red); }
.conflict-badge {
  font-family: 'Gobold', monospace; font-size: .5rem;
  letter-spacing: .1em; color: #f59e0b; margin-right: .4rem;
}
.loadout-footer { padding: .75rem 1rem; border-top: 1px solid var(--border); flex-shrink: 0; }
.loadout-actions { display: flex; flex-direction: column; gap: .4rem; }
.featured-builds {
  border-top: 1px solid var(--border); padding: .5rem 1rem .75rem;
  flex-shrink: 0;
}
.featured-label {
  font-family: 'Gobold', monospace; font-size: .55rem;
  letter-spacing: .2em; color: var(--muted); margin-bottom: .35rem;
}
.featured-btn {
  display: block; width: 100%; text-align: left;
  background: none; border: 1px solid var(--border);
  color: var(--muted); font-family: 'FiraCode', monospace;
  font-size: .7rem; padding: .3rem .5rem;
  cursor: pointer; margin-bottom: .25rem;
}
.featured-btn:hover { border-color: var(--blue); color: var(--blue); }
</style>
</head>
<body class="theme-terminal density-compact">
<div class="launcher-shell">
  <div class="browser-panel">
    <div class="hero" style="min-height:140px">
      <div class="hero-content">
        <div class="eyebrow">LOADOUT BUILDER</div>
        <div class="hero-title" style="font-size:2rem">MOD ARCHIVE</div>
      </div>
    </div>
    <div class="controls" style="padding:.5rem 1rem">
      <input id="search" type="search" placeholder="Search mods…" autocomplete="off">
      <select id="sort" class="ctrl-select">
        <option value="downloads">↓ DOWNLOADS</option>
        <option value="name">NAME A→Z</option>
      </select>
      <span id="count"></span>
    </div>
    <div class="tabs" id="tabs"></div>
    <div class="archive-wrap" style="padding:.75rem 1rem 2rem">
      <div class="archive layout-list" id="archive"></div>
    </div>
  </div>

  <div class="loadout-panel">
    <div class="loadout-header">LOADOUT</div>
    <div class="loadout-sub" id="loadout-count">0 MODS ACTIVE</div>

    <div class="featured-builds">
      <div class="featured-label">FEATURED BUILDS</div>
      <button class="featured-btn" onclick="applyFeatured('completionist')">THE COMPLETIONIST</button>
      <button class="featured-btn" onclick="applyFeatured('ears-only')">EARS ONLY</button>
      <button class="featured-btn" onclick="applyFeatured('clean-ui')">CLEAN UI</button>
    </div>

    <div class="loadout-slots" id="loadout-slots"></div>

    <div class="loadout-footer">
      <div class="loadout-actions">
        <button class="btn btn-primary" onclick="applyLoadout()">⚡ APPLY LOADOUT</button>
        <button class="btn" onclick="exportLoadout()">↗ EXPORT JSON</button>
        <button class="btn" onclick="clearLoadout()">✕ CLEAR</button>
      </div>
    </div>
  </div>
</div>
<script src="../core/mods.js"></script>
<script src="../core/render.js"></script>
<script src="loadout.js"></script>
</body>
</html>
```

**Step 2: Create loadout.js**

```js
const CATS = ['All', ...new Set(MODS.map(m => m.category))];
let activeCat = 'All', query = '', sortBy = 'downloads';
let loadout = JSON.parse(localStorage.getItem('coh-loadout') || '[]');

const FEATURED = {
  'completionist': [9, 19, 20, 17, 11, 18, 16, 51, 110, 220],
  'ears-only':     MODS.filter(m => m.category === 'Audio')
                       .sort((a,b) => (b.downloads||0)-(a.downloads||0))
                       .slice(0,10).map(m => m.id),
  'clean-ui':      MODS.filter(m => ['GUI / Icons','Cursors'].includes(m.category))
                       .sort((a,b) => (b.downloads||0)-(a.downloads||0))
                       .slice(0,8).map(m => m.id),
};

function saveLoadout() {
  localStorage.setItem('coh-loadout', JSON.stringify(loadout));
}

function detectConflicts() {
  const catCounts = {};
  loadout.forEach(id => {
    const m = MODS.find(x => x.id === id);
    if (m) catCounts[m.category] = (catCounts[m.category] || 0) + 1;
  });
  return new Set(Object.entries(catCounts).filter(([,v]) => v > 2).map(([k]) => k));
}

function renderLoadout() {
  const conflicts = detectConflicts();
  const byCategory = {};
  loadout.forEach(id => {
    const m = MODS.find(x => x.id === id);
    if (!m) return;
    if (!byCategory[m.category]) byCategory[m.category] = [];
    byCategory[m.category].push(m);
  });

  const el = document.getElementById('loadout-slots');
  el.innerHTML = Object.entries(byCategory).map(([cat, mods]) => `
    <div class="slot-group">
      <div class="slot-label">${cat.toUpperCase()} (${mods.length})</div>
      ${mods.map(m => `
        <div class="slot-item${conflicts.has(m.category) ? ' conflict' : ''}">
          ${conflicts.has(m.category) ? '<span class="conflict-badge">⚠ CONFLICT</span>' : ''}
          <span class="slot-item-name">${m.name}</span>
          <button class="slot-remove" onclick="removeFromLoadout(${m.id})">✕</button>
        </div>`).join('')}
    </div>`).join('');

  document.getElementById('loadout-count').textContent = loadout.length + ' MODS ACTIVE';
}

function addToLoadout(id) {
  if (!loadout.includes(id)) {
    loadout.push(id);
    saveLoadout();
    renderLoadout();
    renderArchive();
  }
}

function removeFromLoadout(id) {
  loadout = loadout.filter(x => x !== id);
  saveLoadout();
  renderLoadout();
  renderArchive();
}

function clearLoadout() {
  loadout = [];
  saveLoadout();
  renderLoadout();
  renderArchive();
}

function applyFeatured(name) {
  loadout = [...FEATURED[name]];
  saveLoadout();
  renderLoadout();
  renderArchive();
}

function exportLoadout() {
  const data = loadout.map(id => MODS.find(m => m.id === id)).filter(Boolean);
  const blob = new Blob([JSON.stringify({loadout: data}, null, 2)], {type: 'application/json'});
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = 'coh-loadout.json';
  a.click();
}

function applyLoadout() {
  const urls = loadout.map(id => {
    const m = MODS.find(x => x.id === id);
    return m ? m.download_url : null;
  }).filter(Boolean);
  if (!urls.length) return alert('No mods in loadout.');
  if (confirm(`Download ${urls.length} mods now?`)) {
    urls.forEach((url, i) => setTimeout(() => window.open(url, '_blank'), i * 300));
  }
}

function makeLoadoutCard(m) {
  const card = makeCard(m);
  const actions = card.querySelector('.card-actions');
  const inLoadout = loadout.includes(m.id);
  const addBtn = document.createElement('button');
  addBtn.className = 'btn' + (inLoadout ? '' : ' btn-primary');
  addBtn.textContent = inLoadout ? '✓ IN LOADOUT' : '+ LOADOUT';
  if (inLoadout) addBtn.disabled = true;
  addBtn.addEventListener('click', e => { e.stopPropagation(); addToLoadout(m.id); });
  actions.prepend(addBtn);
  return card;
}

function renderArchive() {
  const el = document.getElementById('archive');
  let list = MODS.filter(m => {
    if (activeCat !== 'All' && m.category !== activeCat) return false;
    if (!query) return true;
    const q = query.toLowerCase();
    return (m.name || '').toLowerCase().includes(q)
      || (m.author || '').toLowerCase().includes(q);
  }).sort((a, b) => sortBy === 'name'
    ? (a.name || '').localeCompare(b.name || '')
    : (b.downloads || 0) - (a.downloads || 0));

  document.getElementById('count').textContent = list.length + ' mods';
  el.innerHTML = '';
  list.forEach(m => el.appendChild(makeLoadoutCard(m)));
}

document.getElementById('search').addEventListener('input', e => { query = e.target.value; renderArchive(); });
document.getElementById('sort').addEventListener('change', e => { sortBy = e.target.value; renderArchive(); });

renderTabs(document.getElementById('tabs'), CATS, activeCat, cat => {
  activeCat = cat;
  renderTabs(document.getElementById('tabs'), CATS, activeCat, arguments.callee);
  renderArchive();
});

renderLoadout();
renderArchive();
```

**Step 3: Verify**

Open `d-launcher/index.html`. Expected:
- Left: compact mod list with `+ LOADOUT` buttons
- Right panel: empty loadout
- Click `+ LOADOUT` on a mod → it appears in the right panel under its category
- Click `THE COMPLETIONIST` → right panel fills with curated mods
- Click `EXPORT JSON` → downloads `coh-loadout.json`

**Step 4: Commit**
```bash
git add Upgraded/d-launcher/
git commit -m "feat: build D loadout launcher with conflict detection and featured builds"
```

---

## Phase 4: Build C — Electron

---

### Task 4.1: Scaffold c-electron/ package and main process

**Objective:** Electron app that wraps a-static with native filesystem access.

**Files:**
- Create: `Upgraded/c-electron/package.json`
- Create: `Upgraded/c-electron/main.js`
- Create: `Upgraded/c-electron/preload.js`
- Create: `Upgraded/c-electron/index.html` (copy of a-static with electronAPI calls)

**Step 1: Create package.json**
```json
{
  "name": "cox-mod-archive",
  "version": "1.0.0",
  "description": "CoX Mod Archive — native desktop app",
  "main": "main.js",
  "scripts": {
    "start": "electron ."
  },
  "devDependencies": {
    "electron": "^31.0.0"
  }
}
```

**Step 2: Create main.js**
```js
const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
const fs = require('fs');
const https = require('https');
const http = require('http');

const COH_DATA = '/Applications/coh/data';

function createWindow() {
  const win = new BrowserWindow({
    width: 1400, height: 900,
    title: 'CoX Mod Archive',
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
    },
  });
  win.loadFile('index.html');
}

ipcMain.handle('get-installed', () => {
  if (!fs.existsSync(COH_DATA)) return [];
  return fs.readdirSync(COH_DATA)
    .filter(f => f.endsWith('.pigg'))
    .map(f => path.basename(f, '.pigg'));
});

ipcMain.handle('install-mod', async (_, { url, id }) => {
  return new Promise((resolve) => {
    const fname = url.split('file=').pop().split('/').pop();
    const dest = fs.existsSync(COH_DATA)
      ? path.join(COH_DATA, fname)
      : path.join(__dirname, 'downloads', fname);
    fs.mkdirSync(path.dirname(dest), { recursive: true });
    const file = fs.createWriteStream(dest);
    const get = url.startsWith('https') ? https : http;
    get.get(url, res => {
      res.pipe(file);
      file.on('finish', () => file.close(() => resolve({ ok: true, path: dest, id })));
    }).on('error', e => resolve({ ok: false, error: e.message }));
  });
});

app.whenReady().then(createWindow);
app.on('window-all-closed', () => { if (process.platform !== 'darwin') app.quit(); });
```

**Step 3: Create preload.js**
```js
const { contextBridge, ipcRenderer } = require('electron');
contextBridge.exposeInMainWorld('electronAPI', {
  getInstalled: () => ipcRenderer.invoke('get-installed'),
  installMod: (url, id) => ipcRenderer.invoke('install-mod', { url, id }),
});
```

**Step 4: Create index.html**

Copy `a-static/index.html`. Change the `<script>` at the bottom to add a `<script src="electron-app.js"></script>` that wraps the install logic with `window.electronAPI.installMod()` calls instead of direct download links.

**Step 5: Install and run**
```bash
cd Upgraded/c-electron
npm install
npm start
```
Expected: Native window opens showing the CoX Mod Archive.

**Step 6: Commit**
```bash
git add Upgraded/c-electron/
git commit -m "feat: build C electron app with native install via ipc"
```

---

## Final Verification

```bash
# Confirm all four builds exist
ls Upgraded/a-static/ Upgraded/b-server/ Upgraded/c-electron/ Upgraded/d-launcher/
# Confirm core is shared
ls Upgraded/core/
```

Expected output: all four build folders + core/ with mods.js, render.js, style.css.

```bash
git log --oneline -8
```

Expected: 8 commits covering core extraction + all four builds.
