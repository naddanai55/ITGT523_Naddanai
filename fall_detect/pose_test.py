from ultralytics import YOLO
import numpy as np
import cv2
import os

model = YOLO("yolo11s-pose.pt")

def is_falling(keypoints, threshold_angle=90, tolerance=45, vertical_threshold=1.5):
    if keypoints is None or keypoints.shape[0] < 13:
        print("Error: keypoints detected")
        return False, 90 
    
    left_shoulder = keypoints[5]
    right_shoulder = keypoints[6]
    left_hip = keypoints[11]
    right_hip = keypoints[12]

    if np.isnan(left_shoulder).any() or np.isnan(right_shoulder).any() or np.isnan(left_hip).any() or np.isnan(right_hip).any():
        print("Error: keypoints are NaN")
        return False, 90 
    
    shoulder_mid = (left_shoulder + right_shoulder) / 2
    hip_mid = (left_hip + right_hip) / 2
    dx = hip_mid[0] - shoulder_mid[0]
    dy = hip_mid[1] - shoulder_mid[1]
    print("dx:", dx, "dy:", dy)
    angle = abs(np.degrees(np.arctan2(dy, dx)))

    if abs(angle - threshold_angle) > tolerance:
        return True, angle
    
    return False, angle

capture = cv2.VideoCapture(0)
while True:
    ret, frame = capture.read()
    if not ret:
        print("Error: Unable to capture frame from webcam.")
        break

    try:
        results = model(frame)
    except Exception as e:
        print(f"Error processing frame with YOLO model: {e}")
        continue

    for result in results:
        if result.keypoints is not None:
            keypoints = result.keypoints.xy.cpu().numpy()  # Convert all keypoints to NumPy array
if k                # Draw keypoints
                for x, y in keypoints:
                    cv2.circle(frame, (int(x), int(y)), 5, (0, 0, 255), -1)

                # Call is_falling with the full set of keypoints
                falling, angle = is_falling(keypoints)
                label = "Falling" if falling else "Standing"
                color = (0, 0, 255) if falling else (0, 255, 0)
                cv2.putText(frame, label, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
                cv2.putText(frame, f"Angle: {angle:.1f}", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
            else:
                print("Error: Not enough keypoints detected.")
        else:
            print("Error: No keypoints detected.")

    cv2.imshow("Frame", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

capture.release()
cv2.destroyAllWindows()

