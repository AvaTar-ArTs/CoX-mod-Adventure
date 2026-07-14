// Tauri v2: window.__TAURI__.core.invoke() replaces Electron's ipcRenderer
// Falls back to window.open() when running in a plain browser
const tauriInvoke = window.__TAURI__?.core?.invoke ?? null

const CATS = ['All', ...new Set(MODS.map(m => m.category))]
let activeCat = 'All', query = '', sortBy = 'downloads'
const installed = new Set()

async function loadInstalled() {
  if (!tauriInvoke) return
  try {
    const list = await tauriInvoke('get_installed')  // snake_case — Tauri convention
    list.forEach(s => installed.add(s))
    const badge = document.getElementById('installed-badge')
    if (badge) badge.textContent = installed.size + ' INSTALLED'
  } catch (_) {}
}

function makeTauriCard(m) {
  const card = makeCard(m)
  const actions = card.querySelector('.card-actions')
  const btn = document.createElement('button')
  btn.className = 'btn btn-primary install-btn'
  const fname = (m.download_url.split('file=').pop() || '').split('/').pop()
  const isIn  = installed.has(fname.replace('.pigg',''))
  btn.textContent = isIn ? '✓ INSTALLED' : 'INSTALL'
  if (isIn) { btn.disabled = true; btn.classList.add('done') }

  btn.addEventListener('click', async e => {
    e.stopPropagation()
    if (!tauriInvoke) { window.open(m.download_url, '_blank'); return }
    btn.textContent = 'INSTALLING…'; btn.disabled = true
    const result = await tauriInvoke('install_mod', { url: m.download_url, id: m.id })
    if (result.ok) {
      btn.textContent = '✓ INSTALLED'; btn.classList.add('done')
      installed.add(fname.replace('.pigg',''))
      const badge = document.getElementById('installed-badge')
      if (badge) badge.textContent = installed.size + ' INSTALLED'
      const dPath = document.getElementById('dPath')
      if (dPath && document.getElementById('drawer').classList.contains('open'))
        dPath.textContent = '→ ' + result.path
    } else {
      btn.textContent = 'ERROR'; btn.disabled = false
    }
  })

  const first = actions.querySelector('a')
  if (first) actions.replaceChild(btn, first); else actions.prepend(btn)
  return card
}

function renderArchive() {
  const layout = document.getElementById('layout').value
  const el = document.getElementById('archive')
  el.className = `archive layout-${layout}`
  let list = MODS.filter(m => {
    if (activeCat !== 'All' && m.category !== activeCat) return false
    if (!query) return true
    const q = query.toLowerCase()
    return m.name.toLowerCase().includes(q)
      || (m.author||'').toLowerCase().includes(q)
      || (m.description||'').toLowerCase().includes(q)
  }).sort((a,b) => {
    if (sortBy === 'downloads') return (b.downloads||0) - (a.downloads||0)
    if (sortBy === 'name')      return a.name.localeCompare(b.name)
    return (a.author||'').localeCompare(b.author||'')
  })
  document.getElementById('count').textContent = list.length + ' mods'
  el.innerHTML = ''
  list.forEach(m => {
    const card = makeTauriCard(m)
    card.addEventListener('click', e => { if (!e.target.closest('a,button')) openDrawer(m) })
    el.appendChild(card)
  })
}

function onTabClick(cat) {
  activeCat = cat
  renderTabs(document.getElementById('tabs'), CATS, activeCat, onTabClick)
  renderArchive()
}

document.getElementById('search').addEventListener('input', e => { query = e.target.value; renderArchive() })
document.getElementById('sort').addEventListener('change', e => { sortBy = e.target.value; renderArchive() })
document.getElementById('layout').addEventListener('change', renderArchive)

function openDrawer(m) {
  const dCat = document.getElementById('dCat')
  dCat.textContent = m.category.toUpperCase()
  dCat.className = `drawer-cat ${badgeClass(m.category)}`
  document.getElementById('dName').textContent = m.name
  document.getElementById('dAuthor').textContent = 'BY ' + (m.author || 'Unknown')
  document.getElementById('dThumb').style.backgroundImage = `url('${ART_BASE}${m.art}')`
  document.getElementById('dDl').textContent = '↓ ' + fmtDl(m.downloads) + ' downloads'
  document.getElementById('dDesc').textContent = m.description || 'No description.'
  document.getElementById('dPath').textContent = ''
  document.getElementById('dActions').innerHTML =
    `<a class="btn" href="${m.page_url}" target="_blank">MOD PAGE</a>`
  document.getElementById('drawer').classList.add('open')
  document.getElementById('overlay').classList.add('open')
}
function closeDrawer() {
  document.getElementById('drawer').classList.remove('open')
  document.getElementById('overlay').classList.remove('open')
}
document.getElementById('drawerClose').addEventListener('click', closeDrawer)
document.getElementById('overlay').addEventListener('click', closeDrawer)
document.addEventListener('keydown', e => { if (e.key === 'Escape') closeDrawer() })

// p5 ambient (same as c-electron)
const _amb = { streaks:[], pulses:[], t:0, origin:null }
function drawAmbient(p) {
  if (!_amb.origin) _amb.origin = { x: p.width*.38, y: p.height*.55 }
  p.noStroke(); p.fill(5,5,15,18); p.rect(0,0,p.width,p.height)
  _amb.t += 0.004
  if (_amb.streaks.length < 18 && p.random() < 0.25)
    _amb.streaks.push({ x:p.random(p.width), y:p.random(p.height), len:p.random(40,180), speed:p.random(.15,.55), alpha:p.random(30,80) })
  for (let i=_amb.streaks.length-1;i>=0;i--) {
    const s=_amb.streaks[i]; s.y-=s.speed; s.alpha-=0.4
    if (s.alpha<=0){_amb.streaks.splice(i,1);continue}
    p.stroke(245,158,11,s.alpha); p.strokeWeight(.7); p.line(s.x,s.y,s.x+s.len,s.y)
  }
  if (p.frameCount%55===0) _amb.pulses.push({r:0,alpha:60})
  for (let i=_amb.pulses.length-1;i>=0;i--) {
    const pu=_amb.pulses[i]; pu.r+=3.2; pu.alpha-=1.1
    if (pu.alpha<=0){_amb.pulses.splice(i,1);continue}
    p.noFill(); p.stroke(56,189,248,pu.alpha); p.strokeWeight(1)
    p.ellipse(_amb.origin.x,_amb.origin.y,pu.r*2,pu.r*2)
  }
  p.noStroke()
}
new p5(function(p) {
  p.setup = function() {
    const c=p.createCanvas(window.innerWidth,window.innerHeight)
    c.parent('p5-canvas'); c.style('width','100%'); c.style('height','100%')
    p.background(5,5,15); p.frameRate(30)
  }
  p.draw = function() { drawAmbient(p) }
  p.windowResized = function() { _amb.origin=null; p.resizeCanvas(window.innerWidth,window.innerHeight) }
})

renderBento(document.getElementById('bento'))
renderTabs(document.getElementById('tabs'), CATS, activeCat, onTabClick)
loadInstalled().then(() => renderArchive())
