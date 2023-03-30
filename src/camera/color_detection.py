import cv2
import numpy as np


def main():
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        # ret will return a true value if the frame exists otherwise False
        into_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        # changing the color format from BGr to HSV
        # This will be used to create the mask
        # setting the blue lower limit
        blue_lower_limit = np.array([98, 50, 50])
        # setting the blue upper limit
        blue_upper_limit = np.array([139, 255, 255])

        blue_mask = cv2.inRange(into_hsv, blue_lower_limit, blue_upper_limit)
        # creating the mask using inRange() function
        # this will produce an image where the color of the objects
        # falling in the range will turn white and rest will be black
        blue = cv2.bitwise_and(frame, frame, mask=blue_mask)

        red_lower_limit = np.array([0, 150, 150])
        red_upper_limit = np.array([30, 255, 255])

        red_mask = cv2.inRange(into_hsv, red_lower_limit, red_upper_limit)
        red = cv2.bitwise_and(frame, frame, mask=red_mask)
        # this will give the color to mask.
        cv2.imshow('Original', frame)  # to display the original frame
        cv2.imshow('Blue Detector', blue)  # to display the blue object output
        cv2.imshow('Red Detector', red)

        if cv2.waitKey(1) == 27:
            break
        # this function will be triggered when the ESC key is pressed
        # and the while loop will terminate and so will the program

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        exit()
