def evaluate_conditions(profile: dict, conditions: list):
    matched = 0
    reasons = []

    print(f"\n🔍 Evaluating eligibility for profile: {profile}")
    print(f"📋 Conditions to check: {conditions}")

    for condition in conditions:
        field = condition["field"]
        operator = condition["operator"]
        value = condition["value"]

        profile_value = profile.get(field)

        print(f"\nChecking condition: {field} {operator} {value}")
        print(f"Profile value: {profile_value}")

        if profile_value is None:
            print(f"❌ Field '{field}' not found in profile")
            continue

        # Convert to same type for comparison
        try:
            if isinstance(value, (int, float)) and not isinstance(profile_value, (int, float)):
                profile_value = float(profile_value)
        except:
            pass

        if operator == "<=" and profile_value <= value:
            matched += 1
            reasons.append(f"{field} ({profile_value}) <= {value}")
            print(f"✅ Condition matched: {field} <= {value}")

        elif operator == ">=" and profile_value >= value:
            matched += 1
            reasons.append(f"{field} ({profile_value}) >= {value}")
            print(f"✅ Condition matched: {field} >= {value}")

        elif operator == "==" and str(profile_value).lower() == str(value).lower():
            matched += 1
            reasons.append(f"{field} ({profile_value}) == {value}")
            print(f"✅ Condition matched: {field} == {value}")

        elif operator == "IN" and profile_value in value:
            matched += 1
            reasons.append(f"{field} ({profile_value}) in {value}")
            print(f"✅ Condition matched: {field} in {value}")

        elif operator == "ANY":
            matched += 1
            reasons.append(f"{field} allowed")
            print(f"✅ Condition matched: ANY {field}")

        else:
            print(f"❌ Condition failed: {field} {operator} {value}")

    score = matched / len(conditions) if conditions else 0
    eligible = score == 1

    print(f"\n📊 Final score: {score} ({matched}/{len(conditions)})")
    print(f"🎯 Eligible: {eligible}")

    return {
        "eligible": eligible,
        "score": round(score, 2),
        "reasons": reasons
    }