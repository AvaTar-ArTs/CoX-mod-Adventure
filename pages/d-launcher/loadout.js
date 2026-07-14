// ── Featured build definitions
const FEATURED = {
  'completionist': [9, 19, 20, 17, 205, 11, 18, 16, 51, 110, 220],
  'ears-only': MODS
    .filter(m => m.category === 'Audio')
    .sort((a, b) => (b.downloads || 0) - (a.downloads || 0))
    .slice(0, 10).map(m => m.id),
  'clean-ui': MODS
    .filter(m => ['GUI / Icons', 'Cursors'].includes(m.category))
    .sort((a, b) => (b.downloads || 0) - (a.downloads || 0))
    .slice(0, 8).map(m => m.id),
};

// ── State
const CATS = ['All', ...new Set(MODS.map(m => m.category))];
let activeCat = 'All', query = '', sortBy = 'downloads';
let loadout = JSON.parse(localStorage.getItem('coh-loadout') || '[]');

// ── Persist
function saveLoadout() {
  localStorage.setItem('coh-loadout', JSON.stringify(loadout));
}

// ── Conflict detection: >2 mods in the same category = warn
function conflictedCategories() {
  const counts = {};
  loadout.forEach(id => {
    const m = MODS.find(x => x.id === id);
    if (m) counts[m.category] = (counts[m.category] || 0) + 1;
  });
  return new Set(Object.entries(counts).filter(([, v]) => v > 2).map(([k]) => k));
}

// ── Render loadout panel
function renderLoadout() {
  const conflicts = conflictedCategories();
  const byCategory = {};
  loadout.forEach(id => {
    const m = MODS.find(x => x.id === id);
    if (!m) return;
    (byCategory[m.category] = byCategory[m.category] || []).push(m);
  });

  const el = document.getElementById('loadout-slots');
  if (!loadout.length) {
    el.innerHTML = `<div style="padding:1.5rem 0;font-family:'FiraCode',monospace;font-size:.72rem;color:var(--muted);text-align:center;">ADD MODS FROM THE LEFT PANEL</div>`;
    document.getElementById('loadout-count').textContent = '0 MODS ACTIVE';
    return;
  }

  el.innerHTML = Object.entries(byCategory).map(([cat, mods]) => `
    <div class="slot-group">
      <div class="slot-label">${cat.toUpperCase()} · ${mods.length} MOD${mods.length > 1 ? 'S' : ''}${conflicts.has(cat) ? ' ⚠' : ''}</div>
      ${mods.map(m => `
        <div class="slot-item${conflicts.has(cat) ? ' conflict' : ''}">
          ${conflicts.has(cat) ? '<span class="conflict-badge">CONFLICT</span>' : ''}
          <span class="slot-item-name">${m.name}</span>
          <button class="slot-remove" title="Remove" onclick="removeFromLoadout(${m.id})">✕</button>
        </div>`).join('')}
    </div>`).join('');

  document.getElementById('loadout-count').textContent =
    `${loadout.length} MOD${loadout.length !== 1 ? 'S' : ''} ACTIVE`;
}

// ── Loadout mutations
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
  if (!loadout.length) return;
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
  const blob = new Blob(
    [JSON.stringify({ version: 1, count: data.length, loadout: data }, null, 2)],
    { type: 'application/json' }
  );
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = 'coh-loadout.json';
  a.click();
  URL.revokeObjectURL(a.href);
}

function applyLoadout() {
  if (!loadout.length) {
    alert('No mods in your loadout yet.');
    return;
  }
  const urls = loadout
    .map(id => MODS.find(m => m.id === id))
    .filter(Boolean)
    .map(m => m.download_url);

  if (!confirm(`Download ${urls.length} mod${urls.length !== 1 ? 's' : ''} now?\n\nThis will open each download in a new tab.`)) return;
  urls.forEach((url, i) => setTimeout(() => window.open(url, '_blank'), i * 350));
}

// ── Card with loadout button
function makeLoadoutCard(m) {
  const card = makeCard(m);
  const actions = card.querySelector('.card-actions');
  const inLoadout = loadout.includes(m.id);

  const addBtn = document.createElement('button');
  addBtn.className = 'btn add-btn' + (inLoadout ? '' : ' btn-primary');
  addBtn.textContent = inLoadout ? '✓ IN LOADOUT' : '+ LOADOUT';
  addBtn.disabled = inLoadout;

  addBtn.addEventListener('click', e => {
    e.stopPropagation();
    addToLoadout(m.id);
  });

  actions.prepend(addBtn);
  return card;
}

// ── Archive render
function renderArchive() {
  const el = document.getElementById('archive');
  let list = MODS.filter(m => {
    if (activeCat !== 'All' && m.category !== activeCat) return false;
    if (!query) return true;
    const q = query.toLowerCase();
    return (m.name || '').toLowerCase().includes(q)
      || (m.author || '').toLowerCase().includes(q);
  }).sort((a, b) =>
    sortBy === 'name'
      ? (a.name || '').localeCompare(b.name || '')
      : (b.downloads || 0) - (a.downloads || 0)
  );

  document.getElementById('count').textContent = list.length + ' mods';
  el.innerHTML = '';
  if (!list.length) {
    el.innerHTML = '<div class="empty">NO MODS MATCH · ADJUST FILTERS</div>';
    return;
  }
  list.forEach(m => el.appendChild(makeLoadoutCard(m)));
}

function onTabClick(cat) {
  activeCat = cat;
  renderTabs(document.getElementById('tabs'), CATS, activeCat, onTabClick);
  renderArchive();
}

// ── Controls
document.getElementById('search').addEventListener('input', e => { query = e.target.value; renderArchive(); });
document.getElementById('sort').addEventListener('change', e => { sortBy = e.target.value; renderArchive(); });

// ── Init
renderTabs(document.getElementById('tabs'), CATS, activeCat, onTabClick);
renderLoadout();
renderArchive();
