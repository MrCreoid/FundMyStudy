from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import requests
import logging

logger = logging.getLogger(__name__)
security = HTTPBearer()

# Your Firebase project's Web API Key
FIREBASE_API_KEY = "AIzaSyCzmKUJt7XD7M9MjMxltn22ceps1Yt186Y"

async def verify_firebase_token(id_token: str):
    """Verify Firebase ID token using REST API"""
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:lookup?key={FIREBASE_API_KEY}"
    
    try:
        response = requests.post(url, json={"idToken": id_token})
        response.raise_for_status()
        
        data = response.json()
        if "users" in data and len(data["users"]) > 0:
            user = data["users"][0]
            return {
                "uid": user["localId"],
                "email": user.get("email", ""),
                "email_verified": user.get("emailVerified", False)
            }
        return None
    except Exception as e:
        logger.error(f"Token verification failed: {e}")
        return None

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Verify Firebase ID token and return user UID"""
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication token required",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token = credentials.credentials
    
    # Verify token using Firebase REST API
    user_info = await verify_firebase_token(token)
    
    if not user_info:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    logger.info(f"✅ Authenticated user: {user_info['uid']} ({user_info['email']})")
    return user_info["uid"]