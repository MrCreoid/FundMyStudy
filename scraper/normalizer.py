from datetime import datetime

def normalize(raw):
    return {
        "name": raw["name"],
        "provider": raw["provider"],
        "source_url": raw["source_url"],
        "official_only": True,
        "active": True,
        "last_verified": datetime.utcnow()
    }