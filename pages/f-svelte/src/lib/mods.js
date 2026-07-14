import raw from '../../mods.json'

const ART_BASE = 'file:///Users/steven/Pictures/CoH-ComicArt/'
const ART_MAP = {
  'Audio':      'TerraVolta.jpeg',
  'Graphics':   'KingsRow.jpeg',
  'GUI / Icons':'IndepPort.jpeg',
  'Popmenus':   'PerezPark.jpeg',
  'Maps':       'AncientCity.jpeg',
  'Cursors':    'FutureCity.jpeg',
  'Languages':  'TimeCityscape.jpeg',
  'Other':      'CityscapeView.jpeg',
}

export const MODS = raw.map(m => ({
  ...m,
  art: ART_BASE + (ART_MAP[m.category] ?? 'CityscapeView.jpeg'),
}))

export const CATS = ['All', ...new Set(MODS.map(m => m.category))]

export const BADGE = {
  'Audio':      'badge-audio',
  'Graphics':   'badge-graphics',
  'GUI / Icons':'badge-gui',
  'Popmenus':   'badge-popmenu',
  'Maps':       'badge-maps',
  'Cursors':    'badge-cursors',
}

export function fmtDl(n) {
  return n >= 1000 ? (n / 1000).toFixed(1) + 'k' : String(n)
}
