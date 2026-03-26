from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    avatar_url = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    practice_sessions = db.relationship('PracticeSession', backref='user', lazy=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'avatar_url': self.avatar_url,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'is_active': self.is_active
        }
    
    def get_statistics(self):
        from app.models.practice_session import PracticeSession
        
        total_sessions = PracticeSession.query.filter_by(user_id=self.id).count()
        avg_accuracy = db.session.query(db.func.avg(PracticeSession.accuracy_percentage))\
            .filter_by(user_id=self.id).scalar()
        
        return {
            'total_sessions': total_sessions,
            'average_accuracy': round(float(avg_accuracy), 2) if avg_accuracy else 0
        }
