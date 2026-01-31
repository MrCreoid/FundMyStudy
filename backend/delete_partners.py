
import firebase_admin
from firebase_admin import credentials, firestore
import os

# Initialize Firestore mostly same way as checking env
# Assuming standard google credentials logic
if os.getenv("FIREBASE_CREDENTIALS"):
    import json
    cred = credentials.Certificate(json.loads(os.getenv("FIREBASE_CREDENTIALS")))
    firebase_admin.initialize_app(cred)
else:
    # Try default
    firebase_admin.initialize_app()

db = firestore.client()

def delete_scholarships():
    print("🔍 Searching for scholarships with provider 'Buddy4Study Partner'...")
    
    # Query for the scholarships
    # Note: If there are many, we should paginate, but for a small dataset this is fine
    scholarships_ref = db.collection("scholarships")
    query = scholarships_ref.where("provider", "==", "Buddy4Study Partner")
    
    docs = list(query.stream())
    
    print(f"⚠️  Found {len(docs)} scholarships to delete.")
    
    if len(docs) == 0:
        print("✅ No scholarships found to delete.")
        return

    batch = db.batch()
    count = 0
    deleted_ids = []

    for doc in docs:
        batch.delete(doc.reference)
        # Also try to find associated rules? 
        # Usually they are in eligibility_rules collection with scholarshipId
        deleted_ids.append(doc.id)
        count += 1
        
        if count >= 400: # Batch limit is 500
            print("Commiting batch...")
            batch.commit()
            batch = db.batch()
            count = 0
            
    if count > 0:
        batch.commit()
        
    print("✅ Deleted scholarships from 'scholarships' collection.")
    
    # Now cleanup eligibility rules
    print("🧹 Cleaning up associated eligibility rules...")
    rules_count = 0
    batch = db.batch()
    batch_size = 0
    
    for sch_id in deleted_ids:
        rules = db.collection("eligibility_rules").where("scholarshipId", "==", sch_id).stream()
        for rule in rules:
            batch.delete(rule.reference)
            rules_count += 1
            batch_size += 1
            
            if batch_size >= 400:
                print("Commiting rules batch...")
                batch.commit()
                batch = db.batch()
                batch_size = 0
    
    if batch_size > 0:
        batch.commit()
        
    print(f"✅ Deleted {rules_count} associated eligibility rules.")
    print("🎉 Cleanup complete!")

if __name__ == "__main__":
    delete_scholarships()
