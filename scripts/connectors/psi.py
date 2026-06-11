#!/usr/bin/env python3
"""PageSpeed Insights v5 caller + Core Web Vitals analyzer. Stdlib only.

  python3 psi.py https://example.com
  python3 psi.py https://example.com --strategy desktop --key $PAGESPEED_API_KEY

Keyless works but may hit HTTP 429; set PAGESPEED_API_KEY for automation.
"""
from __future__ import annotations
import argparse
import json
import os
import sys
import urllib.parse

from _http import get_json

ENDPOINT = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"

LAB_AUDITS = {
    "largest-contentful-paint": "LCP_ms",
    "cumulative-layout-shift": "CLS",
    "total-blocking-time": "TBT_ms",
    "first-contentful-paint": "FCP_ms",
    "speed-index": "SI_ms",
    "interactive": "TTI_ms",
}

FIELD_METRICS = {
    "LARGEST_CONTENTFUL_PAINT_MS": "LCP_ms",
    "CUMULATIVE_LAYOUT_SHIFT_SCORE": "CLS",
    "INTERACTION_TO_NEXT_PAINT": "INP_ms",
}

CWV_THRESHOLDS = {
    "LCP_ms": (2500.0, 4000.0),
    "INP_ms": (200.0, 500.0),
    "CLS": (0.1, 0.25),
}


def grade(metric_key, value):
    if value is None:
        return None
    bounds = CWV_THRESHOLDS.get(metric_key)
    if not bounds:
        return None
    good_max, ni_max = bounds
    if value <= good_max:
        return "good"
    if value <= ni_max:
        return "needs-improvement"
    return "poor"


def _num(node):
    if not isinstance(node, dict):
        return None
    v = node.get("numericValue")
    return v if isinstance(v, (int, float)) else None


def parse(payload):
    report = {
        "ok": False,
        "url": None,
        "strategy": None,
        "performance_score": None,
        "lab": {},
        "field": None,
        "verdicts": {},
        "core_web_vitals_pass": None,
        "error": None,
    }
    if not isinstance(payload, dict):
        report["error"] = "response was not a JSON object"
        return report

    api_err = payload.get("error")
    if isinstance(api_err, dict):
        report["error"] = api_err.get("message") or "PSI API error"
        report["error_code"] = api_err.get("code")
        return report

    report["url"] = payload.get("id") or payload.get("loadingExperience", {}).get("id")
    lr = payload.get("lighthouseResult")
    if isinstance(lr, dict):
        report["strategy"] = (
            lr.get("configSettings", {}).get("formFactor")
            or lr.get("configSettings", {}).get("emulatedFormFactor")
        )
        score = lr.get("categories", {}).get("performance", {}).get("score")
        if isinstance(score, (int, float)):
            report["performance_score"] = round(score * 100, 1)
        audits = lr.get("audits", {}) or {}
        for audit_id, key in LAB_AUDITS.items():
            val = _num(audits.get(audit_id))
            entry = {
                "value": val,
                "displayValue": (audits.get(audit_id) or {}).get("displayValue"),
            }
            if key in CWV_THRESHOLDS:
                entry["verdict"] = grade(key, val)
            report["lab"][key] = entry

    le = payload.get("loadingExperience")
    if isinstance(le, dict) and le.get("metrics"):
        field = {"overall_category": le.get("overall_category"), "metrics": {}}
        for metric_id, mv in le["metrics"].items():
            key = FIELD_METRICS.get(metric_id, metric_id)
            pct = mv.get("percentile") if isinstance(mv, dict) else None
            norm = pct / 100.0 if key == "CLS" and isinstance(pct, (int, float)) else pct
            field["metrics"][key] = {
                "percentile": norm,
                "category": mv.get("category") if isinstance(mv, dict) else None,
                "verdict": grade(key, norm),
            }
        report["field"] = field

    verdicts = {}
    for key in ("LCP_ms", "INP_ms", "CLS"):
        src_val, src = None, None
        if report["field"] and key in report["field"]["metrics"]:
            src_val = report["field"]["metrics"][key]["percentile"]
            src = "field"
        elif key != "INP_ms" and key in report["lab"]:
            src_val = report["lab"][key]["value"]
            src = "lab"
        verdicts[key] = {"value": src_val, "source": src, "verdict": grade(key, src_val)}
    report["verdicts"] = verdicts

    graded = [v["verdict"] for v in verdicts.values() if v["verdict"] is not None]
    if graded:
        report["core_web_vitals_pass"] = all(v == "good" for v in graded)
    report["ok"] = report["performance_score"] is not None or bool(graded)
    return report


def build_url(target, strategy, key):
    params = [("url", target), ("strategy", strategy), ("category", "performance")]
    if key:
        params.append(("key", key))
    return ENDPOINT + "?" + urllib.parse.urlencode(params)


def fetch(target, strategy, key):
    url = build_url(target, strategy, key)
    r = get_json(url, timeout=90)
    if r["status"] == 200 and isinstance(r.get("json"), dict):
        rep = parse(r["json"])
        rep["strategy"] = rep.get("strategy") or strategy
        rep["url"] = rep.get("url") or target
        return rep, None
    if isinstance(r.get("json"), dict) and r["json"].get("error"):
        return parse(r["json"]), None
    hint = ""
    if r["status"] == 429:
        hint = " — quota exceeded; set PAGESPEED_API_KEY (free key)"
    return None, (r.get("error") or f"HTTP {r['status']}") + hint


def main():
    ap = argparse.ArgumentParser(description="PageSpeed Insights v5 + Core Web Vitals")
    ap.add_argument("url", nargs="?", help="Page URL to test")
    ap.add_argument("--strategy", choices=["mobile", "desktop"], default="mobile")
    ap.add_argument("--key", help="PageSpeed API key (else env PAGESPEED_API_KEY)")
    ap.add_argument("--file", help="Parse saved PSI JSON instead of calling API")
    args = ap.parse_args()

    if args.file:
        with open(args.file, encoding="utf-8") as fh:
            payload = json.load(fh)
        report = parse(payload)
        report["strategy"] = report.get("strategy") or args.strategy
        print(json.dumps(report, indent=2, ensure_ascii=False))
        return 0 if report.get("core_web_vitals_pass") else (3 if report.get("ok") else 2)

    if not args.url:
        ap.error("a url is required unless --file is given")

    key = args.key or os.environ.get("PAGESPEED_API_KEY")
    report, err = fetch(args.url, args.strategy, key)
    if report is None:
        print(json.dumps({"ok": False, "url": args.url, "strategy": args.strategy, "error": err}, indent=2))
        return 2

    print(json.dumps(report, indent=2, ensure_ascii=False))
    if not report.get("ok"):
        return 2
    return 0 if report.get("core_web_vitals_pass") else 3


if __name__ == "__main__":
    sys.exit(main())
