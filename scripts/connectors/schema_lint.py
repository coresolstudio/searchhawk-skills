#!/usr/bin/env python3
"""Extract and validate JSON-LD locally. Stdlib only.

  python3 schema_lint.py https://example.com
  python3 schema_lint.py --html page.html --pretty

Exit: 0 ok · 1 validation errors · 2 usage/fetch error
"""
from __future__ import annotations
import argparse
import json
import re
import sys
from html.parser import HTMLParser

from _http import get as http_get

__version__ = "1.0"
_ISO_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}(?:[T ]\d{2}:\d{2}(?::\d{2})?(?:\.\d+)?(?:Z|[+-]\d{2}:?\d{2})?)?$")
_ABS_URL = re.compile(r"^https?://", re.I)

RULESET = {
    "Article": {"required": ["headline"], "recommended": ["image", "datePublished", "author", "publisher"]},
    "NewsArticle": {"required": ["headline"], "recommended": ["image", "datePublished", "author", "publisher"]},
    "BlogPosting": {"required": ["headline"], "recommended": ["image", "datePublished", "author", "publisher"]},
    "Product": {"required": ["name"], "recommended": ["image", "offers", "brand"]},
    "FAQPage": {
        "required": ["mainEntity"],
        "recommended": [],
        "deprecated": "FAQ rich results limited for most sites since 2025 — keep for AEO/semantic value.",
    },
    "HowTo": {
        "required": ["name", "step"],
        "recommended": ["image", "totalTime"],
        "deprecated": "HowTo rich results deprecated on desktop — keep for AEO value.",
    },
    "LocalBusiness": {"required": ["name", "address"], "recommended": ["telephone", "url", "geo"]},
    "Organization": {"required": ["name"], "recommended": ["url", "logo", "sameAs"]},
    "BreadcrumbList": {"required": ["itemListElement"], "recommended": []},
    "WebPage": {"required": ["name"], "recommended": ["description", "url"]},
}

_DATE_PROPS = {"datePublished", "dateModified", "uploadDate", "startDate", "endDate"}
_URL_PROPS = {"url", "contentUrl", "thumbnailUrl", "logo", "image"}


class LdExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.blocks = []
        self._cap = False
        self._buf = []

    def handle_starttag(self, tag, attrs):
        if tag == "script":
            a = dict(attrs)
            if "ld+json" in a.get("type", "").lower():
                self._cap = True
                self._buf = []

    def handle_data(self, data):
        if self._cap:
            self._buf.append(data)

    def handle_endtag(self, tag):
        if tag == "script" and self._cap:
            self._cap = False
            self.blocks.append("".join(self._buf))


def flatten(parsed):
    out = []
    items = parsed if isinstance(parsed, list) else [parsed]
    for item in items:
        if not isinstance(item, dict):
            continue
        g = item.get("@graph")
        if isinstance(g, list):
            out.extend(x for x in g if isinstance(x, dict))
        else:
            out.append(item)
    return out


def extract_jsonld(html):
    ext = LdExtractor()
    try:
        ext.feed(html)
    except Exception:
        pass
    nodes, errors = [], []
    for i, raw in enumerate(ext.blocks):
        text = raw.strip()
        if not text:
            continue
        try:
            nodes.extend(flatten(json.loads(text)))
        except json.JSONDecodeError as e:
            errors.append({"block": i, "error": str(e)})
    return nodes, errors


def types_of(obj):
    t = obj.get("@type")
    if t is None:
        return []
    return [str(x) for x in t] if isinstance(t, list) else [str(t)]


def has_prop(obj, prop):
    if prop not in obj or obj[prop] in (None, "", [], {}):
        return False
    return True


def validate_object(obj):
    types = types_of(obj)
    report = {
        "@type": types[0] if len(types) == 1 else (types or None),
        "recognized": False,
        "missing_required": [],
        "missing_recommended": [],
        "warnings": [],
        "sanity_issues": [],
    }
    for prop in _DATE_PROPS:
        v = obj.get(prop)
        if isinstance(v, str) and v.strip() and not _ISO_DATE.match(v.strip()):
            report["sanity_issues"].append(f"{prop} not ISO-8601: {v!r}")
    for prop in _URL_PROPS:
        v = obj.get(prop)
        if isinstance(v, str) and v.strip() and not _ABS_URL.match(v.strip()):
            report["sanity_issues"].append(f"{prop} should be absolute URL: {v!r}")

    matched = [t for t in types if t in RULESET]
    if not matched:
        if not types:
            report["warnings"].append("no @type")
        else:
            report["warnings"].append(f"type(s) not in ruleset: {', '.join(types)}")
        return report

    report["recognized"] = True
    for t in matched:
        rule = RULESET[t]
        for p in rule.get("required", []):
            if not has_prop(obj, p) and p not in report["missing_required"]:
                report["missing_required"].append(p)
        for p in rule.get("recommended", []):
            if not has_prop(obj, p) and p not in report["missing_recommended"]:
                report["missing_recommended"].append(p)
        if rule.get("deprecated"):
            report["warnings"].append("DEPRECATION: " + rule["deprecated"])
    return report


def lint_html(html, source="<html>"):
    nodes, parse_errors = extract_jsonld(html)
    objects = [validate_object(n) for n in nodes]
    errors = sum(len(o["missing_required"]) + len(o["sanity_issues"]) for o in objects) + len(parse_errors)
    warnings = sum(len(o["missing_recommended"]) + len(o["warnings"]) for o in objects)
    notes = []
    if not nodes and not parse_errors:
        notes.append("No JSON-LD found. Use Rich Results Test UI for final eligibility check.")
    return {
        "tool": "schema_lint",
        "version": __version__,
        "source": source,
        "objects": objects,
        "parse_errors": parse_errors,
        "summary": {"objects": len(objects), "recognized": sum(1 for o in objects if o["recognized"]), "errors": errors, "warnings": warnings},
        "notes": notes,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("url", nargs="?", help="URL to fetch")
    ap.add_argument("--html", help="HTML file or '-' for stdin")
    ap.add_argument("--pretty", action="store_true")
    args = ap.parse_args()
    if not args.url and not args.html:
        ap.error("provide URL or --html")
    if args.html:
        html = sys.stdin.read() if args.html == "-" else open(args.html, encoding="utf-8", errors="replace").read()
        source = args.html
    else:
        r = http_get(args.url)
        if r["status"] != 200 or not r["text"]:
            print(json.dumps({"error": r["error"] or f"HTTP {r['status']}"}), file=sys.stderr)
            return 2
        html, source = r["text"], r["url"]
    report = lint_html(html, source)
    if args.pretty:
        s = report["summary"]
        print(f"schema_lint {report['version']} — {source}")
        print(f"  objects: {s['objects']} | errors: {s['errors']} | warnings: {s['warnings']}")
        for i, o in enumerate(report["objects"]):
            print(f"  [{i}] @type={o['@type']}")
            for e in o["missing_required"]:
                print(f"    ERROR missing: {e}")
            for w in o["warnings"]:
                print(f"    WARN {w}")
    else:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    return 1 if report["summary"]["errors"] else 0


if __name__ == "__main__":
    sys.exit(main())
