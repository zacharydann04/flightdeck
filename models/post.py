"""Post model - adaptable for different storage backends."""
from datetime import datetime
from extensions import db


class Post(db.Model):
    """
    Post model for social media content.
    Image URLs can be adapted to use S3, CDN, or other media storage.
    """
    __tablename__ = 'post'
    
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    
    # Media storage - ready for S3, CloudFlare, etc.
    image_url = db.Column(db.String(500))
    image_storage_key = db.Column(db.String(200))  # For S3 or other storage keys
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    
    # Relationships
    likes = db.relationship('Like', backref='post', lazy=True, cascade='all, delete-orphan')
    comments = db.relationship('Comment', backref='post', lazy=True, cascade='all, delete-orphan')
    
    def like_count(self):
        """Get number of likes for this post."""
        return len(self.likes)
    
    def is_liked_by(self, user):
        """Check if a specific user has liked this post."""
        if not user or not user.is_authenticated:
            return False
        return any(like.user_id == user.id for like in self.likes)
    
    def to_dict(self, include_author=True):
        """Convert post to dictionary for API responses."""
        data = {
            'id': self.id,
            'content': self.content,
            'image_url': self.image_url,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'likes_count': self.like_count(),
            'comments_count': len(self.comments)
        }
        
        if include_author:
            data['author'] = {
                'id': self.author.id,
                'username': self.author.username
            }
        
        return data
