import cv2

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

def draw_rect(faces, img, color=(0, 255, 0)):
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), color, 3)


img = cv2.imread('bg.png')

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
faces = face_cascade.detectMultiScale(gray, 1.1, 3)
eyes = eye_cascade.detectMultiScale(gray, 1.1, 3)

draw_rect(faces, img)
draw_rect(eyes, img, (255, 0, 0))    
cv2.imshow('Face', img)     

cv2.waitKey(0)
cv2.destroyAllWindows()