import cv2

image = cv2.imread('images/aux_5_00037.png', cv2.IMREAD_GRAYSCALE)

threshold_value = 15

ret, thresh = cv2.threshold(image, threshold_value, 255, cv2.THRESH_BINARY_INV)

contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

result_image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
cv2.drawContours(result_image, contours, -1, (0, 255, 0), 2)

cv2.imshow('Dark Areas', result_image)
cv2.waitKey(0)
cv2.destroyAllWindows()