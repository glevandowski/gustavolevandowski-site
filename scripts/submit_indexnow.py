#!/usr/bin/env python3
"""Submit canonical URLs to IndexNow (Bing, Yandex, etc.)."""
from __future__ import annotations
import json, sys, urllib.request
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
keys = list(ROOT.glob("[0-9a-f]*.txt"))
keys = [k for k in keys if len(k.stem) >= 32 and k.stem.isalnum()]
if not keys:
    sys.exit("No IndexNow key file found at repo root")
key = keys[0].stem
host = "gustavolevandowski.com"
urls = [
    f"https://{host}/",
    f"https://{host}/en/",
    f"https://{host}/pt/",
    f"https://{host}/sitemap.xml",
    f"https://{host}/llms.txt",
    f"https://{host}/robots.txt",
]
payload = {
    "host": host,
    "key": key,
    "keyLocation": f"https://{host}/{key}.txt",
    "urlList": urls,
}
req = urllib.request.Request(
    "https://api.indexnow.org/indexnow",
    data=json.dumps(payload).encode(),
    headers={"Content-Type": "application/json; charset=utf-8"},
    method="POST",
)
try:
    with urllib.request.urlopen(req, timeout=30) as res:
        print(f"IndexNow {res.status}")
        print(res.read().decode() or "(empty body)")
except Exception as e:
    print("IndexNow request failed:", e)
    # Still print payload for manual retry after deploy
    print(json.dumps(payload, indent=2))
    sys.exit(1)
print("Submitted:", *urls, sep="\n  ")
