from extensions import db, bcrypt

# Association Tables (exact table names matching models below)
problem_tags = db.Table(
    'problem_tags',
    db.Column('problem_id', db.Integer, db.ForeignKey('problems.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True)
)

problem_company_tags = db.Table(
    'problem_company_tags',
    db.Column('problem_id', db.Integer, db.ForeignKey('problems.id'), primary_key=True),
    db.Column('company_tag_id', db.Integer, db.ForeignKey('company_tag.id'), primary_key=True)
)

# User Model
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=True)
    google_id = db.Column(db.String(255), unique=True, nullable=True)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

# Problem Model
class Problem(db.Model):
    __tablename__ = "problems"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False, index=True)
    topic = db.Column(db.String(255), nullable=False, index=True)
    difficulty = db.Column(db.Enum("Easy", "Medium", "Hard"), nullable=False)
    platform = db.Column(db.String(100), nullable=False)
    link = db.Column(db.String(500), nullable=False)

    tags = db.relationship('Tag', secondary=problem_tags, backref='problems')
    company_tags = db.relationship('CompanyTag', secondary=problem_company_tags, backref='problems')

# Tag Model
class Tag(db.Model):
    __tablename__ = 'tag'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

# CompanyTag Model
class CompanyTag(db.Model):
    __tablename__ = 'company_tag'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

# UserProgress Model
class UserProgress(db.Model):
    __tablename__ = "user_progress"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    problem_id = db.Column(db.Integer, db.ForeignKey("problems.id"), nullable=False)
    solved_status = db.Column(db.Boolean, default=False)
    needs_revision = db.Column(db.Boolean, default=False)
    notes = db.Column(db.Text, nullable=True)
    last_updated = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    user = db.relationship("User", backref=db.backref("progress", lazy="dynamic", cascade="all, delete-orphan"))
    problem = db.relationship("Problem", backref=db.backref("progress", lazy="dynamic", cascade="all, delete-orphan"))
