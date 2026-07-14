<script>
  import { MODS, CATS, BADGE, fmtDl } from './lib/mods.js'
  import ModCard from './lib/ModCard.svelte'
  import './theme.css'

  // $state() = reactive variable — Svelte tracks reads and re-runs derived()
  let cat   = $state('All')
  let query = $state('')
  let sort  = $state('downloads')
  let active = $state(null)

  // $derived() = computed value — re-evaluates only when cat/query/sort change
  let visible = $derived((() => {
    const q = query.toLowerCase()
    return MODS
      .filter(m => {
        if (cat !== 'All' && m.category !== cat) return false
        if (!q) return true
        return m.name.toLowerCase().includes(q)
          || (m.author || '').toLowerCase().includes(q)
          || (m.description || '').toLowerCase().includes(q)
      })
      .sort((a, b) => {
        if (sort === 'downloads') return (b.downloads || 0) - (a.downloads || 0)
        if (sort === 'name')     return a.name.localeCompare(b.name)
        return (a.author || '').localeCompare(b.author || '')
      })
  })())

  function closeDrawer() { active = null }
</script>

<svelte:window onkeydown={e => { if (e.key === 'Escape') closeDrawer() }} />

<div class="hero">
  <div class="hero-content">
    <div class="eyebrow">City of Heroes · Homecoming</div>
    <div class="hero-title">MOD ARCHIVE</div>
    <div class="hero-sub">{MODS.length} MODS · SVELTE 5</div>
  </div>
</div>

<div class="controls">
  <input type="search" placeholder="Search mods, authors…" bind:value={query} />
  <select bind:value={sort}>
    <option value="downloads">Sort: Downloads</option>
    <option value="name">Sort: Name A→Z</option>
    <option value="author">Sort: Author</option>
  </select>
  <span class="count">{visible.length} mods</span>
</div>

<div class="tabs">
  {#each CATS as c}
    <button class="tab {c === cat ? 'active' : ''}" onclick={() => cat = c}>{c}</button>
  {/each}
</div>

<div class="archive">
  {#each visible as mod (mod.id)}
    <ModCard {mod} onclick={m => active = m} />
  {/each}
</div>

<!-- Drawer -->
<div class="overlay {active ? 'open' : ''}" onclick={closeDrawer}></div>
<aside class="drawer {active ? 'open' : ''}">
  <button class="drawer-close" onclick={closeDrawer}>✕ CLOSE</button>
  {#if active}
    <span class="drawer-badge {BADGE[active.category] ?? 'badge-other'}">{active.category}</span>
    <div class="drawer-name">{active.name}</div>
    <div class="drawer-author">BY {active.author || 'Unknown'}</div>
    <div class="drawer-thumb" style="background-image:url('{active.art}')"></div>
    <div class="drawer-dl">↓ {fmtDl(active.downloads)} downloads</div>
    <p class="drawer-desc">{active.description || 'No description available.'}</p>
    <div class="drawer-actions">
      <a class="btn btn-primary" href={active.download_url} target="_blank">Download</a>
      <a class="btn" href={active.page_url} target="_blank">Mod Page</a>
    </div>
  {/if}
</aside>

<style>
  /* component-scoped styles would go here */
</style>
