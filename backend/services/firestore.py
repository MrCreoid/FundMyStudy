from google.cloud import firestore
import os

# Use environment variable or default project
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "fundmystudy-527")

try:
    db = firestore.Client(project=PROJECT_ID)
    print(f"✅ Firestore connected to project: {PROJECT_ID}")
except Exception as e:
    print(f"❌ Firestore connection failed: {e}")
    db = None