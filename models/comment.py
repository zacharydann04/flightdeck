"""Comment model for post interactions."""
from datetime import datetime
from extensions import db


class Comment(db.Model):
    """
    Comment model for post discussions.
    Can be extended with nested comments, mentions, etc.
    """
    __tablename__ = 'comment'
    
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False, index=True)
    
    # For future nested comments feature
    parent_id = db.Column(db.Integer, db.ForeignKey('comment.id'))
    
    def to_dict(self, include_author=True):
        """Convert comment to dictionary for API responses."""
        data = {
            'id': self.id,
            'content': self.content,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'post_id': self.post_id
        }
        
        if include_author:
            data['author'] = {
                'id': self.author.id,
                'username': self.author.username
            }
        
        return data
