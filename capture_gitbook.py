#!/usr/bin/env python3
"""Capture the HyperCycle CBNO GitBook into a local folder (a git repo).

Saves, for every page listed in the space's llms.txt:
  docs/<path>.md        the page as Markdown, with links and images made local
  _raw/md/<path>.md     the page exactly as GitBook served it
  _raw/html/<path>.html the rendered HTML page (catches anything Markdown drops)
  assets/<file>         every image and file the pages reference
Plus _raw/llms.txt, _raw/llms-full.txt, a SOURCES.json record (URL, fetch time,
sha256 per file) and a generated README.md table of contents.

Standard library only. Safe to re-run: files are refreshed in place, and
SOURCES.json shows what changed. Nothing is ever deleted.

Usage (from inside the repo folder):
  python3 capture_gitbook.py
  python3 capture_gitbook.py --base <other space url>   # optional
"""
import argparse, hashlib, html as htmllib, json, re, sys, time, urllib.error, urllib.parse, urllib.request
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_BASE = "https://hypercycle-cbno.gitbook.io/hypercycle-cbno/u57KauJomd55OVuTYz6e/"
DEFAULT_ASSET_RE = r"https?://[^\s\"'<>()]*(?:files\.gitbook\.io|gitbook-x-prod\.appspot\.com|/~gitbook/image)[^\s\"'<>()]*"
UA = "Mozilla/5.0 (docs-archive; personal backup)"
LINK_RE = re.compile(r"^- \[(?P<title>[^\]]+)\]\((?P<url>[^)]+)\)(?::\s*(?P<desc>.*))?$")
BANNER_RE = re.compile(r"\A> For the complete documentation index.*?\n\n", re.S)

def fetch(url, tries=3):
    for attempt in range(1, tries + 1):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=30) as r:
                return r.read()
        except (urllib.error.URLError, TimeoutError) as e:
            if isinstance(e, urllib.error.HTTPError) and e.code == 404:
                raise
            if attempt == tries:
                raise
            time.sleep(2 * attempt)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def parse_index(text, base):
    """Return [(section, title, rel_path, desc)] from llms.txt."""
    pages, section = [], ""
    for line in text.splitlines():
        if line.startswith("## "):
            section = line[3:].strip()
        m = LINK_RE.match(line.strip())
        if m and m.group("url").startswith(base):
            rel = m.group("url")[len(base):]
            pages.append((section, m.group("title"), rel, (m.group("desc") or "").strip()))
    return pages

def asset_name(url):
    """Stable local name: short hash of the URL path + original file name."""
    path = urllib.parse.unquote(urllib.parse.urlsplit(url).path)
    if "/~gitbook/image" in url:
        inner = urllib.parse.parse_qs(urllib.parse.urlsplit(url).query).get("url", [""])[0]
        path = urllib.parse.unquote(urllib.parse.urlsplit(inner).path) or path
    name = re.sub(r"[^A-Za-z0-9._-]", "_", path.rsplit("/", 1)[-1]) or "file"
    return f"{hashlib.sha1(path.encode()).hexdigest()[:10]}-{name}"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default=DEFAULT_BASE)
    ap.add_argument("--asset-regex", default=DEFAULT_ASSET_RE)
    ap.add_argument("--delay", type=float, default=0.5, help="seconds between requests")
    args = ap.parse_args()
    base = args.base if args.base.endswith("/") else args.base + "/"
    base_path = urllib.parse.urlsplit(base).path
    asset_re = re.compile(args.asset_regex)
    out = Path.cwd()
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    sources_file = out / "SOURCES.json"
    old = json.loads(sources_file.read_text()) if sources_file.exists() else {"files": {}}
    record = {"base": base, "captured_at": now, "files": {}}
    changed, failed = set(), []

    def save(rel, data, url):
        p = out / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(data)
        h = sha(data)
        if old["files"].get(rel, {}).get("sha256") != h:
            changed.add(rel)
        record["files"][rel] = {"url": url, "sha256": h, "bytes": len(data)}

    print(f"Index: {base}llms.txt")
    index = fetch(base + "llms.txt")
    save("_raw/llms.txt", index, base + "llms.txt")
    try:
        full = fetch(base + "llms-full.txt")
        save("_raw/llms-full.txt", full, base + "llms-full.txt")
    except Exception as e:
        print(f"  (no llms-full.txt: {e})")
    pages = parse_index(index.decode("utf-8"), base)
    print(f"  {len(pages)} pages listed")
    local = {p[2] for p in pages}
    assets = {}

    def local_link(target, from_rel):
        """Map a GitBook page link to a relative local docs/ path, else None."""
        url = urllib.parse.urljoin(base, target)
        frag = ""
        if "#" in url:
            url, frag = url.split("#", 1)
            frag = "#" + frag
        path = urllib.parse.urlsplit(url).path
        if not path.startswith(base_path):
            return None
        rel = path[len(base_path):]
        if rel and not rel.endswith(".md"):
            rel += ".md"
        if rel not in local:
            return None
        depth = from_rel.count("/")
        return ("../" * depth) + rel + frag

    for i, (section, title, rel, _) in enumerate(pages, 1):
        url = base + rel
        print(f"[{i}/{len(pages)}] {rel}")
        try:
            md = fetch(url)
        except Exception as e:
            print(f"  FAILED: {e}"); failed.append(url); continue
        save(f"_raw/md/{rel}", md, url)
        try:
            page_html = fetch(url[:-3])
            save(f"_raw/html/{rel[:-3]}.html", page_html, url[:-3])
        except Exception as e:
            print(f"  html skipped: {e}")
        text = BANNER_RE.sub("", md.decode("utf-8"))
        for a in set(asset_re.findall(text)):
            assets.setdefault(a, asset_name(a))
            text = text.replace(a, ("../" * (rel.count("/") + 1)) + "assets/" + assets[a])
        def relink(m):
            new = local_link(m.group(2), rel)
            return f"{m.group(1)}({new})" if new else m.group(0)
        text = re.sub(r"(\[[^\]]*\])\(([^)\s]+)\)", relink, text)
        text = re.sub(r'href="([^"]+)"',
                      lambda m: f'href="{local_link(m.group(1), rel) or m.group(1)}"', text)
        save(f"docs/{rel}", text.encode("utf-8"), url)
        time.sleep(args.delay)

    print(f"Assets: {len(assets)}")
    for url, name in sorted(assets.items(), key=lambda kv: kv[1]):
        try:
            save(f"assets/{name}", fetch(htmllib.unescape(url)), htmllib.unescape(url))
        except Exception as e:
            print(f"  FAILED {name}: {e}"); failed.append(url)
        time.sleep(args.delay / 2)

    lines = ["# HyperCycle CBNO and Developer Guides (archive)", "",
             f"Archived copy of <{base}>, captured {now}.", "",
             "Pages are in `docs/`, images in `assets/`, and untouched originals in `_raw/`.",
             "`SOURCES.json` records each file's source URL and checksum.", ""]
    section = None
    for sec, title, rel, desc in pages:
        if sec != section:
            section = sec; lines += ["", f"## {sec}", ""]
        indent = "  " * rel.count("/") if sec.startswith("CBNO") else "  " * max(rel.count("/") - 1, 0)
        lines.append(f"{indent}- [{title}](docs/{rel})" + (f": {desc}" if desc else ""))
    save("README.md", ("\n".join(lines) + "\n").encode("utf-8"), base)

    record["failed"] = failed
    sources_file.write_text(json.dumps(record, indent=2) + "\n")
    print(f"\nDone: {len(record['files'])} files, {len(changed)} new or changed, {len(failed)} failed.")
    if failed:
        print("Failed URLs are listed in SOURCES.json; re-run to retry.")
    sys.exit(1 if failed else 0)

if __name__ == "__main__":
    main()
