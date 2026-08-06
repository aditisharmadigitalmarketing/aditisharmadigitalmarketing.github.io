import json
import sys
from datetime import datetime, timezone

def main():
    with open("raw.json", "r", encoding="utf-8") as f:
        raw = json.load(f)

    response = raw.get("response", {}) if isinstance(raw, dict) else {}
    items = response.get("items") or response.get("episodes") or []

    episodes = []
    for ep in items[:20]:
        description = (ep.get("description") or "").strip()
        # Strip any stray HTML tags Spreaker might include in the description
        import re
        description = re.sub("<[^>]+>", "", description)
        if len(description) > 220:
            description = description[:217].rstrip() + "..."

        episodes.append({
            "title": ep.get("title") or "Untitled episode",
            "description": description,
            "published_at": ep.get("published_at"),
            "site_url": ep.get("site_url"),
            "image_url": ep.get("image_url") or ep.get("image_original_url"),
            "duration_ms": ep.get("duration"),
        })

    output = {
        "updated_at": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
        "episodes": episodes,
    }

    with open("podcast-episodes.json", "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"Wrote {len(episodes)} episodes to podcast-episodes.json")

if __name__ == "__main__":
    main()
