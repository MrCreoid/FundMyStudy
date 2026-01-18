import requests
import json

BASE_URL = "http://localhost:8000"

def test_scholarships():
    print("🧪 Testing scholarships endpoints...")
    
    # First, create a test profile
    print("\n1️⃣ Creating test profile...")
    profile_data = {
        "name": "Test Student",
        "income": 180000,
        "caste": "SC",
        "category": "Minority",
        "state": "Maharashtra",
        "course": "B.Tech",
        "marks": 82.5
    }
    
    # Use no-auth endpoint for testing
    try:
        response = requests.post(
            f"{BASE_URL}/profiles",
            json=profile_data,
            headers={"Authorization": "Bearer dev_token_123"}
        )
        print(f"✅ Profile created: {response.status_code}")
        if response.status_code == 200:
            print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"❌ Profile creation failed: {e}")
    
    # Test getting all scholarships
    print("\n2️⃣ Testing /scholarships/all endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/scholarships/all")
        print(f"✅ All scholarships: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Found {data.get('count', 0)} scholarships")
            if data.get('scholarships'):
                for i, sch in enumerate(data['scholarships'][:3]):  # Show first 3
                    print(f"   {i+1}. {sch.get('name', 'No name')}")
        else:
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"❌ Failed to get scholarships: {e}")
    
    # Test eligible scholarships (this requires auth)
    print("\n3️⃣ Testing /scholarships/eligible endpoint...")
    try:
        response = requests.get(
            f"{BASE_URL}/scholarships/eligible",
            headers={"Authorization": "Bearer dev_token_123"}
        )
        print(f"✅ Eligible scholarships: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Response: {data}")
        else:
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"❌ Failed to get eligible scholarships: {e}")

if __name__ == "__main__":
    test_scholarships()