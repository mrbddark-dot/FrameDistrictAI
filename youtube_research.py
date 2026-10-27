import yt_dlp
from datetime import datetime

print("\n=== FRAME DISTRICT | YOUTUBE USA RESEARCH ===")
print("Checked:", datetime.now().strftime("%Y-%m-%d %H:%M"))
print("Research only — no videos will be downloaded.\n")

topics = []
try:
    with open("usa_trends.txt", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and line[0].isdigit() and ". " in line:
                topic = line.split(". ", 1)[1].split(" | Search traffic:")[0]
                topics.append(topic)
except FileNotFoundError:
    print("usa_trends.txt not found. First run: python trends.py")
    raise SystemExit

if not topics:
    print("No topics found. Run: python trends.py")
    raise SystemExit

options = {
    "quiet": True,
    "no_warnings": True,
    "skip_download": True,
    "extract_flat": True,
    "ignoreerrors": True,
    "socket_timeout": 20,
}

with yt_dlp.YoutubeDL(options) as ydl:
    for topic in topics[:5]:
        print(f"\n--- TOPIC: {topic} ---")
        try:
            result = ydl.extract_info(
                "ytsearch5:" + topic,
                download=False
            )
            entries = (result or {}).get("entries") or []
            if not entries:
                print("No results returned.")
                continue

            for i, video in enumerate(entries, 1):
                if not video:
                    continue
                title = video.get("title", "Unknown title")
                channel = video.get("channel") or video.get("uploader") or "Unknown channel"
                views = video.get("view_count")
                url = video.get("url") or video.get("webpage_url")
                if url and not str(url).startswith("http"):
                    url = "https://www.youtube.com/watch?v=" + str(url)
                print(f"{i}. {title}")
                print(f"   Channel: {channel}")
                print(f"   Views: {views if views is not None else 'Not available'}")
                print(f"   URL: {url or 'Not available'}")
        except Exception as e:
            print("Search failed:", str(e)[:180])

print("\nResearch finished.")
