# routes/dataset.py — Sandhiya E
import os, csv, json
from flask import Blueprint, request, jsonify
from models.db import DATASETS, CRIME_RECORDS
from datetime import datetime

dataset_bp = Blueprint("dataset", __name__)

UPLOAD_FOLDER     = "uploads"
ALLOWED_EXTENSIONS = {"csv", "json"}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def validate_csv_columns(filepath):
    required = {"location", "type", "date", "count"}
    with open(filepath, newline="") as f:
        reader = csv.DictReader(f)
        cols   = set(c.strip().lower() for c in (reader.fieldnames or []))
    missing = required - cols
    return list(missing)

def load_csv_to_records(filepath, filename):
    loaded = []
    with open(filepath, newline="") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader, start=len(CRIME_RECORDS) + 1):
            try:
                CRIME_RECORDS.append({
                    "id":          i,
                    "location":    row.get("location", "Unknown"),
                    "district":    row.get("district", "Unknown"),
                    "type":        row.get("type", "Unknown"),
                    "date":        row.get("date", "2024-01-01"),
                    "hour":        int(row.get("hour", 20)),
                    "day_of_week": int(row.get("day_of_week", 0)),
                    "month":       int(row.get("month", 1)),
                    "count":       int(row.get("count", 1)),
                })
                loaded.append(i)
            except Exception:
                continue
    return len(loaded)

# ── Upload ────────────────────────────────────────────────────────────────────
@dataset_bp.route("/upload", methods=["POST"])
def upload_dataset():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400
    if not allowed_file(file.filename):
        return jsonify({"error": "Only CSV or JSON files allowed"}), 400

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    # Validate columns
    missing = validate_csv_columns(filepath)
    if missing:
        os.remove(filepath)
        return jsonify({"error": f"Missing required columns: {missing}"}), 422

    # Load records
    loaded = load_csv_to_records(filepath, file.filename)

    entry = {
        "id":          len(DATASETS) + 1,
        "filename":    file.filename,
        "records":     loaded,
        "uploaded_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "valid":       True,
    }
    DATASETS.append(entry)

    return jsonify({
        "message":  f"'{file.filename}' uploaded and {loaded} records loaded",
        "dataset":  entry
    }), 201

# ── Validate ──────────────────────────────────────────────────────────────────
@dataset_bp.route("/validate", methods=["POST"])
def validate_dataset():
    data     = request.get_json()
    filename = data.get("filename")
    if not filename:
        return jsonify({"error": "Filename required"}), 400
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    if not os.path.exists(filepath):
        return jsonify({"error": "File not found"}), 404

    missing = validate_csv_columns(filepath)
    if missing:
        return jsonify({"valid": False, "missing_columns": missing}), 200
    return jsonify({"valid": True, "message": "All required columns present"}), 200

# ── List ──────────────────────────────────────────────────────────────────────
@dataset_bp.route("/list", methods=["GET"])
def list_datasets():
    return jsonify({"datasets": DATASETS, "count": len(DATASETS)}), 200

# ── Update (re-upload) ────────────────────────────────────────────────────────
@dataset_bp.route("/update/<int:dataset_id>", methods=["PUT"])
def update_dataset(dataset_id):
    ds = next((d for d in DATASETS if d["id"] == dataset_id), None)
    if not ds:
        return jsonify({"error": "Dataset not found"}), 404
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400
    file = request.files["file"]
    if not allowed_file(file.filename):
        return jsonify({"error": "Only CSV or JSON files allowed"}), 400

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)
    ds["filename"]    = file.filename
    ds["uploaded_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")
    return jsonify({"message": "Dataset updated", "dataset": ds}), 200

# ── Delete ────────────────────────────────────────────────────────────────────
@dataset_bp.route("/delete/<int:dataset_id>", methods=["DELETE"])
def delete_dataset(dataset_id):
    global DATASETS
    ds = next((d for d in DATASETS if d["id"] == dataset_id), None)
    if not ds:
        return jsonify({"error": "Dataset not found"}), 404
    filepath = os.path.join(UPLOAD_FOLDER, ds["filename"])
    if os.path.exists(filepath):
        os.remove(filepath)
    DATASETS = [d for d in DATASETS if d["id"] != dataset_id]
    return jsonify({"message": f"Dataset '{ds['filename']}' deleted"}), 200
