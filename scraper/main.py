from firestore_client import db
from normalizer import normalize
from datetime import datetime

def run():
    # Controlled ingestion for demo
    raw_scholarships = [
        {
            "name": "Post Matric Scholarship for OBC",
            "provider": "Ministry of Social Justice",
            "source_url": "https://scholarships.gov.in",
            "official_only": True
        }
    ]

    records_added = 0

    for raw in raw_scholarships:
        data = normalize(raw)
        doc_id = "post_matric_obc"

        db.collection("scholarships").document(doc_id).set(data, merge=True)
        records_added += 1

    db.collection("scrape_logs").add({
        "source": "NSP",
        "recordsAdded": records_added,
        "status": "SUCCESS",
        "fetchedAt": datetime.utcnow()
    })

if __name__ == "__main__":
    run()
