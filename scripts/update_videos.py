#!/usr/bin/env python3
"""Refresh videos.json with the latest uploads from the party's YouTube channel.

Reads the channel's public RSS feed (no API key needed). If the feed can't be
fetched or has no videos, the existing videos.json is left untouched.

Usage: update_videos.py [feed.xml]   (optional local file, for testing)
"""
import json
import re
import sys
import time
import urllib.request
import xml.etree.ElementTree as ET

CHANNEL_ID = "UCzwjceEpfVS8S34zZ4yU6yg"
FEED_URL = f"https://www.youtube.com/feeds/videos.xml?channel_id={CHANNEL_ID}"
OUT_FILE = "videos.json"
MAX_VIDEOS = 6

NS = {
    "atom": "http://www.w3.org/2005/Atom",
    "yt": "http://www.youtube.com/xml/schemas/2015",
}


def fetch_feed():
    last_error = None
    for attempt in range(4):
        try:
            req = urllib.request.Request(FEED_URL, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=30) as resp:
                return resp.read()
        except Exception as e:  # network errors, 404/5xx from YouTube
            last_error = e
            time.sleep(2 ** attempt * 5)
    raise RuntimeError(f"could not fetch feed: {last_error}")


def parse(xml_bytes):
    root = ET.fromstring(xml_bytes)
    videos = []
    for entry in root.findall("atom:entry", NS):
        vid = entry.findtext("yt:videoId", default="", namespaces=NS).strip()
        if not re.fullmatch(r"[A-Za-z0-9_-]{11}", vid):
            continue
        videos.append({
            "id": vid,
            "title": entry.findtext("atom:title", default="", namespaces=NS).strip(),
            "published": entry.findtext("atom:published", default="", namespaces=NS).strip(),
        })
    videos.sort(key=lambda v: v["published"], reverse=True)
    return videos[:MAX_VIDEOS]


def main():
    try:
        data = open(sys.argv[1], "rb").read() if len(sys.argv) > 1 else fetch_feed()
        videos = parse(data)
    except Exception as e:
        print(f"warning: {e}; keeping existing {OUT_FILE}")
        return
    if not videos:
        print(f"warning: feed had no videos; keeping existing {OUT_FILE}")
        return
    with open(OUT_FILE, "w", encoding="utf-8") as f:
        json.dump(videos, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"wrote {len(videos)} videos to {OUT_FILE}")


if __name__ == "__main__":
    main()
