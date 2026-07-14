#!/usr/bin/env python3
"""
Enrichment scraper — fetches individual mod pages to add:
  - version string
  - full description (richer than the listing page snippet)
  - updated_date
  - forum_url (first homecomingservers.com link found)
Also probes IDs beyond the current max to catch newly added mods.
"""

import json, re, time, sys
from pathlib import Path
import urllib.request, urllib.error

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
}
BASE = 'https://cityofheroes.dev/mods/mod/'
KNOWN_GAPS = {2,3,4,5,6,7,8,10,13,14,24,31,32,33,34,55,73,100,103,124,144,183,219,227,228,230,231,273}

def fetch(url, retries=3):
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=15) as r:
                return r.read().decode('utf-8', errors='replace')
        except urllib.error.HTTPError as e:
            if e.code == 404: return None
            time.sleep(2 ** attempt)
        except Exception as e:
            time.sleep(2 ** attempt)
    return None

def parse_page(html, mod_id):
    """Extract enrichment fields from an individual mod page."""
    # Remove scripts/styles for cleaner text extraction
    clean = re.sub(r'<(script|style)[^>]*>.*?</\1>', '', html, flags=re.DOTALL)

    # Version — look for "version X.Y.Z" patterns
    ver = re.findall(r'\bversion\s+([0-9]+[0-9.a-zA-Z_-]*)', clean, re.I)
    version = ver[0] if ver else None

    # Updated date — "Updated by X on <date>" or "updated on <date>"
    date_patterns = [
        r'[Uu]pdated\s+(?:by\s+\w+\s+)?on\s+([\w]+ \d+, \d{4})',
        r'[Uu]pdated\s+(?:by\s+\w+\s+)?on\s+(\d{4}-\d{2}-\d{2})',
        r'[Uu]pload(?:ed)?\s+on\s+([\w]+ \d+, \d{4})',
    ]
    updated = None
    for pat in date_patterns:
        m = re.search(pat, clean)
        if m: updated = m.group(1); break

    # Forum thread URL (first homecoming forums link)
    forum_url = None
    forum_m = re.search(r'(https://forums\.homecomingservers\.com/topic/[\w/-]+)', html)
    if forum_m: forum_url = forum_m.group(1)

    # Full description text (strip tags, trim)
    # Find the main content div — look for the biggest text block
    # Remove nav, header, footer noise
    body = re.sub(r'<(nav|header|footer|aside)[^>]*>.*?</\1>', '', clean, flags=re.DOTALL)
    text = re.sub(r'<[^>]+>', ' ', body)
    text = re.sub(r'\s+', ' ', text).strip()
    # Heuristic: description is usually a paragraph before the download button
    # Take up to 1000 chars of non-boilerplate text
    desc_full = None
    # Look for text segments longer than 80 chars
    segments = [s.strip() for s in re.split(r'[\r\n]{2,}|(?<=[.!?])\s{2,}', text) if len(s.strip()) > 80]
    if segments:
        # Filter out obvious nav text
        nav_words = {'login','register','download','home','mods','menu','copyright','privacy'}
        content = [s for s in segments if not any(w in s.lower() for w in nav_words)]
        if content:
            desc_full = ' '.join(content[:3])[:1200]

    return {
        'version': version,
        'updated_date': updated,
        'forum_url': forum_url,
        'description_full': desc_full,
    }

def main():
    mods_path = Path(__file__).parent / 'Upgraded/mods.json'
    with open(mods_path) as f:
        mods = json.load(f)

    # Build lookup by id
    mod_map = {m['id']: m for m in mods}
    max_id = max(mod_map.keys())

    print(f"Loaded {len(mods)} mods. Max ID: {max_id}")
    print("Enriching individual mod pages...\n")

    new_mods = []
    enriched = 0

    # 1. Enrich existing mods
    for i, mod in enumerate(mods):
        mid = mod['id']
        print(f"  [{i+1}/{len(mods)}] mod #{mid}: {mod['name'][:45]}", end=' ', flush=True)
        html = fetch(BASE + str(mid))
        if not html:
            print("(skip - no response)")
            continue
        extras = parse_page(html, mid)
        mod.update({k: v for k, v in extras.items() if v is not None})
        if extras.get('version') or extras.get('updated_date'):
            enriched += 1
            print(f"✓ v{extras.get('version','?')} {extras.get('updated_date','')}")
        else:
            print("(no new fields)")
        time.sleep(0.4)  # polite delay

    # 2. Probe for new mods beyond current max
    print(f"\nProbing IDs {max_id+1} to {max_id+30} for new mods...")
    for new_id in range(max_id + 1, max_id + 31):
        if new_id in KNOWN_GAPS: continue
        html = fetch(BASE + str(new_id))
        if html and len(html) > 1000 and '404' not in html[:500]:
            print(f"  NEW MOD FOUND: id={new_id}")
            extras = parse_page(html, new_id)
            # Extract name from <title>
            title_m = re.search(r'<title>([^|<]+)', html)
            name = title_m.group(1).strip() if title_m else f'Mod #{new_id}'
            new_mods.append({'id': new_id, 'name': name, 'source': 'probe', **extras})
        else:
            print(f"  id={new_id}: 404/empty")
        time.sleep(0.3)

    # 3. Save enriched data
    out_path = Path(__file__).parent / 'Upgraded/mods-enriched.json'
    all_mods = mods + new_mods
    with open(out_path, 'w') as f:
        json.dump(all_mods, f, indent=2)

    print(f"\n✓ Enriched {enriched}/{len(mods)} existing mods")
    print(f"✓ Found {len(new_mods)} new mods")
    print(f"✓ Saved → {out_path}")

if __name__ == '__main__':
    main()
