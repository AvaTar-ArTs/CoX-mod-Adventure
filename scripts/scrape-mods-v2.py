#!/usr/bin/env python3
"""
CoH Mod Scraper — cityofheroes.dev
Scrapes all mod detail pages to build mods.json with correct download URLs.

Usage:
    python3 scrape-mods.py              # scrape and write mods.json
    python3 scrape-mods.py --download   # scrape + download all pigg files
    python3 scrape-mods.py --dry-run    # show what would be downloaded
"""

import json
import os
import re
import sys
import time
import urllib.request
import urllib.error
import concurrent.futures
from pathlib import Path
from html.parser import HTMLParser

BASE_URL = "https://cityofheroes.dev"
MODS_DIR = Path(__file__).parent / "Mods"
JSON_OUT = Path(__file__).parent / "mods.json"
INSTALL_DIR = Path.home() / "Library/Application Support/LaunchCat/coh/assets/mods"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
    "Accept": "text/html,application/xhtml+xml,*/*",
    "Referer": "https://cityofheroes.dev/mods/",
}

# ─── HTML parsers ────────────────────────────────────────────────────────────

class ModListParser(HTMLParser):
    """Extracts mod IDs from /mods/ listing pages."""
    def __init__(self):
        super().__init__()
        self.mod_ids = []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            href = dict(attrs).get("href", "")
            m = re.match(r"^/?mods?/mod/(\d+)$|^mod/(\d+)$", href)
            if m:
                mod_id = int(m.group(1) or m.group(2))
                if mod_id not in self.mod_ids:
                    self.mod_ids.append(mod_id)


class ModDetailParser(HTMLParser):
    """Extracts name, author, downloads, description, download URL from /mods/mod/{id}."""
    def __init__(self):
        super().__init__()
        self.name = ""
        self.author = ""
        self.downloads = 0
        self.description = ""
        self.download_url = ""
        self.category = ""
        self._in_desc = False
        self._desc_depth = 0
        self._desc_buf = []
        self._capture_next_text = None

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        href = d.get("href", "")

        # download link
        if tag == "a" and "download.php" in href:
            self.download_url = href if href.startswith("http") else BASE_URL + "/mods/" + href

        # card-text div → description
        classes = d.get("class", "")
        if tag == "div" and "card-text" in classes:
            self._in_desc = True
            self._desc_depth = 0

        if self._in_desc:
            self._desc_depth += 1

    def handle_endtag(self, tag):
        if self._in_desc:
            self._desc_depth -= 1
            if self._desc_depth <= 0:
                self._in_desc = False
                self.description = " ".join(" ".join(self._desc_buf).split())

    def handle_data(self, data):
        text = data.strip()
        if not text:
            return

        if self._in_desc:
            self._desc_buf.append(text)
            return

        # card-title → mod name
        if not self.name and len(text) > 2 and len(text) < 120:
            self.name = self.name or text  # will be overwritten by better match

        # Author: / Downloads: labels
        if text == "Author:":
            self._capture_next_text = "author"
        elif text == "Downloads:":
            self._capture_next_text = "downloads"
        elif text == "Category:":
            self._capture_next_text = "category"
        elif self._capture_next_text:
            if self._capture_next_text == "author":
                self.author = text
            elif self._capture_next_text == "downloads":
                try:
                    self.downloads = int(text.replace(",", ""))
                except ValueError:
                    pass
            elif self._capture_next_text == "category":
                self.category = text
            self._capture_next_text = None


# ─── Network helpers ──────────────────────────────────────────────────────────

def fetch(url, retries=3, delay=1.5):
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=20) as r:
                return r.read().decode("utf-8", errors="replace")
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return None
            if attempt < retries - 1:
                time.sleep(delay * (attempt + 1))
        except Exception:
            if attempt < retries - 1:
                time.sleep(delay * (attempt + 1))
    return None


def collect_mod_ids():
    """Scrape all listing pages and return sorted list of mod IDs."""
    ids = set()
    page = 1
    while True:
        url = f"{BASE_URL}/mods/index.php?search=&category=&author=&currentpage={page}"
        html = fetch(url)
        if not html:
            break
        parser = ModListParser()
        parser.feed(html)
        if not parser.mod_ids:
            break
        new = [i for i in parser.mod_ids if i not in ids]
        if not new:
            break
        ids.update(new)
        print(f"  page {page}: found {len(parser.mod_ids)} mods ({len(ids)} total)", flush=True)
        page += 1
        time.sleep(0.5)
    return sorted(ids)


def scrape_mod(mod_id):
    """Scrape a single mod detail page. Returns dict or None."""
    url = f"{BASE_URL}/mods/mod/{mod_id}"
    html = fetch(url)
    if not html:
        return None

    parser = ModDetailParser()
    parser.feed(html)

    # extract name from h3.card-title via regex (more reliable than parser)
    name_m = re.search(r'class="card-title[^"]*"[^>]*>([^<]+)<', html)
    if name_m:
        parser.name = name_m.group(1).strip()

    if not parser.name or not parser.download_url:
        return None

    return {
        "id": mod_id,
        "name": parser.name,
        "author": parser.author,
        "category": parser.category or "Other",
        "downloads": parser.downloads,
        "description": parser.description[:500],
        "download_url": parser.download_url,
        "page_url": url,
    }


# ─── Download ─────────────────────────────────────────────────────────────────

def download_pigg(mod, dest_dir, install=False):
    """Download a .pigg file for a mod. Returns status string."""
    url = mod["download_url"]
    fname = url.split("file=")[-1].split("/")[-1]
    if not fname.endswith(".pigg"):
        fname = f"mod-{mod['id']}.pigg"

    dest = dest_dir / fname
    if dest.exists() and dest.stat().st_size > 1000:
        return f"skip  {fname} (exists)"

    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=120) as r:
            data = r.read()
        if len(data) < 100:
            return f"✗ {fname}: too small ({len(data)} bytes)"
        dest.write_bytes(data)

        if install:
            INSTALL_DIR.mkdir(parents=True, exist_ok=True)
            install_path = INSTALL_DIR / fname
            install_path.write_bytes(data)
            return f"✓ {fname} ({len(data)//1024}KB) → installed"

        return f"✓ {fname} ({len(data)//1024}KB)"
    except Exception as e:
        return f"✗ {fname}: {e}"


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    args = set(sys.argv[1:])
    do_download = "--download" in args
    do_install = "--install" in args
    dry_run = "--dry-run" in args

    print("=== CoH Mod Scraper ===")

    # Load or build mods.json
    if JSON_OUT.exists() and "--rescrape" not in args:
        print(f"Loading existing {JSON_OUT.name} ...")
        mods = json.loads(JSON_OUT.read_text())
        print(f"  {len(mods)} mods loaded")
    else:
        print("Collecting mod IDs from listing pages ...")
        mod_ids = collect_mod_ids()
        print(f"  {len(mod_ids)} mod IDs found: {mod_ids[:5]}...")

        print("Scraping mod detail pages (this takes ~2 min) ...")
        mods = []
        failed = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
            futures = {ex.submit(scrape_mod, mid): mid for mid in mod_ids}
            for i, fut in enumerate(concurrent.futures.as_completed(futures), 1):
                mid = futures[fut]
                result = fut.result()
                if result:
                    mods.append(result)
                    print(f"  [{i}/{len(mod_ids)}] ✓ {result['name'][:50]}", flush=True)
                else:
                    failed.append(mid)
                    print(f"  [{i}/{len(mod_ids)}] ✗ mod-{mid}", flush=True)
                time.sleep(0.1)

        mods.sort(key=lambda m: m["downloads"], reverse=True)
        JSON_OUT.write_text(json.dumps(mods, indent=2, ensure_ascii=False))
        print(f"\n✓ Wrote {JSON_OUT} ({len(mods)} mods, {len(failed)} failed)")
        if failed:
            print(f"  Failed IDs: {failed}")

    if dry_run:
        print("\n--- Dry run: would download ---")
        for m in mods[:10]:
            print(f"  [{m['category']}] {m['name']} → {m['download_url']}")
        print(f"  ... {len(mods)} total")
        return

    if do_download or do_install:
        MODS_DIR.mkdir(parents=True, exist_ok=True)
        dest = INSTALL_DIR if do_install else MODS_DIR
        dest.mkdir(parents=True, exist_ok=True)
        print(f"\nDownloading {len(mods)} mods → {dest} ...")
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:
            futures = {ex.submit(download_pigg, m, MODS_DIR, do_install): m for m in mods}
            for fut in concurrent.futures.as_completed(futures):
                print(f"  {fut.result()}", flush=True)

    print("\nDone.")
    print("Next: run with --install to copy pigg files to LaunchCat's assets/mods/")
    print(f"  Install path: {INSTALL_DIR}")


if __name__ == "__main__":
    main()
