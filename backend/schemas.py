from marshmallow import Schema, fields, validate

# -----------------------------
# User Schema
# -----------------------------
class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    email = fields.Email(required=True, validate=validate.Length(max=255))
    password = fields.Str(load_only=True, required=True, validate=validate.Length(min=6))
    created_at = fields.DateTime(dump_only=True)

user_schema = UserSchema()
user_list_schema = UserSchema(many=True)

# -----------------------------
# Tag Schema
# -----------------------------
class TagSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)


# -----------------------------
# Company Tag Schema
# -----------------------------
class CompanyTagSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)


# -----------------------------
# Problem Schema
# -----------------------------
class ProblemSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True, validate=validate.Length(max=255))
    topic = fields.Str(required=True, validate=validate.Length(max=100))
    difficulty = fields.Str(required=True, validate=validate.OneOf(["Easy", "Medium", "Hard"]))
    platform = fields.Str(required=True, validate=validate.Length(max=100))
    link = fields.Url(required=True, error_messages={"invalid": "Invalid URL format."})
    
    tags = fields.List(fields.Nested(TagSchema), missing=[])  # Ensures default empty list if None
    company_tags = fields.List(fields.Nested(CompanyTagSchema), missing=[])

problem_schema = ProblemSchema()
problem_list_schema = ProblemSchema(many=True)

# -----------------------------
# User Progress Schema
# -----------------------------
class UserProgressSchema(Schema):
    user_id = fields.Int(dump_only=True)  # Ensures user_id is included in responses
    problem_id = fields.Int(required=True)
    solved_status = fields.Bool(default=False)
    needs_revision = fields.Bool(default=False)
    notes = fields.Str(validate=validate.Length(max=500))
    last_updated = fields.DateTime(dump_only=True)

user_progress_schema = UserProgressSchema()
user_progress_list_schema = UserProgressSchema(many=True)
