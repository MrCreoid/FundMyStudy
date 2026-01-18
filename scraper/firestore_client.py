from google.cloud import firestore
import os

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
print("PROJECT:", PROJECT_ID)

db = firestore.Client(project=PROJECT_ID)
