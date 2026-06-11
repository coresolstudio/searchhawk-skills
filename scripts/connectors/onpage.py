#!/usr/bin/env python3
"""Fetch page HTML and extract SEO/AEO/GEO signals. Stdlib only."""
import json, re, sys, urllib.request
from html.parser import HTMLParser

class Extractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title = ""
        self.in_title = False
        self.meta = {}
        self.h1 = []
        self.h2 = []
        self.canonical = ""
        self.jsonld = []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "title": self.in_title = True
        if tag == "meta" and "name" in a: self.meta[a["name"].lower()] = a.get("content","")
        if tag == "meta" and "property" in a: self.meta[a["property"].lower()] = a.get("content","")
        if tag == "link" and a.get("rel") == "canonical": self.canonical = a.get("href","")
        if tag == "h1": self._ht = "h1"
        if tag == "h2": self._ht = "h2"
        if tag == "script" and a.get("type") == "application/ld+json": self._ld = True
    def handle_endtag(self, tag):
        if tag == "title": self.in_title = False
        if tag in ("h1","h2"): self._ht = None
    def handle_data(self, data):
        if self.in_title: self.title += data
        if getattr(self, "_ht", None) == "h1": self.h1.append(data.strip())
        if getattr(self, "_ht", None) == "h2": self.h2.append(data.strip())

def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "SearchHawk/1.0"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return r.read().decode("utf-8", errors="replace")

def main():
    url = sys.argv[1] if len(sys.argv) > 1 else sys.exit("Usage: onpage.py <url>")
    html = fetch(url)
    p = Extractor()
    p.feed(html)
    for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', html, re.S):
        try: p.jsonld.append(json.loads(m.group(1)))
        except: pass
    out = {
        "url": url,
        "title": p.title.strip()[:120],
        "title_len": len(p.title.strip()),
        "meta_description": p.meta.get("description","")[:200],
        "meta_len": len(p.meta.get("description","")),
        "h1": p.h1[:3],
        "h2_count": len(p.h2),
        "h2_sample": p.h2[:5],
        "canonical": p.canonical,
        "robots": p.meta.get("robots",""),
        "og_title": p.meta.get("og:title",""),
        "jsonld_types": [x.get("@type") for x in p.jsonld if isinstance(x, dict)],
    }
    print(json.dumps(out, indent=2))

if __name__ == "__main__":
    main()
