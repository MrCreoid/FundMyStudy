def evaluate_conditions(profile: dict, conditions: list):
    matched = 0
    reasons = []

    for condition in conditions:
        field = condition["field"]
        operator = condition["operator"]
        value = condition["value"]

        profile_value = profile.get(field)

        print("CHECKING:", field, operator, value)
        print("PROFILE VALUE:", profile_value)

        if profile_value is None:
            print("❌ FIELD NOT FOUND")
            continue


        if operator == "<=" and profile_value <= value:
            matched += 1
            reasons.append(f"{field} <= {value}")

        elif operator == ">=" and profile_value >= value:
            matched += 1
            reasons.append(f"{field} >= {value}")

        elif operator == "==" and profile_value == value:
            matched += 1
            reasons.append(f"{field} == {value}")

        elif operator == "IN" and profile_value in value:
            matched += 1
            reasons.append(f"{field} in {value}")

        elif operator == "ANY":
            matched += 1
            reasons.append(f"{field} allowed")

    score = matched / len(conditions) if conditions else 0
    eligible = score == 1

    return {
        "eligible": eligible,
        "score": round(score, 2),
        "reasons": reasons
    }
