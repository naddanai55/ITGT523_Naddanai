import cv2

for i in range(3):
    image = cv2.imread(f'example_0{i+1}.png')
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    canny = cv2.Canny(blurred, 50, 150)
    canny = cv2.dilate(canny, (5, 5))
    contours, _ = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    sorted_contours = sorted(contours, key=cv2.contourArea, reverse=True)
    image_with_contours = image.copy()
    contour_area_threshold = 200
    obj_count = 0
    for contour in(sorted_contours[:10]): 
        cv2.drawContours(image_with_contours, [contour], -1, (0, 255, 0), 2) 
        if cv2.contourArea(contour) > contour_area_threshold:
            obj_count += 1

    print(f"Counter in example_0{i+1}:", obj_count)
    cv2.imshow(f"example_0{i+1}", image_with_contours)
    cv2.waitKey(0)
cv2.destroyAllWindows()