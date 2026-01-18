import requests
import json

# Test the backend
BASE_URL = "http://localhost:8000"

def test_endpoints():
    print("🧪 Testing backend endpoints...")
    
    # Test root endpoint
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"✅ Root endpoint: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"❌ Root endpoint failed: {e}")
    
    # Test health endpoint
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"✅ Health endpoint: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"❌ Health endpoint failed: {e}")
    
    # Test auth endpoints
    try:
        # This should work without auth
        response = requests.get(f"{BASE_URL}/auth/test")
        print(f"✅ Auth test endpoint: {response.status_code}")
    except Exception as e:
        print(f"❌ Auth test failed: {e}")
    
    # Test creating a profile with dev token
    print("\n🧪 Testing profile creation...")
    profile_data = {
        "name": "Test User",
        "income": 250000,
        "caste": "OBC",
        "category": "Minority",
        "state": "Maharashtra",
        "course": "B.Tech",
        "marks": 87.5
    }
    
    try:
        # Try with dev token
        headers = {"Authorization": "Bearer dev_token_123"}
        response = requests.post(
            f"{BASE_URL}/profiles",
            json=profile_data,
            headers=headers
        )
        print(f"✅ Profile creation: {response.status_code}")
        if response.status_code == 200:
            print(f"   Response: {response.json()}")
        else:
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"❌ Profile creation failed: {e}")

if __name__ == "__main__":
    test_endpoints()