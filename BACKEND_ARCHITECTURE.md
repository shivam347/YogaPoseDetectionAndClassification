# Yoga Pose Detection - Backend Architecture

## Overview
Flask-based backend API for Yoga Pose Detection application with MySQL database, JWT authentication, and ML model integration for pose classification.

## Tech Stack
- **Framework**: Flask 3.0+
- **Language**: Python 3.10+
- **Database**: MySQL 8.0
- **ORM**: SQLAlchemy
- **Authentication**: JWT (PyJWT)
- **ML Libraries**: scikit-learn, MediaPipe, NumPy, Pandas
- **API Documentation**: Flask-RESTX
- **CORS**: Flask-CORS

## Project Structure
```
backend/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── extensions.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── exercise.py
│   │   ├── practice_session.py
│   │   └── pain_category.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── exercises.py
│   │   ├── practice.py
│   │   └── pose_detection.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth_service.py
│   │   ├── exercise_service.py
│   │   └── pose_service.py
│   ├── ml/
│   │   ├── __init__.py
│   │   ├── model/
│   │   │   ├── pose_classifier.pkl
│   │   │   └── label_encoder.pkl
│   │   ├── pose_detector.py
│   │   ├── feature_extractor.py
│   │   └── train_model.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── decorators.py
│   │   ├── validators.py
│   │   └── helpers.py
│   └── templates/
│       └── email_templates/
├── migrations/
│   └── (Flask-Migrate files)
├── tests/
│   ├── __init__.py
│   ├── test_auth.py
│   ├── test_exercises.py
│   └── test_pose_detection.py
├── data/
│   ├── yoga_poses_dataset.csv
│   └── pose_images/
├── requirements.txt
├── run.py
└── config.py
```

## Database Schema

### Users Table
```sql
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    avatar_url VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);
```

### Pain Categories Table
```sql
CREATE TABLE pain_categories (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL,
    description TEXT,
    icon VARCHAR(50),
    color VARCHAR(7)
);
```

### Exercises Table
```sql
CREATE TABLE exercises (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    sanskrit_name VARCHAR(100),
    description TEXT,
    benefits TEXT,
    instructions TEXT,
    difficulty_level ENUM('beginner', 'intermediate', 'advanced'),
    pain_category_id INT,
    image_url VARCHAR(255),
    video_url VARCHAR(255),
    target_body_parts VARCHAR(255),
    duration_seconds INT,
    FOREIGN KEY (pain_category_id) REFERENCES pain_categories(id)
);
```

### Practice Sessions Table
```sql
CREATE TABLE practice_sessions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    exercise_id INT NOT NULL,
    accuracy_percentage DECIMAL(5,2),
    duration_seconds INT,
    pose_detected VARCHAR(100),
    feedback TEXT,
    practiced_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (exercise_id) REFERENCES exercises(id)
);
```

## API Endpoints

### Authentication Routes (`/api/auth`)

#### POST /api/auth/register
Register a new user.
```json
Request:
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "securepassword123"
}

Response:
{
  "success": true,
  "message": "User registered successfully",
  "data": {
    "user_id": 1,
    "name": "John Doe",
    "email": "john@example.com",
    "token": "eyJhbGciOiJIUzI1NiIs..."
  }
}
```

#### POST /api/auth/login
Authenticate user and return JWT.
```json
Request:
{
  "email": "john@example.com",
  "password": "securepassword123"
}

Response:
{
  "success": true,
  "message": "Login successful",
  "data": {
    "user_id": 1,
    "name": "John Doe",
    "email": "john@example.com",
    "token": "eyJhbGciOiJIUzI1NiIs..."
  }
}
```

#### GET /api/auth/profile
Get current user profile (protected).
```json
Response:
{
  "success": true,
  "data": {
    "user_id": 1,
    "name": "John Doe",
    "email": "john@example.com",
    "avatar_url": null,
    "created_at": "2024-01-15T10:30:00",
    "total_sessions": 15,
    "average_accuracy": 78.5
  }
}
```

### Exercise Routes (`/api/exercises`)

#### GET /api/exercises
List all exercises with optional filters.
```json
Query Parameters:
- pain_type: string (neck, back, shoulder, knee, stress, general)
- difficulty: string (beginner, intermediate, advanced)
- search: string

Response:
{
  "success": true,
  "data": [
    {
      "id": 1,
      "name": "Neck Stretch",
      "sanskrit_name": "Greeva Sanchalana",
      "description": "Gentle neck stretches to relieve tension",
      "benefits": ["Relieves neck pain", "Reduces stiffness", "Improves flexibility"],
      "difficulty_level": "beginner",
      "image_url": "/images/neck-stretch.jpg",
      "pain_category": "neck"
    }
  ]
}
```

#### GET /api/exercises/:id
Get detailed exercise information.
```json
Response:
{
  "success": true,
  "data": {
    "id": 1,
    "name": "Neck Stretch",
    "sanskrit_name": "Greeva Sanchalana",
    "description": "Gentle neck stretches to relieve tension",
    "benefits": ["Relieves neck pain", "Reduces stiffness", "Improves flexibility"],
    "instructions": [
      "Sit comfortably with spine straight",
      "Slowly tilt head to right shoulder",
      "Hold for 15-20 seconds",
      "Repeat on left side"
    ],
    "difficulty_level": "beginner",
    "duration_seconds": 120,
    "image_url": "/images/neck-stretch.jpg",
    "video_url": "/videos/neck-stretch.mp4",
    "target_body_parts": ["neck", "shoulders"]
  }
}
```

#### GET /api/exercises/pain-categories
Get all pain categories.
```json
Response:
{
  "success": true,
  "data": [
    {
      "id": 1,
      "name": "Neck Pain",
      "description": "Exercises for neck pain relief",
      "icon": "neck_icon",
      "color": "#8B9A7C"
    }
  ]
}
```

### Practice Routes (`/api/practice`)

#### POST /api/practice
Save a practice session (protected).
```json
Request:
{
  "exercise_id": 1,
  "accuracy_percentage": 85.5,
  "duration_seconds": 120,
  "pose_detected": "Neck Stretch",
  "feedback": "Good form, maintain steady breathing"
}

Response:
{
  "success": true,
  "message": "Practice session saved",
  "data": {
    "session_id": 15,
    "practiced_at": "2024-01-15T14:30:00"
  }
}
```

#### GET /api/practice/history
Get user's practice history (protected).
```json
Query Parameters:
- limit: int (default: 10)
- offset: int (default: 0)

Response:
{
  "success": true,
  "data": {
    "sessions": [
      {
        "id": 15,
        "exercise_name": "Neck Stretch",
        "accuracy_percentage": 85.5,
        "duration_seconds": 120,
        "practiced_at": "2024-01-15T14:30:00"
      }
    ],
    "total": 15,
    "statistics": {
      "total_sessions": 15,
      "total_minutes": 180,
      "average_accuracy": 78.5,
      "streak_days": 5
    }
  }
}
```

### Pose Detection Routes (`/api/pose`)

#### POST /api/pose/detect
Process image/frame for pose detection.
```json
Request:
{
  "image": "base64_encoded_image",
  "target_pose": "neck_stretch"
}

Response:
{
  "success": true,
  "data": {
    "pose_detected": "Neck Stretch",
    "confidence": 0.92,
    "accuracy_percentage": 85.5,
    "landmarks": [
      {"x": 0.5, "y": 0.3, "z": 0.0, "visibility": 0.99}
    ],
    "feedback": "Good alignment, shoulders relaxed",
    "corrections": [
      "Keep chin parallel to floor",
      "Relax shoulders away from ears"
    ]
  }
}
```

#### POST /api/pose/classify
Classify pose from landmarks.
```json
Request:
{
  "landmarks": [
    {"x": 0.5, "y": 0.3, "z": 0.0, "visibility": 0.99}
  ]
}

Response:
{
  "success": true,
  "data": {
    "pose_class": "tree_pose",
    "pose_name": "Tree Pose",
    "confidence": 0.89,
    "all_predictions": [
      {"pose": "tree_pose", "confidence": 0.89},
      {"pose": "warrior_ii", "confidence": 0.08}
    ]
  }
}
```

## Machine Learning Module

### Pose Detection Pipeline

```python
class PoseDetectionService:
    def __init__(self):
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(
            static_image_mode=False,
            model_complexity=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.classifier = self.load_model()
        self.label_encoder = self.load_label_encoder()
    
    def extract_landmarks(self, image):
        """Extract 33 pose landmarks using MediaPipe."""
        results = self.pose.process(image)
        if not results.pose_landmarks:
            return None
        
        landmarks = []
        for lm in results.pose_landmarks.landmark:
            landmarks.extend([lm.x, lm.y, lm.z, lm.visibility])
        return np.array(landmarks)  # 132 features (33 * 4)
    
    def classify_pose(self, landmarks):
        """Classify pose using Random Forest classifier."""
        landmarks_reshaped = landmarks.reshape(1, -1)
        prediction = self.classifier.predict(landmarks_reshaped)[0]
        probabilities = self.classifier.predict_proba(landmarks_reshaped)[0]
        
        pose_name = self.label_encoder.inverse_transform([prediction])[0]
        confidence = probabilities[prediction]
        
        return {
            'pose_class': pose_name,
            'confidence': float(confidence),
            'all_probabilities': {
                self.label_encoder.inverse_transform([i])[0]: float(prob)
                for i, prob in enumerate(probabilities)
            }
        }
    
    def calculate_accuracy(self, detected_landmarks, target_pose):
        """Calculate pose accuracy compared to reference."""
        # Compare key angles and positions
        angles = self.calculate_joint_angles(detected_landmarks)
        reference_angles = self.get_reference_angles(target_pose)
        
        accuracy = self.compare_angles(angles, reference_angles)
        feedback = self.generate_feedback(angles, reference_angles)
        
        return accuracy, feedback
```

### Feature Extraction

```python
class FeatureExtractor:
    """Extract features from pose landmarks for ML model."""
    
    KEY_LANDMARKS = {
        'nose': 0,
        'left_shoulder': 11,
        'right_shoulder': 12,
        'left_elbow': 13,
        'right_elbow': 14,
        'left_wrist': 15,
        'right_wrist': 16,
        'left_hip': 23,
        'right_hip': 24,
        'left_knee': 25,
        'right_knee': 26,
        'left_ankle': 27,
        'right_ankle': 28,
    }
    
    @staticmethod
    def calculate_angle(a, b, c):
        """Calculate angle between three points."""
        a, b, c = np.array(a), np.array(b), np.array(c)
        radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - \
                  np.arctan2(a[1] - b[1], a[0] - b[0])
        angle = np.abs(radians * 180.0 / np.pi)
        return 360 - angle if angle > 180 else angle
    
    @staticmethod
    def get_joint_angles(landmarks):
        """Extract key joint angles from landmarks."""
        angles = {}
        lm = landmarks.reshape(-1, 4)
        
        # Shoulder angles
        angles['left_shoulder'] = FeatureExtractor.calculate_angle(
            lm[11], lm[13], lm[15]  # Left shoulder-elbow-wrist
        )
        angles['right_shoulder'] = FeatureExtractor.calculate_angle(
            lm[12], lm[14], lm[16]  # Right shoulder-elbow-wrist
        )
        
        # Hip angles
        angles['left_hip'] = FeatureExtractor.calculate_angle(
            lm[23], lm[25], lm[27]  # Left hip-knee-ankle
        )
        angles['right_hip'] = FeatureExtractor.calculate_angle(
            lm[24], lm[26], lm[28]  # Right hip-knee-ankle
        )
        
        return angles
```

### Model Training

```python
def train_pose_classifier():
    """Train Random Forest classifier on yoga pose dataset."""
    # Load dataset
    df = pd.read_csv('data/yoga_poses_dataset.csv')
    
    # Features: 33 landmarks * 4 values (x, y, z, visibility) = 132 features
    X = df.drop('pose_label', axis=1).values
    y = df['pose_label'].values
    
    # Encode labels
    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
    )
    
    # Train Random Forest
    classifier = RandomForestClassifier(
        n_estimators=200,
        max_depth=20,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42,
        n_jobs=-1
    )
    
    classifier.fit(X_train, y_train)
    
    # Evaluate
    train_accuracy = classifier.score(X_train, y_train)
    test_accuracy = classifier.score(X_test, y_test)
    
    print(f"Training Accuracy: {train_accuracy:.4f}")
    print(f"Testing Accuracy: {test_accuracy:.4f}")
    
    # Save model
    joblib.dump(classifier, 'app/ml/model/pose_classifier.pkl')
    joblib.dump(label_encoder, 'app/ml/model/label_encoder.pkl')
    
    return classifier, label_encoder, test_accuracy
```

## Dataset

### Yoga Poses Dataset
The application uses a comprehensive yoga pose dataset with the following poses:

**Pain-Specific Poses:**
- **Neck Pain**: Neck Stretch, Neck Roll, Chin Tuck, Upper Trapezius Stretch
- **Back Pain**: Cat-Cow, Child's Pose, Cobra Pose, Bridge Pose
- **Shoulder Pain**: Shoulder Roll, Eagle Arms, Thread the Needle, Puppy Pose
- **Knee Pain**: Chair Pose, Warrior I, Warrior II, Supported Squat
- **Stress Relief**: Corpse Pose, Legs Up Wall, Easy Pose, Forward Fold
- **General**: Mountain Pose, Tree Pose, Downward Dog, Plank

**Dataset Format:**
```csv
pose_label,nose_x,nose_y,nose_z,nose_v,...,left_ankle_x,left_ankle_y,left_ankle_z,left_ankle_v
neck_stretch,0.5,0.3,0.0,0.99,...,0.4,0.8,0.0,0.95
```

## Authentication & Security

### JWT Configuration
```python
JWT_SECRET_KEY = 'your-secret-key'
JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
```

### Password Hashing
```python
from werkzeug.security import generate_password_hash, check_password_hash

# Hash password
password_hash = generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)

# Verify password
is_valid = check_password_hash(password_hash, password)
```

### Protected Route Decorator
```python
def jwt_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'success': False, 'message': 'Token missing'}), 401
        
        try:
            token = token.split(' ')[1]  # Remove 'Bearer ' prefix
            payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=['HS256'])
            current_user = User.query.get(payload['user_id'])
            if not current_user:
                raise Exception('User not found')
        except jwt.ExpiredSignatureError:
            return jsonify({'success': False, 'message': 'Token expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'success': False, 'message': 'Invalid token'}), 401
        
        return f(current_user, *args, **kwargs)
    return decorated_function
```

## Error Handling

### Global Error Handler
```python
@app.errorhandler(Exception)
def handle_error(error):
    logger.error(f"Error: {str(error)}")
    
    if isinstance(error, ValidationError):
        return jsonify({
            'success': False,
            'message': 'Validation error',
            'errors': error.errors
        }), 400
    
    if isinstance(error, NotFoundError):
        return jsonify({
            'success': False,
            'message': error.message
        }), 404
    
    return jsonify({
        'success': False,
        'message': 'Internal server error'
    }), 500
```

## Performance Optimization

1. **Database Indexing**: Indexes on frequently queried columns
2. **Connection Pooling**: SQLAlchemy connection pool
3. **Caching**: Redis for frequently accessed data
4. **Async Processing**: Celery for background tasks
5. **Model Optimization**: Quantized ML model for faster inference

## Deployment

### Docker Configuration
```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "run:app"]
```

### Environment Variables
```bash
FLASK_ENV=production
FLASK_APP=run.py
DATABASE_URL=mysql://user:password@localhost/yoga_pose_db
JWT_SECRET_KEY=your-secret-key
REDIS_URL=redis://localhost:6379/0
```
