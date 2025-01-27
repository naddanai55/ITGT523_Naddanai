import cv2
import argparse


face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

def draw_rect(faces, img, color=(0, 255, 0)):
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), color, 2)

parser = argparse.ArgumentParser(description='Scan a document from an image.')
parser.add_argument("-i", "--image", required=True, help="Path to the image to be scanned")
args = parser.parse_args()

img = cv2.imread(args.image)
if img is None:
    raise ValueError("Could not read the image.")

card_img = cv2.imread('bg.png')

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
faces = face_cascade.detectMultiScale(gray, 1.1, 3)
eyes = eye_cascade.detectMultiScale(gray, 1.1, 3)
img2 = img.copy()
draw_rect(faces, img)
draw_rect(eyes, img, (255, 0, 0))

img2 = cv2.getRectSubPix(img2, (faces[0][2], faces[0][3]), (faces[0][0]+faces[0][2]/2, faces[0][1]+faces[0][3]/2))
img2 = cv2.resize(img2, (0, 0), fx=200/img2.shape[0], fy=200/img2.shape[0])

x_offset = -300
y_offset = 260
x_end = x_offset + img2.shape[1]
y_end = y_offset + img2.shape[0]

card_img[y_offset:y_end, x_offset:x_end] = img2

cv2.imshow('img', cv2.resize(img, (0, 0), fx=0.5, fy=0.5))
cv2.imshow('card', card_img)

cv2.waitKey(0)
cv2.destroyAllWindows()