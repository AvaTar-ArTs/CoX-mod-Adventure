import { BADGE, fmtDl } from '../mods.js'

export default function ModCard({ mod, onClick }) {
  return (
    <div className="card" onClick={() => onClick(mod)}>
      <span className={`badge ${BADGE[mod.category] ?? 'badge-other'}`}>
        {mod.category}
      </span>
      <div className="card-name">{mod.name}</div>
      <div className="card-meta">
        <span>{mod.author || 'Unknown'}</span>
        <span className="card-dl">↓ {fmtDl(mod.downloads)}</span>
      </div>
      {mod.description && <p className="card-desc">{mod.description}</p>}
      <div className="card-actions">
        <a className="btn btn-primary" href={mod.download_url} target="_blank" rel="noreferrer"
           onClick={e => e.stopPropagation()}>Download</a>
        <a className="btn" href={mod.page_url} target="_blank" rel="noreferrer"
           onClick={e => e.stopPropagation()}>Info</a>
      </div>
    </div>
  )
}
