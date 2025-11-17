"""
Configuration settings for FlightDeck application.
Easily adaptable for different environments and backend systems.
"""
import os

class Config:
    """Base configuration class."""
    
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Database settings - can be easily swapped for PostgreSQL, MySQL, etc.
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///flightdeck.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # API settings for future REST API implementation
    API_VERSION = 'v1'
    API_PREFIX = f'/api/{API_VERSION}'
    
    # Media storage settings - ready for S3, CloudFlare, etc.
    MEDIA_STORAGE_PROVIDER = os.environ.get('MEDIA_STORAGE_PROVIDER', 'local')
    MEDIA_UPLOAD_FOLDER = os.environ.get('MEDIA_UPLOAD_FOLDER', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    
    # Authentication settings - ready for OAuth, JWT, etc.
    AUTH_PROVIDER = os.environ.get('AUTH_PROVIDER', 'local')
    SESSION_COOKIE_SECURE = os.environ.get('SESSION_COOKIE_SECURE', 'False').lower() == 'true'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # CORS settings for future API integration
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '*').split(',')
    
    # Pagination settings
    POSTS_PER_PAGE = 20
    COMMENTS_PER_PAGE = 50

class DevelopmentConfig(Config):
    """Development environment configuration."""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """Production environment configuration."""
    DEBUG = False
    TESTING = False
    SESSION_COOKIE_SECURE = True

class TestingConfig(Config):
    """Testing environment configuration."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

# Configuration dictionary for easy environment switching
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
