#!/usr/bin/env python3
"""Keyword ideas from Google Autocomplete (unofficial). Stdlib only.

WARNING: Undocumented endpoint — use sparingly, may rate-limit.
  python3 suggest.py "seo audit" --hl en --gl US --expand
"""
from __future__ import annotations
import argparse
import json
import string
import sys
from urllib.parse import urlencode

from _http import get_json, polite_sleep

ENDPOINT = "https://suggestqueries.google.com/complete/search"
WARN = "WARNING: Google Suggest is unofficial — use sparingly."
SLEEP = 0.4


def fetch_suggestions(query, hl="", gl=""):
    params = {"client": "firefox", "q": query, "hl": hl or "", "gl": gl or ""}
    url = ENDPOINT + "?" + urlencode(params)
    r = get_json(url)
    items = []
    if isinstance(r.get("json"), list) and len(r["json"]) > 1 and isinstance(r["json"][1], list):
        items = [str(x) for x in r["json"][1]]
    return items, r


def expand_seeds(seed):
    yield seed
    for ch in string.ascii_lowercase:
        yield f"{seed} {ch}"


def suggest(query, hl="", gl="", expand=False):
    seen, out, errors = set(), [], []
    seeds = list(expand_seeds(query)) if expand else [query]
    for i, seed in enumerate(seeds):
        items, r = fetch_suggestions(seed, hl, gl)
        if r.get("error"):
            errors.append({"seed": seed, "error": r["error"]})
        for s in items:
            k = s.lower()
            if k not in seen:
                seen.add(k)
                out.append(s)
        if expand and i < len(seeds) - 1:
            polite_sleep(SLEEP)
    return {
        "query": query,
        "hl": hl or None,
        "gl": gl or None,
        "expanded": expand,
        "count": len(out),
        "suggestions": out,
        "errors": errors,
    }


def main():
    p = argparse.ArgumentParser(description="Google Autocomplete keyword ideas (unofficial)")
    p.add_argument("query")
    p.add_argument("--hl", default="")
    p.add_argument("--gl", default="")
    p.add_argument("--expand", action="store_true")
    args = p.parse_args()
    print(WARN, file=sys.stderr)
    result = suggest(args.query, args.hl, args.gl, args.expand)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["suggestions"] else 2


if __name__ == "__main__":
    sys.exit(main())
