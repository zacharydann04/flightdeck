# FlightDeck

A social profile platform where users can create accounts, customize their profiles with pictures and bio, and view other users' profiles - similar to Instagram.

## Features

- **User Registration**: Create an account with username, email, and password
- **Authentication**: Secure login system with JWT tokens
- **User Profiles**: Each user has a profile page with:
  - Username
  - Full name
  - Bio
  - Profile picture
  - Member since date
- **Profile Management**: Users can edit their own profiles
- **Profile Picture Upload**: Upload and change profile pictures
- **View Profiles**: Browse other users' profiles

## Technology Stack

- **Backend**: Node.js with Express
- **Database**: SQLite3
- **Authentication**: JWT with bcrypt password hashing
- **File Upload**: Multer for profile pictures
- **Frontend**: HTML, CSS, JavaScript (vanilla)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/zacharydann04/flightdeck.git
cd flightdeck
```

2. Install dependencies:
```bash
npm install
```

3. Start the server:
```bash
npm start
```

4. Open your browser and navigate to:
```
http://localhost:3000
```

## Usage

### Creating an Account

1. Navigate to the homepage
2. Click "Sign Up"
3. Fill in your username, email, password, and optional full name
4. Click "Sign Up" to create your account
5. You'll be redirected to your profile page

### Logging In

1. Click "Login" from the homepage
2. Enter your username and password
3. Click "Login" to access your account

### Editing Your Profile

1. Navigate to your profile page
2. Click "Edit Profile"
3. Update your full name and bio
4. Upload a profile picture (optional)
5. Click "Save Changes"

### Viewing Other Profiles

- Navigate to `/profile/:username` where `:username` is the username of the user you want to view

## API Endpoints

### Authentication

- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - Login
- `POST /api/auth/logout` - Logout

### Profile

- `GET /api/profile/me` - Get current user's profile
- `GET /api/profile/:username` - Get user profile by username
- `PUT /api/profile/me` - Update current user's profile
- `POST /api/profile/me/picture` - Upload profile picture

## Security Features

- Passwords are hashed using bcrypt
- JWT tokens for session management
- HTTP-only cookies for token storage
- Input validation and sanitization
- File upload restrictions (images only, 5MB max)

## Project Structure

```
flightdeck/
├── src/
│   ├── models/
│   │   ├── database.js    # Database initialization
│   │   └── User.js        # User model
│   ├── routes/
│   │   ├── auth.js        # Authentication routes
│   │   └── profile.js     # Profile routes
│   ├── middleware/
│   │   └── auth.js        # Authentication middleware
│   └── server.js          # Express server
├── public/
│   ├── css/
│   │   └── style.css      # Styles
│   ├── js/
│   │   ├── auth.js        # Authentication helpers
│   │   ├── signup.js      # Signup page logic
│   │   ├── login.js       # Login page logic
│   │   ├── profile.js     # Profile view logic
│   │   └── edit-profile.js # Profile edit logic
│   ├── uploads/           # Profile pictures storage
│   ├── index.html         # Homepage
│   ├── signup.html        # Sign up page
│   ├── login.html         # Login page
│   ├── profile.html       # Profile view page
│   └── edit-profile.html  # Profile edit page
├── database.db            # SQLite database (created on first run)
├── package.json
└── README.md
```

## License

ISC