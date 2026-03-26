from flask import Blueprint, request, jsonify
from app import db
from app.models.exercise import Exercise, PainCategory
from app.routes.auth import token_required

exercises_bp = Blueprint('exercises', __name__)


@exercises_bp.route('', methods=['GET'])
def get_exercises():
    try:
        # Query parameters
        pain_type = request.args.get('pain_type', '')
        difficulty = request.args.get('difficulty', '')
        search = request.args.get('search', '')
        
        # Build query
        query = Exercise.query
        
        if pain_type:
            query = query.join(PainCategory).filter(
                db.func.lower(PainCategory.name).like(f'%{pain_type.lower()}%')
            )
        
        if difficulty:
            query = query.filter(Exercise.difficulty_level == difficulty.lower())
        
        if search:
            query = query.filter(
                db.or_(
                    Exercise.name.ilike(f'%{search}%'),
                    Exercise.sanskrit_name.ilike(f'%{search}%'),
                    Exercise.description.ilike(f'%{search}%')
                )
            )
        
        exercises = query.all()
        
        return jsonify({
            'success': True,
            'data': [ex.to_dict() for ex in exercises],
            'count': len(exercises)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Failed to get exercises: {str(e)}'
        }), 500


@exercises_bp.route('/<int:exercise_id>', methods=['GET'])
def get_exercise(exercise_id):
    try:
        exercise = Exercise.query.get(exercise_id)
        
        if not exercise:
            return jsonify({
                'success': False,
                'message': 'Exercise not found'
            }), 404
        
        return jsonify({
            'success': True,
            'data': exercise.to_dict(include_details=True)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Failed to get exercise: {str(e)}'
        }), 500


@exercises_bp.route('/pain-categories', methods=['GET'])
def get_pain_categories():
    try:
        categories = PainCategory.query.all()
        
        return jsonify({
            'success': True,
            'data': [cat.to_dict() for cat in categories]
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Failed to get pain categories: {str(e)}'
        }), 500


@exercises_bp.route('/pain-categories/<int:category_id>/exercises', methods=['GET'])
def get_exercises_by_category(category_id):
    try:
        category = PainCategory.query.get(category_id)
        
        if not category:
            return jsonify({
                'success': False,
                'message': 'Pain category not found'
            }), 404
        
        exercises = Exercise.query.filter_by(pain_category_id=category_id).all()
        
        return jsonify({
            'success': True,
            'data': {
                'category': category.to_dict(),
                'exercises': [ex.to_dict() for ex in exercises]
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Failed to get exercises: {str(e)}'
        }), 500
