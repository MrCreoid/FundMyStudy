from google.cloud import firestore
import os
import logging

logger = logging.getLogger(__name__)

def get_firestore_client():
    """Get Firestore client with default credentials"""
    try:
        # Try with environment variable (JSON string) - Best for Render/Cloud
        # We check both keys since users might prefer one or the other
        firebase_creds = os.getenv("FIREBASE_CREDENTIALS") or os.getenv("GOOGLE_APPLICATION_CREDENTIALS_JSON")
        
        if firebase_creds:
            import json
            from google.oauth2 import service_account
            
            logger.info("✅ Found FIREBASE_CREDENTIALS environment variable")
            try:
                creds_dict = json.loads(firebase_creds)
                credentials = service_account.Credentials.from_service_account_info(creds_dict)
                return firestore.Client(credentials=credentials, project=creds_dict.get("project_id"))
            except json.JSONDecodeError as e:
                logger.error(f"❌ Failed to parse FIREBASE_CREDENTIALS JSON: {e}")
            except Exception as e:
                logger.error(f"❌ Error initializing from FIREBASE_CREDENTIALS: {e}")

        # Try with environment variable path (Standard Google Auth)
        credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        
        if credentials_path and os.path.exists(credentials_path):
            logger.info(f"✅ Using credentials from: {credentials_path}")
            return firestore.Client.from_service_account_json(credentials_path)
        
        # Try with default credentials (for Google Cloud environments)
        logger.info("✅ Using default credentials")
        return firestore.Client()
        
    except Exception as e:
        logger.error(f"❌ Firestore initialization failed: {e}")
        
        # Create a mock client for development
        logger.warning("⚠️  Using mock Firestore client (data won't be saved)")
        
        class MockFirestore:
            def collection(self, name):
                return MockCollection()
        
        class MockCollection:
            def document(self, doc_id):
                return MockDocument()
            
            def where(self, field, operator, value):
                return MockQuery()
            
            def stream(self):
                return []
            
            def add(self, data):
                print(f"📝 [MOCK] Would add to {self}: {data}")
                return None
        
        class MockDocument:
            def get(self):
                return MockDocumentSnapshot()
            
            def set(self, data, merge=False):
                print(f"📝 [MOCK] Would set document: {data}")
                return None
            
            def update(self, data):
                print(f"📝 [MOCK] Would update document: {data}")
                return None
        
        class MockDocumentSnapshot:
            def exists(self):
                return False
            
            def to_dict(self):
                return {}
        
        class MockQuery:
            def stream(self):
                return []
            
            def limit(self, limit):
                return self
        
        return MockFirestore()

# Initialize Firestore client
db = get_firestore_client()
logger.info("✅ Firestore client initialized")