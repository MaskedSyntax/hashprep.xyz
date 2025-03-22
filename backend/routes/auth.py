from flask import Blueprint, request, jsonify
from extensions import db, bcrypt, jwt, limiter, csrf
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models import User

auth_bp = Blueprint("auth", __name__)

# -----------------------------
# User Signup
# -----------------------------
@auth_bp.route("/signup", methods=["POST"])
@csrf.exempt
@limiter.limit("3 per minute")
def signup():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password required"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already exists"}), 409

    user = User(email=email)
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201

# -----------------------------
# User Login
# -----------------------------
@auth_bp.route("/login", methods=["POST"])
@csrf.exempt
@limiter.limit("5 per minute")
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()

    if not user or not user.check_password(password):
        return jsonify({"error": "Invalid credentials"}), 401

    access_token = create_access_token(identity=str(user.id))
    return jsonify({"access_token": access_token}), 200

# -----------------------------
# Protected Route (Example)
# -----------------------------
@auth_bp.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify({"message": f"Welcome user {current_user}!"}), 200
