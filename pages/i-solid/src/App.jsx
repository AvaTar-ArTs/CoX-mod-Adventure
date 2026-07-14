import { createSignal, createMemo, onCleanup } from 'solid-js'
import { For, Show } from 'solid-js'
import { MODS, CATS, BADGE, fmtDl } from './mods.js'
import './theme.css'

export default function App() {
  // createSignal: getter/setter pair — [read, write]
  const [cat, setCat]     = createSignal('All')
  const [query, setQuery] = createSignal('')
  const [sort, setSort]   = createSignal('downloads')
  const [active, setActive] = createSignal(null)

  // createMemo: auto-tracks signals read inside — no dependency array needed
  const visible = createMemo(() => {
    const q = query().toLowerCase()
    return MODS
      .filter(m => {
        if (cat() !== 'All' && m.category !== cat()) return false
        if (!q) return true
        return m.name.toLowerCase().includes(q)
          || (m.author || '').toLowerCase().includes(q)
          || (m.description || '').toLowerCase().includes(q)
      })
      .sort((a, b) => {
        if (sort() === 'downloads') return (b.downloads || 0) - (a.downloads || 0)
        if (sort() === 'name')     return a.name.localeCompare(b.name)
        return (a.author || '').localeCompare(b.author || '')
      })
  })

  const onKey = e => { if (e.key === 'Escape') setActive(null) }
  window.addEventListener('keydown', onKey)
  onCleanup(() => window.removeEventListener('keydown', onKey))

  return (
    <>
      <div class="hero">
        <div class="hero-content">
          <div class="eyebrow">City of Heroes · Homecoming</div>
          <div class="hero-title">MOD ARCHIVE</div>
          <div class="hero-sub">{MODS.length} MODS · SOLID.JS</div>
        </div>
      </div>

      <div class="controls">
        <input type="search" placeholder="Search mods, authors…"
          onInput={e => setQuery(e.target.value)} />
        <select onChange={e => setSort(e.target.value)}>
          <option value="downloads">Sort: Downloads</option>
          <option value="name">Sort: Name A→Z</option>
          <option value="author">Sort: Author</option>
        </select>
        <span class="count">{visible().length} mods</span>
      </div>

      <div class="tabs">
        <For each={CATS}>
          {c => (
            <button class={`tab ${c === cat() ? 'active' : ''}`} onClick={() => setCat(c)}>
              {c}
            </button>
          )}
        </For>
      </div>

      <div class="archive">
        {/* <For> is Solid's list renderer — keyed, minimal DOM ops */}
        <For each={visible()}>
          {mod => (
            <div class="card" onClick={() => setActive(mod)}>
              <span class={`badge ${BADGE[mod.category] ?? 'badge-other'}`}>{mod.category}</span>
              <div class="card-name">{mod.name}</div>
              <div class="card-meta">
                <span>{mod.author || 'Unknown'}</span>
                <span class="card-dl">↓ {fmtDl(mod.downloads)}</span>
              </div>
              <Show when={mod.description}>
                <p class="card-desc">{mod.description}</p>
              </Show>
              <div class="card-actions">
                <a class="btn btn-primary" href={mod.download_url} target="_blank"
                   onClick={e => e.stopPropagation()}>Download</a>
                <a class="btn" href={mod.page_url} target="_blank"
                   onClick={e => e.stopPropagation()}>Info</a>
              </div>
            </div>
          )}
        </For>
      </div>

      {/* Drawer */}
      <div class={`overlay ${active() ? 'open' : ''}`} onClick={() => setActive(null)} />
      <aside class={`drawer ${active() ? 'open' : ''}`}>
        <button class="drawer-close" onClick={() => setActive(null)}>✕ CLOSE</button>
        <Show when={active()}>
          {mod => <>
            <span class={`drawer-badge ${BADGE[mod().category] ?? 'badge-other'}`}>{mod().category}</span>
            <div class="drawer-name">{mod().name}</div>
            <div class="drawer-author">BY {mod().author || 'Unknown'}</div>
            <div class="drawer-thumb" style={`background-image:url('${mod().art}')`} />
            <div class="drawer-dl">↓ {fmtDl(mod().downloads)} downloads</div>
            <p class="drawer-desc">{mod().description || 'No description available.'}</p>
            <div class="drawer-actions">
              <a class="btn btn-primary" href={mod().download_url} target="_blank">Download</a>
              <a class="btn" href={mod().page_url} target="_blank">Mod Page</a>
            </div>
          </>}
        </Show>
      </aside>
    </>
  )
}
