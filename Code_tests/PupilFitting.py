import cv2
import numpy as np
import matplotlib.pyplot as plt
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))

def fitPupil(image,kernel):
        temp_image = image.copy()
        image_gray = cv2.cvtColor(temp_image , cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(image_gray,(5,5),3)
        ret,thresh1 = cv2.threshold(blur,60,255,cv2.THRESH_BINARY)
        opening = cv2.morphologyEx(thresh1, cv2.MORPH_OPEN, kernel)
        closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)

        temp_image  = 255 - closing
        contours, hierarchy = cv2.findContours(temp_image , cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        hull = []
        for contour in contours:
            area = cv2.contourArea(contour)
            perimeter = cv2.arcLength(contour, True)
            circularity = 4 * np.pi * (area / (perimeter * perimeter))

            circularity_thresh = 0.0
            if circularity > circularity_thresh:
                hull.append(cv2.convexHull(contour, False))
        # for i in range(len(contours)):
        #     hull.append(cv2.convexHull(contours[i], False))
        cnt = sorted(hull, key=cv2.contourArea)
        
        if cnt :
                maxcnt = cnt[-1]
                cv2.drawContours(image,cnt,0,(0,255,0),2)
                
                
                try:
            
                        ellipse = cv2.fitEllipse(maxcnt)
                        # cv2.ellipse(image,ellipse,(0,255,0),1)
                        
                        # cv2.circle(image,(int(ellipse[0][0]),int(ellipse[0][1])),1,(0,0,255),2)#
                        
                                
                        #ellipse = cv2.fitEllipse(maxcnt)
                        #cv2.ellipse(frame,ellipse,(0,255,0),1)
                except: pass
        
        return cnt

cap = cv2.VideoCapture("http://192.168.1.100:81/stream")
while True:
      ret, frame = cap.read()
    #   frame = frame[:100,:100]
       
      orig_frame = frame.copy()

      #gray = cv2.cvtColor(orig_frame, cv2.COLOR_BGR2GRAY)
      blurred = cv2.GaussianBlur(orig_frame, (7, 7), 2)


      # thresh = cv2.adaptiveThreshold(blurred, 255,
	    # cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 21, 5)
      # cv2.imshow("Mean Adaptive Thresholding", thresh)

      hist = cv2.calcHist([blurred], [0], None, [256], [0, 256])

      pdf = hist / np.sum(hist)
      cdf = np.cumsum(hist)
      cdf_normalized = cdf / np.sum(cdf)
      inverse_cdf = 1 - cdf_normalized

      #plt.cla()
      # plt.plot(pdf)
      # plt.xlabel('Pixel Intensity')
      # plt.ylabel('Probability Density')
      # plt.title('PDF of Image')
      # plt.ylim((0,.3))

      # cdf
      #plt.plot(cdf_normalized)
#       plt.plot(inverse_cdf)
#       plt.xlabel('Pixel Intensity')
#       plt.ylabel('Cumulative Probability')
#       plt.title('CDF of Image')
#       plt.pause(0.04)


      


      #cv2.imwrite("test.png",orig_frame)
      cnt_blur = fitPupil(blurred,kernel)
      cnt = fitPupil(frame,kernel)

      vis = np.concatenate((blurred,frame), axis=1)

      cv2.imshow("vis",vis)

      if cv2.waitKey(1) == ord('q'):
            break
cap.release()
cv2.destroyAllWindows()

