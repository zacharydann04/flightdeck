"""User profile routes."""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import User, Post
from services import AuthService

users_bp = Blueprint('users', __name__)


@users_bp.route('/profile/<username>')
@login_required
def profile(username):
    """View user profile."""
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(user_id=user.id).order_by(Post.created_at.desc()).all()
    return render_template('profile.html', user=user, posts=posts)


@users_bp.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    """Edit user profile."""
    if request.method == 'POST':
        bio = request.form.get('bio', '')
        
        success, error = AuthService.update_user_profile(current_user, bio=bio)
        
        if error:
            flash(error)
        else:
            flash('Profile updated successfully!')
        
        return redirect(url_for('users.profile', username=current_user.username))
    
    return render_template('edit_profile.html')
