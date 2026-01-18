from fastapi import APIRouter
from services.auth_dependency import get_current_user, security
from fastapi import Depends

router = APIRouter(prefix="/auth", tags=["auth"])

@router.get("/test")
def test_auth(token: str = Depends(security)):
    """Test if authentication is working"""
    return {
        "message": "Token received",
        "token_length": len(token.credentials),
        "token_preview": token.credentials[:50] + "..." if len(token.credentials) > 50 else token.credentials
    }

@router.get("/me")
def get_current_user_info(uid: str = Depends(get_current_user)):
    """Get current user info"""
    return {
        "user_id": uid,
        "authenticated": True,
        "message": "Authentication successful"
    }