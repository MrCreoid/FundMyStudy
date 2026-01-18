from services.firestore import db
from datetime import datetime

def populate_test_scholarships():
    """Add test scholarships to Firestore"""
    
    test_scholarships = [
        {
            "name": "Test Scholarship 1",
            "provider": "Test Provider",
            "description": "This is a test scholarship",
            "amount": "₹10,000",
            "deadline": "2024-12-31",
            "source_url": "https://example.com",
            "application_link": "https://example.com/apply",
            "active": True,
            "category": "Test",
            "icon": "🎓"
        },
        {
            "name": "Test Scholarship 2",
            "provider": "Test Provider 2",
            "description": "Another test scholarship",
            "amount": "₹15,000",
            "deadline": "2024-11-30",
            "source_url": "https://example2.com",
            "application_link": "https://example2.com/apply",
            "active": True,
            "category": "Test",
            "icon": "⭐"
        }
    ]
    
    test_eligibility_rules = [
        {
            "scholarshipId": "test_scholarship_1",
            "conditions": [
                {"field": "income", "operator": "<=", "value": 250000},
                {"field": "marks", "operator": ">=", "value": 60}
            ]
        },
        {
            "scholarshipId": "test_scholarship_2",
            "conditions": [
                {"field": "caste", "operator": "==", "value": "OBC"},
                {"field": "income", "operator": "<=", "value": 500000}
            ]
        }
    ]
    
    print("📝 Adding test scholarships to Firestore...")
    
    # Add scholarships
    for i, scholarship in enumerate(test_scholarships):
        doc_id = f"test_scholarship_{i+1}"
        scholarship["created_at"] = datetime.utcnow().isoformat()
        scholarship["last_updated"] = datetime.utcnow().isoformat()
        
        db.collection("scholarships").document(doc_id).set(scholarship)
        print(f"✅ Added scholarship: {scholarship['name']}")
    
    # Add eligibility rules
    for rule in test_eligibility_rules:
        rule_id = f"{rule['scholarshipId']}_rules"
        rule["updated_at"] = datetime.utcnow().isoformat()
        
        db.collection("eligibility_rules").document(rule_id).set(rule)
        print(f"✅ Added eligibility rules for: {rule['scholarshipId']}")
    
    print("\n✅ Test data populated successfully!")
    print("Run the scraper for real scholarships: cd scraper && python main.py --source mock")

if __name__ == "__main__":
    populate_test_scholarships()