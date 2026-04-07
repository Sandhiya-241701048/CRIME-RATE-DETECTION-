# routes/reports.py — Gokul Krishna I S
from flask import Blueprint, request, jsonify
from models.db import get_all_records, get_records_by_location, REPORTS
from collections import defaultdict
from datetime import datetime

reports_bp = Blueprint("reports", __name__)

def build_report(records, title, filters=None):
    total     = sum(r["count"] for r in records)
    by_type   = defaultdict(int)
    by_loc    = defaultdict(int)
    by_month  = defaultdict(int)
    for r in records:
        by_type[r["type"]]         += r["count"]
        by_loc[r["location"]]      += r["count"]
        by_month[r["date"][:7]]    += r["count"]

    return {
        "title":        title,
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "filters":      filters or {},
        "summary": {
            "total_crimes":  total,
            "total_records": len(records),
        },
        "by_crime_type": dict(by_type),
        "by_location":   dict(by_loc),
        "by_month":      dict(sorted(by_month.items())),
        "records":       records,
    }

# ── Generate Report ───────────────────────────────────────────────────────────
@reports_bp.route("/generate", methods=["POST"])
def generate_report():
    data     = request.get_json()
    rtype    = data.get("type", "full")        # full | location | type
    location = data.get("location", "").strip()
    crtype   = data.get("crime_type", "").strip()

    if rtype == "location" and location:
        records = get_records_by_location(location)
        title   = f"Crime Report — {location}"
        filters = {"location": location}
    elif rtype == "type" and crtype:
        from models.db import get_records_by_type
        records = get_records_by_type(crtype)
        title   = f"Crime Report — {crtype}"
        filters = {"crime_type": crtype}
    else:
        records = get_all_records()
        title   = "Full Crime Report"
        filters = {}

    report = build_report(records, title, filters)
    report["id"] = len(REPORTS) + 1
    REPORTS.append(report)

    return jsonify({"message": "Report generated", "report": report}), 200

# ── List Reports ──────────────────────────────────────────────────────────────
@reports_bp.route("/list", methods=["GET"])
def list_reports():
    summaries = [{
        "id":           r["id"],
        "title":        r["title"],
        "generated_at": r["generated_at"],
        "total_crimes": r["summary"]["total_crimes"],
    } for r in REPORTS]
    return jsonify({"reports": summaries}), 200

# ── Get Specific Report ───────────────────────────────────────────────────────
@reports_bp.route("/<int:report_id>", methods=["GET"])
def get_report(report_id):
    report = next((r for r in REPORTS if r["id"] == report_id), None)
    if not report:
        return jsonify({"error": "Report not found"}), 404
    return jsonify(report), 200

# ── Dashboard Stats (for Gokul's charts) ─────────────────────────────────────
@reports_bp.route("/dashboard-stats", methods=["GET"])
def dashboard_stats():
    records     = get_all_records()
    total       = sum(r["count"] for r in records)
    by_type     = defaultdict(int)
    by_location = defaultdict(int)
    by_month    = defaultdict(int)
    hourly      = defaultdict(int)

    for r in records:
        by_type[r["type"]]         += r["count"]
        by_location[r["location"]] += r["count"]
        by_month[r["date"][:7]]    += r["count"]
        hourly[r["hour"]]          += r["count"]

    peak_hour = max(hourly, key=hourly.get) if hourly else 22

    return jsonify({
        "total_crimes":    total,
        "total_records":   len(records),
        "total_locations": len(set(r["location"] for r in records)),
        "total_reports":   len(REPORTS),
        "peak_hour":       f"{peak_hour}:00",
        "by_type":         [{"type": k, "count": v} for k, v in sorted(by_type.items(), key=lambda x: x[1], reverse=True)],
        "by_location":     [{"location": k, "count": v} for k, v in sorted(by_location.items(), key=lambda x: x[1], reverse=True)],
        "by_month":        [{"month": k, "count": v} for k, v in sorted(by_month.items())],
    }), 200
