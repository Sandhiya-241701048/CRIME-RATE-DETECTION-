# models/db.py — In-memory database (replace with Azure SQL later)
# All data is stored here so the app works without any database setup

import hashlib
from datetime import datetime

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# ── Users ────────────────────────────────────────────────────────────────────
USERS = {
    "user@crime.com":  {"password": hash_password("user123"),  "role": "user",  "name": "John User"},
    "admin@crime.com": {"password": hash_password("admin123"), "role": "admin", "name": "Admin"},
}

# ── Crime Records ─────────────────────────────────────────────────────────────
CRIME_RECORDS = [
    {"id":  1, "location": "Chennai",   "district": "Tambaram",    "type": "Theft",    "date": "2024-01-05", "hour": 22, "day_of_week": 4, "month": 1, "count": 45},
    {"id":  2, "location": "Chennai",   "district": "Anna Nagar",  "type": "Robbery",  "date": "2024-01-10", "hour": 23, "day_of_week": 2, "month": 1, "count": 20},
    {"id":  3, "location": "Chennai",   "district": "T Nagar",     "type": "Assault",  "date": "2024-01-18", "hour": 21, "day_of_week": 5, "month": 1, "count": 15},
    {"id":  4, "location": "Mumbai",    "district": "Andheri",     "type": "Assault",  "date": "2024-01-12", "hour": 20, "day_of_week": 1, "month": 1, "count": 30},
    {"id":  5, "location": "Mumbai",    "district": "Dadar",       "type": "Fraud",    "date": "2024-01-22", "hour": 14, "day_of_week": 3, "month": 1, "count": 25},
    {"id":  6, "location": "Delhi",     "district": "Connaught",   "type": "Theft",    "date": "2024-02-15", "hour": 19, "day_of_week": 5, "month": 2, "count": 60},
    {"id":  7, "location": "Delhi",     "district": "Karol Bagh",  "type": "Robbery",  "date": "2024-02-20", "hour": 23, "day_of_week": 3, "month": 2, "count": 35},
    {"id":  8, "location": "Bangalore", "district": "Whitefield",  "type": "Fraud",    "date": "2024-03-01", "hour": 11, "day_of_week": 4, "month": 3, "count": 15},
    {"id":  9, "location": "Bangalore", "district": "Koramangala", "type": "Theft",    "date": "2024-03-10", "hour": 22, "day_of_week": 5, "month": 3, "count": 28},
    {"id": 10, "location": "Hyderabad", "district": "Banjara Hills","type": "Assault", "date": "2024-03-15", "hour": 21, "day_of_week": 4, "month": 3, "count": 18},
    {"id": 11, "location": "Chennai",   "district": "Velachery",   "type": "Fraud",    "date": "2024-04-02", "hour": 10, "day_of_week": 1, "month": 4, "count": 12},
    {"id": 12, "location": "Mumbai",    "district": "Bandra",      "type": "Theft",    "date": "2024-04-14", "hour": 22, "day_of_week": 6, "month": 4, "count": 40},
    {"id": 13, "location": "Delhi",     "district": "Lajpat Nagar","type": "Assault",  "date": "2024-05-03", "hour": 20, "day_of_week": 4, "month": 5, "count": 22},
    {"id": 14, "location": "Bangalore", "district": "Indiranagar", "type": "Robbery",  "date": "2024-05-18", "hour": 23, "day_of_week": 5, "month": 5, "count": 10},
    {"id": 15, "location": "Hyderabad", "district": "Hitech City", "type": "Fraud",    "date": "2024-06-07", "hour": 13, "day_of_week": 4, "month": 6, "count": 20},
    {"id": 16, "location": "Chennai",   "district": "Porur",       "type": "Theft",    "date": "2024-06-20", "hour": 22, "day_of_week": 3, "month": 6, "count": 33},
    {"id": 17, "location": "Mumbai",    "district": "Kurla",       "type": "Robbery",  "date": "2024-07-08", "hour": 21, "day_of_week": 0, "month": 7, "count": 27},
    {"id": 18, "location": "Delhi",     "district": "Saket",       "type": "Theft",    "date": "2024-07-22", "hour": 23, "day_of_week": 0, "month": 7, "count": 50},
    {"id": 19, "location": "Bangalore", "district": "Marathahalli","type": "Assault",  "date": "2024-08-05", "hour": 20, "day_of_week": 0, "month": 8, "count": 14},
    {"id": 20, "location": "Hyderabad", "district": "Madhapur",    "type": "Theft",    "date": "2024-08-19", "hour": 22, "day_of_week": 0, "month": 8, "count": 38},
]

DATASETS = []
REPORTS  = []

def get_all_records():
    return CRIME_RECORDS

def get_records_by_location(location):
    return [r for r in CRIME_RECORDS if r["location"].lower() == location.lower()]

def get_records_by_type(crime_type):
    return [r for r in CRIME_RECORDS if r["type"].lower() == crime_type.lower()]

def get_all_locations():
    return sorted(list(set(r["location"] for r in CRIME_RECORDS)))

def get_all_crime_types():
    return sorted(list(set(r["type"] for r in CRIME_RECORDS)))
