import firebase_admin
from firebase_admin import credentials

# Initialize Firebase Admin only once
if not firebase_admin._apps:
    try:
        # Try to load service account key
        cred = credentials.Certificate("serviceAccountKey.json")
        firebase_admin.initialize_app(cred)
        print("✅ Firebase Admin initialized successfully")
    except Exception as e:
        print(f"⚠️  Firebase Admin init failed: {e}")
        print("⚠️  Running without Firebase Admin - some features may not work")