#!/usr/bin/env python3
"""Internal-link graph from crawl.py JSON. Stdlib only. No network I/O.

  python3 crawl.py https://example.com --max-pages 30 | python3 linkgraph.py -
  python3 linkgraph.py crawl.json --top 15
"""
from __future__ import annotations
import argparse
import json
import sys


def load_pages(source):
    raw = sys.stdin.read() if source == "-" else open(source, encoding="utf-8").read()
    data = json.loads(raw)
    if not isinstance(data, list):
        raise ValueError("expected JSON array of crawl records")
    pages = []
    for i, obj in enumerate(data):
        if not isinstance(obj, dict) or not obj.get("url"):
            raise ValueError(f"page {i} missing url")
        links = obj.get("links_out") or []
        pages.append({
            "url": obj["url"],
            "depth": obj.get("depth"),
            "title": obj.get("title") or "",
            "links_out": [u for u in links if isinstance(u, str)],
        })
    return pages


def pagerank(nodes, out_edges, alpha=0.85, max_iter=100, tol=1e-6):
    n = len(nodes)
    if not n:
        return {}
    x = dict.fromkeys(nodes, 1.0 / n)
    p = 1.0 / n
    out_deg = {node: len(out_edges.get(node, ())) for node in nodes}
    dangling = [node for node in nodes if out_deg[node] == 0]
    for _ in range(max_iter):
        xlast = x
        x = dict.fromkeys(nodes, 0.0)
        danglesum = alpha * sum(xlast[node] for node in dangling)
        for node in nodes:
            share = alpha * xlast[node] / out_deg[node] if out_deg[node] else 0.0
            for tgt in out_edges.get(node, ()):
                x[tgt] += share
        for node in nodes:
            x[node] += danglesum * p + (1.0 - alpha) * p
        if sum(abs(x[node] - xlast[node]) for node in nodes) < n * tol:
            break
    return x


def analyze(pages, top=10):
    nodes = [p["url"] for p in pages]
    node_set = set(nodes)
    depth = {p["url"]: p.get("depth") for p in pages}
    title = {p["url"]: p.get("title") or "" for p in pages}

    out_edges, in_deg = {}, dict.fromkeys(nodes, 0)
    for pg in pages:
        url = pg["url"]
        seen, targets = set(), []
        for tgt in pg["links_out"]:
            if tgt in node_set and tgt != url and tgt not in seen:
                seen.add(tgt)
                targets.append(tgt)
                in_deg[tgt] += 1
        out_edges[url] = targets
    out_deg = {u: len(t) for u, t in out_edges.items()}

    orphans = sorted(u for u in nodes if in_deg[u] == 0 and depth.get(u) != 0)
    deep = sorted(u for u in nodes if isinstance(depth.get(u), int) and depth[u] > 3)

    hist = {}
    for u in nodes:
        d = depth.get(u)
        key = d if d is not None else "unknown"
        hist[key] = hist.get(key, 0) + 1

    pr = pagerank(nodes, out_edges)
    ranked = sorted(nodes, key=lambda u: (-pr.get(u, 0), -in_deg[u], u))
    top_list = [{
        "url": u,
        "pagerank": round(pr.get(u, 0), 6),
        "in": in_deg[u],
        "out": out_deg[u],
        "depth": depth.get(u),
        "title": title.get(u, ""),
    } for u in ranked[: max(0, int(top))]]

    return {
        "summary": {
            "pages": len(nodes),
            "orphans": len(orphans),
            "deep_pages": len(deep),
            "max_depth": max((d for d in depth.values() if isinstance(d, int)), default=None),
            "total_internal_links": sum(out_deg.values()),
        },
        "depth_histogram": {str(k): hist[k] for k in sorted(hist, key=lambda d: (d == "unknown", d))},
        "orphans": orphans,
        "deep_pages": deep,
        "degrees": {u: {"in": in_deg[u], "out": out_deg[u]} for u in nodes},
        "pagerank": {u: round(pr.get(u, 0), 6) for u in nodes},
        "top": top_list,
    }


def main():
    ap = argparse.ArgumentParser(description="Analyze crawl.py JSON for internal links")
    ap.add_argument("crawl", help="crawl JSON file or '-' for stdin")
    ap.add_argument("--top", type=int, default=10)
    args = ap.parse_args()
    try:
        pages = load_pages(args.crawl)
    except (OSError, ValueError, json.JSONDecodeError) as e:
        print(f"linkgraph: {e}", file=sys.stderr)
        return 1
    json.dump(analyze(pages, top=args.top), sys.stdout, indent=2)
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
