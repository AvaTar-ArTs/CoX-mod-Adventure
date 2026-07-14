import { BADGE, fmtDl } from '../mods.js'

export default function ModDrawer({ mod, onClose }) {
  const open = mod !== null

  return (
    <>
      <div className={`overlay ${open ? 'open' : ''}`} onClick={onClose} />
      <aside className={`drawer ${open ? 'open' : ''}`}>
        <button className="drawer-close" onClick={onClose}>✕ CLOSE</button>
        {mod && <>
          <span className={`drawer-badge ${BADGE[mod.category] ?? 'badge-other'}`}>
            {mod.category}
          </span>
          <div className="drawer-name">{mod.name}</div>
          <div className="drawer-author">BY {mod.author || 'Unknown'}</div>
          <div className="drawer-thumb" style={{ backgroundImage: `url('${mod.art}')` }} />
          <div className="drawer-dl">↓ {fmtDl(mod.downloads)} downloads</div>
          <p className="drawer-desc">{mod.description || 'No description available.'}</p>
          <div className="drawer-actions">
            <a className="btn btn-primary" href={mod.download_url} target="_blank" rel="noreferrer">Download</a>
            <a className="btn" href={mod.page_url} target="_blank" rel="noreferrer">Mod Page</a>
          </div>
        </>}
      </aside>
    </>
  )
}
