from flask import Blueprint, request, jsonify
from app import db
from app.models.practice_session import PracticeSession
from app.models.exercise import Exercise
from app.routes.auth import token_required

practice_bp = Blueprint('practice', __name__)


@practice_bp.route('', methods=['POST'])
@token_required
def save_practice(current_user):
    try:
        data = request.get_json()
        
        # Validation
        if not data or not data.get('exercise_id'):
            return jsonify({
                'success': False,
                'message': 'Exercise ID is required'
            }), 400
        
        # Verify exercise exists
        exercise = Exercise.query.get(data['exercise_id'])
        if not exercise:
            return jsonify({
                'success': False,
                'message': 'Exercise not found'
            }), 404
        
        # Create practice session
        session = PracticeSession(
            user_id=current_user.id,
            exercise_id=data['exercise_id'],
            accuracy_percentage=data.get('accuracy_percentage'),
            duration_seconds=data.get('duration_seconds'),
            pose_detected=data.get('pose_detected'),
            feedback=data.get('feedback')
        )
        
        db.session.add(session)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Practice session saved',
            'data': {
                'session_id': session.id,
                'practiced_at': session.practiced_at.isoformat()
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Failed to save practice: {str(e)}'
        }), 500


@practice_bp.route('/history', methods=['GET'])
@token_required
def get_practice_history(current_user):
    try:
        # Query parameters
        limit = request.args.get('limit', 10, type=int)
        offset = request.args.get('offset', 0, type=int)
        
        # Get sessions
        sessions = PracticeSession.query\
            .filter_by(user_id=current_user.id)\
            .order_by(PracticeSession.practiced_at.desc())\
            .offset(offset)\
            .limit(limit)\
            .all()
        
        total = PracticeSession.query.filter_by(user_id=current_user.id).count()
        
        # Calculate statistics
        from sqlalchemy import func
        
        stats = db.session.query(
            func.count(PracticeSession.id).label('total_sessions'),
            func.sum(PracticeSession.duration_seconds).label('total_seconds'),
            func.avg(PracticeSession.accuracy_percentage).label('avg_accuracy')
        ).filter_by(user_id=current_user.id).first()
        
        # Calculate streak
        streak = calculate_streak(current_user.id)
        
        return jsonify({
            'success': True,
            'data': {
                'sessions': [s.to_dict() for s in sessions],
                'total': total,
                'statistics': {
                    'total_sessions': stats.total_sessions or 0,
                    'total_minutes': round((stats.total_seconds or 0) / 60, 1),
                    'average_accuracy': round(float(stats.avg_accuracy), 2) if stats.avg_accuracy else 0,
                    'streak_days': streak
                }
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Failed to get practice history: {str(e)}'
        }), 500


def calculate_streak(user_id):
    """Calculate consecutive days streak."""
    from datetime import datetime, timedelta
    from sqlalchemy import func, cast, Date
    
    # Get distinct practice dates
    dates = db.session.query(
        func.distinct(cast(PracticeSession.practiced_at, Date)).label('practice_date')
    ).filter_by(user_id=user_id)\
     .order_by(func.distinct(cast(PracticeSession.practiced_at, Date)).desc())\
     .all()
    
    if not dates:
        return 0
    
    streak = 0
    today = datetime.utcnow().date()
    expected_date = today
    
    for date_row in dates:
        practice_date = date_row.practice_date
        
        if practice_date == expected_date or practice_date == today:
            streak += 1
            expected_date = practice_date - timedelta(days=1)
        elif practice_date == expected_date + timedelta(days=1):
            # Same day, continue
            continue
        else:
            break
    
    return streak


@practice_bp.route('/statistics', methods=['GET'])
@token_required
def get_statistics(current_user):
    try:
        from sqlalchemy import func
        
        # Overall statistics
        stats = db.session.query(
            func.count(PracticeSession.id).label('total_sessions'),
            func.sum(PracticeSession.duration_seconds).label('total_seconds'),
            func.avg(PracticeSession.accuracy_percentage).label('avg_accuracy'),
            func.max(PracticeSession.accuracy_percentage).label('best_accuracy')
        ).filter_by(user_id=current_user.id).first()
        
        # Most practiced exercises
        top_exercises = db.session.query(
            Exercise.name,
            func.count(PracticeSession.id).label('count')
        ).join(PracticeSession).filter(
            PracticeSession.user_id == current_user.id
        ).group_by(Exercise.id).order_by(func.count(PracticeSession.id).desc()).limit(5).all()
        
        return jsonify({
            'success': True,
            'data': {
                'total_sessions': stats.total_sessions or 0,
                'total_minutes': round((stats.total_seconds or 0) / 60, 1),
                'average_accuracy': round(float(stats.avg_accuracy), 2) if stats.avg_accuracy else 0,
                'best_accuracy': round(float(stats.best_accuracy), 2) if stats.best_accuracy else 0,
                'top_exercises': [{'name': ex.name, 'count': ex.count} for ex in top_exercises]
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Failed to get statistics: {str(e)}'
        }), 500
