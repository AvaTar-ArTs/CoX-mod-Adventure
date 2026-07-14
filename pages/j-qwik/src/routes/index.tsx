import { component$, useSignal, useComputed$ } from '@builder.io/qwik'
import type { DocumentHead } from '@builder.io/qwik-city'
import rawMods from '../../mods.json'

const ART_BASE = 'file:///Users/steven/Pictures/CoH-ComicArt/'
const ART_MAP: Record<string,string> = {
  'Audio':'TerraVolta.jpeg','Graphics':'KingsRow.jpeg','GUI / Icons':'IndepPort.jpeg',
  'Popmenus':'PerezPark.jpeg','Maps':'AncientCity.jpeg','Cursors':'FutureCity.jpeg',
  'Languages':'TimeCityscape.jpeg','Other':'CityscapeView.jpeg',
}
const BADGE: Record<string,string> = {
  'Audio':'badge-audio','Graphics':'badge-graphics','GUI / Icons':'badge-gui',
  'Popmenus':'badge-popmenu','Maps':'badge-maps','Cursors':'badge-cursors',
}
const MODS = rawMods.map((m: any) => ({ ...m, art: ART_BASE + (ART_MAP[m.category] ?? 'CityscapeView.jpeg') }))
const CATS = ['All', ...new Set(MODS.map((m: any) => m.category as string))]

function fmtDl(n: number) { return n >= 1000 ? (n/1000).toFixed(1)+'k' : String(n) }

// component$ marks this as a resumable Qwik component
export default component$(() => {
  // useSignal: like useState but serializable across server/client boundary
  const cat   = useSignal('All')
  const query = useSignal('')
  const sort  = useSignal('downloads')
  const active = useSignal<any>(null)

  // useComputed$: reactive memo, auto-tracks signals read inside
  const visible = useComputed$(() => {
    const q = query.value.toLowerCase()
    return MODS
      .filter((m: any) => {
        if (cat.value !== 'All' && m.category !== cat.value) return false
        if (!q) return true
        return m.name.toLowerCase().includes(q)
          || (m.author || '').toLowerCase().includes(q)
          || (m.description || '').toLowerCase().includes(q)
      })
      .sort((a: any, b: any) => {
        if (sort.value === 'downloads') return (b.downloads||0) - (a.downloads||0)
        if (sort.value === 'name')     return a.name.localeCompare(b.name)
        return (a.author||'').localeCompare(b.author||'')
      })
  })

  return (
    <>
      <div class="hero">
        <div class="hero-content">
          <div class="eyebrow">City of Heroes · Homecoming</div>
          <div class="hero-title">MOD ARCHIVE</div>
          <div class="hero-sub">{MODS.length} MODS · QWIK</div>
        </div>
      </div>

      <div class="controls">
        <input type="search" placeholder="Search mods, authors…"
          onInput$={e => query.value = (e.target as HTMLInputElement).value} />
        <select onChange$={e => sort.value = (e.target as HTMLSelectElement).value}>
          <option value="downloads">Sort: Downloads</option>
          <option value="name">Sort: Name A→Z</option>
          <option value="author">Sort: Author</option>
        </select>
        <span class="count">{visible.value.length} mods</span>
      </div>

      <div class="tabs">
        {CATS.map(c => (
          <button key={c} class={`tab ${c === cat.value ? 'active' : ''}`}
            onClick$={() => cat.value = c}>{c}</button>
        ))}
      </div>

      <div class="archive">
        {visible.value.map((mod: any) => (
          <div key={mod.id} class="card" onClick$={() => active.value = mod}>
            <span class={`badge ${BADGE[mod.category] ?? 'badge-other'}`}>{mod.category}</span>
            <div class="card-name">{mod.name}</div>
            <div class="card-meta">
              <span>{mod.author || 'Unknown'}</span>
              <span class="card-dl">↓ {fmtDl(mod.downloads)}</span>
            </div>
            {mod.description && <p class="card-desc">{mod.description}</p>}
            <div class="card-actions">
              <a class="btn btn-primary" href={mod.download_url} target="_blank"
                 onClick$={e => e.stopPropagation()}>Download</a>
              <a class="btn" href={mod.page_url} target="_blank"
                 onClick$={e => e.stopPropagation()}>Info</a>
            </div>
          </div>
        ))}
      </div>

      {/* Drawer */}
      <div class={`overlay ${active.value ? 'open' : ''}`}
        onClick$={() => active.value = null} />
      <aside class={`drawer ${active.value ? 'open' : ''}`}>
        <button class="drawer-close" onClick$={() => active.value = null}>✕ CLOSE</button>
        {active.value && <>
          <span class={`drawer-badge ${BADGE[active.value.category] ?? 'badge-other'}`}>
            {active.value.category}
          </span>
          <div class="drawer-name">{active.value.name}</div>
          <div class="drawer-author">BY {active.value.author || 'Unknown'}</div>
          <div class="drawer-thumb" style={`background-image:url('${active.value.art}')`} />
          <div class="drawer-dl">↓ {fmtDl(active.value.downloads)} downloads</div>
          <p class="drawer-desc">{active.value.description || 'No description.'}</p>
          <div class="drawer-actions">
            <a class="btn btn-primary" href={active.value.download_url} target="_blank">Download</a>
            <a class="btn" href={active.value.page_url} target="_blank">Mod Page</a>
          </div>
        </>}
      </aside>
    </>
  )
})

export const head: DocumentHead = { title: 'CoX Mod Archive · Qwik' }
