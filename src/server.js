const express = require('express');
const cookieParser = require('cookie-parser');
const path = require('path');
const authRoutes = require('./routes/auth');
const profileRoutes = require('./routes/profile');

const app = express();
const PORT = process.env.PORT || 3000;

// Initialize database
require('./models/database');

// Middleware
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, '../public')));

// Routes
app.use('/api/auth', authRoutes);
app.use('/api/profile', profileRoutes);

// Serve HTML pages
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, '../public/index.html'));
});

app.get('/signup', (req, res) => {
  res.sendFile(path.join(__dirname, '../public/signup.html'));
});

app.get('/login', (req, res) => {
  res.sendFile(path.join(__dirname, '../public/login.html'));
});

app.get('/profile/:username', (req, res) => {
  res.sendFile(path.join(__dirname, '../public/profile.html'));
});

app.get('/edit-profile', (req, res) => {
  res.sendFile(path.join(__dirname, '../public/edit-profile.html'));
});

// Start server
app.listen(PORT, () => {
  console.log(`FlightDeck server running on http://localhost:${PORT}`);
});
