import cv2
import numpy as np

# Read the image file
img = cv2.imread("image.jpg")

# Convert BGR to HSV
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# Define range of red color in HSV
lower_red = np.array([0, 50, 50])
upper_red = np.array([10, 255, 255])
mask1 = cv2.inRange(hsv, lower_red, upper_red)

lower_red = np.array([170, 50, 50])
upper_red = np.array([180, 255, 255])
mask2 = cv2.inRange(hsv, lower_red, upper_red)


# Combine the masks
mask = cv2.bitwise_or(mask1, mask2)

# Find contours
contours, hierarchy = cv2.findContours(
    mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Find the largest contour and its centroid
if len(contours) > 0:
    largest_contour = max(contours, key=cv2.contourArea)
    M = cv2.moments(largest_contour)
    if M['m00'] != 0:
        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])
        # Draw a circle at the centroid
        cv2.circle(img, (cx, cy), 7, (255, 255, 255), -1)
        cv2.imshow('Centroid', img)
        cv2.waitKey(0)

cv2.destroyAllWindows()
