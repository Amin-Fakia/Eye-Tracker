import cv2
import numpy as np
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
def fitPupil(image,kernel):
        temp_image = image.copy()
        image_gray = cv2.cvtColor(temp_image , cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(image_gray,(7,7),7)
        ret,thresh1 = cv2.threshold(blur,70,255,cv2.THRESH_BINARY)
        opening = cv2.morphologyEx(thresh1, cv2.MORPH_OPEN, kernel)
        closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)

        temp_image  = 255 - closing
        contours, hierarchy = cv2.findContours(temp_image , cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        hull = []
        for contour in contours:
            area = cv2.contourArea(contour)
            perimeter = cv2.arcLength(contour, True)
            circularity = 4 * np.pi * (area / (perimeter * perimeter))

            circularity_thresh = 0.8
            if circularity > circularity_thresh:
                hull.append(cv2.convexHull(contour, False))
        # for i in range(len(contours)):
        #     hull.append(cv2.convexHull(contours[i], False))
        cnt = sorted(hull, key=cv2.contourArea)
        
        return cnt


cap = cv2.VideoCapture("outpy.avi")
while True:
      ret, frame = cap.read()
    #   frame = frame[:100,:100]
       
      orig_frame = frame.copy()
      cv2.imwrite("test.png",orig_frame)
      cnt = fitPupil(frame,kernel)
 
      if cnt:
        maxcnt = cnt[-1]
        try:
            ellipse = cv2.fitEllipse(maxcnt)
            cv2.ellipse(frame,ellipse,(0,255,0),1)
        except: pass
    

      cv2.imshow('Grayscale Video', frame)
      cv2.imshow('orig', orig_frame)


      if cv2.waitKey(500) == ord('q'):
            break
cap.release()
cv2.destroyAllWindows()

