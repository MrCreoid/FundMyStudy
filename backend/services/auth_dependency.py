from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import firebase_admin
from firebase_admin import auth as firebase_auth
import requests
import json

security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials
    
    print(f"🔐 Received token (first 50 chars): {token[:50]}...")
    
    # Try Firebase Admin SDK first
    try:
        decoded_token = firebase_auth.verify_id_token(token)
        uid = decoded_token["uid"]
        print(f"✅ Firebase Admin verified user: {uid}")
        return uid
    except Exception as e:
        print(f"⚠️  Firebase Admin verification failed: {e}")
    
    # Fallback: Verify with Firebase REST API
    try:
        # Firebase REST API endpoint
        url = f"https://identitytoolkit.googleapis.com/v1/accounts:lookup?key=AIzaSyCzmKUJt7XD7M9MjMxltn22ceps1Yt186Y"
        
        response = requests.post(url, json={"idToken": token})
        
        if response.status_code == 200:
            data = response.json()
            if "users" in data and len(data["users"]) > 0:
                uid = data["users"][0]["localId"]
                print(f"✅ Firebase REST API verified user: {uid}")
                return uid
        
        print(f"❌ Firebase REST API failed: {response.status_code}, {response.text}")
        
    except Exception as e:
        print(f"❌ All verification methods failed: {e}")
    
    # For development only - accept a mock token
    if token == "dev_token_123" or token.startswith("dev_"):
        print("⚠️  Using development token (INSECURE - FOR DEV ONLY)")
        return token
    
    raise HTTPException(status_code=401, detail="Invalid or expired token")