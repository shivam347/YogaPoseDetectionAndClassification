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