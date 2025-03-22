import os
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()

class Config:
    """Flask Configuration Class"""
    
    # Secret keys
    SECRET_KEY = os.getenv("SECRET_KEY", "fallback-secret-key")  # Fallback for local dev
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "fallback-jwt-secret")

    # Database Configuration
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "mysql://user:password@localhost/hashprep").replace("mysql://", "mysql+pymysql://")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # OAuth Configuration (For Google Login)
    GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
    
    # Security Configs
    SESSION_COOKIE_SECURE = True  # Use Secure Cookies (Only HTTPS)
    SESSION_COOKIE_HTTPONLY = True  # Prevent JavaScript Access
    SESSION_COOKIE_SAMESITE = "Lax"  # Protect Against CSRF