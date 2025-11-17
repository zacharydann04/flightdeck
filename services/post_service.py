"""
Post service for managing posts, likes, and comments.
Business logic separated for easy API integration.
"""
from models import Post, Like, Comment
from extensions import db


class PostService:
    """
    Service for handling post operations.
    Encapsulates business logic for posts, likes, and comments.
    """
    
    @staticmethod
    def create_post(user, content, image_url=None):
        """
        Create a new post.
        Returns: (post, error_message)
        """
        if not content or not content.strip():
            return None, 'Post content cannot be empty'
        
        try:
            post = Post(
                content=content,
                image_url=image_url,
                user_id=user.id
            )
            db.session.add(post)
            db.session.commit()
            return post, None
        except Exception as e:
            db.session.rollback()
            return None, f'Failed to create post: {str(e)}'
    
    @staticmethod
    def delete_post(post, user):
        """
        Delete a post (only by the author).
        Returns: (success, error_message)
        """
        if post.user_id != user.id:
            return False, 'You can only delete your own posts'
        
        try:
            db.session.delete(post)
            db.session.commit()
            return True, None
        except Exception as e:
            db.session.rollback()
            return False, f'Failed to delete post: {str(e)}'
    
    @staticmethod
    def toggle_like(post, user):
        """
        Toggle like on a post (like if not liked, unlike if already liked).
        Returns: (liked_status, like_count)
        """
        existing_like = Like.query.filter_by(user_id=user.id, post_id=post.id).first()
        
        try:
            if existing_like:
                # Unlike
                db.session.delete(existing_like)
                db.session.commit()
                return False, post.like_count()
            else:
                # Like
                like = Like(user_id=user.id, post_id=post.id)
                db.session.add(like)
                db.session.commit()
                return True, post.like_count()
        except Exception as e:
            db.session.rollback()
            return None, str(e)
    
    @staticmethod
    def add_comment(post, user, content):
        """
        Add a comment to a post.
        Returns: (comment, error_message)
        """
        if not content or not content.strip():
            return None, 'Comment cannot be empty'
        
        try:
            comment = Comment(
                content=content,
                user_id=user.id,
                post_id=post.id
            )
            db.session.add(comment)
            db.session.commit()
            return comment, None
        except Exception as e:
            db.session.rollback()
            return None, f'Failed to add comment: {str(e)}'
    
    @staticmethod
    def get_feed(page=1, per_page=20):
        """
        Get paginated feed of all posts.
        Returns: (posts, has_next, has_prev)
        """
        pagination = Post.query.order_by(Post.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        return pagination.items, pagination.has_next, pagination.has_prev
    
    @staticmethod
    def get_user_posts(user, page=1, per_page=20):
        """
        Get paginated posts for a specific user.
        Returns: (posts, has_next, has_prev)
        """
        pagination = Post.query.filter_by(user_id=user.id).order_by(
            Post.created_at.desc()
        ).paginate(page=page, per_page=per_page, error_out=False)
        return pagination.items, pagination.has_next, pagination.has_prev
