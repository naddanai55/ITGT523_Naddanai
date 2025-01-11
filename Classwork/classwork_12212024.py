import cv2 as cv
import numpy as np

# offset = 0

# def nothing(x):
#     pass

# def resize(image, size=(500, 500)):
#     return cv.resize(image, size, interpolation=cv.INTER_AREA)

# cv.namedWindow('image')
# cv.createTrackbar('offset', 'image', 0, 255, nothing)

# img = cv.imread('Pikachu.jpg')
# img = cv.cvtColor(img, cv.COLOR_BGR2HSV)

# while True:
#     img_hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

#     offset = cv.getTrackbarPos("offset", "image")
#     for row in range (0, img_hsv.shape[0]):
#         for colom in range(0, img_hsv.shape[1]):
#             img[row][colom] =  img_hsv[row][colom] + offset

#     img_final = cv.cvtColor(img_hsv, cv.COLOR_HSV2BGR)

#     img_final = resize(img_final)
#     cv.imshow('image', img_final)
#     if cv.waitKey(1) & 0xFF == 27:
#         break

# cv.destroyAllWindows()
test = np.array([[0, 0, 0, 0, 0, 0, 0],
                  [0, 3, 1, 2, 0, 1, 0], 
                  [0, 0, 1, 3, 2, 0, 0], 
                  [0, 1, 2, 1, 0, 2, 0], 
                  [0, 2, 1, 0, 1, 3, 0], 
                  [0, 1, 0, 1, 2, 1, 0], 
                  [0, 0, 0, 0, 0, 0, 0]])


a = np.array([[0, 0, 0,], [0, 3, 1], [0, 0, 1]])
b = np.array([[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]])
c = np.vdot(a, b)
print(c)
print(test*c)

# for i in test:
#     ans = np.append(test[i])

# print(ans)