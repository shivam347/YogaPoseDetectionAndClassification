import pandas as pd
import json
import numpy as np

def calculate_reference_angles():
    df = pd.read_csv(r"c:\Projects\Yoga Pose Detection App\backend\data\YogaPose_Final_Dataset.csv")

    cols_to_extract = {
        'left_elbow_angle': 'left_elbow',
        'right_elbow_angle': 'right_elbow',
        'left_shoulder_angle': 'left_shoulder',
        'right_shoulder_angle': 'right_shoulder',
        'left_knee_angle': 'left_knee',
        'right_knee_angle': 'right_knee',
        'angle_for_ardhaChandrasana1': 'ardha_chandrasana_1',
        'angle_for_ardhaChandrasana2': 'ardha_chandrasana_2',
        'hand_angle': 'hand',
        'left_hip_angle': 'left_hip',
        'right_hip_angle': 'right_hip',
        'neck_angle_uk': 'neck',
        'left_wrist_angle_bk': 'left_wrist',
        'right_wrist_angle_bk': 'right_wrist',
    }

    # Group by Label and calculate median for robustness against outliers
    medians = df.groupby('Label')[list(cols_to_extract.keys())].median()

    # Format into perfectly rounded python dictionary
    result = {}
    for pose in medians.index:
        pose_angles = {}
        for csv_col, dict_key in cols_to_extract.items():
            pose_angles[dict_key] = round(float(medians.loc[pose, csv_col]), 2)
        result[pose] = pose_angles

    # Write clearly to file
    dict_str = json.dumps(result, indent=12).replace('"', "'")
    with open('dataset_angles.json', 'w', encoding='utf-8') as f:
        f.write(dict_str)
    print("Done")

if __name__ == "__main__":
    calculate_reference_angles()
