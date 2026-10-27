import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime

URL = "https://trends.google.com/trending/rss?geo=US"

def main():
    print("\n=== FRAME DISTRICT | USA TREND RESEARCH ===\n")
    req = urllib.request.Request(
        URL,
        headers={"User-Agent": "Mozilla/5.0"}
    )

    try:
        with urllib.request.urlopen(req, timeout=20) as response:
            xml_data = response.read()

        root = ET.fromstring(xml_data)
        items = root.findall(".//item")

        if not items:
            print("No trends returned. Try again later.")
            return

        lines = [
            "FRAME DISTRICT - USA TREND RESEARCH",
            "Checked: " + datetime.now().strftime("%Y-%m-%d %H:%M"),
            ""
        ]

        for i, item in enumerate(items[:20], 1):
            title = item.findtext("title", default="Unknown")
            traffic = item.findtext(
                "{https://trends.google.com/trending/rss}approx_traffic",
                default="Not provided"
            )
            print(f"{i}. {title} | Search traffic: {traffic}")
            lines.append(f"{i}. {title} | Search traffic: {traffic}")

        with open("usa_trends.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

        print("\nSaved results to usa_trends.txt")

    except Exception as e:
        print("\nCould not fetch trends:", e)
        print("Check your internet connection and try again.")

if __name__ == "__main__":
    main()
