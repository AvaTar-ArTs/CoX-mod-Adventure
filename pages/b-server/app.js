// ── State
const CATS = ['All', ...new Set(MODS.map(m => m.category))];
let activeCat = 'All', query = '', sortBy = 'downloads';
const installed = new Set();

// ── Fetch installed mods from server
async function fetchInstalled() {
  try {
    const r = await fetch('/api/installed');
    const list = await r.json();
    list.forEach(id => installed.add(id));
    const el = document.getElementById('installed-count');
    if (el) el.textContent = installed.size + ' INSTALLED';
  } catch (_) {}
}

// ── Card with server install button
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
    try {
      const res = await fetch('/api/install', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id: m.id, download_url: m.download_url }),
      });
      const json = await res.json();
      if (json.ok) {
        installBtn.textContent = '✓ INSTALLED';
        installed.add(String(m.id));
        const ct = document.getElementById('installed-count');
        if (ct) ct.textContent = installed.size + ' INSTALLED';
      } else {
        installBtn.textContent = 'ERROR';
        installBtn.disabled = false;
        console.error('Install failed:', json.error);
      }
    } catch (err) {
      installBtn.textContent = 'ERROR';
      installBtn.disabled = false;
      console.error(err);
    }
  });

  // Replace first btn (DOWNLOAD) with INSTALL, keep INFO
  const firstBtn = actions.querySelector('a');
  if (firstBtn) actions.replaceChild(installBtn, firstBtn);
  else actions.prepend(installBtn);

  return card;
}

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
  list.forEach(m => el.appendChild(makeServerCard(m)));
}

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

// ── p5 ambient (shared logic, same as a-static)
const _amb = { streaks: [], pulses: [], t: 0, origin: null };
function drawAmbient(p) {
  if (!_amb.origin) _amb.origin = { x: p.width * 0.38, y: p.height * 0.55 };
  p.noStroke(); p.fill(5, 5, 15, 18); p.rect(0, 0, p.width, p.height);
  _amb.t += 0.004;
  if (_amb.streaks.length < 18 && p.random() < 0.25) {
    _amb.streaks.push({ x: p.random(p.width), y: p.random(p.height),
      len: p.random(40, 180), speed: p.random(0.15, 0.55), alpha: p.random(30, 80) });
  }
  for (let i = _amb.streaks.length - 1; i >= 0; i--) {
    const s = _amb.streaks[i];
    s.y -= s.speed; s.alpha -= 0.4;
    if (s.alpha <= 0) { _amb.streaks.splice(i, 1); continue; }
    p.stroke(245, 158, 11, s.alpha); p.strokeWeight(0.7);
    p.line(s.x, s.y, s.x + s.len, s.y);
  }
  if (p.frameCount % 55 === 0) _amb.pulses.push({ r: 0, alpha: 60 });
  for (let i = _amb.pulses.length - 1; i >= 0; i--) {
    const pu = _amb.pulses[i];
    pu.r += 3.2; pu.alpha -= 1.1;
    if (pu.alpha <= 0) { _amb.pulses.splice(i, 1); continue; }
    p.noFill(); p.stroke(56, 189, 248, pu.alpha); p.strokeWeight(1);
    p.ellipse(_amb.origin.x, _amb.origin.y, pu.r * 2, pu.r * 2);
  }
  p.noStroke();
}
new p5(function(p) {
  p.setup = function() {
    const c = p.createCanvas(window.innerWidth, window.innerHeight);
    c.parent('p5-canvas'); c.style('width','100%'); c.style('height','100%');
    p.background(5, 5, 15); p.frameRate(30);
  };
  p.draw = function() { drawAmbient(p); };
  p.windowResized = function() { _amb.origin = null; p.resizeCanvas(window.innerWidth, window.innerHeight); };
});

// ── Init
renderBento(document.getElementById('bento'));
renderTabs(document.getElementById('tabs'), CATS, activeCat, onTabClick);
fetchInstalled().then(() => renderArchive());
