from flask import Blueprint, jsonify, request
from app.models import User
from app.db import db
import re
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from datetime import timedelta

bcrypt = Bcrypt()

users_bp = Blueprint("users", __name__)


@users_bp.route("/sign-up", methods=["POST"])
def add_users():
    try:
        data = request.get_json()
        full_name = data.get("full_name")
        email = data.get("email")
        password = data.get("password")
        confirm_password = data.get("confirm_password")
        terms_accepted = data.get("terms_accepted")

        
        if not full_name:
            return jsonify({"error": "Full Name is required"}), 400
        
        if len(full_name.strip()) < 2:
            return jsonify({"error": "Full Name must be at least 2 characters"}), 400
        
        if not email:
            return jsonify({"error": "Email is required"}), 400

        # Validate email format
        email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(email_regex, email):
            return jsonify({"error": "Invalid Email Address"}), 400

        if not password:
            return jsonify({"error": "Password is required"}), 400

        if len(password) < 8:
            return jsonify({"error": "Password must be at least 8 characters long"}), 400
        
        if not confirm_password:
            return jsonify({"error": "Please confirm your password"}), 400
        
        if password != confirm_password:
            return jsonify({"error": "Passwords do not match"}), 400

        if not terms_accepted:
            return jsonify({"error": "You must accept the terms and conditions"}), 400

        
        exists = User.query.filter_by(email=email).first()
        if exists:
            return jsonify({"error": "User with this email already exists"}), 409

        # Hash password
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        
        new_user = User(
            full_name=full_name,
            email=email,
            password=hashed_password,
            terms_accepted=terms_accepted
            
        )

        
        db.session.add(new_user)
        db.session.commit()

        
        access_token = create_access_token(
            identity=str(new_user.id),
            additional_claims={"email": new_user.email},
            expires_delta=timedelta(hours=1)
        )

        
        return jsonify({
            "message": "User created successfully",
            "user": {
                "user_id": new_user.id,
                "full_name": new_user.full_name,
                "email": new_user.email,
                "terms_accepted": new_user.terms_accepted
            },
            "access_token": access_token
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@users_bp.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")

        
        if not email:
            return jsonify({"error": "Email is required"}), 400
        
        if not password:
            return jsonify({"error": "Password is required"}), 400

        
        user = User.query.filter_by(email=email).first()
        
        if not user:
            return jsonify({"error": "Invalid email or password"}), 401
        
        
        if not bcrypt.check_password_hash(user.password, password):
            return jsonify({"error": "Invalid email or password"}), 401

        
        access_token = create_access_token(
            identity=str(user.id),
            additional_claims={"email": user.email},
            expires_delta=timedelta(hours=1)
        )

        
        return jsonify({
            "message": "Login successful",
            "user": {
                "user_id": user.id,
                "full_name": user.full_name,
                "email": user.email
            },
            "access_token": access_token
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# @users_bp.route("/profile", methods=["GET"])
# def get_profile():
#     try:
#         user_id = get_jwt_identity()
#         user = User.query.get(user_id)
        
#         if not user:
#             return jsonify({"error": "User not found"}), 404
        
#         return jsonify({
#             "user": {
#                 "user_id": user.id,
#                 "full_name": user.full_name,
#                 "email": user.email
#             }
#         }), 200

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500


# @users_bp.route("/logout", methods=["POST"])
# def logout():
#     return jsonify({
#         "message": "Logged out successfully"
#     }), 200