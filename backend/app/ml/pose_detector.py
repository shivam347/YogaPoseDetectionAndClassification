import mediapipe as mp
import numpy as np
import cv2
import joblib
import os
import json
import math
from typing import Dict, List, Tuple, Optional

mp_pose = mp.solutions.pose
VIS_MIN = 0.40


def get_lm(landmarks, idx):
    lm = landmarks[idx]
    if lm.visibility < VIS_MIN:
        return None
    return (lm.x, lm.y, lm.z)


def angle_2d(a, b, c):
    if a is None or b is None or c is None:
        return 0.0
    ax, ay = a[0] - b[0], a[1] - b[1]
    cx, cy = c[0] - b[0], c[1] - b[1]
    angle = math.degrees(math.atan2(cy, cx) - math.atan2(ay, ax))
    angle = abs(angle)
    if angle > 180:
        angle = 360 - angle
    return round(angle, 4)


def vector_angle_xy(a, b):
    if a is None or b is None:
        return 0.0
    return round(math.degrees(math.atan2(b[1] - a[1], b[0] - a[0])), 4)


def midpoint(a, b):
    if a is None or b is None:
        return None
    return ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2, (a[2] + b[2]) / 2)


def extract_all_features(landmarks):
    P = mp_pose.PoseLandmark

    # Extract landmarks
    lms = {
        name: get_lm(landmarks, P[name].value)
        for name in P.__members__
        if name in P.__members__
    }
    # Frequently used landmarks
    nose = lms.get("NOSE")
    l_sh = lms.get("LEFT_SHOULDER")
    r_sh = lms.get("RIGHT_SHOULDER")
    l_el = lms.get("LEFT_ELBOW")
    r_el = lms.get("RIGHT_ELBOW")
    l_wr = lms.get("LEFT_WRIST")
    r_wr = lms.get("RIGHT_WRIST")
    l_hi = lms.get("LEFT_HIP")
    r_hi = lms.get("RIGHT_HIP")
    l_kn = lms.get("LEFT_KNEE")
    r_kn = lms.get("RIGHT_KNEE")
    l_an = lms.get("LEFT_ANKLE")
    r_an = lms.get("RIGHT_ANKLE")
    l_foot = lms.get("LEFT_FOOT_INDEX")
    r_foot = lms.get("RIGHT_FOOT_INDEX")

    mid_sh = midpoint(l_sh, r_sh)
    mid_hi = midpoint(l_hi, r_hi)

    # Reference torso length
    if mid_sh and mid_hi:
        torso_len = math.hypot(mid_sh[0] - mid_hi[0], mid_sh[1] - mid_hi[1])
        if torso_len < 1e-6:
            torso_len = 1.0
    else:
        torso_len = 1.0

    # 1. Joint Angles — /180 to match training's normalize_angles()
    # spine_tilt uses atan2(dx, -dy) to match feature_engineering.py exactly
    _spine_tilt = None
    if mid_sh and mid_hi:
        dx = mid_sh[0] - mid_hi[0]
        dy = mid_sh[1] - mid_hi[1]
        _spine_tilt = round(math.degrees(math.atan2(dx, -dy)), 4)

    feat_angles = {
        "left_elbow_angle": angle_2d(l_sh, l_el, l_wr) / 180.0,
        "right_elbow_angle": angle_2d(r_sh, r_el, r_wr) / 180.0,
        "left_shoulder_angle": angle_2d(l_el, l_sh, l_hi) / 180.0,
        "right_shoulder_angle": angle_2d(r_hi, r_sh, r_el) / 180.0,
        "neck_angle": angle_2d(nose, l_sh, r_sh) / 180.0,
        "left_hip_angle": angle_2d(l_sh, l_hi, l_kn) / 180.0,
        "right_hip_angle": angle_2d(r_sh, r_hi, r_kn) / 180.0,
        "left_knee_angle": angle_2d(l_hi, l_kn, l_an) / 180.0,
        "right_knee_angle": angle_2d(r_hi, r_kn, r_an) / 180.0,
        "left_ankle_angle": angle_2d(l_kn, l_an, l_foot) / 180.0,
        "right_ankle_angle": angle_2d(r_kn, r_an, r_foot) / 180.0,
        "spine_tilt_deg": (_spine_tilt / 180.0) if _spine_tilt is not None else 0.0,
        "pelvis_tilt_deg": vector_angle_xy(l_hi, r_hi) / 180.0,
        "shoulder_line_deg": vector_angle_xy(l_sh, r_sh) / 180.0,
        "inter_ankle_angle_L": angle_2d(r_an, r_hi, l_an) / 180.0,
        "inter_ankle_angle_R": angle_2d(l_an, l_hi, r_an) / 180.0,
    }

    # 2. Orientation — raw torso-normalised ratios to match feature_engineering.py
    #    (The old (v+1)/2 remapping was WRONG — training stored raw ratios)
    sh_yaw = (
        math.atan2(r_sh[1] - l_sh[1], r_sh[0] - l_sh[0]) if (l_sh and r_sh) else 0.0
    )
    hi_yaw = (
        math.atan2(r_hi[1] - l_hi[1], r_hi[0] - l_hi[0]) if (l_hi and r_hi) else 0.0
    )

    feat_orient = {
        "shoulder_yaw_sin": round(math.sin(sh_yaw), 6),
        "shoulder_yaw_cos": round(math.cos(sh_yaw), 6),
        "hip_yaw_sin": round(math.sin(hi_yaw), 6),
        "hip_yaw_cos": round(math.cos(hi_yaw), 6),
        "shoulder_depth_diff": round((l_sh[2] - r_sh[2]) / torso_len, 6)
        if (l_sh and r_sh)
        else 0.0,
        "hip_depth_diff": round((l_hi[2] - r_hi[2]) / torso_len, 6)
        if (l_hi and r_hi)
        else 0.0,
        "ankle_depth_diff": round((l_an[2] - r_an[2]) / torso_len, 6)
        if (l_an and r_an)
        else 0.0,
        "spine_lean_depth": round(
            ((l_sh[2] + r_sh[2]) / 2 - (l_hi[2] + r_hi[2]) / 2) / torso_len, 6
        )
        if (l_sh and r_sh and l_hi and r_hi)
        else 0.0,
        "head_hip_depth_diff": round((nose[2] - (l_hi[2] + r_hi[2]) / 2) / torso_len, 6)
        if (nose and l_hi and r_hi)
        else 0.0,
    }

    # 3. Symmetry
    sd = lambda a, b: (a - b) if (a and b) else 0.0
    l_el_a = angle_2d(l_sh, l_el, l_wr)
    r_el_a = angle_2d(r_sh, r_el, r_wr)
    l_sh_a = angle_2d(l_el, l_sh, l_hi)
    r_sh_a = angle_2d(r_hi, r_sh, r_el)
    l_hi_a = angle_2d(l_sh, l_hi, l_kn)
    r_hi_a = angle_2d(r_sh, r_hi, r_kn)
    l_kn_a = angle_2d(l_hi, l_kn, l_an)
    r_kn_a = angle_2d(r_hi, r_kn, r_an)
    l_an_a = angle_2d(l_kn, l_an, l_foot)
    r_an_a = angle_2d(r_kn, r_an, r_foot)

    feat_sym = {
        "elbow_diff": sd(l_el_a, r_el_a) / 180.0,
        "shoulder_diff": sd(l_sh_a, r_sh_a) / 180.0,
        "hip_diff": sd(l_hi_a, r_hi_a) / 180.0,
        "knee_diff": sd(l_kn_a, r_kn_a) / 180.0,
        "ankle_diff": sd(l_an_a, r_an_a) / 180.0,
        "elbow_abs_diff": abs(sd(l_el_a, r_el_a)) / 180.0,
        "shoulder_abs_diff": abs(sd(l_sh_a, r_sh_a)) / 180.0,
        "hip_abs_diff": abs(sd(l_hi_a, r_hi_a)) / 180.0,
        "knee_abs_diff": abs(sd(l_kn_a, r_kn_a)) / 180.0,
        "ankle_abs_diff": abs(sd(l_an_a, r_an_a)) / 180.0,
        "knee_dominant_side": (1 if l_kn_a < r_kn_a else -1)
        if (l_kn_a and r_kn_a)
        else 0,
        "hip_dominant_side": (1 if l_hi_a < r_hi_a else -1)
        if (l_hi_a and r_hi_a)
        else 0,
    }

    # 4. Raw Landmarks
    LANDMARK_NAMES = [
        "NOSE",
        "LEFT_EYE_INNER",
        "LEFT_EYE",
        "LEFT_EYE_OUTER",
        "RIGHT_EYE_INNER",
        "RIGHT_EYE",
        "RIGHT_EYE_OUTER",
        "LEFT_EAR",
        "RIGHT_EAR",
        "MOUTH_LEFT",
        "MOUTH_RIGHT",
        "LEFT_SHOULDER",
        "RIGHT_SHOULDER",
        "LEFT_ELBOW",
        "RIGHT_ELBOW",
        "LEFT_WRIST",
        "RIGHT_WRIST",
        "LEFT_PINKY",
        "RIGHT_PINKY",
        "LEFT_INDEX",
        "RIGHT_INDEX",
        "LEFT_THUMB",
        "RIGHT_THUMB",
        "LEFT_HIP",
        "RIGHT_HIP",
        "LEFT_KNEE",
        "RIGHT_KNEE",
        "LEFT_ANKLE",
        "RIGHT_ANKLE",
        "LEFT_HEEL",
        "RIGHT_HEEL",
        "LEFT_FOOT_INDEX",
        "RIGHT_FOOT_INDEX",
    ]
    feat_raw = {}
    for name in LANDMARK_NAMES:
        lm = landmarks[P[name].value]
        feat_raw[f"{name}_x"] = round(lm.x, 6)
        feat_raw[f"{name}_y"] = round(lm.y, 6)
        feat_raw[f"{name}_z"] = (
            round(lm.z / torso_len, 6) if torso_len > 1e-6 else round(lm.z, 6)
        )
        feat_raw[f"{name}_vis"] = round(lm.visibility, 6)

    return {**feat_raw, **feat_angles, **feat_orient, **feat_sym}


class PoseDetectionService:
    """Service for pose detection and classification using MediaPipe and Random Forest."""

    def __init__(self):
        # Initialize MediaPipe Pose
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(
            static_image_mode=False,
            model_complexity=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7,
        )
        self.mp_drawing = mp.solutions.drawing_utils

        # Load ML model
        self.model_path = os.path.join(
            os.path.dirname(__file__), "model", "model.pkl"
        )
        self.encoder_path = os.path.join(
            os.path.dirname(__file__), "model", "label_encoder.pkl"
        )
        self.feature_cols_path = os.path.join(
            os.path.dirname(__file__), "model", "feature_columns.json"
        )

        self.classifier = None
        self.label_encoder = None
        self.feature_columns: Optional[List[str]] = None
        self.load_model()

        # Reference angles for poses (for accuracy calculation)
        self.reference_angles = self._init_reference_angles()

    def load_model(self):
        """Load the trained Random Forest model and label encoder."""
        try:
            if os.path.exists(self.model_path):
                self.classifier = joblib.load(self.model_path)
                print(f"Model loaded from {self.model_path}")
            else:
                print(f"Warning: Model file not found at {self.model_path}")

            if os.path.exists(self.encoder_path):
                self.label_encoder = joblib.load(self.encoder_path)
                print(f"Label encoder loaded from {self.encoder_path}")
            else:
                print(f"Warning: Label encoder file not found at {self.encoder_path}")

            # Load feature column order if available to ensure runtime features match training order
            if os.path.exists(self.feature_cols_path):
                try:
                    with open(self.feature_cols_path, "r", encoding="utf-8") as f:
                        self.feature_columns = json.load(f)
                    print(f"Feature columns loaded from {self.feature_cols_path} ({len(self.feature_columns)} cols)")
                except Exception as fe:
                    print(f"Warning: Failed to load feature columns: {fe}")

            # Sanity check: warn if model labels don't align with our reference dict
            try:
                if self.label_encoder is not None:
                    model_labels = set(map(str, getattr(self.label_encoder, "classes_", [])))
                    ref_labels = set(self._init_reference_angles().keys())
                    missing_in_ref = model_labels - ref_labels
                    if missing_in_ref:
                        print(f"Warning: {len(missing_in_ref)} model classes missing in reference angles: {sorted(list(missing_in_ref))[:5]}...")
            except Exception:
                pass

        except Exception as e:
            print(f"Error loading model: {e}")

   
#  Extracts landmarks from the image using MediaPipe Pose
    def extract_landmarks(self, image: np.ndarray) -> Optional[np.ndarray]:
        # Extract features EXACTLY like dataset (landmarks + angles).

        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.pose.process(image_rgb)

        if not results.pose_landmarks:
            return None

        landmarks = results.pose_landmarks.landmark
        feature_dict = extract_all_features(landmarks)

        if hasattr(self, "feature_columns") and self.feature_columns is not None:
            return np.array([feature_dict.get(col, 0) for col in self.feature_columns])

        return np.array(list(feature_dict.values()))

    def classify_pose(self, features: np.ndarray) -> Dict:
    # ---------------------------
    # 0. Check model
    # ---------------------------
        if self.classifier is None or self.label_encoder is None:
           return {
            "pose_class": "unknown",
            "pose_name": "Unknown Pose",
            "confidence": 0.0,
            "all_predictions": [],
          }

    # ---------------------------
    # 1. Ensure correct shape & Align with Dataset
    # ---------------------------
        # The custom dataset CSV has exactly 14 angles leading, followed by 132 landmarks.
        # But extract_landmarks yields [132 landmarks, 14 angles]. We swap them inline to protect frontend drawing arrays.
        if len(features) == 146:
            ml_features = np.concatenate([features[132:146], features[:132]])
        else:
            ml_features = features

        if ml_features.ndim == 1:
            ml_features = ml_features.reshape(1, -1)

    # ---------------------------
    # 2. Predict
    # ---------------------------
        pred_index = self.classifier.predict(ml_features)[0]
        probabilities = self.classifier.predict_proba(ml_features)[0]

    # ---------------------------
    # 3. Get class labels
    # ---------------------------
        class_labels = self.label_encoder.classes_

        pose_class = class_labels[pred_index]
        confidence = probabilities[pred_index]

    # ---------------------------
    # 4. All predictions
    # ---------------------------
        all_predictions = []

        for idx, prob in enumerate(probabilities):
           if prob > 0.01:
                all_predictions.append({
                   "pose": class_labels[idx],
                   "confidence": float(prob)
                })

    # Sort
        all_predictions.sort(key=lambda x: x["confidence"], reverse=True)

    # ---------------------------
    # 5. Display name
    # ---------------------------
        pose_display_name = self._get_pose_display_name(pose_class)

        return {
            "pose_class": pose_class,
            "pose_name": pose_display_name,
            "confidence": float(confidence),
            "all_predictions": all_predictions[:5],
       }
  

    def process_frame(self, image: np.ndarray, target_pose: str = "") -> Optional[Dict]:
        """Process a frame: extract landmarks, classify pose, calculate accuracy.

        Args:
            image: BGR image from OpenCV
            target_pose: Optional target pose key for accuracy calculation

        Returns:
            Dictionary with detection results or None if no pose detected
        """
        # Extract landmarks
        landmarks = self.extract_landmarks(image)

        if landmarks is None:
            return None

        # Classify pose
        classification = self.classify_pose(landmarks)

        # Calculate accuracy if target pose specified
        accuracy = 0
        feedback = ""
        corrections = []

        if target_pose:
            accuracy, feedback, corrections = self.calculate_accuracy(
                landmarks, target_pose
            )

        # Format landmarks for response
        landmarks_list = []
        for i in range(33):
            idx = i * 4
            landmarks_list.append(
                {
                    "x": float(landmarks[idx]),
                    "y": float(landmarks[idx + 1]),
                    "z": float(landmarks[idx + 2]),
                    "visibility": float(landmarks[idx + 3]),
                }
            )

        return {
            "pose_detected": classification["pose_name"],
            "pose_class": classification["pose_class"],
            "confidence": classification["confidence"],
            "accuracy_percentage": accuracy,
            "landmarks": landmarks_list,
            "feedback": feedback,
            "corrections": corrections,
            "all_predictions": classification["all_predictions"],
        }

    def calculate_accuracy(
        self, landmarks: np.ndarray, target_pose: str
    ) -> Tuple[float, str, List[str]]:
        """Calculate pose accuracy compared to reference pose.

        Args:
            landmarks: numpy array of shape (146,)
            target_pose: target pose key (can be exercise pose_key like 'tree_pose' or model label like 'TreePose')

        Returns:
            Tuple of (accuracy_percentage, feedback_message, corrections_list)
        """
        # Normalize incoming target pose key to our internal label format
        norm_key = self._normalize_pose_key(target_pose)

        # Get current angles
        current_angles = self._calculate_joint_angles(landmarks)

        # Get reference angles
        ref_angles = self.reference_angles.get(norm_key, {})

        if not ref_angles:
            return 50.0, "Keep practicing!", ["Focus on your form"]

        # Compare angles
        angle_diffs = []
        corrections = []

        for joint, ref_angle in ref_angles.items():
            if joint in current_angles:
                diff = abs(current_angles[joint] - ref_angle)
                angle_diffs.append(diff)

                # Generate correction if difference is significant
                if diff > 20:
                    if diff > 40:
                        level = "significantly"
                    else:
                        level = "slightly"

                    direction = (
                        "increase" if current_angles[joint] < ref_angle else "decrease"
                    )
                    corrections.append(
                        f"{joint.replace('_', ' ').title()}: {direction} angle ({level} off)"
                    )

        # Calculate accuracy based on angle differences
        if angle_diffs:
            avg_diff = np.mean(angle_diffs)
            accuracy = max(0, 100 - (avg_diff * 2))
        else:
            accuracy = 50

        # Generate feedback
        if accuracy >= 90:
            feedback = "Excellent form! Perfect alignment."
        elif accuracy >= 75:
            feedback = "Good job! Minor adjustments needed."
        elif accuracy >= 50:
            feedback = "Getting there. Focus on the corrections."
        else:
            feedback = "Keep practicing. Check your alignment."

        return round(accuracy, 1), feedback, corrections[:3]  # Top 3 corrections

    def _calculate_joint_angles(self, landmarks: np.ndarray) -> Dict[str, float]:
        """Calculate key joint angles from landmarks. Aligned with dataset features."""
        angles = {}

        if len(landmarks) >= 169:
            # New 169-feature format: angles are normalized (/ 180.0), so we multiply by 180.0 to get degrees
            angles["left_elbow"] = float(landmarks[132]) * 180.0
            angles["right_elbow"] = float(landmarks[133]) * 180.0
            angles["left_shoulder"] = float(landmarks[134]) * 180.0
            angles["right_shoulder"] = float(landmarks[135]) * 180.0
            angles["neck"] = float(landmarks[136]) * 180.0
            angles["left_hip"] = float(landmarks[137]) * 180.0
            angles["right_hip"] = float(landmarks[138]) * 180.0
            angles["left_knee"] = float(landmarks[139]) * 180.0
            angles["right_knee"] = float(landmarks[140]) * 180.0
            return angles

        if len(landmarks) == 146:
            # Old 146-feature format (values are in degrees)
            angles["left_elbow"] = float(landmarks[132])
            angles["right_elbow"] = float(landmarks[133])
            angles["left_shoulder"] = float(landmarks[134])
            angles["right_shoulder"] = float(landmarks[135])
            angles["left_knee"] = float(landmarks[136])
            angles["right_knee"] = float(landmarks[137])
            angles["ardha_chandrasana_1"] = float(landmarks[138])
            angles["ardha_chandrasana_2"] = float(landmarks[139])
            angles["hand"] = float(landmarks[140])
            angles["left_hip"] = float(landmarks[141])
            angles["right_hip"] = float(landmarks[142])
            angles["neck"] = float(landmarks[143])
            angles["left_wrist"] = float(landmarks[144])
            angles["right_wrist"] = float(landmarks[145])
            return angles

        # Fallback if just raw 132 landmarks passed
        lm = landmarks[:132].reshape(-1, 4)

        # Helper to get point
        def get_point(idx):
            return [lm[idx][0], lm[idx][1]]

        try:
            # Angles corresponding exactly to dataset's _angles_finder formulas
            angles["left_shoulder"] = self._calculate_angle(get_point(13), get_point(11), get_point(23))
            angles["right_shoulder"] = self._calculate_angle(get_point(24), get_point(12), get_point(14))
            
            angles["left_hip"] = self._calculate_angle(get_point(11), get_point(23), get_point(25))
            angles["right_hip"] = self._calculate_angle(get_point(12), get_point(24), get_point(26))
            
            angles["left_elbow"] = self._calculate_angle(get_point(11), get_point(13), get_point(15))
            angles["right_elbow"] = self._calculate_angle(get_point(12), get_point(14), get_point(16))
            
            angles["left_knee"] = self._calculate_angle(get_point(23), get_point(25), get_point(27))
            angles["right_knee"] = self._calculate_angle(get_point(24), get_point(26), get_point(28))
            
            angles["ardha_chandrasana_1"] = self._calculate_angle(get_point(16), get_point(14), get_point(12))
            angles["ardha_chandrasana_2"] = self._calculate_angle(get_point(15), get_point(13), get_point(11))
            angles["hand"] = self._calculate_angle(get_point(16), get_point(20), get_point(18))
            
            # Neck angle (nose, left shoulder, right shoulder) corresponds to neck_angle_uk
            angles["neck"] = self._calculate_angle(get_point(0), get_point(11), get_point(12))

            angles["left_wrist"] = self._calculate_angle(get_point(15), get_point(17), get_point(19))
            angles["right_wrist"] = self._calculate_angle(get_point(16), get_point(18), get_point(20))

        except Exception as e:
            print(f"Error calculating angles: {e}")

        return angles

#  Helper method to calculate angle between three points
    def _calculate_angle(self, a: List[float], b: List[float], c: List[float]) -> float:
        """Calculate angle between three points."""
        a, b, c = np.array(a), np.array(b), np.array(c)

        radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(
            a[1] - b[1], a[0] - b[0]
        )
        angle = np.abs(radians * 180.0 / np.pi)

        return 360 - angle if angle > 180 else angle

#  method for perfect textbook angles for different joints in various yoga poses
    def _init_reference_angles(self) -> Dict[str, Dict[str, float]]:
        """Initialize reference angles for each pose from dataset averages."""
        return {
            'AnjaneyasanaPose': {'left_elbow': 163.45, 'right_elbow': 163.23, 'left_shoulder': 155.73, 'right_shoulder': 156.29, 'left_knee': 106.49, 'right_knee': 81.78, 'ardha_chandrasana_1': 110.21, 'ardha_chandrasana_2': 112.35, 'hand': 7.95, 'left_hip': 120.56, 'right_hip': 94.04, 'neck': 70.31, 'left_wrist': 110.69, 'right_wrist': 130.66},
            'BoatPose': {'left_elbow': 177.33, 'right_elbow': 179.16, 'left_shoulder': 171.36, 'right_shoulder': 116.7, 'left_knee': 178.6, 'right_knee': 179.76, 'ardha_chandrasana_1': 357.68, 'ardha_chandrasana_2': 1.81, 'hand': 22.07, 'left_hip': 196.4, 'right_hip': 234.44, 'neck': 264.04, 'left_wrist': 192.25, 'right_wrist': 246.65},
            'BridgePose': {'left_elbow': 184.09, 'right_elbow': 179.55, 'left_shoulder': 157.07, 'right_shoulder': 162.41, 'left_knee': 191.74, 'right_knee': 181.68, 'ardha_chandrasana_1': 346.09, 'ardha_chandrasana_2': 12.83, 'hand': 18.03, 'left_hip': 178.21, 'right_hip': 183.84, 'neck': 272.96, 'left_wrist': 184.08, 'right_wrist': 168.74},
            'CamelPose': {'left_elbow': 181.21, 'right_elbow': 185.53, 'left_shoulder': 189.89, 'right_shoulder': 92.78, 'left_knee': 193.08, 'right_knee': 200.59, 'ardha_chandrasana_1': 4.28, 'ardha_chandrasana_2': 355.56, 'hand': 187.82, 'left_hip': 198.96, 'right_hip': 208.7, 'neck': 172.0, 'left_wrist': 267.43, 'right_wrist': 283.48},
            'CatCowPose': {'left_elbow': 174.05, 'right_elbow': 174.28, 'left_shoulder': 71.22, 'right_shoulder': 70.84, 'left_knee': 92.24, 'right_knee': 91.26, 'ardha_chandrasana_1': 1.65, 'ardha_chandrasana_2': 1.61, 'hand': 4.62, 'left_hip': 108.61, 'right_hip': 107.6, 'neck': 74.22, 'left_wrist': 81.0, 'right_wrist': 81.77},
            'ChairPose': {'left_elbow': 163.75, 'right_elbow': 163.81, 'left_shoulder': 152.09, 'right_shoulder': 152.78, 'left_knee': 102.84, 'right_knee': 98.95, 'ardha_chandrasana_1': 2.18, 'ardha_chandrasana_2': 2.15, 'hand': 9.15, 'left_hip': 96.83, 'right_hip': 98.26, 'neck': 62.14, 'left_wrist': 128.29, 'right_wrist': 130.52},
            'ChildPose': {'left_elbow': 184.14, 'right_elbow': 186.81, 'left_shoulder': 195.05, 'right_shoulder': 163.81, 'left_knee': 159.34, 'right_knee': 82.94, 'ardha_chandrasana_1': 351.11, 'ardha_chandrasana_2': 8.43, 'hand': 23.86, 'left_hip': 286.73, 'right_hip': 308.72, 'neck': 102.67, 'left_wrist': 197.18, 'right_wrist': 252.56},
            'CobraPose': {'left_elbow': 183.28, 'right_elbow': 183.72, 'left_shoulder': 197.49, 'right_shoulder': 33.07, 'left_knee': 178.24, 'right_knee': 177.49, 'ardha_chandrasana_1': 3.21, 'ardha_chandrasana_2': 356.55, 'hand': 341.94, 'left_hip': 144.57, 'right_hip': 148.84, 'neck': 97.22, 'left_wrist': 192.69, 'right_wrist': 189.04},
            'CorpsePose': {'left_elbow': 176.99, 'right_elbow': 183.51, 'left_shoulder': 38.81, 'right_shoulder': 40.57, 'left_knee': 179.99, 'right_knee': 181.2, 'ardha_chandrasana_1': 346.14, 'ardha_chandrasana_2': 14.18, 'hand': 64.5, 'left_hip': 173.54, 'right_hip': 183.34, 'neck': 297.25, 'left_wrist': 119.73, 'right_wrist': 244.02},
            'DownwardDogPose': {'left_elbow': 183.47, 'right_elbow': 183.91, 'left_shoulder': 181.74, 'right_shoulder': 177.86, 'left_knee': 179.16, 'right_knee': 180.37, 'ardha_chandrasana_1': 351.32, 'ardha_chandrasana_2': 5.19, 'hand': 34.81, 'left_hip': 273.5, 'right_hip': 271.01, 'neck': 199.05, 'left_wrist': 278.96, 'right_wrist': 276.28},
            'GoddessPose': {'left_elbow': 161.79, 'right_elbow': 203.18, 'left_shoulder': 88.47, 'right_shoulder': 83.44, 'left_knee': 238.13, 'right_knee': 119.77, 'ardha_chandrasana_1': 292.95, 'ardha_chandrasana_2': 66.35, 'hand': 153.71, 'left_hip': 117.76, 'right_hip': 242.18, 'neck': 304.47, 'left_wrist': 142.38, 'right_wrist': 217.19},
            'HalasanaPose': {'left_elbow': 172.09, 'right_elbow': 171.39, 'left_shoulder': 85.83, 'right_shoulder': 87.52, 'left_knee': 172.43, 'right_knee': 170.59, 'ardha_chandrasana_1': 0.76, 'ardha_chandrasana_2': 0.76, 'hand': 16.54, 'left_hip': 55.41, 'right_hip': 53.26, 'neck': 56.48, 'left_wrist': 93.91, 'right_wrist': 95.01},
            'LocustPose': {'left_elbow': 168.53, 'right_elbow': 167.27, 'left_shoulder': 25.24, 'right_shoulder': 24.02, 'left_knee': 165.51, 'right_knee': 166.74, 'ardha_chandrasana_1': 2.05, 'ardha_chandrasana_2': 2.02, 'hand': 22.87, 'left_hip': 139.92, 'right_hip': 140.22, 'neck': 73.93, 'left_wrist': 90.16, 'right_wrist': 89.97},
            'ParsvottanasanaPose': {'left_elbow': 163.61, 'right_elbow': 160.33, 'left_shoulder': 76.85, 'right_shoulder': 71.06, 'left_knee': 174.15, 'right_knee': 173.64, 'ardha_chandrasana_1': 50.86, 'ardha_chandrasana_2': 49.64, 'hand': 10.91, 'left_hip': 57.32, 'right_hip': 49.08, 'neck': 76.06, 'left_wrist': 67.31, 'right_wrist': 64.75},
            'PaschimottanasanaPose': {'left_elbow': 152.16, 'right_elbow': 148.68, 'left_shoulder': 63.03, 'right_shoulder': 63.27, 'left_knee': 166.78, 'right_knee': 166.0, 'ardha_chandrasana_1': 3.86, 'ardha_chandrasana_2': 4.27, 'hand': 23.04, 'left_hip': 64.65, 'right_hip': 62.44, 'neck': 55.88, 'left_wrist': 14.6, 'right_wrist': 15.07},
            'PigeonPose': {'left_elbow': 180.62, 'right_elbow': 184.78, 'left_shoulder': 188.65, 'right_shoulder': 111.02, 'left_knee': 168.66, 'right_knee': 134.43, 'ardha_chandrasana_1': 225.62, 'ardha_chandrasana_2': 149.08, 'hand': 67.2, 'left_hip': 138.21, 'right_hip': 240.38, 'neck': 243.07, 'left_wrist': 183.53, 'right_wrist': 219.93},
            'PlankPose': {'left_elbow': 177.01, 'right_elbow': 181.68, 'left_shoulder': 91.9, 'right_shoulder': 108.72, 'left_knee': 180.23, 'right_knee': 180.04, 'ardha_chandrasana_1': 313.99, 'ardha_chandrasana_2': 50.19, 'hand': 180.0, 'left_hip': 172.97, 'right_hip': 187.07, 'neck': 271.69, 'left_wrist': 130.67, 'right_wrist': 214.29},
            'TreePose': {'left_elbow': 172.3, 'right_elbow': 182.67, 'left_shoulder': 157.54, 'right_shoulder': 159.88, 'left_knee': 185.22, 'right_knee': 84.22, 'ardha_chandrasana_1': 306.95, 'ardha_chandrasana_2': 41.5, 'hand': 252.05, 'left_hip': 175.72, 'right_hip': 215.19, 'neck': 309.13, 'left_wrist': 188.99, 'right_wrist': 169.82},
            'TrianglePose': {'left_elbow': 174.22, 'right_elbow': 185.81, 'left_shoulder': 104.67, 'right_shoulder': 102.74, 'left_knee': 180.87, 'right_knee': 180.64, 'ardha_chandrasana_1': 282.39, 'ardha_chandrasana_2': 72.81, 'hand': 176.76, 'left_hip': 191.22, 'right_hip': 213.2, 'neck': 306.74, 'left_wrist': 175.51, 'right_wrist': 189.81},
            'Warrior2Pose': {'left_elbow': 173.18, 'right_elbow': 172.92, 'left_shoulder': 98.88, 'right_shoulder': 102.31, 'left_knee': 172.17, 'right_knee': 129.21, 'ardha_chandrasana_1': 77.85, 'ardha_chandrasana_2': 79.27, 'hand': 169.73, 'left_hip': 129.31, 'right_hip': 120.56, 'neck': 45.87, 'left_wrist': 108.65, 'right_wrist': 118.81}
        }

    def _get_pose_display_name(self, pose_class: str) -> str:
        """Get human-readable pose name."""
        import re
        display_names = {
            'AnjaneyasanaPose': 'Anjaneyasana Pose',
            'BoatPose': 'Boat Pose',
            'BridgePose': 'Bridge Pose',
            'CamelPose': 'Camel Pose',
            'CatCowPose': 'Cat Cow Pose',
            'ChairPose': 'Chair Pose',
            'ChildPose': 'Child Pose',
            'CobraPose': 'Cobra Pose',
            'CorpsePose': 'Corpse Pose',
            'DownwardDogPose': 'Downward Dog Pose',
            'GoddessPose': 'Goddess Pose',
            'HalasanaPose': 'Halasana Pose',
            'LocustPose': 'Locust Pose',
            'ParsvottanasanaPose': 'Parsvottanasana Pose',
            'PaschimottanasanaPose': 'Paschimottanasana Pose',
            'PigeonPose': 'Pigeon Pose',
            'PlankPose': 'Plank Pose',
            'TreePose': 'Tree Pose',
            'TrianglePose': 'Triangle Pose',
            'Warrior2Pose': 'Warrior 2 Pose'
        }
        return display_names.get(pose_class, re.sub(r'(?<!^)(?=[A-Z])', ' ', pose_class).title())

    def _normalize_pose_key(self, key: str) -> str:
        """Map frontend exercise pose_key (snake_case) or display name to model label key used in reference angles.

        Examples:
            'tree_pose' -> 'TreePose'
            'warrior_ii' -> 'Warrior2Pose'
            'Downward Dog Pose' -> 'DownwardDogPose'
            'TreePose' -> 'TreePose' (idempotent)
        """
        if not key:
            return key
        k = key.strip()
        # If already a direct key in our reference map, return as-is
        if k in self.reference_angles:
            return k
        # Accept display names too
        display_to_key = {self._get_pose_display_name(p): p for p in self.reference_angles.keys()}
        if k in display_to_key:
            return display_to_key[k]
        # Known mappings from exercise.pose_key to model labels
        mapping = {
            'anjaneyasana': 'AnjaneyasanaPose',
            'boat_pose': 'BoatPose',
            'bridge_pose': 'BridgePose',
            'camel_pose': 'CamelPose',
            'cat_cow': 'CatCowPose',
            'chair_pose': 'ChairPose',
            'child_pose': 'ChildPose',
            'cobra_pose': 'CobraPose',
            'corpse_pose': 'CorpsePose',
            'downward_dog': 'DownwardDogPose',
            'goddess_pose': 'GoddessPose',
            'halasana': 'HalasanaPose',
            'locust': 'LocustPose',
            'parsvottanasana': 'ParsvottanasanaPose',
            'paschimottanasana': 'PaschimottanasanaPose',
            'pigeon_pose': 'PigeonPose',
            'plank': 'PlankPose',
            'tree_pose': 'TreePose',
            'triangle_pose': 'TrianglePose',
            'warrior_ii': 'Warrior2Pose',
        }
        return mapping.get(k.lower(), k)

    def get_supported_poses(self) -> List[Dict]:
        """Get list of supported poses."""
        poses = []
        for pose_key in self.reference_angles.keys():
            poses.append(
                {"key": pose_key, "name": self._get_pose_display_name(pose_key)}
            )
        return poses

    def draw_landmarks(self, image: np.ndarray, landmarks: List[Dict]) -> np.ndarray:
        """Draw landmarks on image for visualization."""
        h, w, _ = image.shape

        for i, lm in enumerate(landmarks):
            if lm["visibility"] > 0.5:
                x = int(lm["x"] * w)
                y = int(lm["y"] * h)
                cv2.circle(image, (x, y), 5, (0, 255, 0), -1)
                cv2.putText(
                    image,
                    str(i),
                    (x + 5, y),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.3,
                    (255, 0, 0),
                    1,
                )

        return image
