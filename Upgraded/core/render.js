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
