from flask import Blueprint, request, jsonify
import base64
import numpy as np
from PIL import Image
import io
import cv2
from app.routes.auth import token_required
from app.ml.pose_detector import PoseDetectionService

pose_bp = Blueprint('pose', __name__)
pose_service = PoseDetectionService()


def decode_base64_image(base64_string):
    """Decode base64 image to numpy array."""
    try:
        # Remove data URL prefix if present
        if ',' in base64_string:
            base64_string = base64_string.split(',')[1]
        
        image_bytes = base64.b64decode(base64_string)
        image = Image.open(io.BytesIO(image_bytes))
        return cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    except Exception as e:
        raise ValueError(f"Invalid image data: {str(e)}")


@pose_bp.route('/detect', methods=['POST'])
def detect_pose():
    try:
        data = request.get_json()
        
        if not data or not data.get('image'):
            return jsonify({
                'success': False,
                'message': 'Image data is required'
            }), 400
        
        # Decode image
        image = decode_base64_image(data['image'])
        target_pose = data.get('target_pose', '')
        
        # Detect pose
        result = pose_service.process_frame(image, target_pose)
        
        if result is None:
            return jsonify({
                'success': False,
                'message': 'No pose detected in image'
            }), 400
        
        return jsonify({
            'success': True,
            'data': result
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Pose detection failed: {str(e)}'
        }), 500


@pose_bp.route('/classify', methods=['POST'])
def classify_pose():
    try:
        data = request.get_json()
        
        if not data or not data.get('landmarks'):
            return jsonify({
                'success': False,
                'message': 'Landmarks data is required'
            }), 400
        
        # Convert landmarks to numpy array
        landmarks = np.array(data['landmarks']).flatten()
        
        # Classify pose
        result = pose_service.classify_pose(landmarks)
        
        return jsonify({
            'success': True,
            'data': result
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Pose classification failed: {str(e)}'
        }), 500

# Change in this function is requirred 
@pose_bp.route('/landmarks', methods=['POST'])
def extract_landmarks():
    try:
        data = request.get_json()
        
        if not data or not data.get('image'):
            return jsonify({
                'success': False,
                'message': 'Image data is required'
            }), 400
        
        # Decode image
        image = decode_base64_image(data['image'])
        
        # Extract landmarks
        landmarks = pose_service.extract_landmarks(image)
        
        if landmarks is None:
            return jsonify({
                'success': False,
                'message': 'No pose detected in image'
            }), 400
        
        # Convert to list format
        landmarks_list = []
        for i in range(33):  # MediaPipe has 33 landmarks
            idx = i * 4
            landmarks_list.append({
                'x': float(landmarks[idx]),
                'y': float(landmarks[idx + 1]),
                'z': float(landmarks[idx + 2]),
                'visibility': float(landmarks[idx + 3])
            })
        
        return jsonify({
            'success': True,
            'data': {
                'landmarks': landmarks_list,
                'landmark_count': len(landmarks_list)
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Landmark extraction failed: {str(e)}'
        }), 500


@pose_bp.route('/poses', methods=['GET'])
def get_supported_poses():
    """Get list of supported poses."""
    try:
        poses = pose_service.get_supported_poses()
        
        return jsonify({
            'success': True,
            'data': poses
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Failed to get poses: {str(e)}'
        }), 500

#  No change is requirred in this function
@pose_bp.route('/feedback', methods=['POST'])
def get_pose_feedback():
    """Get feedback for current pose compared to target."""
    try:
        data = request.get_json()
        
        if not data or not data.get('landmarks') or not data.get('target_pose'):
            return jsonify({
                'success': False,
                'message': 'Landmarks and target_pose are required'
            }), 400
        
        landmarks = np.array(data['landmarks']).flatten()
        target_pose = data['target_pose']
        
        # Calculate accuracy and get feedback
        accuracy, feedback, corrections = pose_service.calculate_accuracy(
            landmarks, target_pose
        )
        
        return jsonify({
            'success': True,
            'data': {
                'accuracy_percentage': accuracy,
                'feedback': feedback,
                'corrections': corrections
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Failed to get feedback: {str(e)}'
        }), 500
