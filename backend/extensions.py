from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Initialize Flask extensions
db = SQLAlchemy()      # Database ORM
jwt = JWTManager()     # JWT Authentication
bcrypt = Bcrypt()      # Password Hashing
migrate = Migrate()    # Database Migrations
csrf = CSRFProtect()
limiter = Limiter(get_remote_address, default_limits=["5 per minute"])