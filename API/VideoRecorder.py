from libraries_import import *

## Video Capture / Image processing, potentially TODO: seperate image processing and video capture
class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)
    keypoints = pyqtSignal(tuple)
    record = False
    detector = cv2.SimpleBlobDetector_create()
    blank = np.zeros((1, 1))
    img = None
    blur = 0
    canny = 0
    rotate_index = 0
    blobs = np.zeros((240,320,3),dtype=np.uint8)
    out =  cv2.VideoWriter()
    blink_count = pyqtSignal(int)
    blinkCount = 0
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
    ellipse = ((0, 0), (0, 0), 0)
    filename="test"
    frame_width,frame_height = 0,0#
    circularity_thresh = 0
    def __init__(self) -> None:
        super(VideoThread,self).__init__()
        self._isRunning = True
        #model = load_model("./NN/eyecloseopen.h5")
        # self.lmodel =  LiteModel.from_file("./NN/model.tflite")#LiteModel.from_keras_model(model) 

    def toggleRecording(self,filename="test"):
        
        self.record = not self.record
        if self.record == True:
            self.out = cv2.VideoWriter("./data/"+ filename+ "/Video/" + filename +".avi",cv2.VideoWriter_fourcc('M','J','P','G'), 30, (self.frame_width,self.frame_height))
    def update_circularity(self,value):
        self.circularity_thresh = value
    def fitPupil(self,image):
        temp_image = image.copy()
        image_gray = cv2.cvtColor(temp_image , cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(image_gray,(3,3),0)
        ret,thresh1 = cv2.threshold(blur,70,255,cv2.THRESH_BINARY)
        opening = cv2.morphologyEx(thresh1, cv2.MORPH_OPEN, self.kernel)
        closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, self.kernel)

        temp_image  = 255 - closing
        contours, hierarchy = cv2.findContours(temp_image , cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        hull = []
        for contour in contours:
            area = cv2.contourArea(contour)
            perimeter = cv2.arcLength(contour, True)
            circularity = 4 * np.pi * (area / (perimeter * perimeter))

            
            if circularity > self.circularity_thresh:
                hull.append(cv2.convexHull(contour, False))
        # for i in range(len(contours)):
        #     hull.append(cv2.convexHull(contours[i], False))
        cnt = sorted(hull, key=cv2.contourArea)
        return cnt
        
    def process_canny(self, img,thresh_value):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(gray, thresh_value,255,0)
        contours,_ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        # cnt = contours[1]
        # ellipse = cv2.fitEllipse(cnt)

        cv2.drawContours(img, contours, -1, (0, 255, 0), 3)

    

    def run(self):
        # capture from web cam
        #file_path = "C:/Users/ameen/Desktop/Git_Master/Master/Software Eyetracker/outpy.avi"
    
        cap = cv2.VideoCapture("http://192.168.1.100:81/stream")
        #keyPoints_temp = cv2.KeyPoint()
        
        if not cap.isOpened():
            print("Error opening video stream or file")
            self.stop()
        self.frame_width = int(cap.get(3))
        self.frame_height = int(cap.get(4))
        
         # fourcc, cv2.VideoWriter_fourcc('M','J','P','G')
        idx = 0
        while self._isRunning:
            ret, self.img = cap.read()
            
            if self.record:
                self.out.write(self.img)
            
            
            
            if ret:
                #new_frame_time = time.time()
                #self.img = cv2.rotate(self.img, cv2.ROTATE_90_COUNTERCLOCKWISE)
                # if self.rotate_index:
                self.img = self.img[:,0:200]
                #self.img = cv2.resize(self.img,(500,500))

                
                if not ret:
                    break
                for _ in range(self.rotate_index):
                    self.img = cv2.rotate(self.img, cv2.ROTATE_90_COUNTERCLOCKWISE)

                
                        #self.img = cv2.Canny(self.img, self.canny, self.canny*2)    
                
                if self.blur:
                    self.img= cv2.GaussianBlur(self.img,(6*self.blur+1,6*self.blur+1),0)
                
                # Neural Network Approach # 
                # resized = np.expand_dims(cv2.resize(self.img,(256,256))/255,0)
                
                # try:
                #     yhat = self.lmodel.predict(resized)[0][0]
                #     if yhat < 0.1:
                #         self.blinkCount+=1
                #         # idx +=1
                #         # if idx >9:
                #         #     self.blinkCount-=1
                #         # if idx >50:
                #         #     idx=0
                # except: pass

                try:
                    if self.canny:
                        self.img = self.process_canny(self.img,self.canny)
                except: pass


                # Pupil Detection using Blob Detector #

                # keyPoints = self.detector.detect(self.img)
              
                # if keyPoints:
                #     keyPoints_temp = keyPoints
                #     self.blobs = cv2.drawKeypoints(self.img, keyPoints, self.blank, (255, 0, 255),
                #                     cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
                #     cv2.line(self.blobs,(int(keyPoints[0].pt[0]),0),(int(keyPoints[0].pt[0]),int(self.img.shape[0])),(255,255,255),1)
                #     cv2.line(self.blobs,(0,int(keyPoints[0].pt[1])),(int(self.img.shape[1]),int(keyPoints[0].pt[1])),(255,255,255),1)
                # else:
                #     try:
                #         self.blobs = cv2.drawKeypoints(self.img, keyPoints_temp, self.blank, (255, 0, 255),
                #                         cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
                #         cv2.line(self.blobs,(int(keyPoints_temp[0].pt[0]),0),(int(keyPoints_temp[0].pt[0]),int(self.img.shape[0])),(255,255,255),1)
                #         cv2.line(self.blobs,(0,int(keyPoints_temp[0].pt[1])),(int(self.img.shape[1]),int(keyPoints_temp[0].pt[1])),(255,255,255),1)
                #     except: pass
                # print(keyPoints)

                # Track FPS #
                # try:
                    
                #     fps = 1/(new_frame_time-prev_frame_time)
                    
                # except: pass


                processed_img = self.img.copy()
                cnt = self.fitPupil(processed_img)

                if cnt:
                    maxcnt = cnt[-1]
                    try:
                        self.ellipse = cv2.fitEllipse(maxcnt)
                        cv2.ellipse(processed_img,self.ellipse,(0,255,0),1)
                        cv2.circle(processed_img,tuple(map(int,self.ellipse[0])),1,(255,255,0),1)
                    except:
                        pass

                ## Simple Frame Counter to detect blinks
                else:
                    idx+=1
                    if idx>2:
                        self.blinkCount+=1
                        idx=0
                

                
                #self.change_pixmap_signal.emit(processed_img)
                self.change_pixmap_signal.emit(processed_img)
                self.keypoints.emit(self.ellipse)
                self.blink_count.emit(self.blinkCount)
                # prev_frame_time = new_frame_time
                # fps = str(int(fps))
                # cv2.putText(self.blobs, fps, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255,0),1,cv2.LINE_AA)
                
                #time.sleep(1/60)
                #self.rotate = False
    def update_detector(self,params):
        self.detector = cv2.SimpleBlobDetector_create(parameters=params)
    def set_blur(self,blur):
        self.blur = blur
    def set_canny(self,canny):
        self.canny = canny
    def set_rotate(self):
        self.rotate_index += 1
        if self.rotate_index == 4:
            self.rotate_index = 0
    def stop(self):
        print("Stopping VideoThread")
        self.quit()
        self.out.close()
        self._isRunning = False