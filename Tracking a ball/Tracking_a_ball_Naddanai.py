from collections import deque
from imutils.video import VideoStream
import cv2
import imutils

pts = deque(maxlen=64)
video = cv2.VideoCapture("ball_tracking_example.mp4")
while True:
	frame = video.read()
	if frame:
		frame = frame[1]  
	if frame is None:
		break

	frame = imutils.resize(frame, width=600)
	blurred = cv2.GaussianBlur(frame, (5, 5), 0)
	hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
	mask = cv2.inRange(hsv, (29, 86, 6), (64, 255, 255))
	mask = cv2.erode(mask, None, iterations=2)
	mask = cv2.dilate(mask, None, iterations=2)
	mask_copy = mask.copy()
	contour = cv2.findContours(mask_copy, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	contour = imutils.grab_contours(contour)
	center = None
	if len(contour) > 0:
		c = max(contour, key=cv2.contourArea)
		((x, y), radius) = cv2.minEnclosingCircle(c)
		M = cv2.moments(c)
		center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
		if radius:
			cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)

	pts.appendleft(center)
	for i in range(1, len(pts)):
		if pts[i - 1] is None or pts[i] is None:
			continue
		cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), 2)

	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF
	if key == ord("q"):
		break

if video:
    video.release()
else:
    video.stop()

cv2.destroyAllWindows()