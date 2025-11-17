"""
Application entry point.
Use this file to run the development server.

WARNING: Debug mode is enabled for development only.
For production, use a WSGI server like Gunicorn:
    gunicorn -w 4 -b 0.0.0.0:8000 'app:create_app("production")'
"""
from app import create_app
import os

if __name__ == '__main__':
    # Development server only - DO NOT use in production
    env = os.environ.get('FLASK_ENV', 'development')
    app = create_app(env)
    
    # Debug mode should only be enabled in development
    debug_mode = env == 'development'
    app.run(debug=debug_mode, host='0.0.0.0', port=5000)
