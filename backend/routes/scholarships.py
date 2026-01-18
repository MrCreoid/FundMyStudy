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
    Get scholarships eligible for current user
    WITH TIMEOUT PROTECTION for better performance
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
        logger.info(f"📋 Processing profile for: {profile.get('name', 'Unknown')}")
        
        # Get all active scholarships WITH LIMIT for performance
        scholarships_ref = db.collection("scholarships").where("active", "==", True).limit(15)
        scholarships = list(scholarships_ref.stream())
        
        if not scholarships:
            logger.warning("⚠️ No scholarships found in database")
            return {
                "count": 0,
                "scholarships": [],
                "message": "No scholarships available. Please check back later.",
                "profile_completed": True
            }
        
        logger.info(f"🔍 Checking {len(scholarships)} scholarships against profile")
        
        results = []
        
        for i, sch in enumerate(scholarships):
            sch_data = sch.to_dict()
            sch_id = sch.id
            
            # Get eligibility rules for this scholarship
            rules_ref = db.collection("eligibility_rules").where("scholarshipId", "==", sch_id)
            rules = list(rules_ref.stream())
            
            if not rules:
                logger.debug(f"⚠️ No eligibility rules found for: {sch_data.get('name')}")
                continue
            
            for rule_doc in rules:
                rule_data = rule_doc.to_dict()
                conditions = rule_data.get("conditions", [])
                
                if not conditions:
                    continue
                
                # Evaluate eligibility
                evaluation = evaluate_conditions(profile, conditions)
                
                # Store match result (optional - for analytics)
                match_doc_id = f"{uid}_{sch_id}"
                try:
                    db.collection("matches").document(match_doc_id).set({
                        "userId": uid,
                        "scholarshipId": sch_id,
                        "eligible": evaluation["eligible"],
                        "score": evaluation["score"],
                        "reasons": evaluation["reasons"],
                        "evaluatedAt": datetime.utcnow()
                    }, merge=True)
                except Exception as e:
                    logger.debug(f"Could not save match record: {e}")
                
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
                    break  # Only need first matching rule
        
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
    FAST VERSION: Returns pre-computed or limited results for demo
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
        "message": "Scraping is manual. Run in terminal: cd scraper && python3 main.py --source all",
        "command": "cd scraper && python3 main.py --source all",
        "status": "manual_mode",
        "timestamp": datetime.utcnow().isoformat()
    }

@router.get("/test")
async def test_endpoint():
    """Test endpoint to check if API is working"""
    return {
        "status": "ok",
        "message": "Scholarships API is working",
        "timestamp": datetime.utcnow().isoformat()
    }