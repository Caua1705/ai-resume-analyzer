def score_badge(score):

    if score >= 85:
        return "🟢 Excellent"
    elif score >= 70:
        return "🟡 Good"
    elif score >= 50:
        return "🟠 Moderate"
    elif score >= 30:
        return "🔴 Weak"
    else:
        return "⚫ Very Weak"