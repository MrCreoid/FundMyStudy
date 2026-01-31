from fastapi import APIRouter, Depends, HTTPException, status
from services.firestore import db
from services.auth_dependency import get_current_user
from datetime import datetime
import logging
from typing import Optional

router = APIRouter(prefix="/profiles", tags=["profiles"])
logger = logging.getLogger(__name__)

@router.get("/me")
async def get_profile(uid: str = Depends(get_current_user)):
    """Get current user's profile"""
    logger.info(f"📋 Getting profile for user: {uid}")
    
    try:
        doc = db.collection("profiles").document(uid).get()
        if doc.exists:
            profile_data = doc.to_dict()
            logger.info(f"✅ Found profile for user: {uid}")
            return profile_data
        else:
            logger.info(f"⚠️  Profile not found for user: {uid}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Profile not found. Please create a profile first."
            )
    except Exception as e:
        logger.error(f"❌ Error getting profile: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve profile"
        )

@router.post("")
async def create_or_update_profile(
    profile: dict,
    uid: str = Depends(get_current_user)
):
    """Save or update user profile"""
    logger.info(f"💾 Saving profile for user: {uid}")
    
    try:
        # Validate required fields
        required_fields = ["name", "state", "course"]
        missing_fields = []
        
        for field in required_fields:
            if field not in profile or not str(profile[field]).strip():
                missing_fields.append(field)
        
        if missing_fields:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Missing required fields: {', '.join(missing_fields)}"
            )
        
        # Prepare profile data
        profile_data = {
            "name": str(profile.get("name", "")).strip(),
            "state": str(profile.get("state", "")).strip(),
            "course": str(profile.get("course", "")).strip(),
            "phone": str(profile.get("phone", "")).strip(),
            "gender": str(profile.get("gender", "Other")).strip(),  # New Field
            "income": float(profile.get("income", 0)) if profile.get("income") else 0,
            "caste": str(profile.get("caste", "General")).strip(),
            "category": str(profile.get("category", "Not Minority")).strip(),
            "marks": float(profile.get("marks", 0)) if profile.get("marks") else 0,
            "updatedAt": datetime.utcnow().isoformat(),
            "userId": uid
        }
        
        # Add createdAt if not exists
        existing_doc = db.collection("profiles").document(uid).get()
        if not existing_doc.exists:
            profile_data["createdAt"] = datetime.utcnow().isoformat()
        
        # Save to Firestore
        db.collection("profiles").document(uid).set(profile_data, merge=True)
        
        logger.info(f"✅ Profile saved successfully for user: {uid}")
        
        return {
            "status": "success",
            "message": "Profile saved successfully",
            "uid": uid,
            "profile": profile_data
        }
        
    except HTTPException:
        raise
    except ValueError as e:
        logger.error(f"❌ Validation error: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid data format. Please check your input values."
        )
    except Exception as e:
        logger.error(f"❌ Error saving profile: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to save profile. Please try again."
        )