"""
FlightDeck - Instagram-style social media platform.

Modular architecture ready for:
- Backend server integration (separate API server)
- Database migration (PostgreSQL, MySQL, etc.)
- Enhanced authentication (OAuth, JWT)
- External APIs
- Cloud media storage (S3, CloudFlare)
"""
from flask import Flask
import os

from config import config
from extensions import db, init_extensions
from routes import auth_bp, posts_bp, users_bp


def create_app(config_name=None):
    """
    Application factory pattern for flexible configuration.
    Allows easy switching between development, production, and testing environments.
    """
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    init_extensions(app)
    
    # Register blueprints (modular routes)
    app.register_blueprint(auth_bp)
    app.register_blueprint(posts_bp)
    app.register_blueprint(users_bp)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app


# For direct execution (development)
app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)
