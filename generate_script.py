import os
import json
import urllib.request
import urllib.error
from pathlib import Path

key = os.environ.get("GEMINI_API_KEY")
if not key:
    raise SystemExit("ERROR: GEMINI_API_KEY secret is missing")

trend_file = Path("usa_trends.txt")
if not trend_file.exists():
    raise SystemExit("ERROR: usa_trends.txt not found")

trends = trend_file.read_text(encoding="utf-8").strip()
if not trends:
    raise SystemExit("ERROR: trend list is empty")

prompt = f"""
You are the English-language YouTube Shorts scriptwriter for Frame District,
a general-audience US entertainment and trending-stories channel.

Potential trending topics from a trend feed:
{trends[:10000]}

Choose ONE promising topic. Trends are leads, not proof of facts.
Do not invent events, quotes, dates, statistics, or claims.
If the topic cannot be responsibly covered from the supplied information,
write a short note saying verification is needed and do not fabricate details.

Create a COMPLETE original 30-45 second English YouTube Shorts draft. The voiceover must contain 75-110 spoken words, at least 5 complete sentences, and must never end mid-sentence. Do not output a teaser or partial draft.
Include:
# Topic
# Suggested title
# Voiceover script
# On-screen captions (short lines)
# Description
# Verification notes

Use a compelling but truthful hook. Avoid copying headlines or other scripts.
Do not claim the story is verified if the supplied data does not verify it. If recall details cannot be verified from supplied information, make the script a cautious consumer-awareness piece and clearly say viewers should check official sources.
"""

payload = {
    "contents": [{"parts": [{"text": prompt}]}],
    "generationConfig": {
        "temperature": 0.7,
        "maxOutputTokens": 1200
    }
}

url = (
    "https://generativelanguage.googleapis.com/v1beta/"
    "models/gemini-3.5-flash:generateContent"
)

req = urllib.request.Request(
    url,
    data=json.dumps(payload).encode("utf-8"),
    headers={
        "Content-Type": "application/json",
        "x-goog-api-key": key
    },
    method="POST"
)

try:
    with urllib.request.urlopen(req, timeout=90) as response:
        data = json.loads(response.read().decode("utf-8"))
    text = data["candidates"][0]["content"]["parts"][0]["text"].strip()
except urllib.error.HTTPError as exc:
    details = exc.read().decode("utf-8", errors="replace")
    raise SystemExit(f"Gemini API HTTP {exc.code}: {details[:1200]}")
except (urllib.error.URLError, KeyError, IndexError, ValueError) as exc:
    raise SystemExit(f"Script generation failed: {exc}")

Path("script.md").write_text(text + "\n", encoding="utf-8")
print("SUCCESS: script.md created")
print(text[:700])
