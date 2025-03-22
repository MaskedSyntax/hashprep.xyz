from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models import UserProgress, Problem
from schemas import user_progress_schema, user_progress_list_schema

user_progress_bp = Blueprint("user_progress", __name__)

@user_progress_bp.route("/progress", methods=["POST"])
@jwt_required()
def update_progress():
    """Validates and updates user progress."""
    user_id = get_jwt_identity()
    data = request.get_json()

    errors = user_progress_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    problem = Problem.query.get(data["problem_id"])
    if not problem:
        return jsonify({"error": "Problem does not exist"}), 404

    progress = UserProgress.query.filter_by(user_id=user_id, problem_id=data["problem_id"]).first()

    if not progress:
        progress = UserProgress(
            user_id=user_id,
            problem_id=data["problem_id"],
            solved_status=data.get("solved_status", False),
            needs_revision=data.get("needs_revision", False),
            notes=data.get("notes", "")
        )
        db.session.add(progress)
    else:
        progress.solved_status = data.get("solved_status", progress.solved_status)
        progress.needs_revision = data.get("needs_revision", progress.needs_revision)
        progress.notes = data.get("notes", progress.notes)

    db.session.commit()

    return jsonify(user_progress_schema.dump(progress)), 200


@user_progress_bp.route("/progress", methods=["GET"])
@jwt_required()
def get_user_progress():
    """Fetches the progress of the authenticated user on all problems."""
    user_id = get_jwt_identity()

    progress_entries = (
        db.session.query(UserProgress, Problem)
        .join(Problem, Problem.id == UserProgress.problem_id)
        .filter(UserProgress.user_id == user_id)
        .all()
    )

    if not progress_entries:
        return jsonify({"message": "No progress found"}), 200

    return jsonify(user_progress_list_schema.dump([
        {
            "problem_id": problem.id,
            "title": problem.title,
            "topic": problem.topic,
            "difficulty": problem.difficulty,
            "platform": problem.platform,
            "link": problem.link,
            "tags": problem.tags.split(", ") if problem.tags else [],
            "company_tags": problem.company_tags.split(", ") if problem.company_tags else [],
            "solved_status": progress.solved_status,
            "needs_revision": progress.needs_revision,
            "notes": progress.notes
        }
        for progress, problem in progress_entries
    ])), 200
