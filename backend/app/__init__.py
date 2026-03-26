from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
from dotenv import load_dotenv
import os

load_dotenv()

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
        'DATABASE_URL', 
        'mysql://root:password@localhost/yoga_pose_db'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'jwt-secret-key')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 86400  # 24 hours
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app, resources={
        r"/api/*": {
            "origins": ["http://localhost:5173", "http://localhost:3000"],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Authorization", "Content-Type"]
        }
    })
    
    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.exercises import exercises_bp
    from app.routes.practice import practice_bp
    from app.routes.pose_detection import pose_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(exercises_bp, url_prefix='/api/exercises')
    app.register_blueprint(practice_bp, url_prefix='/api/practice')
    app.register_blueprint(pose_bp, url_prefix='/api/pose')
    
    @app.route('/api/health')
    def health_check():
        return {'status': 'healthy', 'service': 'yoga-pose-api'}
    
    return app
