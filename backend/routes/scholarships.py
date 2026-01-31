from fastapi import APIRouter, Depends, HTTPException
from services.firestore import db
from services.auth_dependency import get_current_user
from services.eligibility_engine import evaluate_conditions
from datetime import datetime
import logging
import asyncio
from typing import List

router = APIRouter(prefix="/scholarships", tags=["scholarships"])
logger = logging.getLogger(__name__)

@router.get("/eligible")
async def get_eligible_scholarships(uid: str = Depends(get_current_user)):
    """
    Get scholarships eligible for current user.
    """
    try:
        logger.info(f"🎯 Getting eligible scholarships for user: {uid}")
        
        # Get user profile
        profile_doc = db.collection("profiles").document(uid).get()
        if not profile_doc.exists:
            logger.warning(f"⚠️ Profile not found for user: {uid}")
            return {
                "error": "Profile not found. Please complete your profile first.",
                "count": 0,
                "scholarships": []
            }

        profile = profile_doc.to_dict()
        
        # Get active scholarships (increased limit to ensure we find matches)
        scholarships_ref = db.collection("scholarships").where("active", "==", True).limit(200)
        scholarships = list(scholarships_ref.stream())
        
        if not scholarships:
            logger.warning("⚠️ No scholarships found in database")
            return {
                "count": 0,
                "scholarships": [],
                "message": "No scholarships available. Please check back later.",
                "profile_completed": True
            }
        

        
        # OPTIMIZATION: Fetch all eligibility rules in one go to avoid N+1 queries
        # This is strictly better for performance on Render
        all_rules_docs = db.collection("eligibility_rules").stream()
        rules_map = {}
        for doc in all_rules_docs:
            data = doc.to_dict()
            sch_id = data.get("scholarshipId")
            if sch_id:
                rules_map[sch_id] = data.get("conditions", [])
        
        results = []
        
        for i, sch in enumerate(scholarships):
            sch_data = sch.to_dict()
            sch_id = sch.id
            
            # Fast lookup in memory
            conditions = rules_map.get(sch_id)
            
            if not conditions:
                continue
            
            # Evaluate eligibility
            evaluation = evaluate_conditions(profile, conditions)
            
            # Store match result (optional - for analytics)
            match_doc_id = f"{uid}_{sch_id}"
            try:
                # Optimized: Don't await/block on this write if possible, or skip for speed
                # db.collection("matches").document(match_doc_id).set({...}) 
                pass 
            except Exception:
                pass
            
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
                logger.debug(f"✅ Eligible: {sch_data.get('name')}")
        
        # Sort by score (highest first)
        results.sort(key=lambda x: x["score"], reverse=True)
        
        logger.info(f"📊 Found {len(results)} eligible scholarships out of {len(scholarships)} checked")
        
        return {
            "count": len(results),
            "scholarships": results,
            "profile_completed": True,
            "total_checked": len(scholarships),
            "processing_time_ms": "fast"  # Add timing in production
        }
        
    except Exception as e:
        logger.error(f"❌ Error getting eligible scholarships: {e}", exc_info=True)
        return {
            "error": "Failed to fetch scholarships. Please try again.",
            "details": "Server error",
            "count": 0,
            "scholarships": []
        }

@router.get("/eligible-fast")
async def get_eligible_scholarships_fast(uid: str = Depends(get_current_user)):
    """
    Fast lookup returning pre-computed or limited results for demo purposes.
    """
    try:
        logger.info(f"🚀 Fast scholarships lookup for user: {uid}")
        
        # Get user profile
        profile_doc = db.collection("profiles").document(uid).get()
        if not profile_doc.exists:
            return {
                "error": "Profile not found",
                "count": 0,
                "scholarships": []
            }

        profile = profile_doc.to_dict()
        
        # Get ONLY 5 scholarships for fast response
        scholarships_ref = db.collection("scholarships").where("active", "==", True).limit(5)
        scholarships = list(scholarships_ref.stream())
        
        results = []
        
        # Quick check for first 3 scholarships
        for sch in scholarships[:3]:
            sch_data = sch.to_dict()
            sch_id = sch.id
            
            # Get eligibility rules
            rules_ref = db.collection("eligibility_rules").where("scholarshipId", "==", sch_id)
            rules = list(rules_ref.stream())
            
            if rules:
                rule_data = rules[0].to_dict()  # Take first rule
                conditions = rule_data.get("conditions", [])
                
                if conditions:
                    evaluation = evaluate_conditions(profile, conditions)
                    
                    if evaluation["eligible"]:
                        results.append({
                            "scholarshipId": sch_id,
                            "name": sch_data.get("name", "Unknown"),
                            "provider": sch_data.get("provider", "Unknown"),
                            "deadline": sch_data.get("deadline", "Not specified"),
                            "amount": sch_data.get("amount", "Not specified"),
                            "score": evaluation["score"],
                            "reasons": evaluation["reasons"],
                            "apply_link": sch_data.get("application_link", "#"),
                            "description": sch_data.get("description", "")
                        })
        
        return {
            "count": len(results),
            "scholarships": results,
            "profile_completed": True,
            "note": "Fast mode - limited to 3 scholarships for demo"
        }
        
    except Exception as e:
        logger.error(f"❌ Fast lookup failed: {e}")
        return {
            "error": "Fast lookup failed",
            "count": 0,
            "scholarships": []
        }

@router.get("/all")
async def get_all_scholarships(limit: int = 20):
    """Get all scholarships (for debugging) - LIMITED for performance"""
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
            "scholarships": scholarships,
            "limit": limit
        }
    except Exception as e:
        logger.error(f"❌ Error getting all scholarships: {e}")
        return {"error": str(e)}

@router.post("/refresh")
def refresh_scholarships():
    """Manual scholarship data refresh"""
    return {
        "message": "Scraper must be run manually: python3 scraper/main.py --source all",
        "status": "manual_only"
    }

@router.get("/test")
async def test_endpoint():
    """Test endpoint to check if API is working"""
    return {
        "status": "ok",
        "message": "Scholarships API is working",
        "timestamp": datetime.utcnow().isoformat()
    }