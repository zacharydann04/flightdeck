"""
Database models package.
Separated for easy migration to different ORMs or database systems.
"""
from .user import User
from .post import Post
from .like import Like
from .comment import Comment

__all__ = ['User', 'Post', 'Like', 'Comment']
