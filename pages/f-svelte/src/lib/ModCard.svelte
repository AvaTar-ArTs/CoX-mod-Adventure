<script>
  import { BADGE, fmtDl } from './mods.js'
  let { mod, onclick } = $props()
</script>

<div class="card" onclick={() => onclick(mod)}>
  <span class="badge {BADGE[mod.category] ?? 'badge-other'}">{mod.category}</span>
  <div class="card-name">{mod.name}</div>
  <div class="card-meta">
    <span>{mod.author || 'Unknown'}</span>
    <span class="card-dl">↓ {fmtDl(mod.downloads)}</span>
  </div>
  {#if mod.description}
    <p class="card-desc">{mod.description}</p>
  {/if}
  <div class="card-actions">
    <a class="btn btn-primary" href={mod.download_url} target="_blank"
       onclick={e => e.stopPropagation()}>Download</a>
    <a class="btn" href={mod.page_url} target="_blank"
       onclick={e => e.stopPropagation()}>Info</a>
  </div>
</div>
