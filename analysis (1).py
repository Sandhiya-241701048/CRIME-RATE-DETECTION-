# routes/analysis.py — Meenashi S
from flask import Blueprint, request, jsonify
from models.db import get_all_records, get_records_by_location, get_records_by_type, get_all_locations, get_all_crime_types
from collections import defaultdict

analysis_bp = Blueprint("analysis", __name__)

# ── Summary ───────────────────────────────────────────────────────────────────
@analysis_bp.route("/summary", methods=["GET"])
def view_summary():
    records      = get_all_records()
    total_crimes = sum(r["count"] for r in records)
    by_type      = defaultdict(int)
    by_location  = defaultdict(int)
    for r in records:
        by_type[r["type"]]         += r["count"]
        by_location[r["location"]] += r["count"]
    return jsonify({
        "total_crimes":  total_crimes,
        "total_records": len(records),
        "by_type":       dict(by_type),
        "by_location":   dict(by_location),
        "locations":     get_all_locations(),
        "crime_types":   get_all_crime_types(),
    }), 200

# ── Filter by Location ────────────────────────────────────────────────────────
@analysis_bp.route("/filter/location", methods=["GET"])
def filter_by_location():
    location = request.args.get("location", "").strip()
    if not location:
        return jsonify({"error": "Location parameter required"}), 400
    results = get_records_by_location(location)
    total   = sum(r["count"] for r in results)
    return jsonify({
        "location": location,
        "results":  results,
        "total":    total,
        "count":    len(results)
    }), 200

# ── Filter by Crime Type ──────────────────────────────────────────────────────
@analysis_bp.route("/filter/type", methods=["GET"])
def filter_by_type():
    crime_type = request.args.get("type", "").strip()
    if not crime_type:
        return jsonify({"error": "Crime type parameter required"}), 400
    results = get_records_by_type(crime_type)
    total   = sum(r["count"] for r in results)
    return jsonify({
        "crime_type": crime_type,
        "results":    results,
        "total":      total,
        "count":      len(results)
    }), 200

# ── Crime Trends (monthly) ────────────────────────────────────────────────────
@analysis_bp.route("/trends", methods=["GET"])
def view_trends():
    records = get_all_records()
    monthly = defaultdict(int)
    for r in records:
        month = r["date"][:7]
        monthly[month] += r["count"]
    trend_list = [{"month": k, "total": v} for k, v in sorted(monthly.items())]
    return jsonify({"trends": trend_list}), 200

# ── Crime by Hour (for charts) ────────────────────────────────────────────────
@analysis_bp.route("/by-hour", methods=["GET"])
def by_hour():
    records  = get_all_records()
    hourly   = defaultdict(int)
    for r in records:
        hourly[r["hour"]] += r["count"]
    result = [{"hour": h, "count": hourly.get(h, 0)} for h in range(24)]
    return jsonify({"by_hour": result}), 200

# ── Top Locations ─────────────────────────────────────────────────────────────
@analysis_bp.route("/top-locations", methods=["GET"])
def top_locations():
    records    = get_all_records()
    by_location = defaultdict(int)
    for r in records:
        by_location[r["location"]] += r["count"]
    sorted_locs = sorted(by_location.items(), key=lambda x: x[1], reverse=True)
    return jsonify({
        "top_locations": [{"location": k, "total": v} for k, v in sorted_locs]
    }), 200

# ── All Records ───────────────────────────────────────────────────────────────
@analysis_bp.route("/records", methods=["GET"])
def all_records():
    return jsonify({"records": get_all_records()}), 200
