from ultralytics import YOLO
import numpy as np
import cv2
import os
import csv

# Load YOLO pose model
model = YOLO("yolo11n-pose.pt")

def is_falling(keypoints, threshold_angle=90, tolerance=25):
    if keypoints is None or keypoints.shape[0] < 13:
        return False, 90

    left_shoulder = keypoints[5]
    right_shoulder = keypoints[6]
    left_hip = keypoints[11]
    right_hip = keypoints[12]

    if any((x == 0 and y == 0) for x, y in [left_shoulder, right_shoulder, left_hip, right_hip]):
        return False, 90

    shoulder_mid = (left_shoulder + right_shoulder) / 2
    hip_mid = (left_hip + right_hip) / 2
    dx = hip_mid[0] - shoulder_mid[0]
    dy = hip_mid[1] - shoulder_mid[1]
    angle = abs(np.degrees(np.arctan2(dy, dx)))

    return abs(angle - threshold_angle) > tolerance, angle

# Root dataset directory
dataset_dir = r"C:\Users\Nai\OneDrive\GT - Mahidol\Class\2nd\ITGT523 Computer Vision\ITGT523_Naddanai\fall_detect\Homemade CCTV Falling Dataset"

# Output CSV file
output_csv = "fall_detection_results.csv"

with open(output_csv, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Category", "Video Name", "Total Frames", "Fall Frames", "Fall %", "Fall Detected"])

    for category in os.listdir(dataset_dir):
        category_path = os.path.join(dataset_dir, category)

        if not os.path.isdir(category_path):
            continue

        for video_file in os.listdir(category_path):
            if not video_file.lower().endswith(".mp4"):
                continue

            video_path = os.path.join(category_path, video_file)
            cap = cv2.VideoCapture(video_path)

            total_frames = 0
            fall_frames = 0

            while True:
                ret, frame = cap.read()
                if not ret:
                    break

                results = model.predict(frame, verbose=False)
                total_frames += 1

                for r in results:
                    keypoints = r.keypoints.xy.cpu().numpy()[0] if r.keypoints.xy is not None else None
                    falling, angle = is_falling(keypoints)
                    if falling:
                        fall_frames += 1
                    break  # just use first detection (assumes 1 person)

            cap.release()

            fall_percent = (fall_frames / total_frames) * 100 if total_frames > 0 else 0
            fall_detected = fall_percent > 30  # you can adjust threshold
            writer.writerow([category, video_file, total_frames, fall_frames, f"{fall_percent:.2f}", fall_detected])

print("Finished processing all videos.")