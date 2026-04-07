# routes/alerts.py — Mukesh V A
from flask import Blueprint, request, jsonify
from models.db import get_all_records, get_records_by_location
from collections import defaultdict

alerts_bp = Blueprint("alerts", __name__)

def calculate_safety_score(crime_count):
    if crime_count == 0:
        return 100, "Safe"
    elif crime_count <= 15:
        return 80, "Safe"
    elif crime_count <= 30:
        return 60, "Moderate Risk"
    elif crime_count <= 50:
        return 35, "High Risk"
    else:
        return 10, "Extreme Risk"

def get_risk_color(level):
    return {
        "Safe":         "green",
        "Moderate Risk":"yellow",
        "High Risk":    "orange",
        "Extreme Risk": "red",
    }.get(level, "gray")

# ── Safety Score ──────────────────────────────────────────────────────────────
@alerts_bp.route("/safety-score", methods=["GET"])
def safety_score():
    location = request.args.get("location", "").strip()
    if not location:
        return jsonify({"error": "Location parameter required"}), 400

    records     = get_records_by_location(location)
    total       = sum(r["count"] for r in records)
    score, level = calculate_safety_score(total)

    return jsonify({
        "location":    location,
        "score":       score,
        "risk_level":  level,
        "color":       get_risk_color(level),
        "crime_count": total,
        "records":     len(records),
    }), 200

# ── All Safety Scores ─────────────────────────────────────────────────────────
@alerts_bp.route("/all-scores", methods=["GET"])
def all_scores():
    records     = get_all_records()
    by_location = defaultdict(int)
    for r in records:
        by_location[r["location"]] += r["count"]

    result = []
    for loc, total in sorted(by_location.items(), key=lambda x: x[1], reverse=True):
        score, level = calculate_safety_score(total)
        result.append({
            "location":   loc,
            "score":      score,
            "risk_level": level,
            "color":      get_risk_color(level),
            "total":      total,
        })
    return jsonify({"scores": result}), 200

# ── Peak Crime Time ───────────────────────────────────────────────────────────
@alerts_bp.route("/peak-time", methods=["GET"])
def peak_crime_time():
    location = request.args.get("location", "").strip()
    records  = get_records_by_location(location) if location else get_all_records()

    hourly   = defaultdict(int)
    daily    = defaultdict(int)
    days_map = {0:"Monday",1:"Tuesday",2:"Wednesday",3:"Thursday",4:"Friday",5:"Saturday",6:"Sunday"}

    for r in records:
        hourly[r["hour"]]        += r["count"]
        daily[r["day_of_week"]]  += r["count"]

    peak_hour = max(hourly, key=hourly.get) if hourly else 22
    peak_day  = days_map[max(daily, key=daily.get)] if daily else "Friday"

    return jsonify({
        "location":   location or "All",
        "peak_hour":  f"{peak_hour}:00 - {(peak_hour+1)%24}:00",
        "peak_day":   peak_day,
        "hourly_data":  [{"hour": h, "count": hourly.get(h, 0)} for h in range(24)],
        "daily_data":   [{"day": days_map[d], "count": daily.get(d, 0)} for d in range(7)],
    }), 200

# ── Crime Alert Check ─────────────────────────────────────────────────────────
@alerts_bp.route("/check", methods=["POST"])
def check_alert():
    data     = request.get_json()
    location = data.get("location", "").strip()
    if not location:
        return jsonify({"error": "Location required"}), 400

    records = get_records_by_location(location)
    total   = sum(r["count"] for r in records)
    score, level = calculate_safety_score(total)
    alert   = level in ("High Risk", "Extreme Risk")

    messages = {
        "Safe":         f"✅ {location} is currently safe.",
        "Moderate Risk":f"⚠️ Moderate crime activity detected in {location}.",
        "High Risk":    f"🚨 High crime activity in {location}! Stay cautious.",
        "Extreme Risk": f"🔴 EXTREME risk in {location}! Avoid if possible.",
    }

    return jsonify({
        "location":    location,
        "alert":       alert,
        "risk_level":  level,
        "score":       score,
        "crime_count": total,
        "message":     messages.get(level, "Unknown"),
    }), 200

# ── Auto Alerts for All Locations ─────────────────────────────────────────────
@alerts_bp.route("/auto", methods=["GET"])
def auto_alerts():
    records     = get_all_records()
    by_location = defaultdict(int)
    for r in records:
        by_location[r["location"]] += r["count"]

    alerts = []
    for loc, total in by_location.items():
        score, level = calculate_safety_score(total)
        if level in ("High Risk", "Extreme Risk"):
            alerts.append({
                "location":  loc,
                "risk_level": level,
                "score":     score,
                "total":     total,
            })
    return jsonify({"alerts": alerts, "count": len(alerts)}), 200
