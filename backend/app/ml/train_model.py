#!/usr/bin/env python3
"""
Train pose classification model using provided YogaPose_Final_Dataset.csv.
Saves model.pkl, label_encoder.pkl, and feature_columns.json under app/ml/model.

This aligns feature ordering with runtime inference:
- Angles first (14), followed by 33 landmarks x 4 coords each (x,y,z,vis) in dataset order.
"""

import os
import json
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, accuracy_score
from sklearn.model_selection import train_test_split


def _dataset_paths():
    here = os.path.dirname(__file__)
    data_csv = os.path.normpath(os.path.join(here, "..", "..", "data", "YogaPose_Final_Dataset.csv"))
    model_dir = os.path.join(here, "model")
    os.makedirs(model_dir, exist_ok=True)
    return data_csv, model_dir


def _build_feature_columns(df: pd.DataFrame) -> list[str]:
    # Landmark bases in standard order (matches LANDMARK_NAMES in pose_detector.py)
    landmark_names = [
        "NOSE", "LEFT_EYE_INNER", "LEFT_EYE", "LEFT_EYE_OUTER",
        "RIGHT_EYE_INNER", "RIGHT_EYE", "RIGHT_EYE_OUTER",
        "LEFT_EAR", "RIGHT_EAR", "MOUTH_LEFT", "MOUTH_RIGHT",
        "LEFT_SHOULDER", "RIGHT_SHOULDER", "LEFT_ELBOW", "RIGHT_ELBOW",
        "LEFT_WRIST", "RIGHT_WRIST", "LEFT_PINKY", "RIGHT_PINKY",
        "LEFT_INDEX", "RIGHT_INDEX", "LEFT_THUMB", "RIGHT_THUMB",
        "LEFT_HIP", "RIGHT_HIP", "LEFT_KNEE", "RIGHT_KNEE",
        "LEFT_ANKLE", "RIGHT_ANKLE", "LEFT_HEEL", "RIGHT_HEEL",
        "LEFT_FOOT_INDEX", "RIGHT_FOOT_INDEX"
    ]
    
    raw_cols = []
    for name in landmark_names:
        for sfx in ("x", "y", "z", "vis"):
            raw_cols.append(f"{name}_{sfx}")

    angle_cols = [
        "left_elbow_angle", "right_elbow_angle", "left_shoulder_angle", "right_shoulder_angle",
        "neck_angle", "left_hip_angle", "right_hip_angle", "left_knee_angle", "right_knee_angle",
        "left_ankle_angle", "right_ankle_angle", "spine_tilt_deg", "pelvis_tilt_deg",
        "shoulder_line_deg", "inter_ankle_angle_L", "inter_ankle_angle_R"
    ]

    orient_cols = [
        "shoulder_yaw_sin", "shoulder_yaw_cos", "hip_yaw_sin", "hip_yaw_cos",
        "shoulder_depth_diff", "hip_depth_diff", "ankle_depth_diff", "spine_lean_depth",
        "head_hip_depth_diff"
    ]

    sym_cols = [
        "elbow_diff", "shoulder_diff", "hip_diff", "knee_diff", "ankle_diff",
        "elbow_abs_diff", "shoulder_abs_diff", "hip_abs_diff", "knee_abs_diff", "ankle_abs_diff",
        "knee_dominant_side", "hip_dominant_side"
    ]

    return raw_cols + angle_cols + orient_cols + sym_cols


def train_model():
    data_csv, model_dir = _dataset_paths()
    if not os.path.exists(data_csv):
        raise FileNotFoundError(f"Dataset not found at {data_csv}")

    print(f"Loading dataset: {data_csv}")
    df = pd.read_csv(data_csv)

    feature_columns = _build_feature_columns(df)
    missing = [c for c in feature_columns if c not in df.columns]
    if missing:
        raise ValueError(f"Missing expected columns in dataset: {missing[:10]} ... total {len(missing)}")

    # Clean NaNs in features and label
    if "label" not in df.columns:
        # Fallback to case-insensitive check if label column name is different
        label_col = [c for c in df.columns if c.lower() == "label"]
        if label_col:
            df = df.rename(columns={label_col[0]: "label"})
        else:
            raise KeyError("Label/label column not found in the dataset.")

    initial_len = len(df)
    df = df.dropna(subset=feature_columns + ["label"])
    dropped = initial_len - len(df)
    if dropped > 0:
        print(f"Dropped {dropped} rows containing NaNs. Total rows remaining: {len(df)}")

    X = df[feature_columns].values
    y_text = df["label"].astype(str).values

    print(f"Dataset shape: X={X.shape}, y={y_text.shape}")

    le = LabelEncoder()
    y = le.fit_transform(y_text)

    X_train, X_val, y_train, y_val = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    clf = RandomForestClassifier(
        n_estimators=500,
        max_depth=None,
        class_weight="balanced_subsample",
        random_state=42,
        n_jobs=-1,
    )

    print("Training RandomForestClassifier ...")
    clf.fit(X_train, y_train)

    y_pred = clf.predict(X_val)
    acc = accuracy_score(y_val, y_pred)
    print(f"Validation accuracy: {acc:.4f}")
    try:
        report = classification_report(y_val, y_pred, target_names=le.classes_)
        print(report)
    except Exception:
        pass

    # Save artifacts
    model_path = os.path.join(model_dir, "model.pkl")
    enc_path = os.path.join(model_dir, "label_encoder.pkl")
    cols_path = os.path.join(model_dir, "feature_columns.json")

    joblib.dump(clf, model_path)
    joblib.dump(le, enc_path)
    with open(cols_path, "w", encoding="utf-8") as f:
        json.dump(feature_columns, f, ensure_ascii=False, indent=2)

    print(f"Saved model -> {model_path}")
    print(f"Saved label encoder -> {enc_path}")
    print(f"Saved feature columns -> {cols_path}")


if __name__ == "__main__":
    train_model()
