# ml-model/crime_predictor.py — Mukesh V A
from collections import defaultdict

# ── Rule-based risk engine (works without any ML library) ────────────────────
RISK_THRESHOLDS = {
    "Extreme Risk": 50,
    "High Risk":    30,
    "Moderate Risk":15,
    "Safe":          0,
}

def calculate_safety_score(crime_count):
    if crime_count >= 50: return 10,  "Extreme Risk"
    if crime_count >= 30: return 35,  "High Risk"
    if crime_count >= 15: return 60,  "Moderate Risk"
    return 90, "Safe"

def predict_peak_hour(records):
    hourly = defaultdict(int)
    for r in records:
        hourly[r.get("hour", 20)] += r.get("count", 1)
    if not hourly:
        return 22
    return max(hourly, key=hourly.get)

def predict_peak_day(records):
    days_map = {0:"Monday",1:"Tuesday",2:"Wednesday",
                3:"Thursday",4:"Friday",5:"Saturday",6:"Sunday"}
    daily = defaultdict(int)
    for r in records:
        daily[r.get("day_of_week", 4)] += r.get("count", 1)
    if not daily:
        return "Friday"
    return days_map[max(daily, key=daily.get)]

def analyze_location(location, records):
    loc_records = [r for r in records if r["location"].lower() == location.lower()]
    total       = sum(r["count"] for r in loc_records)
    score, level = calculate_safety_score(total)
    peak_hour   = predict_peak_hour(loc_records)
    peak_day    = predict_peak_day(loc_records)

    type_breakdown = defaultdict(int)
    for r in loc_records:
        type_breakdown[r["type"]] += r["count"]

    most_common_crime = max(type_breakdown, key=type_breakdown.get) if type_breakdown else "Unknown"

    return {
        "location":          location,
        "total_crimes":      total,
        "safety_score":      score,
        "risk_level":        level,
        "peak_hour":         f"{peak_hour}:00 - {(peak_hour+1)%24}:00",
        "peak_day":          peak_day,
        "most_common_crime": most_common_crime,
        "type_breakdown":    dict(type_breakdown),
        "recommendations":   get_recommendations(level, most_common_crime),
    }

def get_recommendations(risk_level, crime_type):
    base = {
        "Safe":          ["Area is generally safe", "Stay alert at night"],
        "Moderate Risk": ["Avoid isolated areas after dark", "Keep valuables secured"],
        "High Risk":     ["Travel in groups", "Avoid area late at night", "Report suspicious activity"],
        "Extreme Risk":  ["Avoid area if possible", "Contact local authorities", "Emergency: call 100"],
    }
    specific = {
        "Theft":   ["Keep bags in front", "Don't display expensive items"],
        "Assault": ["Avoid confrontations", "Stay in well-lit areas"],
        "Robbery": ["Use ATMs in safe locations", "Travel in groups"],
        "Fraud":   ["Verify identities", "Don't share personal info"],
    }
    return base.get(risk_level, []) + specific.get(crime_type, [])

# ── Quick test ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    from models.db import get_all_records, get_all_locations
    import sys
    sys.path.insert(0, "../backend")
    records   = get_all_records()
    locations = get_all_locations()
    print("\n=== Crime Prediction Report ===")
    for loc in locations:
        result = analyze_location(loc, records)
        print(f"\n{loc}: {result['risk_level']} (Score: {result['safety_score']})")
        print(f"  Peak: {result['peak_day']} at {result['peak_hour']}")
        print(f"  Most common: {result['most_common_crime']}")
