#!/usr/bin/env python3
"""SearchHawk HTML report generator. Stdlib only.

Turns a JSON report payload into a self-contained, styled HTML report
(inline CSS, inline SVG charts — no external assets, safe to email or host).

  python3 report_html.py report.json -o report.html
  python3 report_html.py report.json                  # writes report.html next to input
  python3 report_html.py --sample > report.json       # print sample payload / schema
  python3 report_html.py report.json --theme dark

All values in the payload are treated as data and HTML-escaped. Every metric
should carry a source tag: "measured", "user", or "estimated" — never present
an estimate as measured.
"""
from __future__ import annotations
import argparse
import datetime
import html
import json
import sys
from pathlib import Path

SAMPLE = {
    "title": "SEO & GEO Performance Report",
    "domain": "example.com",
    "period": "May 2026",
    "compared_to": "April 2026",
    "prepared": "2026-06-12",
    "overall": "good",
    "summary": (
        "Organic clicks up 12% period-over-period. Impressions flat. "
        "Two money pages lost positions — content decay suspected, not seasonality."
    ),
    "highlights": {
        "wins": ["Branded CTR +0.8pt", "/guides/descale-breville +24% sessions"],
        "watch": ["/guides/best-espresso-under-500 clicks −22%"],
        "actions": ["Refresh decaying guide", "Add FAQ schema to top 3 guides"],
    },
    "metrics": [
        {"label": "Organic Clicks", "value": 12480, "previous": 11120, "target": 13000, "source": "measured"},
        {"label": "Impressions", "value": 411000, "previous": 408500, "source": "measured"},
        {"label": "Avg CTR", "value": "3.0%", "previous": "2.7%", "delta": "+0.3pt", "direction": "up", "source": "measured"},
        {"label": "Keywords in Top 10", "value": 42, "previous": 38, "source": "user"},
        {"label": "AI Citations", "value": 9, "previous": 6, "source": "user"},
        {"label": "Hawk-Trust Score", "value": "78/100", "delta": "n/a", "direction": "flat", "source": "estimated"},
    ],
    "sections": [
        {
            "title": "Top Queries (GSC)",
            "source": "measured",
            "table": {
                "headers": ["Query", "Clicks", "Δ", "Avg position"],
                "rows": [
                    ["homebrew beans", 842, "+5%", 1.2],
                    ["best espresso under 500", 118, "−22%", 14.1],
                    ["descale breville barista", 76, "+18%", 6.4],
                ],
            },
        },
        {
            "title": "Organic Sessions by Landing Page",
            "source": "measured",
            "chart": {
                "items": [
                    {"label": "/", "value": 3210},
                    {"label": "/guides/best-espresso-under-500", "value": 890},
                    {"label": "/guides/descale-breville", "value": 412},
                ]
            },
        },
        {
            "title": "Backlinks",
            "status": "not-evaluated",
            "text": "No link data provided this period. Run domain-trust-check or connect an SEO MCP server.",
        },
    ],
    "recommendations": [
        {"action": "Refresh /guides/best-espresso-under-500", "priority": "high",
         "impact": "Recover ~200 clicks/mo", "owner": "Content", "skill": "content-updater"},
        {"action": "Add FAQPage schema to top 3 guides", "priority": "medium",
         "impact": "AEO snippet eligibility", "owner": "Dev", "skill": "schema-helper"},
    ],
    "sources": ["GSC export 2026-06-10", "GA4 export 2026-06-10", "psi.py mobile run"],
}

STATUS_META = {
    "excellent": ("Excellent", "#1a7f37"),
    "good": ("Good", "#1a7f37"),
    "watch": ("Watch", "#9a6700"),
    "needs-attention": ("Needs attention", "#9a6700"),
    "critical": ("Critical", "#cf222e"),
}

SOURCE_LABEL = {"measured": "Measured", "user": "User-provided", "estimated": "Estimated"}

PRIORITY_COLOR = {"high": "#cf222e", "medium": "#9a6700", "low": "#1a7f37"}

THEMES = {
    "light": {
        "bg": "#f6f7f9", "card": "#ffffff", "ink": "#1c1f23", "mute": "#646b74",
        "line": "#e4e7eb", "accent": "#d11a0e", "chart": "#d11a0e",
        "table_head": "#f0f2f5", "shadow": "0 1px 3px rgba(16,20,24,0.07)",
    },
    "dark": {
        "bg": "#101418", "card": "#1a2026", "ink": "#e8eaed", "mute": "#9aa3ad",
        "line": "#2b333c", "accent": "#ff5a4e", "chart": "#ff5a4e",
        "table_head": "#222a32", "shadow": "0 1px 3px rgba(0,0,0,0.4)",
    },
}


def esc(value):
    return html.escape(str(value), quote=True)


def to_number(value):
    try:
        return float(str(value).replace(",", "").replace("%", ""))
    except (ValueError, TypeError):
        return None


def fmt_number(value):
    n = to_number(value)
    if n is None:
        return esc(value)
    if isinstance(value, str) and not value.replace(",", "").replace(".", "").isdigit():
        return esc(value)
    if n == int(n):
        return f"{int(n):,}"
    return f"{n:,.2f}"


def compute_delta(metric):
    """Return (delta_text, direction). Honors explicit 'delta'/'direction' keys."""
    direction = metric.get("direction")
    if "delta" in metric:
        return str(metric["delta"]), direction or "flat"
    cur, prev = to_number(metric.get("value")), to_number(metric.get("previous"))
    if cur is None or prev is None or prev == 0:
        return "", direction or "flat"
    pct = (cur - prev) / abs(prev) * 100
    direction = direction or ("up" if pct > 0.05 else "down" if pct < -0.05 else "flat")
    sign = "+" if pct >= 0 else "−"
    return f"{sign}{abs(pct):.1f}%", direction


def source_tag(source, theme):
    if not source:
        return ""
    label = SOURCE_LABEL.get(str(source).lower(), str(source))
    return (
        f'<span style="font-size:11px;color:{theme["mute"]};border:1px solid {theme["line"]};'
        f'border-radius:10px;padding:1px 8px;vertical-align:middle">{esc(label)}</span>'
    )


def render_metric_card(metric, theme):
    delta_text, direction = compute_delta(metric)
    arrow = {"up": "▲", "down": "▼", "flat": "■"}.get(direction, "■")
    color = {"up": "#1a7f37", "down": "#cf222e", "flat": theme["mute"]}.get(direction, theme["mute"])
    prev_html = ""
    if metric.get("previous") is not None:
        prev_html = (
            f'<div style="font-size:12px;color:{theme["mute"]};margin-top:4px">'
            f'prev {fmt_number(metric["previous"])}</div>'
        )
    target_html = ""
    if metric.get("target") is not None:
        target_html = (
            f'<div style="font-size:12px;color:{theme["mute"]}">target {fmt_number(metric["target"])}</div>'
        )
    delta_html = ""
    if delta_text:
        delta_html = (
            f'<span style="color:{color};font-size:13px;font-weight:600;margin-left:8px">'
            f'{arrow} {esc(delta_text)}</span>'
        )
    return f"""
    <div style="background:{theme['card']};border:1px solid {theme['line']};border-radius:10px;
                padding:18px 20px;box-shadow:{theme['shadow']}">
      <div style="font-size:13px;color:{theme['mute']};margin-bottom:6px">
        {esc(metric.get('label', ''))} {source_tag(metric.get('source'), theme)}
      </div>
      <div style="font-size:28px;font-weight:700;color:{theme['ink']};line-height:1.1">
        {fmt_number(metric.get('value', '—'))}{delta_html}
      </div>
      {prev_html}{target_html}
    </div>"""


def render_table(table, theme):
    headers = table.get("headers", [])
    rows = table.get("rows", [])
    th = "".join(
        f'<th style="text-align:left;padding:10px 14px;font-size:12px;text-transform:uppercase;'
        f'letter-spacing:0.04em;color:{theme["mute"]};border-bottom:1px solid {theme["line"]}">'
        f"{esc(h)}</th>"
        for h in headers
    )
    body_rows = []
    for row in rows:
        tds = []
        for cell in row:
            cell_str = str(cell)
            color = theme["ink"]
            if cell_str.startswith(("+",)):
                color = "#1a7f37"
            elif cell_str.startswith(("−", "-")) and to_number(cell_str.lstrip("−-")) is not None:
                color = "#cf222e"
            tds.append(
                f'<td style="padding:10px 14px;font-size:14px;color:{color};'
                f'border-bottom:1px solid {theme["line"]}">{esc(cell)}</td>'
            )
        body_rows.append("<tr>" + "".join(tds) + "</tr>")
    return (
        f'<table style="width:100%;border-collapse:collapse;background:{theme["card"]}">' 
        f"<thead><tr>{th}</tr></thead><tbody>{''.join(body_rows)}</tbody></table>"
    )


def render_chart(chart, theme):
    items = chart.get("items", [])
    if not items:
        return ""
    max_value = max((to_number(i.get("value")) or 0) for i in items) or 1
    bar_h, gap, label_w = 26, 10, 240
    width = 720
    height = len(items) * (bar_h + gap)
    bars = []
    for idx, item in enumerate(items):
        value = to_number(item.get("value")) or 0
        bar_len = max(2, (width - label_w - 90) * value / max_value)
        y = idx * (bar_h + gap)
        label = str(item.get("label", ""))
        if len(label) > 34:
            label = label[:31] + "…"
        bars.append(
            f'<text x="0" y="{y + bar_h / 2 + 4}" font-size="13" fill="{theme["mute"]}">{esc(label)}</text>'
            f'<rect x="{label_w}" y="{y}" width="{bar_len:.0f}" height="{bar_h}" rx="3" fill="{theme["chart"]}" opacity="0.85"/>'
            f'<text x="{label_w + bar_len + 8:.0f}" y="{y + bar_h / 2 + 4}" font-size="13" '
            f'font-weight="600" fill="{theme["ink"]}">{fmt_number(value)}</text>'
        )
    return (
        f'<svg viewBox="0 0 {width} {height}" width="100%" role="img" '
        f'style="max-width:{width}px;font-family:inherit">{"".join(bars)}</svg>'
    )


def render_section(section, theme):
    status = str(section.get("status", "")).lower()
    badge = ""
    if status == "not-evaluated":
        badge = (
            f'<span style="font-size:11px;color:{theme["mute"]};border:1px dashed {theme["line"]};'
            f'border-radius:10px;padding:2px 10px;margin-left:10px">Not yet evaluated</span>'
        )
    parts = [
        f'<h2 style="font-size:18px;font-weight:700;color:{theme["ink"]};margin:36px 0 14px">' 
        f'{esc(section.get("title", ""))} {source_tag(section.get("source"), theme)}{badge}</h2>'
    ]
    if section.get("text"):
        parts.append(
            f'<p style="font-size:14px;line-height:1.6;color:{theme["mute"]};margin:0 0 12px">'
            f'{esc(section["text"])}</p>'
        )
    if section.get("table"):
        parts.append(
            f'<div style="background:{theme["card"]};border:1px solid {theme["line"]};border-radius:10px;'
            f'overflow:hidden;box-shadow:{theme["shadow"]}">{render_table(section["table"], theme)}</div>'
        )
    if section.get("chart"):
        parts.append(
            f'<div style="background:{theme["card"]};border:1px solid {theme["line"]};border-radius:10px;'
            f'padding:20px;box-shadow:{theme["shadow"]}">{render_chart(section["chart"], theme)}</div>'
        )
    return "".join(parts)


def render_highlights(highlights, theme):
    if not highlights:
        return ""
    columns = []
    for key, heading, color in (
        ("wins", "Wins", "#1a7f37"),
        ("watch", "Watch areas", "#9a6700"),
        ("actions", "Action required", theme["accent"]),
    ):
        entries = highlights.get(key) or []
        if not entries:
            continue
        lis = "".join(
            f'<li style="font-size:14px;line-height:1.6;color:{theme["ink"]}">{esc(e)}</li>'
            for e in entries
        )
        columns.append(
            f'<div style="flex:1;min-width:200px;background:{theme["card"]};border:1px solid {theme["line"]};'
            f'border-radius:10px;padding:16px 20px;box-shadow:{theme["shadow"]}">' 
            f'<div style="font-size:13px;font-weight:700;color:{color};margin-bottom:8px;'
            f'text-transform:uppercase;letter-spacing:0.04em">{heading}</div>'
            f'<ul style="margin:0;padding-left:18px">{lis}</ul></div>'
        )
    if not columns:
        return ""
    return f'<div style="display:flex;flex-wrap:wrap;gap:14px;margin-top:18px">{"".join(columns)}</div>'


def render_recommendations(recs, theme):
    if not recs:
        return ""
    rows = []
    for rec in recs:
        priority = str(rec.get("priority", "medium")).lower()
        p_color = PRIORITY_COLOR.get(priority, theme["mute"])
        skill = rec.get("skill")
        skill_html = (
            f'<code style="font-size:12px;background:{theme["table_head"]};border-radius:4px;'
            f'padding:2px 7px;color:{theme["ink"]}">{esc(skill)}</code>' if skill else "—"
        )
        rows.append(
            "<tr>"
            f'<td style="padding:10px 14px;border-bottom:1px solid {theme["line"]}">'
            f'<span style="display:inline-block;font-size:11px;font-weight:700;color:#fff;'
            f'background:{p_color};border-radius:10px;padding:2px 10px;text-transform:uppercase">'
            f"{esc(priority)}</span></td>"
            f'<td style="padding:10px 14px;font-size:14px;color:{theme["ink"]};'
            f'border-bottom:1px solid {theme["line"]}">{esc(rec.get("action", ""))}</td>'
            f'<td style="padding:10px 14px;font-size:13px;color:{theme["mute"]};'
            f'border-bottom:1px solid {theme["line"]}">{esc(rec.get("impact", "—"))}</td>'
            f'<td style="padding:10px 14px;font-size:13px;color:{theme["mute"]};'
            f'border-bottom:1px solid {theme["line"]}">{esc(rec.get("owner", "—"))}</td>'
            f'<td style="padding:10px 14px;border-bottom:1px solid {theme["line"]}">{skill_html}</td>'
            "</tr>"
        )
    head = "".join(
        f'<th style="text-align:left;padding:10px 14px;font-size:12px;text-transform:uppercase;'
        f'letter-spacing:0.04em;color:{theme["mute"]};border-bottom:1px solid {theme["line"]}">{h}</th>'
        for h in ("Priority", "Action", "Expected impact", "Owner", "Next skill")
    )
    return (
        f'<h2 style="font-size:18px;font-weight:700;color:{theme["ink"]};margin:36px 0 14px">'
        "Recommendations</h2>"
        f'<div style="background:{theme["card"]};border:1px solid {theme["line"]};border-radius:10px;'
        f'overflow:hidden;box-shadow:{theme["shadow"]}">'
        f'<table style="width:100%;border-collapse:collapse"><thead><tr>{head}</tr></thead>'
        f'<tbody>{"".join(rows)}</tbody></table></div>'
    )


def build_html(data, theme_name="light"):
    theme = THEMES.get(theme_name, THEMES["light"])
    title = data.get("title", "SEO Performance Report")
    domain = data.get("domain", "")
    period = data.get("period", "")
    compared = data.get("compared_to", "")
    prepared = data.get("prepared") or datetime.date.today().isoformat()
    overall = str(data.get("overall", "")).lower()
    overall_label, overall_color = STATUS_META.get(overall, ("", theme["mute"]))

    meta_bits = [b for b in (
        f"<strong>{esc(domain)}</strong>" if domain else "",
        f"Period: {esc(period)}" if period else "",
        f"vs {esc(compared)}" if compared else "",
        f"Prepared: {esc(prepared)}",
    ) if b]
    overall_html = ""
    if overall_label:
        overall_html = (
            f'<span style="display:inline-block;font-size:13px;font-weight:700;color:#fff;'
            f'background:{overall_color};border-radius:14px;padding:4px 14px;margin-left:14px;'
            f'vertical-align:middle">{overall_label}</span>'
        )

    metric_cards = "".join(render_metric_card(m, theme) for m in data.get("metrics", []))
    sections_html = "".join(render_section(s, theme) for s in data.get("sections", []))
    summary_html = ""
    if data.get("summary"):
        summary_html = (
            f'<p style="font-size:16px;line-height:1.65;color:{theme["ink"]};max-width:72ch;'
            f'margin:18px 0 0">{esc(data["summary"])}</p>'
        )
    sources_html = ""
    if data.get("sources"):
        items = " · ".join(esc(s) for s in data["sources"])
        sources_html = (
            f'<p style="font-size:12px;color:{theme["mute"]};margin-top:8px">Data sources: {items}</p>'
        )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(title)}{' — ' + esc(domain) if domain else ''}</title>
<style>
  @media print {{ body {{ background: #fff !important; }} .card-grid > div {{ break-inside: avoid; }} }}
  @media (max-width: 640px) {{ .card-grid {{ grid-template-columns: 1fr !important; }} }}
</style>
</head>
<body style="margin:0;background:{theme['bg']};font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;-webkit-font-smoothing:antialiased">
<div style="max-width:880px;margin:0 auto;padding:48px 24px 64px">
  <header style="border-bottom:3px solid {theme['accent']};padding-bottom:24px">
    <div style="font-size:12px;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;color:{theme['accent']}">
      SearchHawk Report
    </div>
    <h1 style="font-size:30px;font-weight:800;color:{theme['ink']};margin:10px 0 8px;line-height:1.15">
      {esc(title)}{overall_html}
    </h1>
    <div style="font-size:14px;color:{theme['mute']}">{' &nbsp;·&nbsp; '.join(meta_bits)}</div>
    {summary_html}
  </header>

  {render_highlights(data.get('highlights'), theme)}

  <div class="card-grid" style="display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:14px;margin-top:28px">
    {metric_cards}
  </div>

  {sections_html}

  {render_recommendations(data.get('recommendations'), theme)}

  <footer style="margin-top:48px;padding-top:18px;border-top:1px solid {theme['line']}">
    <p style="font-size:12px;color:{theme['mute']};margin:0">
      Generated by SearchHawk Skills · performance-snapshot · metrics tagged Measured / User-provided / Estimated
    </p>
    {sources_html}
  </footer>
</div>
</body>
</html>"""


def main():
    parser = argparse.ArgumentParser(description="SearchHawk HTML report generator (stdlib only)")
    parser.add_argument("input", nargs="?", help="Path to report JSON payload")
    parser.add_argument("-o", "--output", help="Output HTML path (default: <input>.html)")
    parser.add_argument("--theme", choices=sorted(THEMES), default="light")
    parser.add_argument("--sample", action="store_true", help="Print sample JSON payload and exit")
    args = parser.parse_args()

    if args.sample:
        json.dump(SAMPLE, sys.stdout, indent=2, ensure_ascii=False)
        print()
        return 0

    if not args.input:
        parser.error("provide a report JSON file, or --sample to see the payload schema")

    src = Path(args.input)
    try:
        data = json.loads(src.read_text(encoding="utf-8"))
    except FileNotFoundError:
        print(f"error: {src} not found", file=sys.stderr)
        return 1
    except json.JSONDecodeError as e:
        print(f"error: invalid JSON in {src}: {e}", file=sys.stderr)
        return 1

    out = Path(args.output) if args.output else src.with_suffix(".html")
    out.write_text(build_html(data, args.theme), encoding="utf-8")
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
