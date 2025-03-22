from flask import Blueprint, jsonify

test_bp = Blueprint("test", __name__)

@test_bp.route("/test", methods=["GET"])
def test_api():
    """Temporary test API to say Hello, World!"""
    return jsonify({"message": "Hello, World!"}), 200
