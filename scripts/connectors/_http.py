"""SearchHawk connector HTTP helpers — stdlib only."""
from __future__ import annotations
import gzip
import json
import time
import urllib.error
import urllib.request

USER_AGENT = "SearchHawk-Connector/2.3 (+https://github.com/creativehassan/searchhawk-skills)"
TIMEOUT = 20
MAX_BYTES = 2_000_000


def get(url, headers=None, timeout=TIMEOUT):
    h = {"User-Agent": USER_AGENT, "Accept-Encoding": "gzip"}
    if headers:
        h.update(headers)
    req = urllib.request.Request(url, headers=h)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = resp.read(MAX_BYTES + 1)
            if len(body) > MAX_BYTES:
                body = body[:MAX_BYTES]
            if resp.headers.get("Content-Encoding") == "gzip":
                body = gzip.decompress(body)
            text = body.decode("utf-8", errors="replace")
            return {
                "url": resp.geturl(),
                "status": resp.status,
                "headers": dict(resp.headers),
                "text": text,
                "body": body,
                "error": None,
            }
    except urllib.error.HTTPError as e:
        body = e.read(MAX_BYTES) if e.fp else b""
        text = body.decode("utf-8", errors="replace") if body else ""
        return {
            "url": url,
            "status": e.code,
            "headers": dict(e.headers or {}),
            "text": text,
            "body": body,
            "error": str(e),
        }
    except Exception as e:
        return {"url": url, "status": 0, "headers": {}, "text": "", "body": b"", "error": str(e)}


def get_json(url, timeout=TIMEOUT):
    r = get(url, headers={"Accept": "application/json"}, timeout=timeout)
    parsed = None
    if r["text"]:
        try:
            parsed = json.loads(r["text"])
        except json.JSONDecodeError:
            pass
    r["json"] = parsed
    return r


def polite_sleep(seconds):
    if seconds > 0:
        time.sleep(seconds)
