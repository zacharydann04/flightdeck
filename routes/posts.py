"""Post-related routes."""
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from models import Post
from services import PostService

posts_bp = Blueprint('posts', __name__)


@posts_bp.route('/')
def index():
    """Main feed page."""
    if current_user.is_authenticated:
        posts, _, _ = PostService.get_feed()
        return render_template('feed.html', posts=posts)
    return render_template('landing.html')


@posts_bp.route('/post/create', methods=['GET', 'POST'])
@login_required
def create_post():
    """Create new post endpoint."""
    if request.method == 'POST':
        content = request.form.get('content')
        image_url = request.form.get('image_url')
        
        post, error = PostService.create_post(current_user, content, image_url)
        
        if error:
            flash(error)
            return redirect(url_for('posts.create_post'))
        
        flash('Post created successfully!')
        return redirect(url_for('posts.index'))
    
    return render_template('create_post.html')


@posts_bp.route('/post/<int:post_id>')
@login_required
def view_post(post_id):
    """View individual post."""
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', post=post)


@posts_bp.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    """Delete post endpoint."""
    post = Post.query.get_or_404(post_id)
    
    success, error = PostService.delete_post(post, current_user)
    
    if error:
        flash(error)
        return redirect(url_for('posts.index'))
    
    flash('Post deleted successfully!')
    return redirect(url_for('users.profile', username=current_user.username))


@posts_bp.route('/post/<int:post_id>/like', methods=['POST'])
@login_required
def like_post(post_id):
    """Like/unlike post endpoint (API)."""
    post = Post.query.get_or_404(post_id)
    
    liked, like_count = PostService.toggle_like(post, current_user)
    
    if liked is None:
        return jsonify({'success': False, 'error': like_count}), 500
    
    return jsonify({
        'success': True,
        'liked': liked,
        'like_count': like_count
    })


@posts_bp.route('/post/<int:post_id>/comment', methods=['POST'])
@login_required
def add_comment(post_id):
    """Add comment to post endpoint (API)."""
    post = Post.query.get_or_404(post_id)
    content = request.form.get('content')
    
    comment, error = PostService.add_comment(post, current_user, content)
    
    if error:
        return jsonify({'success': False, 'error': error}), 400
    
    return jsonify({
        'success': True,
        'comment': {
            'id': comment.id,
            'content': comment.content,
            'author': comment.author.username,
            'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M')
        }
    })


@posts_bp.route('/post/<int:post_id>/likes')
@login_required
def view_likes(post_id):
    """View all users who liked a post."""
    post = Post.query.get_or_404(post_id)
    return render_template('likes.html', post=post)


@posts_bp.route('/post/<int:post_id>/comments')
@login_required
def view_comments(post_id):
    """View all comments on a post."""
    post = Post.query.get_or_404(post_id)
    return render_template('comments.html', post=post)
