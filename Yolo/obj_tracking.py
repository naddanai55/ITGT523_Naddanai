import os
import cv2
from ultralytics import solutions

os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"

def count_specific_classes(video_path, model_path, classes_to_count):
    cap = cv2.VideoCapture(video_path)
    assert cap.isOpened(), "Error reading video file"
    counter = solutions.ObjectCounter(show=True,
                                      region=[(20, 400), (1080, 400)],
                                      model=model_path, 
                                      classes=classes_to_count,
                                      line_width=2)
    while cap.isOpened():
        success, im0 = cap.read()
        if not success:
            print("Video frame is empty or video processing has been successfully completed.")
            break
        im0 = counter.count(im0)

    cap.release()
    cv2.destroyAllWindows()

count_specific_classes("cctv.mp4", "yolo11n.pt", [0])
