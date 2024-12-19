import cv2 as cv
import numpy as np

def resize(image, size=(300, 300)):
    return cv.resize(image, size, interpolation=cv.INTER_AREA)

def gray_scale(image):
    image = cv.cvtColor(image, cv.COLOR_BGR2GRAY) 
    image = cv.cvtColor(image, cv.COLOR_GRAY2BGR)
    return image

def binary_image(image):
    image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    threshold, image = cv.threshold(image, 127, 255, cv.THRESH_BINARY)
    image = cv.cvtColor(image, cv.COLOR_GRAY2BGR)
    return image

img1 = cv.imread('Blastoise.jpg')
img2 = cv.imread('Bulbasaur.jpg')
img3 = cv.imread('Charizard.jpg')
img4 = cv.imread('Pikachu.jpg')

img1 = gray_scale(img1)  
img2 = binary_image(img2)  
img3 = gray_scale(img3)  
img4 = binary_image(img4) 

img1 = resize(img1)
img2 = resize(img2)
img3 = resize(img3)
img4 = resize(img4)
     
col1 = np.hstack((img1, img2))
col2 = np.hstack((img3, img4))
all_img = np.vstack((col1, col2))

cv.circle(all_img, (all_img.shape[1]-150, all_img.shape[0]-150), 150, (0, 0, 255), 2)
cv.imshow('2 Pokemons', all_img)
cv.waitKey(0)