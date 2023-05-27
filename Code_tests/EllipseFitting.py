import cv2

filepath = "test.avi"
streampath = "http://192.168.1.100:81/stream"
cap = cv2.VideoCapture(streampath)
if not cap.isOpened():
  raise Exception("Couldn't open camera {}".format("test"))
_,image = cap.read()
# frame_width = int(cap.get(3))
# frame_height = int(cap.get(4))
# size = (frame_width, frame_height)
# result = cv2.VideoWriter('test.avi', 
#                          cv2.VideoWriter_fourcc(*'MJPG'),
#                          30, size)
alpha = 1.5 # Contrast control
beta = 10 # Brightness control
thresh_val = 100
def on_change(value):
    global thresh_val
    thresh_val = value

def alpha_change(value):
    global alpha
    alpha = value

def beta_change(value):
    global beta
    beta = value

cv2.imshow("image", image)

cv2.createTrackbar('slider', "image", 0, 255, on_change)
cv2.createTrackbar('alpha', "image", 0, 3, alpha_change)
cv2.createTrackbar('beta', "image", 0, 100, beta_change)
detector = cv2.SimpleBlobDetector_create()
while True:
    success,image = cap.read()
    image = cv2.rotate(image,cv2.ROTATE_90_COUNTERCLOCKWISE)
    
    
    image = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)
    if success:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        gray = cv2.GaussianBlur(gray, (15, 15), 0)
        
        ret,thresh = cv2.threshold(gray,thresh_val,255,0)

        contours,hierarchy = cv2.findContours(thresh, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

        #äcnt = contours[2]
        try:
           # ellipse = cv2.fitEllipse(cnt)
            
            for cnt in contours:


                ellipse = cv2.fitEllipse(cnt)

                #print(ellipse)

                cv2.ellipse(image,ellipse, (0,0,255), 1)
        except: pass

        cv2.imshow("Ellipse", thresh)
        cv2.imshow("image",image)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break
cap.release()

cv2.destroyAllWindows()
