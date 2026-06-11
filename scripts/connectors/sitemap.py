#!/usr/bin/env python3
"""Fetch and parse sitemaps, sitemap indexes, and llms.txt. Stdlib only.

  python3 sitemap.py https://example.com
  python3 sitemap.py https://example.com/sitemap.xml --limit 500
"""
from __future__ import annotations
import argparse
import gzip
import json
import re
import sys
import xml.etree.ElementTree as ET
from urllib.parse import urljoin, urlsplit, urlunsplit

from _http import get as http_get

DEFAULT_LIMIT = 5000
MAX_DEPTH = 8
MAX_CHILD_SITEMAPS = 200
MAX_REDIRECTS = 5

_MD_LINK = re.compile(r"\[[^\]]*\]\((https?://[^)\s]+)\)")
_BARE_URL = re.compile(r"https?://[^\s<>\"]+")


def _localname(tag):
    return tag.rsplit("}", 1)[-1].lower() if "}" in tag else tag.lower()


def _follow(url):
    seen = set()
    current = url
    for _ in range(MAX_REDIRECTS + 1):
        r = http_get(current)
        status = r.get("status", 0)
        if status in (301, 302, 303, 307, 308) and not r.get("text"):
            loc = None
            for k, v in (r.get("headers") or {}).items():
                if k.lower() == "location":
                    loc = v
                    break
            if not loc:
                r["final_url"] = current
                return r
            nxt = urljoin(current, loc.strip())
            if nxt in seen or nxt == current:
                r["final_url"] = current
                return r
            seen.add(current)
            current = nxt
            continue
        r["final_url"] = current
        return r
    r = http_get(current)
    r["final_url"] = current
    return r


def _maybe_gunzip(body, url):
    if not body:
        return body
    if url.lower().endswith(".gz") or body[:2] == b"\x1f\x8b":
        try:
            return gzip.decompress(body)
        except OSError:
            return body
    return body


def _normalize_input_url(arg):
    raw = arg.strip()
    if "://" not in raw:
        raw = "https://" + raw
    parts = urlsplit(raw)
    has_path = bool(parts.path.strip("/"))
    return urlunsplit((parts.scheme, parts.netloc, parts.path, parts.query, "")), has_path


def _parse_llms_txt(text):
    seen, out = set(), []
    for m in _MD_LINK.finditer(text):
        u = m.group(1).rstrip(".,);")
        if u not in seen:
            seen.add(u)
            out.append(u)
    for m in _BARE_URL.finditer(text):
        u = m.group(0).rstrip(".,);")
        if u not in seen:
            seen.add(u)
            out.append(u)
    return out


def _parse_xml(body):
    try:
        root = ET.fromstring(body)
    except ET.ParseError as e:
        return "error", f"XML parse error: {e}"
    rootname = _localname(root.tag)
    if rootname == "sitemapindex":
        locs = []
        for sm in root:
            if _localname(sm.tag) != "sitemap":
                continue
            for child in sm:
                if _localname(child.tag) == "loc" and (child.text or "").strip():
                    locs.append(child.text.strip())
        return "index", locs
    if rootname == "urlset":
        items = []
        for url in root:
            if _localname(url.tag) != "url":
                continue
            entry = {}
            for child in url:
                name = _localname(child.tag)
                val = (child.text or "").strip()
                if not val:
                    continue
                if name == "loc":
                    entry["loc"] = val
                elif name in ("lastmod", "changefreq", "priority"):
                    entry[name] = val
            if entry.get("loc"):
                items.append(entry)
        return "urlset", items
    locs = [(e.text or "").strip() for e in root.iter() if _localname(e.tag) == "loc"]
    scavenged = [v for v in locs if v]
    if scavenged:
        return "urlset", [{"loc": v} for v in scavenged]
    return "error", f"unrecognized root element <{rootname}>"


def _discover_from_robots(base_url):
    parts = urlsplit(base_url)
    robots_url = urlunsplit((parts.scheme, parts.netloc, "/robots.txt", "", ""))
    r = http_get(robots_url)
    out = []
    for line in (r.get("text") or "").splitlines():
        line = line.split("#", 1)[0].strip()
        if ":" not in line:
            continue
        field, _, value = line.partition(":")
        if field.strip().lower() == "sitemap" and value.strip():
            out.append(urljoin(robots_url, value.strip()))
    return out, robots_url


def collect(start_url, limit=DEFAULT_LIMIT):
    full_url, has_path = _normalize_input_url(start_url)
    result = {
        "input": start_url,
        "resolved_url": full_url,
        "type": None,
        "url_count": 0,
        "limit": limit,
        "truncated": False,
        "urls": [],
        "child_sitemaps_fetched": 0,
        "sources": [],
        "errors": [],
    }
    queue, visited, seen_locs = [], set(), set()

    if not has_path:
        parts = urlsplit(full_url)
        queue.append((urlunsplit((parts.scheme, parts.netloc, "/sitemap.xml", "", "")), 0))
        sm_urls, robots_url = _discover_from_robots(full_url)
        result["sources"].append({"discovery": "robots.txt", "url": robots_url, "found": sm_urls})
        for u in sm_urls:
            queue.append((u, 0))
    elif full_url.rstrip("/").lower().endswith("llms.txt"):
        queue.append((full_url, 0))
    else:
        queue.append((full_url, 0))

    while queue:
        if len(result["urls"]) >= limit:
            result["truncated"] = True
            break
        url, depth = queue.pop(0)
        if url in visited:
            continue
        visited.add(url)

        r = _follow(url)
        status = r.get("status", 0)
        final_url = r.get("final_url", url)
        src = {"url": url, "status": status, "depth": depth}
        if final_url != url:
            src["final_url"] = final_url
        is_llms = final_url.rstrip("/").lower().endswith("llms.txt")
        if status != 200 or not r.get("body"):
            src["note"] = r.get("error") or f"HTTP {status}"
            result["sources"].append(src)
            if r.get("error"):
                result["errors"].append({"url": url, "error": r["error"]})
            continue

        body = _maybe_gunzip(r["body"], final_url)

        if is_llms:
            text = body.decode("utf-8", errors="replace")
            found = _parse_llms_txt(text)
            src.update({"kind": "llms.txt", "found": len(found)})
            result["sources"].append(src)
            if result["type"] is None:
                result["type"] = "llms.txt"
            for loc in found:
                if loc in seen_locs:
                    continue
                seen_locs.add(loc)
                result["urls"].append({"loc": loc})
                if len(result["urls"]) >= limit:
                    result["truncated"] = True
                    break
            continue

        kind, items = _parse_xml(body)
        src["kind"] = kind
        if kind == "error":
            src["note"] = items
            result["sources"].append(src)
            result["errors"].append({"url": url, "error": items})
            continue

        if kind == "index":
            child = [c for c in items if c not in visited][:MAX_CHILD_SITEMAPS]
            src["children"] = len(child)
            result["sources"].append(src)
            if result["type"] is None:
                result["type"] = "sitemapindex"
            if depth < MAX_DEPTH:
                for c in child:
                    queue.append((c, depth + 1))
            else:
                result["errors"].append({"url": url, "error": "max sitemap depth reached"})
            continue

        if depth > 0:
            result["child_sitemaps_fetched"] += 1
        src["found"] = len(items)
        result["sources"].append(src)
        if result["type"] is None:
            result["type"] = "sitemap"
        for entry in items:
            loc = entry["loc"]
            if loc in seen_locs:
                continue
            seen_locs.add(loc)
            result["urls"].append(entry)
            if len(result["urls"]) >= limit:
                result["truncated"] = True
                break

    result["url_count"] = len(result["urls"])
    if result["type"] is None:
        result["type"] = "unknown"
    return result


def main():
    ap = argparse.ArgumentParser(description="Fetch + parse sitemap.xml / llms.txt")
    ap.add_argument("target", help="Sitemap URL, llms.txt URL, or site root")
    ap.add_argument("--limit", type=int, default=DEFAULT_LIMIT)
    args = ap.parse_args()
    limit = args.limit if args.limit and args.limit > 0 else DEFAULT_LIMIT
    result = collect(args.target, limit=limit)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    if result["url_count"] == 0 and (result["errors"] or not result["sources"]):
        any_ok = any(s.get("status") == 200 for s in result["sources"])
        if not any_ok:
            return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
