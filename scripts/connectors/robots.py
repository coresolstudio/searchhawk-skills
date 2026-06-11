#!/usr/bin/env python3
"""robots.txt checker for SearchHawk. Stdlib only.

  python3 robots.py https://example.com
  python3 robots.py https://example.com --check-ai-bots
"""
from __future__ import annotations
import argparse
import json
import sys
from urllib.parse import urlparse

from _http import get as http_get

AI_BOTS = ["GPTBot", "ChatGPT-User", "Google-Extended", "ClaudeBot", "PerplexityBot", "Bytespider"]


def parse_robots(text):
    groups = []
    agents, rules = [], []
    for line in text.splitlines():
        line = line.split("#", 1)[0].strip()
        if not line or ":" not in line:
            continue
        k, _, v = line.partition(":")
        k, v = k.strip().lower(), v.strip()
        if k == "user-agent":
            if rules:
                groups.append({"agents": agents, "rules": rules})
            agents, rules = [v], []
        elif k in ("disallow", "allow"):
            rules.append({"type": k, "path": v})
    if rules:
        groups.append({"agents": agents, "rules": rules})
    return groups


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("url")
    ap.add_argument("--check-ai-bots", action="store_true")
    args = ap.parse_args()
    p = urlparse(args.url if "://" in args.url else "https://" + args.url)
    robots_url = f"{p.scheme}://{p.netloc}/robots.txt"
    r = http_get(robots_url)
    out = {"robots_url": robots_url, "status": r["status"], "groups": []}
    if r["status"] == 200:
        out["groups"] = parse_robots(r["text"])
    if args.check_ai_bots and r["text"]:
        blocks = {}
        for bot in AI_BOTS:
            blocks[bot] = bot.lower() in r["text"].lower()
        out["ai_bot_mentions"] = blocks
    print(json.dumps(out, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
