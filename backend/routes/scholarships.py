@router.get("/eligible")
def get_eligible_scholarships(uid: str = Depends(get_current_user)):
    """Get scholarships eligible for current user"""
    try:
        print(f"\n🎯 Getting eligible scholarships for user: {uid}")
        
        # Get user profile
        profile_doc = db.collection("profiles").document(uid).get()
        if not profile_doc.exists:
            print(f"❌ Profile not found for user: {uid}")
            return {
                "error": "Profile not found. Please complete your profile first.",
                "count": 0,
                "scholarships": []
            }

        profile = profile_doc.to_dict()
        print(f"📋 User profile: {profile}")

        # Get all active scholarships
        scholarships_ref = db.collection("scholarships").where("active", "==", True)
        scholarships = scholarships_ref.stream()

        results = []
        total_checked = 0

        # If no scholarships in database, return empty with message
        scholarship_count = len(list(scholarships_ref.stream()))
        if scholarship_count == 0:
            print("⚠️  No scholarships found in database")
            return {
                "count": 0,
                "scholarships": [],
                "message": "No scholarships in database. Run scraper first.",
                "profile_completed": True,
                "user_id": uid
            }

        # Reset iterator
        scholarships = scholarships_ref.stream()

        for sch in scholarships:
            sch_data = sch.to_dict()
            sch_id = sch.id
            total_checked += 1
            
            print(f"\n🔍 Checking scholarship {total_checked}: {sch_data.get('name', 'Unknown')}")

            # Get eligibility rules
            rules_ref = db.collection("eligibility_rules").where("scholarshipId", "==", sch_id)
            rules = rules_ref.stream()

            rule_found = False
            for rule_doc in rules:
                rule_found = True
                rule_data = rule_doc.to_dict()
                conditions = rule_data.get("conditions", [])
                
                if not conditions:
                    print(f"⚠️  No conditions found for {sch_id}")
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
                    "evaluatedAt": datetime.utcnow().isoformat()
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
                    print(f"✅ ELIGIBLE: {sch_data.get('name')}")

            if not rule_found:
                print(f"⚠️  No eligibility rules found for {sch_id}")

        print(f"\n📊 Checked {total_checked} scholarships, found {len(results)} eligible")

        # Sort by score (highest first)
        results.sort(key=lambda x: x["score"], reverse=True)
        
        return {
            "count": len(results),
            "scholarships": results,
            "profile_completed": True,
            "user_id": uid,
            "total_checked": total_checked
        }
        
    except Exception as e:
        print(f"❌ Error in get_eligible_scholarships: {e}")
        import traceback
        traceback.print_exc()
        return {
            "error": "Failed to fetch scholarships",
            "details": str(e),
            "count": 0,
            "scholarships": []
        }