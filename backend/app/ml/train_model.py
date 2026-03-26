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
    angle_cols = [
        "left_elbow_angle",
        "right_elbow_angle",
        "left_shoulder_angle",
        "right_shoulder_angle",
        "left_knee_angle",
        "right_knee_angle",
        "angle_for_ardhaChandrasana1",
        "angle_for_ardhaChandrasana2",
        "hand_angle",
        "left_hip_angle",
        "right_hip_angle",
        "neck_angle_uk",
        "left_wrist_angle_bk",
        "right_wrist_angle_bk",
    ]
    # Landmark bases in dataset order (the CSV lists NOSE_x, LEFT_EYE_INNER_x, ...)
    landmark_x_cols = [c for c in df.columns if c.endswith("_x")]
    bases = [c[:-2] for c in landmark_x_cols]
    landmark_cols = [f"{b}_{sfx}" for b in bases for sfx in ("x", "y", "z", "vis")]
    return angle_cols + landmark_cols


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

    X = df[feature_columns].values
    y_text = df["Label"].astype(str).values

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
