import cv2
import numpy as np

kernel = np.ones((5,5), np.uint8)
img = cv2.imread('example_01.png')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (19, 19), 0)
_, binary = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)

canny = cv2.Canny(binary, threshold1=100, threshold2=200)

# edged = cv2.Canny(blurred, 50, 100)
# edged = cv2.dilate(edged, None, iterations=1)
# edged = cv2.erode(edged, None, iterations=1)

# kernel = np.ones((7,7), np.uint8)

# _, binary = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)

# dilated = cv2.dilate(binary, kernel, iterations=1)

# kernel = np.ones((5,5), np.uint8)
# Perform dilation
# dilation = cv2.dilate(binary, kernel, iterations=1)
# erosion = cv2.erode(binary, kernel, iterations=1)
# opening = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)
# closing = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)

contours, hierarchy = cv2.findContours(canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
result = img.copy()

# cv2.imshow('Original', binary)
# cv2.imshow('Dilation', dilation)
# cv2.imshow('Erosion', erosion)
# cv2.imshow('Opening', opening)
# cv2.imshow('Closing', closing)

# print(hierarchy.shape)

cv2.drawContours(result, contours, -1, (0, 255, 0), 2)

# cv2.imshow('gray', gray)
# cv2.imshow('blurred', blurred)
# cv2.imshow('canny', canny)
cv2.imshow('canny', canny)

# cv2.imshow('dilated', dilated)

cv2.imshow('Contours', result)
# cv2.imshow('Dilation', dilation)
object_count = len(contours)
print(object_count)

cv2.waitKey(0)
cv2.destroyAllWindows()