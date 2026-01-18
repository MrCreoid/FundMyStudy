"""
Helper to save scholarships to Firestore
"""
import os
import sys
from datetime import datetime
import logging

print("💾 Initializing Firestore Helper...")

# Add the backend directory to path to access shared Firebase config
backend_path = os.path.join(os.path.dirname(__file__), "../../backend")
sys.path.insert(0, backend_path)

try:
    from services.firestore import db
    print("✅ Using shared Firestore client from backend")
except ImportError:
    print("⚠️  Could not import shared Firestore client, initializing directly...")
    try:
        # Initialize Firebase directly
        import firebase_admin
        from firebase_admin import credentials
        from google.cloud import firestore
        
        # Path to service account key
        cred_path = os.path.join(backend_path, "serviceAccountKey.json")
        
        if os.path.exists(cred_path):
            cred = credentials.Certificate(cred_path)
            if not firebase_admin._apps:
                firebase_admin.initialize_app(cred)
            db = firestore.Client()
            print("✅ Firebase initialized directly")
        else:
            print(f"❌ Service account key not found at: {cred_path}")
            db = None
    except Exception as e:
        print(f"❌ Failed to initialize Firebase: {e}")
        db = None

class FirestoreHelper:
    def __init__(self):
        self.db = db
        if self.db:
            print("✅ FirestoreHelper ready")
        else:
            print("❌ FirestoreHelper: No database connection")
    
    def save_scholarships(self, scholarships):
        """
        Save scholarships to Firestore
        Returns: {"saved": X, "updated": Y}
        """
        if not self.db:
            print("❌ Cannot save: No database connection")
            return {"saved": 0, "updated": 0, "error": "No database"}
        
        saved = 0
        updated = 0
        errors = 0
        
        print(f"\n💾 Saving {len(scholarships)} scholarships to Firestore...")
        
        for scholarship in scholarships:
            try:
                # Generate document ID
                doc_id = self._generate_doc_id(scholarship["name"])
                
                # Prepare data
                scholarship_data = {
                    "name": scholarship.get("name", ""),
                    "provider": scholarship.get("provider", ""),
                    "description": scholarship.get("description", ""),
                    "amount": scholarship.get("amount", "Not specified"),
                    "deadline": scholarship.get("deadline", ""),
                    "source_url": scholarship.get("source_url", ""),
                    "application_link": scholarship.get("application_link", ""),
                    "official_only": scholarship.get("official_only", True),
                    "category": scholarship.get("category", "General"),
                    "state_specific": scholarship.get("state_specific", False),
                    "state": scholarship.get("state", ""),
                    "source": scholarship.get("source", "unknown"),
                    "active": True,
                    "last_updated": datetime.utcnow().isoformat(),
                    "icon": scholarship.get("icon", "🎓")
                }
                
                # Remove None values
                scholarship_data = {k: v for k, v in scholarship_data.items() if v is not None}
                
                # Check if document exists
                existing_doc = self.db.collection("scholarships").document(doc_id).get()
                
                if existing_doc.exists:
                    # Update existing
                    self.db.collection("scholarships").document(doc_id).update(scholarship_data)
                    updated += 1
                    print(f"   🔄 Updated: {scholarship['name'][:50]}...")
                else:
                    # Create new
                    scholarship_data["created_at"] = datetime.utcnow().isoformat()
                    self.db.collection("scholarships").document(doc_id).set(scholarship_data)
                    saved += 1
                    print(f"   ✅ Saved new: {scholarship['name'][:50]}...")
                
                # Save eligibility rules separately
                eligibility_conditions = scholarship.get("eligibility_conditions")
                if eligibility_conditions:
                    self._save_eligibility_rules(doc_id, eligibility_conditions)
                    
            except Exception as e:
                errors += 1
                print(f"   ❌ Error saving '{scholarship.get('name', 'Unknown')}': {e}")
        
        print(f"\n📊 Save completed: {saved} new, {updated} updated, {errors} errors")
        
        return {
            "saved": saved,
            "updated": updated,
            "errors": errors,
            "total": len(scholarships)
        }
    
    def _generate_doc_id(self, name):
        """Generate Firestore document ID from scholarship name"""
        import re
        
        # Clean the name
        doc_id = name.lower().strip()
        
        # Replace special characters
        doc_id = re.sub(r'[^a-z0-9\s]', ' ', doc_id)
        doc_id = re.sub(r'\s+', '_', doc_id)
        
        # Limit length
        if len(doc_id) > 100:
            doc_id = doc_id[:100]
        
        return doc_id
    
    def _save_eligibility_rules(self, scholarship_id, conditions):
        """Save eligibility rules for a scholarship"""
        try:
            rule_id = f"{scholarship_id}_rules"
            rule_data = {
                "scholarshipId": scholarship_id,
                "conditions": conditions,
                "updated_at": datetime.utcnow().isoformat()
            }
            
            self.db.collection("eligibility_rules").document(rule_id).set(rule_data, merge=True)
            print(f"   📝 Saved eligibility rules for {scholarship_id}")
        except Exception as e:
            print(f"   ⚠️  Error saving eligibility rules: {e}")