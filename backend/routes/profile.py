from fastapi import APIRouter, Depends, HTTPException
from services.firestore import db
from services.auth_dependency import get_current_user
from datetime import datetime
import logging

router = APIRouter(prefix="/profiles", tags=["profiles"])
logger = logging.getLogger(__name__)

# Development mode - allow profile access without auth for testing
DEV_MODE = True

@router.get("/me")
def get_profile(uid: str = Depends(get_current_user) if not DEV_MODE else "dev_user_123"):
    """Get current user's profile"""
    print(f"📋 Getting profile for user: {uid}")
    
    doc = db.collection("profiles").document(uid).get()
    if doc.exists:
        profile = doc.to_dict()
        print(f"✅ Found profile: {profile}")
        return profile
    else:
        print(f"❌ Profile not found for {uid}")
        return {"message": "Profile not found"}

@router.post("")
def create_or_update_profile(
    profile: dict,
    uid: str = Depends(get_current_user) if not DEV_MODE else "dev_user_123"
):
    """Save or update user profile"""
    
    print(f"\n💾 Saving profile for user: {uid}")
    print(f"📝 Profile data: {profile}")
    
    # Add timestamps
    profile["updatedAt"] = datetime.utcnow().isoformat()
    if "createdAt" not in profile:
        profile["createdAt"] = datetime.utcnow().isoformat()
    
    # Ensure numeric fields are numbers
    numeric_fields = ["income", "marks"]
    for field in numeric_fields:
        if field in profile and profile[field]:
            try:
                profile[field] = float(profile[field])
            except:
                print(f"⚠️  Could not convert {field} to number: {profile[field]}")
    
    # Save to Firestore
    try:
        db.collection("profiles").document(uid).set(profile, merge=True)
        print(f"✅ Profile saved successfully for {uid}")
        
        return {
            "status": "success",
            "message": "Profile saved successfully",
            "uid": uid,
            "profile": profile
        }
    except Exception as e:
        print(f"❌ Error saving profile: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to save profile: {str(e)}")