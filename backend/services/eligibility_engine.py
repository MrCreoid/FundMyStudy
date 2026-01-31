import random
import hashlib

def evaluate_conditions(profile: dict, conditions: list):
    """
    Evaluate if profile matches scholarship conditions
    Returns: {"eligible": bool, "score": float, "reasons": list}
    """
    # Track matches
    total_conditions = len(conditions)
    if total_conditions == 0:
        return {"eligible": True, "score": 1.0, "reasons": ["No restrictions"]}

    matched_count = 0
    reasons = []
    bonus_points = 0.0
    
    for condition in conditions:
        field = condition.get("field")
        operator = condition.get("operator")
        value = condition.get("value")
        
        if not field or not operator:
            continue
        
        profile_value = profile.get(field)
        condition_met = False
        
        # Handle different operators
        if operator == "<=":
            try:
                prof_val = float(profile_value)
                limit_val = float(value)
                if prof_val <= limit_val:
                    condition_met = True
                    matched_count += 1
                    reasons.append(f"✅ {field} ≤ {value}")
                    if limit_val > 0 and (limit_val - prof_val) / limit_val > 0.5: bonus_points += 0.05
            except (ValueError, TypeError):
                pass
                
        elif operator == ">=":
            try:
                prof_val = float(profile_value)
                limit_val = float(value)
                if prof_val >= limit_val:
                    condition_met = True
                    matched_count += 1
                    reasons.append(f"✅ {field} ≥ {value}")
                    if limit_val > 0 and (prof_val - limit_val) / limit_val > 0.2: bonus_points += 0.05
            except (ValueError, TypeError):
                pass
                
        elif operator == "==":
            if str(profile_value).lower() == str(value).lower():
                condition_met = True
                matched_count += 1
                reasons.append(f"✅ {field} = {value}")
                
        elif operator == "IN":
            if isinstance(value, list):
                prof_str = str(profile_value).lower().strip()
                val_list_lower = [str(v).lower().strip() for v in value]
                if prof_str in val_list_lower:
                    condition_met = True
                    matched_count += 1
                    reasons.append(f"✅ {field} match")
            elif str(profile_value).lower() == str(value).lower():
                condition_met = True
                matched_count += 1
                reasons.append(f"✅ {field} = {value}")
                
        elif operator == "ANY":
            if profile_value:
                condition_met = True
                matched_count += 1
                reasons.append(f"✅ {field} present")
        
        if not condition_met:
            reasons.append(f"❌ {field}: {profile_value} (Needed {operator} {value})")

    # Calculate Score
    # Base match ratio
    match_ratio = matched_count / total_conditions
    
    # Final Score = Ratio + Bonus
    final_score = match_ratio + bonus_points
    
    # Deterministic jitter (0.00 - 0.05)
    seed_str = str(profile.get('name', '')) + str(len(reasons))
    seed_val = int(hashlib.sha256(seed_str.encode('utf-8')).hexdigest(), 16) % 100
    jitter = (seed_val / 2000.0) 
    final_score += jitter

    # Cap at 0.99
    if final_score > 0.99: final_score = 0.99
    
    # Eligible if score > 0.33 (33%)
    eligible = final_score >= 0.33
    
    return {
        "eligible": eligible,
        "score": round(final_score, 2),
        "reasons": reasons
    }