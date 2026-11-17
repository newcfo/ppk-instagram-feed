#!/usr/bin/env python3
"""Build a public weekly six-post Instagram snapshot for GitHub Pages.

Only public Behold feed metadata are exposed. No credentials or OAuth tokens.
"""
import datetime as dt
import json
import pathlib
from urllib.parse import urlparse
from urllib.request import Request, urlopen

FEED_URL = "https://feeds.behold.so/fKa88VuEXiiD0hwbuOJQ"
EXPECTED_USERNAME = "perfectpotion.kr"
SITE = pathlib.Path("_site")


def is_good_url(url, allowed_hosts=None, behold_images=False):
    if not isinstance(url, str):
        return False
    p = urlparse(url)
    if p.scheme != "https" or p.username or p.password or not p.hostname:
        return False
    host = p.hostname.lower()
    if behold_images:
        return host == "behold.pictures" or host.endswith(".behold.pictures")
    return host in allowed_hosts


def build_payload(feed, now=None):
    if not isinstance(feed, dict) or not isinstance(feed.get("posts"), list):
        raise ValueError("Expected Behold JSON with a posts array")
    if str(feed.get("username", "")).lstrip("@").lower() != EXPECTED_USERNAME:
        raise ValueError("Unexpected Instagram account: refusing publication")
    items = []
    seen = set()
    for post in sorted(feed["posts"], key=lambda x: x.get("timestamp") or "", reverse=True):
        link = post.get("permalink")
        if not is_good_url(link, {"www.instagram.com", "instagram.com"}):
            continue
        if not urlparse(link).path.startswith(("/p/", "/reel/", "/tv/")):
            continue
        if link in seen:
            continue
        sizes = post.get("sizes") or {}
        image = None
        for size in ("medium", "small", "large", "full"):
            v = sizes.get(size) or {}
            candidate = v.get("mediaUrl") if isinstance(v, dict) else None
            if is_good_url(candidate, behold_images=True):
                image = candidate
                break
        if not image:
            continue
        caption = str(post.get("altText") or post.get("prunedCaption") or "퍼펙트포션 인스타그램 게시물")
        caption = " ".join(caption.split())[:160]
        items.append({
            "url": link,
            "image": image,
            "alt": caption,
            "reel": bool(post.get("isReel")),
        })
        seen.add(link)
        if len(items) == 6:
            break
    if len(items) != 6:
        raise ValueError(f"Expected 6 valid posts, got {len(items)}; preserving last successful deployment")
    stamp = now if now is not None else dt.datetime.now(dt.timezone.utc)
    return {"username": EXPECTED_USERNAME, "updatedAt": stamp.isoformat(), "posts": items}


def build_js(payload):
    encoded = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
    encoded = encoded.replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")
    encoded = encoded.replace("\u2028", "\\u2028").replace("\u2029", "\\u2029")
    return "window.PPK_INSTAGRAM_WEEKLY = " + encoded + ";\n"


def main():
    req = Request(FEED_URL, headers={"User-Agent": "PPK-Public-Weekly-Snapshot/1.0"})
    with urlopen(req, timeout=25) as response:
        feed = json.load(response)
    payload = build_payload(feed)
    SITE.mkdir(parents=True, exist_ok=True)
    (SITE / ".nojekyll").write_text("", encoding="utf-8")
    (SITE / "ppk-instagram-weekly.js").write_text(build_js(payload), encoding="utf-8")
    (SITE / "index.html").write_text(
        '<!doctype html><html lang="ko"><meta charset="utf-8"><title>PPK Instagram weekly feed</title>'
        '<h1>Perfect Potion Instagram weekly feed</h1>'
        '<p>Public asset: <a href="ppk-instagram-weekly.js">ppk-instagram-weekly.js</a></p>'
        '<p>This endpoint contains only links to public Instagram posts and thumbnails.</p></html>',
        encoding="utf-8",
    )
    print(f"Prepared GitHub Pages snapshot: {len(payload['posts'])} posts")


if __name__ == "__main__":
    main()
