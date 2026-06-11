#!/usr/bin/env python3
"""Polite same-host BFS crawler. Stdlib only.

  python3 crawl.py https://example.com --max-pages 20 --max-depth 3
"""
from __future__ import annotations
import argparse
import json
import sys
import time
from collections import deque
from html.parser import HTMLParser
from urllib.parse import urldefrag, urljoin, urlparse

from _http import get as http_get

UA_TOKEN = "searchhawk"
DELAY = 1.0


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.hrefs = []
        self.title = ""
        self._in_title = False

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            for k, v in attrs:
                if k == "href" and v:
                    self.hrefs.append(v)
        if tag == "title":
            self._in_title = True

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False

    def handle_data(self, data):
        if self._in_title:
            self.title += data


def parse_disallows(text, token):
    rules = []
    agents, group = [], []
    for line in text.splitlines():
        line = line.split("#", 1)[0].strip()
        if not line or ":" not in line:
            continue
        k, _, v = line.partition(":")
        k, v = k.strip().lower(), v.strip()
        if k == "user-agent":
            if group:
                if any(token in a.lower() or a.strip() == "*" for a in agents):
                    rules.extend(group)
            agents, group = [v], []
        elif k == "disallow" and v:
            group.append(v)
    if group and any(token in a.lower() or a.strip() == "*" for a in agents):
        rules.extend(group)
    return rules


def blocked(path, rules):
    path = path or "/"
    return any(path.startswith(r) or r == "/" for r in rules)


def crawl(start, max_pages=50, max_depth=5, respect_robots=True, delay=DELAY):
    start = urldefrag(start)[0]
    p = urlparse(start)
    if p.scheme not in ("http", "https") or not p.netloc:
        return []
    host = p.netloc.lower()
    rules = []
    if respect_robots:
        rb = http_get(f"{p.scheme}://{host}/robots.txt")
        if rb["status"] == 200:
            rules = parse_disallows(rb["text"], UA_TOKEN)

    seen = {start}
    q = deque([(start, 0)])
    out = []
    while q and len(out) < max_pages:
        url, depth = q.popleft()
        if respect_robots and blocked(urlparse(url).path, rules):
            continue
        if out:
            time.sleep(delay)
        r = http_get(url)
        final = urldefrag(r["url"] or url)[0]
        title, links = "", []
        if r["status"] == 200 and r["text"] and "html" in (r["headers"].get("Content-Type", "").lower() + "html"):
            parser = PageParser()
            try:
                parser.feed(r["text"])
            except Exception:
                pass
            title = parser.title.strip()
            for href in parser.hrefs:
                href = href.strip()
                if not href or href.startswith(("javascript:", "mailto:", "tel:", "#")):
                    continue
                absu = urldefrag(urljoin(final, href))[0]
                if absu.startswith(("http://", "https://")) and urlparse(absu).netloc.lower() == host:
                    links.append(absu)
            links = list(dict.fromkeys(links))
        out.append({"url": final, "status": r["status"], "depth": depth, "title": title, "links_out": links})
        if depth < max_depth:
            for link in links:
                if link not in seen and len(seen) < max_pages * 20:
                    seen.add(link)
                    q.append((link, depth + 1))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("start_url")
    ap.add_argument("--max-pages", type=int, default=50)
    ap.add_argument("--max-depth", type=int, default=5)
    ap.add_argument("--no-robots", action="store_true")
    ap.add_argument("--delay", type=float, default=DELAY)
    ap.add_argument("--quiet", action="store_true", help="suppress progress on stderr")
    args = ap.parse_args()
    # Note: progress logging can be added to stderr when not quiet
    records = crawl(args.start_url, args.max_pages, args.max_depth, not args.no_robots, args.delay)
    json.dump(records, sys.stdout, indent=2, ensure_ascii=False)
    print()
    return 0 if records else 2


if __name__ == "__main__":
    sys.exit(main())
