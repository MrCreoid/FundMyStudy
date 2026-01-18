from fastapi import APIRouter, Depends
from services.firestore import db
from services.auth_dependency import get_current_user
from datetime import datetime

router = APIRouter(prefix="/profiles", tags=["profiles"])

@router.get("/me")
def get_profile(uid: str = Depends(get_current_user)):
    doc = db.collection("profiles").document(uid).get()
    if doc.exists:
        return doc.to_dict()
    return {"message": "Profile not found"}

@router.post("")
def create_or_update_profile(
    profile: dict,
    uid: str = Depends(get_current_user)
):
    profile["updatedAt"] = datetime.utcnow()
    profile["createdAt"] = profile.get("createdAt", datetime.utcnow())

    db.collection("profiles").document(uid).set(profile)
    return {"status": "Profile saved"}
