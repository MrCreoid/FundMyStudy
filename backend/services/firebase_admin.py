import firebase_admin
from firebase_admin import credentials, auth

# Initialize Firebase Admin only once
if not firebase_admin._apps:
    firebase_admin.initialize_app()