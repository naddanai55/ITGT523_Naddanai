# import numpy as np
# import cv2 as cv

# # Kernel
# kernel_x = np.array([[-1, 1, 1],
#                    [-1, 0, 1],
#                    [-1, 0, -1]])

# kernel_y = np.array([[1, 1, 1],
#                    [0, 0, 0],
#                    [1, 1, 1]])
# # small blur
# # kernel = np.array([[1/9, 1/9, 1/9],
# #                    [1/9, 1/9, 1/9],
# #                    [1/9, 1/9, 1/9]])

# # cool!
# # kernel = np.array([[1/25, 1/25, 1/25, 1/25, 1/25],
# #                    [1/25, 1/25, 1/25, 1/25, 1/25],
# #                    [1/25, 1/25, 1/25, 1/25, 1/25],
# #                    [1/25, 1/25, 1/25, 1/25, 1/25],
# #                    [1/25, 1/25, 1/25, 1/25, 1/25]])

# def convolve(image, kernel):
#     h, w = image.shape
#     kh, kw = kernel.shape

#     pad = kh // 2
#     padded_image = np.pad(image, pad_width= pad, mode="constant", constant_values = 0)
#     output = np.zeros_like(image)

#     for i in range(h):
#         for j in range(w):
#             region = padded_image[i:i+kh, j:j+kw]
#             output[i, j] = np.sum(region * kernel)

#     return output

# image = cv.imread("naipic.JPG")
# gray_image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
# # cv.imshow("gray", gray_image)

# conv_img_x = convolve(gray_image, kernel=kernel_x)
# cv.imshow("conv_x", conv_img_x)

# conv_img_y = convolve(gray_image, kernel=kernel_y)
# cv.imshow("conv_y", conv_img_y)

# combind_img = cv.magnitude(conv_img_x.astype(np.float64), conv_img_y.astype(np.float64))
# cv.imshow("combind", cv.convertScaleAbs(combind_img))


# cv.waitKey(0)
# cv.destroyAllWindows()

import cv2
import numpy as np
# Read image
img = cv2.imread('naipic.jpg')
# Convert to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# Apply Gaussian blur to reduce noise
blurred = cv2.GaussianBlur(gray, (19, 19), 0)
# Apply different edge detection methods
# Sobel
sobelx = cv2.Sobel(blurred, cv2.CV_64F, 1, 0, ksize=3)
sobely = cv2.Sobel(blurred, cv2.CV_64F, 0, 1, ksize=3)
sobel_combined = cv2.magnitude(sobelx, sobely)
# Canny
canny = cv2.Canny(blurred, threshold1=100, threshold2=200)
# Laplacian
laplacian = cv2.Laplacian(blurred, cv2.CV_64F)
# Convert to uint8 and normalize for display
sobel_combined = np.uint8(np.absolute(sobel_combined))
laplacian = np.uint8(np.absolute(laplacian))

_, binary = cv2.threshold(blurred, 127, 255, cv2.THRESH_BINARY)

_, binary_2 = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

# Find contours
contours_1, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
# Create copy of original image for drawing

contours_2, hierarchy = cv2.findContours(binary_2, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)


# Define kernel for morphological operations
kernel = np.ones((5,5), np.uint8)
# Perform dilation
dilation = cv2.dilate(binary, kernel, iterations=1)
# Perform erosion
erosion = cv2.erode(binary, kernel, iterations=1)

# Perform opening (erosion followed by dilation)
opening = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)
# Perform closing (dilation followed by erosion)
closing = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
# Display results



result_1 = img.copy()
result_2 = img.copy()

cv2.drawContours(result_1, contours_1, -1, (0, 255, 0), 2)
cv2.drawContours(result_2, contours_2, -1, (0, 255, 0), 2)

print()
print(len(contours_1))
print()
print(len(contours_2))
print()

# anime = canny.copy()
# Display results
# cv2.imshow('Original', img)
# cv2.imshow('blurred', blurred)
# cv2.imshow('Sobel', sobel_combined)
# cv2.imshow('Canny', canny)
cv2.imshow('Contours1', result_1)
cv2.imshow('Contours2', result_2)

# cv2.imshow('Original', binary)
# cv2.imshow('Dilation', dilation)
# cv2.imshow('Erosion', erosion)
cv2.imshow('Opening', opening) 
# cv2.imshow('Closing', closing)

# cv2.imshow()

# cv2.imshow('Laplacian', laplacian)


cv2.waitKey(0)
cv2.destroyAllWindows()