"""
Authentication service - ready for OAuth, JWT, and other auth providers.
"""
from models import User
from extensions import db


class AuthService:
    """
    Authentication service handling user registration, login, and verification.
    Can be extended to support OAuth, JWT, and other authentication methods.
    """
    
    @staticmethod
    def register_user(username, email, password):
        """
        Register a new user.
        Returns: (user, error_message)
        """
        # Check if username exists
        if User.query.filter_by(username=username).first():
            return None, 'Username already exists'
        
        # Check if email exists
        if User.query.filter_by(email=email).first():
            return None, 'Email already registered'
        
        # Create new user
        user = User(username=username, email=email)
        user.set_password(password)
        
        try:
            db.session.add(user)
            db.session.commit()
            return user, None
        except Exception as e:
            db.session.rollback()
            return None, f'Registration failed: {str(e)}'
    
    @staticmethod
    def authenticate_user(username, password):
        """
        Authenticate user with username and password.
        Returns: (user, error_message)
        """
        user = User.query.filter_by(username=username).first()
        
        if not user or not user.check_password(password):
            return None, 'Invalid username or password'
        
        return user, None
    
    @staticmethod
    def update_user_profile(user, bio=None):
        """
        Update user profile information.
        Returns: (success, error_message)
        """
        try:
            if bio is not None:
                user.bio = bio
            
            db.session.commit()
            return True, None
        except Exception as e:
            db.session.rollback()
            return False, f'Profile update failed: {str(e)}'
    
    # Future OAuth integration methods
    @staticmethod
    def authenticate_oauth(provider, oauth_id, user_data):
        """
        Placeholder for OAuth authentication.
        Can be implemented for Google, GitHub, Facebook, etc.
        """
        # Check if user exists with this OAuth provider
        user = User.query.filter_by(oauth_provider=provider, oauth_id=oauth_id).first()
        
        if not user:
            # Create new user from OAuth data
            user = User(
                username=user_data.get('username'),
                email=user_data.get('email'),
                oauth_provider=provider,
                oauth_id=oauth_id
            )
            user.set_password('oauth-user-no-password')  # OAuth users don't need password
            db.session.add(user)
            db.session.commit()
        
        return user, None
