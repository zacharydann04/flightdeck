const db = require('./database');
const bcrypt = require('bcryptjs');

class User {
  static async create(username, email, password, fullName) {
    const hashedPassword = await bcrypt.hash(password, 10);
    
    return new Promise((resolve, reject) => {
      db.run(
        'INSERT INTO users (username, email, password, full_name) VALUES (?, ?, ?, ?)',
        [username, email, hashedPassword, fullName],
        function(err) {
          if (err) {
            reject(err);
          } else {
            resolve(this.lastID);
          }
        }
      );
    });
  }

  static async findByUsername(username) {
    return new Promise((resolve, reject) => {
      db.get(
        'SELECT * FROM users WHERE username = ?',
        [username],
        (err, row) => {
          if (err) {
            reject(err);
          } else {
            resolve(row);
          }
        }
      );
    });
  }

  static async findById(id) {
    return new Promise((resolve, reject) => {
      db.get(
        'SELECT id, username, email, full_name, bio, profile_picture, created_at FROM users WHERE id = ?',
        [id],
        (err, row) => {
          if (err) {
            reject(err);
          } else {
            resolve(row);
          }
        }
      );
    });
  }

  static async updateProfile(id, updates) {
    const { fullName, bio, profilePicture } = updates;
    const fields = [];
    const values = [];

    if (fullName !== undefined) {
      fields.push('full_name = ?');
      values.push(fullName);
    }
    if (bio !== undefined) {
      fields.push('bio = ?');
      values.push(bio);
    }
    if (profilePicture !== undefined) {
      fields.push('profile_picture = ?');
      values.push(profilePicture);
    }

    fields.push('updated_at = CURRENT_TIMESTAMP');
    values.push(id);

    return new Promise((resolve, reject) => {
      db.run(
        `UPDATE users SET ${fields.join(', ')} WHERE id = ?`,
        values,
        function(err) {
          if (err) {
            reject(err);
          } else {
            resolve(this.changes);
          }
        }
      );
    });
  }

  static async verifyPassword(password, hashedPassword) {
    return bcrypt.compare(password, hashedPassword);
  }
}

module.exports = User;
