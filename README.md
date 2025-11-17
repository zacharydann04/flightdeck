# FlightDeck - Social Media Platform

FlightDeck is an Instagram-style social media platform where users can create accounts, share posts, and interact with content through likes and comments.

## Features

- **User Authentication**: Register, login, and logout functionality
- **User Profiles**: Customizable profiles with bio and post history
- **Posts**: Create, view, and delete posts with optional images
- **Likes**: Like posts and see who has liked them
- **Comments**: Comment on posts and view all comments
- **Social Feed**: View posts from all users in chronological order

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python run.py
```

Or use the app directly:
```bash
python app.py
```

3. Open your browser and navigate to `http://localhost:5000`

## Architecture

FlightDeck uses a modular architecture that makes it easy to integrate with external backends, databases, and services. See [API_INTEGRATION.md](API_INTEGRATION.md) for detailed integration guidance.

## Usage

1. Register a new account
2. Login with your credentials
3. Create posts from the "Create Post" page
4. Browse the feed and interact with posts by liking or commenting
5. View user profiles to see their posts
6. Edit your profile bio from your profile page

## Technology Stack

- **Backend**: Flask (Python web framework)
- **Database**: SQLite with SQLAlchemy ORM
- **Authentication**: Flask-Login
- **Frontend**: HTML, CSS, JavaScript
- **Security**: Werkzeug password hashing

## Project Structure

```
flightdeck/
├── app.py                  # Application factory
├── run.py                  # Development server entry point
├── extensions.py           # Flask extensions initialization
├── requirements.txt        # Python dependencies
├── API_INTEGRATION.md      # Integration guide for backends/APIs
├── config/                 # Configuration management
│   └── settings.py         # Environment-specific settings
├── models/                 # Database models (easily adaptable)
│   ├── user.py            # User model
│   ├── post.py            # Post model
│   ├── like.py            # Like model
│   └── comment.py         # Comment model
├── services/              # Business logic layer
│   ├── auth_service.py    # Authentication service
│   ├── post_service.py    # Post operations service
│   └── media_service.py   # Media storage service (ready for S3/CDN)
├── routes/                # HTTP endpoints (blueprints)
│   ├── auth.py            # Authentication routes
│   ├── posts.py           # Post-related routes
│   └── users.py           # User profile routes
├── templates/             # HTML templates
│   ├── base.html          # Base template
│   ├── landing.html       # Landing page
│   ├── login.html         # Login page
│   ├── register.html      # Registration page
│   ├── feed.html          # Main feed
│   ├── profile.html       # User profile
│   ├── edit_profile.html  # Profile editing
│   ├── create_post.html   # Post creation
│   ├── post.html          # Individual post view
│   ├── likes.html         # View post likes
│   └── comments.html      # View post comments
└── static/
    ├── css/
    │   └── style.css      # Styling
    └── js/
        └── main.js        # Frontend JavaScript
```

## Future Integration

FlightDeck is designed with modularity in mind for easy integration with:

- **Backend Servers**: Separate API server (Node.js, Django, etc.)
- **Databases**: PostgreSQL, MySQL, MongoDB (currently SQLite)
- **Authentication**: OAuth (Google, GitHub), JWT tokens
- **APIs**: RESTful API ready (see API_INTEGRATION.md)
- **Media Storage**: AWS S3, CloudFlare R2, Azure Blob Storage

See [API_INTEGRATION.md](API_INTEGRATION.md) for detailed integration instructions.