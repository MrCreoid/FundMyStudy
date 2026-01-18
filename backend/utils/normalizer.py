from datetime import datetime

def normalize(raw):
    return {
        "name": raw.get("name", ""),
        "provider": raw.get("provider", ""),
        "source_url": raw.get("source_url", ""),
        "official_only": raw.get("official_only", True),
        "active": True,
        "last_verified": datetime.utcnow().isoformat()
    }