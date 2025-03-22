from flask import Flask, request
from config import Config
from extensions import db, jwt, bcrypt, migrate, csrf, limiter
from routes.auth import auth_bp
from routes.problems import problems_bp
from routes.user_progress import user_progress_bp
from routes.test import test_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)  

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)
    limiter.init_app(app)

    # # Disable CSRF for JSON API requests
    # @app.before_request
    # def disable_csrf_for_json():
    #     if request.content_type == "application/json":
    #         csrf._disable_on_request()

    # Register Blueprints
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(problems_bp, url_prefix="/problems")
    app.register_blueprint(user_progress_bp, url_prefix="/user")
    app.register_blueprint(test_bp, url_prefix="/")  # Temporary test API

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
