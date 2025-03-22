from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db, csrf
from models import Problem, UserProgress, User
from schemas import problem_schema, problem_list_schema

problems_bp = Blueprint("problems", __name__)

@problems_bp.route("/", methods=["GET"])
@jwt_required()
@csrf.exempt
def get_all_problems():
    """Fetches all problems with optional filtering & pagination."""
    topic = request.args.get("topic")
    difficulty = request.args.get("difficulty")
    platform = request.args.get("platform")
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)

    query = Problem.query

    if topic:
        query = query.filter(Problem.topic == topic)
    if difficulty:
        query = query.filter(Problem.difficulty == difficulty)
    if platform:
        query = query.filter(Problem.platform == platform)

    problems = query.paginate(page=page, per_page=per_page, error_out=False)

    return jsonify({
        "total_problems": problems.total,
        "problems": problem_list_schema.dump(problems.items)
    }), 200


@problems_bp.route("/<int:problem_id>", methods=["GET"])
@jwt_required()
@csrf.exempt
def get_problem(problem_id):
    """Fetches a single problem by its ID."""
    problem = Problem.query.get(problem_id)

    if not problem:
        return jsonify({"error": "Problem not found"}), 404

    return jsonify(problem_schema.dump(problem)), 200


@problems_bp.route("/", methods=["POST"])
@jwt_required()
@csrf.exempt
def add_problem():
    """Admin-only: Adds a new problem."""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user or user.email != "admin@hashprep.com":
        return jsonify({"error": "Unauthorized: Admin access required"}), 403

    data = request.get_json()
    
    errors = problem_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    
    new_problem = Problem(
        title=data["title"],
        topic=data["topic"],
        difficulty=data["difficulty"],
        platform=data["platform"],
        link=data["link"],
        tags=", ".join(data.get("tags", [])),
        company_tags=", ".join(data.get("company_tags", []))
    )

    print(data.get("company_tags", []))
    print(new_problem.company_tags)

    db.session.add(new_problem)
    db.session.commit()

    return jsonify(problem_schema.dump(new_problem)), 201


@problems_bp.route("/bookmark/toggle", methods=["POST"])
@jwt_required()
@csrf.exempt
def toggle_bookmark():
    """Allows a user to toggle the bookmark status (`needs_revision`)."""
    user_id = get_jwt_identity()
    data = request.get_json()
    problem_id = data.get("problem_id")

    if not problem_id:
        return jsonify({"error": "Problem ID is required"}), 400

    problem = Problem.query.get(problem_id)
    if not problem:
        return jsonify({"error": "Problem not found"}), 404

    progress = UserProgress.query.filter_by(user_id=user_id, problem_id=problem_id).first()

    if not progress:
        progress = UserProgress(user_id=user_id, problem_id=problem_id, needs_revision=True)
        db.session.add(progress)
        message = "Problem bookmarked"
    else:
        progress.needs_revision = not progress.needs_revision
        message = "Bookmark removed" if not progress.needs_revision else "Problem bookmarked"

    db.session.commit()
    return jsonify({"message": message, "needs_revision": progress.needs_revision}), 200


@problems_bp.route("/bookmarked", methods=["GET"])
@jwt_required()
@csrf.exempt
def get_bookmarked_problems():
    """Fetch all problems bookmarked by the authenticated user."""
    user_id = get_jwt_identity()
    
    bookmarked_problems = (
        db.session.query(Problem)
        .join(UserProgress, UserProgress.problem_id == Problem.id)
        .filter(UserProgress.user_id == user_id, UserProgress.needs_revision == True)
        .all()
    )

    if not bookmarked_problems:
        return jsonify({"message": "No bookmarked problems found"}), 200

    return jsonify(problem_list_schema.dump(bookmarked_problems)), 200
