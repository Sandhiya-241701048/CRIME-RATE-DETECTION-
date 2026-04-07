# routes/auth.py — Vaishnav Perumal
from flask import Blueprint, request, jsonify, session
from models.db import USERS, hash_password

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["POST"])
def login():
    data     = request.get_json()
    email    = data.get("email", "").strip().lower()
    password = data.get("password", "").strip()

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    user = USERS.get(email)
    if user and user["password"] == hash_password(password):
        session["user"] = email
        session["role"] = user["role"]
        session["name"] = user["name"]
        return jsonify({
            "message": "Login successful",
            "role":    user["role"],
            "name":    user["name"],
            "email":   email
        }), 200

    return jsonify({"error": "Invalid email or password"}), 401

@auth_bp.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"message": "Logged out successfully"}), 200

@auth_bp.route("/validate", methods=["GET"])
def validate():
    if "user" in session:
        return jsonify({
            "loggedIn": True,
            "email":    session["user"],
            "role":     session["role"],
            "name":     session["name"]
        }), 200
    return jsonify({"loggedIn": False}), 401

@auth_bp.route("/users", methods=["GET"])
def list_users():
    users = [{"email": e, "role": u["role"], "name": u["name"]} for e, u in USERS.items()]
    return jsonify({"users": users}), 200
