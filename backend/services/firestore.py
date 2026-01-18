from google.cloud import firestore
import os

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")

db = firestore.Client(project=PROJECT_ID)
