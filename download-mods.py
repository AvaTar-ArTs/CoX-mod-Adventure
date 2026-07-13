#!/usr/bin/env python3
"""
City of Heroes Mods Downloader
Downloads all mods from cityofheroes.dev/mods/
"""
import os
import urllib.request
import concurrent.futures
from pathlib import Path

MODS_DIR = Path("/Users/steven/CoX-mod-Adventure/Mods")
MOD_URLS = [
    "1",
    "101",
    "102",
    "104",
    "105",
    "106",
    "107",
    "108",
    "109",
    "11"
]

# Read mod IDs from the list
with open("/Users/steven/CoX-mod-Adventure/coh-mods-list.txt") as f:
    for line in f:
        if line.startswith("https://cityofheroes.dev/mod/"):
            mod_id = line.strip().split("/")[-1]
            MOD_URLS.append(mod_id)

def download_mod(mod_id):
    """Download a single mod"""
    url = f"https://cityofheroes.dev/download/go.php?id={mod_id}"
    filename = MODS_DIR / f"mod-{mod_id}.zip"
    try:
        urllib.request.urlretrieve(url, filename)
        return f"✓ mod-{mod_id}"
    except Exception as e:
        return f"✗ mod-{mod_id}: {e}"

if __name__ == "__main__":
    MODS_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Downloading {len(MOD_URLS)} mods...")
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        for result in executor.map(download_mod, MOD_URLS):
            print(result)
