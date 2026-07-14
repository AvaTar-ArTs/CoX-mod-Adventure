import { useState, useMemo, useCallback, useEffect } from 'react'
import { MODS, CATS } from './mods.js'
import ModCard from './components/ModCard.jsx'
import ModDrawer from './components/ModDrawer.jsx'
import './theme.css'

export default function App() {
  const [cat, setCat]     = useState('All')
  const [query, setQuery] = useState('')
  const [sort, setSort]   = useState('downloads')
  const [active, setActive] = useState(null)   // mod open in drawer

  // Close drawer on Escape
  useEffect(() => {
    const fn = e => { if (e.key === 'Escape') setActive(null) }
    window.addEventListener('keydown', fn)
    return () => window.removeEventListener('keydown', fn)
  }, [])

  // TODO(human): implement filterAndSort
  // useMemo re-runs ONLY when its dependency array changes — not on every render.
  // Return the filtered + sorted subset of MODS based on cat, query, and sort.
  // MODS is the full 291-item array imported above.
  const visible = useMemo(() => filterAndSort(MODS, cat, query, sort), [cat, query, sort])

  const onTabClick = useCallback(c => setCat(c), [])

  return (
    <>
      <div className="hero">
        <div className="hero-content">
          <div className="eyebrow">City of Heroes · Homecoming</div>
          <div className="hero-title">MOD ARCHIVE</div>
          <div className="hero-sub">{MODS.length} MODS · REACT + VITE</div>
        </div>
      </div>

      <div className="controls">
        <input
          type="search"
          placeholder="Search mods, authors…"
          value={query}
          onChange={e => setQuery(e.target.value)}
        />
        <select value={sort} onChange={e => setSort(e.target.value)}>
          <option value="downloads">Sort: Downloads</option>
          <option value="name">Sort: Name A→Z</option>
          <option value="author">Sort: Author</option>
        </select>
        <span className="count">{visible.length} mods</span>
      </div>

      <div className="tabs">
        {CATS.map(c => (
          <button
            key={c}
            className={`tab ${c === cat ? 'active' : ''}`}
            onClick={() => onTabClick(c)}
          >
            {c}
          </button>
        ))}
      </div>

      <div className="archive">
        {visible.map(m => (
          <ModCard key={m.id} mod={m} onClick={setActive} />
        ))}
      </div>

      <ModDrawer mod={active} onClose={() => setActive(null)} />
    </>
  )
}

function filterAndSort(mods, cat, query, sort) {
  const q = query.toLowerCase()
  return mods
    .filter(m => {
      if (cat !== 'All' && m.category !== cat) return false
      if (!q) return true
      return m.name.toLowerCase().includes(q)
        || (m.author || '').toLowerCase().includes(q)
        || (m.description || '').toLowerCase().includes(q)
    })
    .sort((a, b) => {
      if (sort === 'downloads') return (b.downloads || 0) - (a.downloads || 0)
      if (sort === 'name')      return a.name.localeCompare(b.name)
      return (a.author || '').localeCompare(b.author || '')
    })
}
