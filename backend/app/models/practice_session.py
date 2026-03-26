from app import db
from datetime import datetime

class PracticeSession(db.Model):
    __tablename__ = 'practice_sessions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'), nullable=False)
    accuracy_percentage = db.Column(db.Numeric(5, 2))
    duration_seconds = db.Column(db.Integer)
    pose_detected = db.Column(db.String(100))
    feedback = db.Column(db.Text)
    practiced_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'exercise_name': self.exercise.name if self.exercise else None,
            'accuracy_percentage': float(self.accuracy_percentage) if self.accuracy_percentage else None,
            'duration_seconds': self.duration_seconds,
            'pose_detected': self.pose_detected,
            'feedback': self.feedback,
            'practiced_at': self.practiced_at.isoformat() if self.practiced_at else None
        }
