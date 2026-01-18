import logging

logger = logging.getLogger(__name__)

def initialize_firebase():
    """Initialize Firebase (no service account needed for REST API)"""
    try:
        # We're using REST API for authentication, so no Firebase Admin SDK needed
        logger.info("✅ Using Firebase REST API for authentication")
        return True
    except Exception as e:
        logger.error(f"❌ Firebase setup error: {e}")
        return False

# Initialize on import
initialize_firebase()