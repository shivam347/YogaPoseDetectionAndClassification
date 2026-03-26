from flask import Blueprint, request, jsonify
import jwt
import datetime
from functools import wraps
from app import db
from app.models.user import User
from os import environ

auth_bp = Blueprint('auth', __name__)

JWT_SECRET_KEY = environ.get('JWT_SECRET_KEY', 'jwt-secret-key')

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(' ')[1]
            except IndexError:
                return jsonify({'success': False, 'message': 'Token malformed'}), 401
        
        if not token:
            return jsonify({'success': False, 'message': 'Token is missing'}), 401
        
        try:
            data = jwt.decode(token, JWT_SECRET_KEY, algorithms=['HS256'])
            current_user = User.query.get(data['user_id'])
            if not current_user:
                return jsonify({'success': False, 'message': 'User not found'}), 401
        except jwt.ExpiredSignatureError:
            return jsonify({'success': False, 'message': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'success': False, 'message': 'Token is invalid'}), 401
        
        return f(current_user, *args, **kwargs)
    
    return decorated


@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        
        # Validation
        if not data or not data.get('name') or not data.get('email') or not data.get('password'):
            return jsonify({
                'success': False,
                'message': 'Name, email, and password are required'
            }), 400
        
        # Check if user exists
        existing_user = User.query.filter_by(email=data['email']).first()
        if existing_user:
            return jsonify({
                'success': False,
                'message': 'Email already registered'
            }), 409
        
        # Create new user
        new_user = User(
            name=data['name'],
            email=data['email']
        )
        new_user.set_password(data['password'])
        
        db.session.add(new_user)
        db.session.commit()
        
        # Generate JWT token
        token = jwt.encode(
            {
                'user_id': new_user.id,
                'email': new_user.email,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
            },
            JWT_SECRET_KEY,
            algorithm='HS256'
        )
        
        return jsonify({
            'success': True,
            'message': 'User registered successfully',
            'data': {
                'user_id': new_user.id,
                'name': new_user.name,
                'email': new_user.email,
                'token': token
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Registration failed: {str(e)}'
        }), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        
        # Validation
        if not data or not data.get('email') or not data.get('password'):
            return jsonify({
                'success': False,
                'message': 'Email and password are required'
            }), 400
        
        # Find user
        user = User.query.filter_by(email=data['email']).first()
        
        if not user or not user.check_password(data['password']):
            return jsonify({
                'success': False,
                'message': 'Invalid email or password'
            }), 401
        
        if not user.is_active:
            return jsonify({
                'success': False,
                'message': 'Account is deactivated'
            }), 403
        
        # Generate JWT token
        token = jwt.encode(
            {
                'user_id': user.id,
                'email': user.email,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
            },
            JWT_SECRET_KEY,
            algorithm='HS256'
        )
        
        return jsonify({
            'success': True,
            'message': 'Login successful',
            'data': {
                'user_id': user.id,
                'name': user.name,
                'email': user.email,
                'token': token
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Login failed: {str(e)}'
        }), 500


@auth_bp.route('/profile', methods=['GET'])
@token_required
def get_profile(current_user):
    try:
        stats = current_user.get_statistics()
        
        return jsonify({
            'success': True,
            'data': {
                **current_user.to_dict(),
                **stats
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Failed to get profile: {str(e)}'
        }), 500


@auth_bp.route('/profile', methods=['PUT'])
@token_required
def update_profile(current_user):
    try:
        data = request.get_json()
        
        if data.get('name'):
            current_user.name = data['name']
        
        if data.get('avatar_url'):
            current_user.avatar_url = data['avatar_url']
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Profile updated successfully',
            'data': current_user.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Failed to update profile: {str(e)}'
        }), 500
