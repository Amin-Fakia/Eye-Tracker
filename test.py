# import the necessary packages
import numpy as np
import argparse
import cv2
import dlib
# construct the argument parse and parse the arguments
import time


# load the image and convert it to grayscale
cap = cv2.VideoCapture("http://192.168.1.100:81/stream")
eye_detector = cv2.CascadeClassifier(r'C:\Users\sup_fakiaa\Desktop\Master\Models\haarcascade_eye.xml')

t1 = 0

def eye_aspect_ratio(eye):
    # Compute the euclidean distances between the two sets of
    # vertical eye landmarks (x, y)-coordinates
    A = np.linalg.norm(eye[1]-eye[5])
    B = np.linalg.norm(eye[2]-eye[4])

    # Compute the euclidean distance between the horizontal
    # eye landmark (x, y)-coordinates
    C = np.linalg.norm(eye[0]-eye[3])

    # Compute the eye aspect ratio
    ear = (A+B) / (2.0 * C)

    return ear
fps = cap.get(cv2.CAP_PROP_FPS)
utime = 0
while True:
    ret, image = cap.read()
    if ret:
        
        # Display the resulting frame
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        eye = eye_detector.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=0)
        if len(eyes) == 0:
            
        
            # time_no_eye +=1
            # if time_no_eye > blink_duration:
            #     eye_blinks+=1
            #     time_no_eye = 0
            
        

        #cv2.putText(image, str(eye_blinks), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        cv2.imshow('Frame', image)
        # Press Q on keyboard to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

cap.release()
cv2.destroyAllWindows()
