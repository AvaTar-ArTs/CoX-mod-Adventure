// ── State
const CATS = ['All', ...new Set(MODS.map(m => m.category))];
let activeCat = 'All', query = '', sortBy = 'downloads';

// ── Archive render
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

  if (!list.length) {
    el.innerHTML = '<div class="empty">NO MODS MATCH · ADJUST FILTERS</div>';
    return;
  }
  list.forEach(m => {
    const card = makeCard(m);
    card.addEventListener('click', e => {
      if (!e.target.closest('a')) openDrawer(m);
    });
    el.appendChild(card);
  });
}

// ── Tab handler (named fn — avoids arguments.callee in strict mode)
function onTabClick(cat) {
  activeCat = cat;
  renderTabs(document.getElementById('tabs'), CATS, activeCat, onTabClick);
  renderArchive();
}

// ── Controls
document.getElementById('search').addEventListener('input', e => { query = e.target.value; renderArchive(); });
document.getElementById('sort').addEventListener('change', e => { sortBy = e.target.value; renderArchive(); });
document.getElementById('layout').addEventListener('change', () => renderArchive());
document.getElementById('density').addEventListener('change', e => {
  document.body.className = document.body.className.replace(/density-\S+/, '') + ' density-' + e.target.value;
});
document.getElementById('theme').addEventListener('change', e => {
  document.body.className = document.body.className.replace(/theme-\S+/, '') + ' theme-' + e.target.value;
});

// ── Detail drawer
function openDrawer(m) {
  const dCat = document.getElementById('dCat');
  dCat.textContent = m.category.toUpperCase();
  dCat.className = `drawer-cat ${badgeClass(m.category)}`;
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
document.addEventListener('keydown', e => { if (e.key === 'Escape') closeDrawer(); });

// ── p5 ambient canvas (city energy + pulse rings)
const _amb = { streaks: [], pulses: [], t: 0, origin: null };

function drawAmbient(p) {
  if (!_amb.origin) _amb.origin = { x: p.width * 0.38, y: p.height * 0.55 };
  p.noStroke();
  p.fill(5, 5, 15, 18);
  p.rect(0, 0, p.width, p.height);
  _amb.t += 0.004;

  if (_amb.streaks.length < 18 && p.random() < 0.25) {
    _amb.streaks.push({ x: p.random(p.width), y: p.random(p.height),
      len: p.random(40, 180), speed: p.random(0.15, 0.55), alpha: p.random(30, 80) });
  }
  for (let i = _amb.streaks.length - 1; i >= 0; i--) {
    const s = _amb.streaks[i];
    s.y -= s.speed; s.alpha -= 0.4;
    if (s.alpha <= 0) { _amb.streaks.splice(i, 1); continue; }
    p.stroke(245, 158, 11, s.alpha);
    p.strokeWeight(0.7);
    p.line(s.x, s.y, s.x + s.len, s.y);
  }

  if (p.frameCount % 55 === 0) _amb.pulses.push({ r: 0, alpha: 60 });
  for (let i = _amb.pulses.length - 1; i >= 0; i--) {
    const pu = _amb.pulses[i];
    pu.r += 3.2; pu.alpha -= 1.1;
    if (pu.alpha <= 0) { _amb.pulses.splice(i, 1); continue; }
    p.noFill();
    p.stroke(56, 189, 248, pu.alpha);
    p.strokeWeight(1);
    p.ellipse(_amb.origin.x, _amb.origin.y, pu.r * 2, pu.r * 2);
  }
  p.noStroke();
}

new p5(function(p) {
  p.setup = function() {
    const canvas = p.createCanvas(window.innerWidth, window.innerHeight);
    canvas.parent('p5-canvas');
    canvas.style('width', '100%');
    canvas.style('height', '100%');
    p.background(5, 5, 15);
    p.frameRate(30);
  };
  p.draw = function() { drawAmbient(p); };
  p.windowResized = function() {
    _amb.origin = null;
    p.resizeCanvas(window.innerWidth, window.innerHeight);
  };
});

// ── Init
renderBento(document.getElementById('bento'));
renderTabs(document.getElementById('tabs'), CATS, activeCat, onTabClick);
renderArchive();
