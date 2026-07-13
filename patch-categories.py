#!/usr/bin/env python3
"""Patch categories in mods.json by scraping listing pages via subprocess curl."""
import json, re, subprocess, time
from pathlib import Path

JSON_OUT = Path(__file__).parent / "mods.json"

def curl_get(url):
    r = subprocess.run(
        ["curl", "-sL", "--connect-timeout", "15", url,
         "-H", "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"],
        capture_output=True, text=True
    )
    return r.stdout

id_to_cat = {}
for page in range(1, 18):
    url = f"https://cityofheroes.dev/mods/index.php?search=&category=&author=&currentpage={page}"
    html = curl_get(url)
    cards = re.findall(
        r'<a href="mod/(\d+)"[^>]*>.*?<span class=\'badge[^\']*\'[^>]*>([^<]+)</span>',
        html, re.DOTALL
    )
    for mid, cat in cards:
        id_to_cat[int(mid)] = cat.strip()
    print(f"  page {page}: {len(cards)} categories")
    time.sleep(0.4)

print(f"Total mappings: {len(id_to_cat)}")

mods = json.loads(JSON_OUT.read_text())
updated = 0
for m in mods:
    cat = id_to_cat.get(m["id"])
    if cat:
        m["category"] = cat
        updated += 1

mods.sort(key=lambda m: m["downloads"], reverse=True)
JSON_OUT.write_text(json.dumps(mods, indent=2, ensure_ascii=False))

cats = {}
for m in mods:
    cats[m["category"]] = cats.get(m["category"], 0) + 1
print(f"Updated {updated}/{len(mods)} categories")
for k, v in sorted(cats.items(), key=lambda x: -x[1]):
    print(f"  {k}: {v}")
