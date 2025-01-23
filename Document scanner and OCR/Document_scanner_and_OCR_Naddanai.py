import cv2
import argparse
from transformation import four_point_transform
import pytesseract

parser = argparse.ArgumentParser(description='Scan a document from an image.')
parser.add_argument("-i", "--image", required=True, help="Path to the image to be scanned")
args = parser.parse_args()

img = cv2.imread(args.image)
if img is None:
    raise ValueError("Could not read the image.")

origin = img.copy()
ratio = img.shape[0] / 500
img = cv2.resize(img, (0, 0), fx=500/img.shape[0], fy=500/img.shape[0])

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (5, 5), 0)
edged = cv2.Canny(blur, 75, 200)
contours, _ = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
contours = sorted(contours, key = cv2.contourArea, reverse = True)[:5]

screenCnt = None
for c in contours :
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.02 * peri, True)
    if len(approx) == 4:
        screenCnt = approx
        break

cv2.drawContours(img, [screenCnt], -1, (0, 255, 0), 2)
warped = four_point_transform(origin, screenCnt.reshape(4, 2) * ratio)
warped_gray = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
thresh = cv2.adaptiveThreshold(warped_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 10)
text = pytesseract.image_to_string(cv2.cvtColor(thresh, cv2.COLOR_BGR2RGB), config="--psm 4")

print("----------------------------------------")
print()
print(text)
print()
print("----------------------------------------")

cv2.imshow("Scanned", cv2.resize(thresh, (0, 0), fx=500/thresh.shape[0], fy=500/thresh.shape[0]))
cv2.waitKey(0)
cv2.destroyAllWindows()