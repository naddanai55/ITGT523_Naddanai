from ultralytics import YOLO
import pygame
import cv2
import numpy as np
import time
from button import Button
from slider import Slider

model = YOLO("yolo11n-pose.pt")

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Fall-Detection-App-Prototype")

BLUE = (41, 115, 178)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ORANGE = (228, 158, 41)
BGC = (248, 242, 223)

font = pygame.font.Font(None, 36)
s_font = pygame.font.Font(None, 24)

sound_start_path = 'Sound/startup.mp3'
sound_button_click_path = 'Sound/click.mp3'
sound_alarm_path = 'Sound/alarm.mp3'

pygame.mixer.music.load(sound_start_path)
click_sound = pygame.mixer.Sound(sound_button_click_path)
alarm_sound = pygame.mixer.Sound(sound_alarm_path)

def is_falling(keypoints, threshold_angle=90, tolerance=25):
    if keypoints is None or keypoints.shape[0] < 13:
        print("Error: keypoints detected")
        return False, 90 
    
    left_shoulder = keypoints[5]
    right_shoulder = keypoints[6]
    left_hip = keypoints[11]
    right_hip = keypoints[12]

    if any(x==0 and y==0 for x, y in [left_shoulder, right_shoulder, left_hip, right_hip]):
        print("Error: keypoints are zero")
        return False, 90
    
    shoulder_mid = (left_shoulder + right_shoulder) / 2
    hip_mid = (left_hip + right_hip) / 2
    dx = hip_mid[0] - shoulder_mid[0]
    dy = hip_mid[1] - shoulder_mid[1]
    angle = abs(np.degrees(np.arctan2(dy, dx)))

    if abs(angle - threshold_angle) > tolerance:
        return True, angle
    
    return False, angle

def save_fall_log():
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    with open("fall_log.txt", "a") as log_file:
        log_file.write(f"[{timestamp}] Fall Detected!\n")

def show_log():
    with open("fall_log.txt", "r") as log_file:
        return log_file.readlines()

def get_available_cameras(max_test=5):
    available_cameras = []
    for i in range(max_test):
        cap = cv2.VideoCapture(i)
        if cap.read()[0]:
            available_cameras.append(i)
        cap.release()
    return available_cameras

def change_camera():
    global camera_index, cap
    if available_cameras:
        camera_index = (camera_index + 1) % len(available_cameras)
        cap.release() 
        cap = cv2.VideoCapture(available_cameras[camera_index])
        print(f"Switched to Camera: {camera_index}")
    
def toggle_log():
    global showing_log, log_text
    showing_log = not showing_log
    if showing_log:
        log_text = show_log()
    else:
        log_text = []

def toggle_detection():
    global detecting
    detecting = not detecting


buttons = [
    Button("Toggle Detection", 950, 100, 250, 60, ORANGE, WHITE, toggle_detection, click_sound),
    Button("Show Log", 950, 180, 250, 60, ORANGE, WHITE, toggle_log, click_sound),
    Button("Switch Camera", 950, 260, 250, 60, ORANGE, WHITE, change_camera, click_sound)
]

detecting = False
fall_detected = False
showing_log = False  
log_text = []
camera_index = 0 
bg_color = BGC
tolerance_slider = Slider(950, 340, 250, 10, 0, 180, 30)
available_cameras = get_available_cameras()
cap = cv2.VideoCapture(camera_index)
pygame.mixer.music.play(0, 0.0)

running = True
while running:
    screen.fill(bg_color)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for button in buttons:
                if button.is_clicked(event):
                    break

        tolerance_slider.handle_event(event)

    screen.blit(font.render("SETTING", True, ORANGE), (1030, 50))

    for button in buttons:
        button.draw(screen)

    ret, frame = cap.read()
    if not ret:
        continue

    tolerance = tolerance_slider.get_value()
    if detecting:
        tolerance_slider.draw(screen)
        results = model(frame, conf=0.4)
        fall_detected = False
        for result in results:
            if result.keypoints is not None:
                for keypoint in result.keypoints.xy:
                    keypoint = np.array(keypoint)
                    for x, y in keypoint:
                        cv2.circle(frame, (int(x), int(y)), 5, (0, 0, 255), -1)
                    falling, angle = is_falling(keypoint, tolerance=tolerance)
                    fall_detected = falling
                    if falling:
                        save_fall_log()
                        if not pygame.mixer.get_busy():
                            alarm_sound.play()

        if fall_detected:
            bg_color = RED
            fall_text = font.render("Fall Detected!", True, WHITE)
            screen.blit(fall_text, (600, 10))

        if not fall_detected:
            bg_color = BGC
            alarm_sound.stop()
    
    else:
        bg_color = BGC
        alarm_sound.stop()

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = np.rot90(frame) 
    frame_surface = pygame.surfarray.make_surface(frame)
    screen.blit(pygame.transform.scale(frame_surface, (800, 600)), (50, 50))

    if showing_log:
        pygame.draw.rect(screen, WHITE, (865, 360, 400, 300))
        pygame.draw.rect(screen, BLACK, (865, 360, 400, 300), 3)

    y_offset = 370
    for line in log_text[-13:]:
        log_surface = s_font.render(line.strip(), True, RED)
        screen.blit(log_surface, (885, y_offset))
        y_offset += 22

    camera_text = font.render(f"Camera: {camera_index}", True, ORANGE)
    screen.blit(camera_text, (55, 55))

    if detecting:
        screen.blit(font.render(f"Detection: {'ON' if detecting else 'OFF'}", True, GREEN if detecting else RED), (350, 55))

    pygame.display.flip()

cap.release()
pygame.quit()