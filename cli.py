#!/usr/bin/env python3
"""
MovieBox CLI - Movie name se direct proxy stream links nikaalo
Usage:
  1. Pehle server chalao:  python main.py
  2. Dusre terminal mein:  python cli.py
"""

import sys
import os
from urllib.parse import quote

# Add current dir
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from api import MovieBoxEngine, engine

PROXY_BASE = "http://127.0.0.1:8000/proxy"

def make_proxy(url: str, referer: str = "https://123moviesfree.club/") -> str:
    return f"{PROXY_BASE}?url={quote(url, safe='')}&referer={quote(referer, safe='')}"

def print_banner():
    print("\n" + "="*60)
    print("  MovieBox CLI  |  Movie name → All Quality Proxy Links")
    print("="*60)
    print("  Server chal raha hona chahiye:  python main.py")
    print("  Proxy base: http://127.0.0.1:8000/proxy")
    print("="*60 + "\n")

def search_and_pick():
    while True:
        query = input("\n🎬 Movie / Series ka naam daalo (ya 'q' quit): ").strip()
        if not query or query.lower() in ("q", "quit", "exit"):
            print("Bye!")
            return None

        print(f"\n🔍 Searching: {query} ...")
        try:
            results = engine.search(query, page=1, per_page=15)
        except Exception as e:
            print(f"❌ Search failed: {e}")
            print("   (Server chal raha hai? Region India/allowed hai?)")
            continue

        if not results:
            print("Kuch nahi mila. Dusra naam try karo.")
            continue

        print(f"\n📋 {len(results)} results:\n")
        for i, r in enumerate(results, 1):
            year = (r.get("release_date") or "")[:4]
            rating = r.get("imdb_rating") or "-"
            typ = r.get("type") or "?"
            print(f"  {i:2d}. [{typ}] {r.get('title')}  ({year})  ⭐ {rating}")

        print()
        choice = input("Number choose karo (ya Enter = dubara search): ").strip()
        if not choice:
            continue
        try:
            idx = int(choice) - 1
            if idx < 0 or idx >= len(results):
                print("Invalid number")
                continue
        except ValueError:
            print("Number daalo")
            continue

        return results[idx]

def get_season_ep(item):
    if item.get("type") != "Series" and item.get("subject_type") != 2:
        return 0, 0

    print("\n📺 Yeh Series hai.")
    try:
        seasons = engine.get_episodes(item["subject_id"])
        if seasons:
            print("Available seasons:")
            for s in seasons:
                print(f"  Season {s['season']} → {s['episode_count']} episodes")
    except Exception:
        seasons = []

    se = input("Season number (default 1): ").strip() or "1"
    ep = input("Episode number (default 1): ").strip() or "1"
    try:
        return int(se), int(ep)
    except:
        return 1, 1

def show_streams(item, se=0, ep=0):
    sid = item["subject_id"]
    title = item.get("title", "Unknown")
    print(f"\n⏳ Streams nikaal raha hun: {title}")
    if se or ep:
        print(f"   Season {se} Episode {ep}")

    try:
        streams = engine.get_streams(sid, season=se, episode=ep, detail_path=item.get("detail_path"))
    except Exception as e:
        print(f"❌ Stream error: {e}")
        return

    if not streams:
        print("Koi stream nahi mila.")
        return

    # Sort by quality high → low
    streams = sorted(streams, key=lambda x: x.get("quality_value") or 0, reverse=True)

    print(f"\n✅ {len(streams)} streams mil gaye:\n")
    print("-" * 70)

    for i, st in enumerate(streams, 1):
        quality = st.get("quality") or st.get("resolution_tag") or "?"
        size = st.get("size_mb")
        size_str = f"{size} MB" if size else "?"
        fmt = st.get("format", "MP4")
        source = st.get("source", "")
        url = st.get("url")
        referer = (st.get("headers") or {}).get("Referer", "https://123moviesfree.club/")

        proxy = make_proxy(url, referer)

        print(f"[{i}] {quality}  |  {fmt}  |  {size_str}  |  {source}")
        print(f"    PROXY → {proxy}")
        print()

    print("-" * 70)
    print("👆 Upar wale PROXY links ko VLC / MX Player / browser mein kholo.")
    print("   (Server chalna zaroori hai tabhi proxy kaam karega)")
    print()

def main():
    print_banner()
    print("Engine ready. (Pehli baar thoda time lag sakta hai token ke liye)\n")

    while True:
        item = search_and_pick()
        if item is None:
            break

        se, ep = get_season_ep(item)
        show_streams(item, se, ep)

        again = input("Aur movie search karni hai? (y/n): ").strip().lower()
        if again not in ("y", "yes", "ha", "h"):
            print("Bye!")
            break

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nBye!")
