from fastapi import APIRouter, Depends
from services.firestore import db
from services.auth_dependency import get_current_user
from services.eligibility_engine import evaluate_conditions
from datetime import datetime

router = APIRouter(prefix="/scholarships", tags=["scholarships"])

@router.get("/eligible")
def get_eligible_scholarships(uid: str = Depends(get_current_user)):
    profile_doc = db.collection("profiles").document(uid).get()
    if not profile_doc.exists:
        return {"error": "Profile not found"}

    profile = profile_doc.to_dict()

    scholarships = db.collection("scholarships").where("active", "==", True).stream()

    results = []

    for sch in scholarships:
        sch_data = sch.to_dict()
        sch_id = sch.id

        rules = db.collection("eligibility_rules") \
                  .where("scholarshipId", "==", sch_id) \
                  .stream()

        for rule_doc in rules:
            rule_data = rule_doc.to_dict()
            evaluation = evaluate_conditions(profile, rule_data["conditions"])

            match_doc_id = f"{uid}_{sch_id}"

            db.collection("matches").document(match_doc_id).set({
                "userId": uid,
                "scholarshipId": sch_id,
                "eligible": evaluation["eligible"],
                "score": evaluation["score"],
                "reasons": evaluation["reasons"],
                "evaluatedAt": datetime.utcnow()
            })

            if evaluation["eligible"]:
                results.append({
                    "scholarshipId": sch_id,
                    "name": sch_data["name"],
                    "provider": sch_data["provider"],
                    "deadline": sch_data["deadline"],
                    "score": evaluation["score"],
                    "reasons": evaluation["reasons"],
                    "apply_link": sch_data["source_url"]
                })

    return results
