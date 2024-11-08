from flask import Blueprint, jsonify, request
from flask_login import current_user, login_user, logout_user
from ..models.user import User
from sqlalchemy import or_

bp = Blueprint("session", __name__, url_prefix="/api/session")


@bp.route("/", methods=["GET"])
def get_current_user():
    if current_user.is_authenticated:
        return jsonify({"user": current_user.to_dict()}), 200
    return jsonify({"user": None})


@bp.route("/", methods=["POST"])
def login():
    if current_user.is_authenticated:
        return jsonify({"message": "already logged in bro"})
    # should hide login button

    data = request.get_json()
    if not data:
        return jsonify({"error": "something wrong with request format"})

    credential = data.get("credential")
    password = data.get("password")

    if not credential or not password:
        return jsonify({"error": "username/email and password are required"}), 404

    user = User.query.filter(
        or_(User.username == credential, User.email == credential)
    ).first()

    if not user or not user.check_password(password):
        return jsonify({"error": "Invalid username or password"}), 400

    login_user(user)
    return jsonify({"user": user.to_dict()}), 200


@bp.route("/", methods=["DELETE"])
def logout():
    if not current_user.is_authenticated:
        return jsonify({"error": "No user logged in"}), 401

    logout_user()
    return jsonify({"message": "Logout success"}), 200
