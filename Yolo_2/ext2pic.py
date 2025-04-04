import cv2 
import os 

cam = cv2.VideoCapture("ragnarok.mp4") 

try: 
	if not os.path.exists('data'): 
		os.makedirs('data') 

except OSError: 
	print ('Error: Creating directory of data') 

currentframe = 0
ret = True
while(ret):
	currentframe += 1
	ret,frame = cam.read()
	if ret and currentframe % 60 == 0:
		name = './data/frame' + str(currentframe) + '.jpg'
		print ('Creating...' + name) 
		cv2.imwrite(name, frame) 

cam.release() 
cv2.destroyAllWindows() 
