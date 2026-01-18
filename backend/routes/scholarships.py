from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException, status
from services.firestore import db
from services.auth_dependency import get_current_user
from services.eligibility_engine import evaluate_conditions
from datetime import datetime
import logging

router = APIRouter(prefix="/scholarships", tags=["scholarships"])
logger = logging.getLogger(__name__)

@router.get("/eligible")
async def get_eligible_scholarships(uid: str = Depends(get_current_user)):
    """Get scholarships eligible for current user"""
    try:
        logger.info(f"🎯 Getting eligible scholarships for user: {uid}")
        
        # Get user profile
        profile_doc = db.collection("profiles").document(uid).get()
        if not profile_doc.exists:
            logger.warning(f"⚠️  Profile not found for user: {uid}")
            return {
                "error": "Profile not found. Please complete your profile first.",
                "count": 0,
                "scholarships": []
            }

        profile = profile_doc.to_dict()
        logger.info(f"📋 Processing profile for: {profile.get('name', 'Unknown')}")
        
        # Get all active scholarships
        scholarships_ref = db.collection("scholarships").where("active", "==", True)
        scholarships = list(scholarships_ref.stream())
        
        if not scholarships:
            logger.warning("⚠️  No scholarships found in database")
            return {
                "count": 0,
                "scholarships": [],
                "message": "No scholarships available. Please check back later.",
                "profile_completed": True
            }
        
        results = []
        
        for sch in scholarships:
            sch_data = sch.to_dict()
            sch_id = sch.id
            
            # Get eligibility rules for this scholarship
            rules_ref = db.collection("eligibility_rules").where("scholarshipId", "==", sch_id)
            rules = list(rules_ref.stream())
            
            if not rules:
                logger.debug(f"⚠️  No eligibility rules found for: {sch_data.get('name')}")
                continue
            
            for rule_doc in rules:
                rule_data = rule_doc.to_dict()
                conditions = rule_data.get("conditions", [])
                
                if not conditions:
                    continue
                
                # Evaluate eligibility
                evaluation = evaluate_conditions(profile, conditions)
                
                # Store match result
                match_doc_id = f"{uid}_{sch_id}"
                db.collection("matches").document(match_doc_id).set({
                    "userId": uid,
                    "scholarshipId": sch_id,
                    "eligible": evaluation["eligible"],
                    "score": evaluation["score"],
                    "reasons": evaluation["reasons"],
                    "evaluatedAt": datetime.utcnow()
                }, merge=True)
                
                # If eligible, add to results
                if evaluation["eligible"]:
                    result_item = {
                        "scholarshipId": sch_id,
                        "name": sch_data.get("name", "Unknown Scholarship"),
                        "provider": sch_data.get("provider", "Unknown Provider"),
                        "deadline": sch_data.get("deadline", "Not specified"),
                        "amount": sch_data.get("amount", "Not specified"),
                        "score": evaluation["score"],
                        "reasons": evaluation["reasons"],
                        "apply_link": sch_data.get("application_link") or 
                                     sch_data.get("source_url", "#"),
                        "description": sch_data.get("description", ""),
                        "icon": sch_data.get("icon", "🎓")
                    }
                    results.append(result_item)
                    logger.info(f"✅ Eligible: {sch_data.get('name')}")
        
        # Sort by score (highest first)
        results.sort(key=lambda x: x["score"], reverse=True)
        
        logger.info(f"📊 Found {len(results)} eligible scholarships out of {len(scholarships)} total")
        
        return {
            "count": len(results),
            "scholarships": results,
            "profile_completed": True
        }
        
    except Exception as e:
        logger.error(f"❌ Error getting eligible scholarships: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch scholarships. Please try again."
        )

@router.get("/all")
async def get_all_scholarships(limit: int = 100):
    """Get all scholarships (for debugging)"""
    try:
        scholarships = []
        docs = db.collection("scholarships") \
                .where("active", "==", True) \
                .limit(limit) \
                .stream()
        
        for doc in docs:
            sch_data = doc.to_dict()
            sch_data["id"] = doc.id
            scholarships.append(sch_data)
        
        return {
            "count": len(scholarships),
            "scholarships": scholarships
        }
    except Exception as e:
        logger.error(f"❌ Error getting all scholarships: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch scholarships"
        )

@router.post("/refresh")
async def refresh_scholarships(background_tasks: BackgroundTasks):
    """Trigger scholarship data refresh (admin function)"""
    # Note: In production, add admin authentication here
    try:
        from services.scraper_service import scraper_service
        background_tasks.add_task(scraper_service.run_scraper, "all")
        
        return {
            "message": "Scholarship refresh started in background",
            "status": "processing",
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"❌ Error starting scraper: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to start scholarship refresh"
        )