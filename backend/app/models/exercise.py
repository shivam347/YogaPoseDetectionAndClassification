from app import db

class PainCategory(db.Model):
    __tablename__ = 'pain_categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    icon = db.Column(db.String(50))
    color = db.Column(db.String(7))
    
    # Relationships
    exercises = db.relationship('Exercise', backref='pain_category', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'icon': self.icon,
            'color': self.color
        }


class Exercise(db.Model):
    __tablename__ = 'exercises'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    sanskrit_name = db.Column(db.String(100))
    description = db.Column(db.Text)
    benefits = db.Column(db.Text)  # JSON string of benefits list
    instructions = db.Column(db.Text)  # JSON string of instructions list
    difficulty_level = db.Column(db.Enum('beginner', 'intermediate', 'advanced', name='difficulty_level'))
    pain_category_id = db.Column(db.Integer, db.ForeignKey('pain_categories.id'))
    image_url = db.Column(db.String(255))
    video_url = db.Column(db.String(255))
    target_body_parts = db.Column(db.String(255))  # Comma-separated
    duration_seconds = db.Column(db.Integer)
    pose_key = db.Column(db.String(50))  # Key for ML model classification
    
    # Relationships
    practice_sessions = db.relationship('PracticeSession', backref='exercise', lazy=True)
    
    def to_dict(self, include_details=False):
        import json
        
        data = {
            'id': self.id,
            'name': self.name,
            'sanskrit_name': self.sanskrit_name,
            'description': self.description,
            'difficulty_level': self.difficulty_level,
            'image_url': self.image_url,
            'duration_seconds': self.duration_seconds,
            'pose_key': self.pose_key
        }
        
        if self.benefits:
            try:
                data['benefits'] = json.loads(self.benefits)
            except:
                data['benefits'] = self.benefits.split(',')
        
        if self.target_body_parts:
            data['target_body_parts'] = self.target_body_parts.split(',')
        
        if include_details:
            if self.instructions:
                try:
                    data['instructions'] = json.loads(self.instructions)
                except:
                    data['instructions'] = self.instructions.split('\n')
            data['video_url'] = self.video_url
            
        if self.pain_category:
            data['pain_category'] = self.pain_category.to_dict()
            
        return data
