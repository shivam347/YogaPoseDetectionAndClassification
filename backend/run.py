#!/usr/bin/env python3
"""
Yoga Pose Detection API - Flask Application Entry Point
"""

import os
import sys

# Add app directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from flask_migrate import Migrate

app = create_app()
migrate = Migrate(app, db)

@app.cli.command("init-db")
def init_db():
    """Initialize the database."""
    with app.app_context():
        db.create_all()
        print("Database initialized successfully!")

@app.cli.command("seed-db")
def seed_db():
    """Seed database with initial data."""
    from seed_data import seed_database
    with app.app_context():
        seed_database()
        print("Database seeded successfully!")

@app.cli.command("train-model")
def train_model():
    """Train the pose classification model."""
    from app.ml.train_model import train_model as train
    train()

if __name__ == '__main__':
    print("=" * 60)
    print("Yoga Pose Detection API")
    print("=" * 60)
    print(f"Environment: {os.environ.get('FLASK_ENV', 'development')}")
    print(f"Debug: {os.environ.get('FLASK_DEBUG', 'True')}")
    print("-" * 60)
    print("API Endpoints:")
    print("  - Health Check: GET  /api/health")
    print("  - Register:     POST /api/auth/register")
    print("  - Login:        POST /api/auth/login")
    print("  - Exercises:    GET  /api/exercises")
    print("  - Pose Detect:  POST /api/pose/detect")
    print("=" * 60)
    
    app.run(
        host='0.0.0.0',
        port=int(os.environ.get('PORT', 5000)),
        debug=os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    )
