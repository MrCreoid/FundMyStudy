def evaluate_conditions(profile: dict, conditions: list):
    """
    Evaluate if profile matches scholarship conditions
    Returns: {"eligible": bool, "score": float, "reasons": list}
    """
    matched = 0
    reasons = []
    
    for condition in conditions:
        field = condition.get("field")
        operator = condition.get("operator")
        value = condition.get("value")
        
        if not field or not operator:
            continue
        
        profile_value = profile.get(field)
        
        # Handle different operators
        if operator == "<=":
            try:
                if float(profile_value) <= float(value):
                    matched += 1
                    reasons.append(f"{field} ≤ {value}")
            except (ValueError, TypeError):
                pass
                
        elif operator == ">=":
            try:
                if float(profile_value) >= float(value):
                    matched += 1
                    reasons.append(f"{field} ≥ {value}")
            except (ValueError, TypeError):
                pass
                
        elif operator == "==":
            if str(profile_value).lower() == str(value).lower():
                matched += 1
                reasons.append(f"{field} = {value}")
                
        elif operator == "IN":
            if isinstance(value, list) and profile_value in value:
                matched += 1
                reasons.append(f"{field} in {value}")
            elif str(profile_value).lower() == str(value).lower():
                matched += 1
                reasons.append(f"{field} = {value}")
                
        elif operator == "ANY":
            if profile_value:
                matched += 1
                reasons.append(f"{field} present")
    
    score = matched / len(conditions) if conditions else 0
    eligible = score == 1
    
    return {
        "eligible": eligible,
        "score": round(score, 2),
        "reasons": reasons
    }