import yt_dlp
from datetime import datetime, timezone

def age_days(upload_date):
    if not upload_date:
        return None
    try:
        d = datetime.strptime(upload_date, "%Y%m%d").replace(tzinfo=timezone.utc)
        return (datetime.now(timezone.utc) - d).days
    except ValueError:
        return None

with open("usa_trends.txt", encoding="utf-8") as f:
    topics = []
    for line in f:
        line = line.strip()
        if line and line[0].isdigit() and ". " in line:
            topics.append(line.split(". ", 1)[1].split(" | Search traffic:")[0])

opts = {
    "quiet": True,
    "no_warnings": True,
    "skip_download": True,
    "ignoreerrors": True,
    "socket_timeout": 20,
}

results = []

with yt_dlp.YoutubeDL(opts) as ydl:
    for topic in topics[:5]:
        print(f"\nSearching: {topic}")
        try:
            data = ydl.extract_info("ytsearch5:" + topic, download=False)
            for v in (data or {}).get("entries") or []:
                if not v:
                    continue
                days = age_days(v.get("upload_date"))
                views = v.get("view_count")
                item = {
                    "topic": topic,
                    "title": v.get("title", "Unknown"),
                    "channel": v.get("channel") or v.get("uploader") or "Unknown",
                    "views": views,
                    "date": v.get("upload_date") or "Unknown",
                    "days": days,
                    "url": v.get("webpage_url") or v.get("url") or ""
                }
                results.append(item)
                print(f"  {item['title']}")
                print(f"  Channel: {item['channel']} | Views: {views if views is not None else 'N/A'}")
                print(f"  Upload date: {item['date']} | Age (days): {days if days is not None else 'N/A'}")
        except Exception as e:
            print("Search error:", str(e)[:150])

with open("trend_report.txt", "w", encoding="utf-8") as f:
    for v in results:
        f.write(
            f"Topic: {v['topic']}\nTitle: {v['title']}\n"
            f"Channel: {v['channel']}\nViews: {v['views']}\n"
            f"Upload date: {v['date']}\nAge days: {v['days']}\n"
            f"URL: {v['url']}\n\n"
        )

print(f"\nSaved {len(results)} results to trend_report.txt")
print("Note: YouTube search results may omit dates or views.")
