from libraries_import import *
from TableView import TableView
from VideoRecorder import VideoThread
from MicrophoneRecorder import MicrophoneRecorder
from SerialReceiver import SerielReceiver


# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    filepath = "/data/"
    def range_box(self,box_name=None,label1=None,label2=None,label1_value=(0,100),label2_value=(0,100),active=True):
        Layout = QVBoxLayout()
        Box = QGroupBox()
        Box.setTitle(box_name)
        Box.setLayout(Layout)
        Box.setCheckable(active)
        Layout.addWidget(QLabel(label1))
        valueMin = QSpinBox()
        valueMin.setRange(label1_value[0],label1_value[1])
        Layout.addWidget(valueMin)
        Layout.addWidget(QLabel(label2))
        valueMax = QSpinBox()
        valueMax.setRange(label2_value[0],label2_value[1])
        Layout.addWidget(valueMax)

        return Box
    
    def range_dial(self,dial_name=None,label_value=(0,100)):
        Layout = QVBoxLayout()
        Box = QGroupBox()
        Box.setTitle(dial_name)
        Box.setLayout(Layout)
        Box.setCheckable(True)
        
        dial = QDial()
        dial.setRange(label_value[0],label_value[1])
     
        Layout.addWidget(dial)
        range_dial_label = QLabel()
        range_dial_label.setText(f"Value : "+ str(dial.value()))
        dial.valueChanged.connect(lambda: self.update(dial.value(),range_dial_label))
        Layout.addWidget(range_dial_label)
        
        return Box


    def update(self, value,label):
        label.setText(f'Value : {value}')
        
    def playTick(self):
        self.time = self.time.addSecs(1)
        self.timeLabel.setText("Recording Time : " + self.time.toString("hh:mm:ss"))
        

    @pyqtSlot(tuple)
    def saveData(self,data):
        # lock = threading.Lock()
        # while self.isRecording:
        #     # with lock:

        with open("./data/"+self.patientInput.text()+"/"+self.patientInput.text()+"_"+self.filename,'a+') as f:
            writer = csv.DictWriter(f,fieldnames=["Pupil Diameter (relative)","time","XY-Position","Heart Rate (BPM)","Blinks"],delimiter=",",lineterminator="\n")
            #[d.size for d in data], next(iter([d.size for d in data]), "None")
            data_object = {"time":datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                           "Pupil Diameter (relative)":[self.pupil_radius_],
                           "XY-Position": data[0],
                           "Heart Rate (BPM)": self.pulse_data[-1],
                           "Blinks": self.blink_count,
                           }
            if f.tell() == 0:
                writer.writeheader()
                print("file doesnt exist, creating file with name: " + self.filename)
            writer.writerow(data_object)




    def createFolder(self):
        self.folder_path = f'./data/{self.patientInput.text()}'
        if not os.path.exists(self.folder_path):
            os.mkdir(self.folder_path)
            os.mkdir(self.folder_path+"/Audio")
            os.mkdir(self.folder_path+"/Video")
                


    def play(self):
        # now = datetime.datetime.now()
        # self.time = QTime(now.hour,now.minute,now.second)
        self.timeLabel.setText("Recording Time : " + self.time.toString("hh:mm:ss"))
        self.createFolder()
        self.isRecording = True

        self.audioThread.start_recording()
        self.audioThread.voice_data.connect(self.update_voice_recorder)
        

        self.videoThread.keypoints.connect(self.saveData)
        self.videoThread.toggleRecording(self.patientInput.text())
        

        self.playTimer.start(1000)
        self.playBtn.setDisabled(True)
        self.stopBtn.setEnabled(True)
    def stop(self):
        self.playTimer.stop()
        self.videoThread.toggleRecording(self.patientInput.text())
        self.videoThread.keypoints.disconnect(self.saveData)
        self.audioThread.voice_data.disconnect(self.update_voice_recorder)
        
        self.audioThread.stop_recording()
        self.audioThread.save_file(filename=self.patientInput.text())
        self.timeLabel.setText("Recording Time : " + self.time.toString("hh:mm:ss"))
        self.time = QTime(0,0,0)
        #print("Stopped at : " + self.time.toString("hh:mm:ss"))
        self.playBtn.setDisabled(False)
        self.stopBtn.setDisabled(True)
        # self.popUp = MyPopup()
        # self.popUp.setGeometry(QRect(100, 100, 300, 100))
        # self.popUp.show()
    
    def apply_params(self):
        params = cv2.SimpleBlobDetector_Params()
        params.filterByArea = self.area_box.isChecked()
        params.minArea = int(self.area_box.children()[2].value())
        params.maxArea = int(self.area_box.children()[4].value())

        params.filterByCircularity = self.circul_dial.isChecked()
        params.minCircularity = self.circul_dial.children()[1].value()/100


        params.filterByConvexity = self.convex_dial.isChecked()
        params.minConvexity=self.convex_dial.children()[1].value()/100

        params.filterByInertia = self.inertia_dial.isChecked()
        params.minInertiaRatio = self.inertia_dial.children()[1].value()/100

        params.minThreshold = int(self.threshold_box.children()[2].value())
        params.maxThreshold = int(self.threshold_box.children()[4].value())

        self.videoThread.update_detector(params)
        # self.thread.blur = True
        # self.thread.kernel_size = (11,11)


        #self.detector = cv2.SimpleBlobDetector_create(parameters=params)
    def initialize_gui(self):
        self.area_box.setChecked(True)
        self.area_box.children()[2].setValue(500)
        self.area_box.children()[4].setValue(5000)
        self.threshold_box.children()[4].setValue(120)
        self.threshold_box.children()[2].setValue(0)
        self.circul_dial.children()[1].setValue(25)
        self.convex_dial.setChecked(False)
        self.inertia_dial.setChecked(False)

        self.apply_params()
        

    def __init__(self):
        super().__init__()
        #self.detector = cv2.SimpleBlobDetector_create()
        self.threadpool = QThreadPool()
        print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())
        self.videoThread = VideoThread()
        self.audioThread = MicrophoneRecorder(12000)
        self.serielThread = SerielReceiver(com_port="COM7")

        self.data = {}
        self.tableView = TableView(self.data)
        self.filename = f"data_{datetime.datetime.now().year}_{datetime.datetime.now().month}_{datetime.datetime.now().day}.csv"
        self.setWindowTitle("Eye Tracker")
        self.setWindowIcon(QIcon("./Icons/Eye_Tracker_Icon.png"))
        self.setMinimumWidth(1200)
        self.setMinimumHeight(700)
        self.playTimer = QTimer()
        
        self.time = QTime(0,0,0)
        self.playTimer.timeout.connect(self.playTick)


        self.mainLayout = QGridLayout()

      
        self.blink_count = 0

        tabs = QTabWidget()
        tabs.setMaximumHeight(300)

        slider1 =  QSlider()

        
        controlFrame = QFrame()
        controlLayout = QHBoxLayout()
        self.area_box =self.range_box("Area","Minimum Area: ","Maximum Area:",(1,10000),(1,10000)) # [2].value()
        
        self.threshold_box =self.range_box("Threshold","Minimum Threshold: ","Maximum Threshold:",(0,255),(0,255),False)
        self.circul_dial = self.range_dial("Circularity",(1,100))
        self.convex_dial = self.range_dial("Convexity",(1,100))
        self.inertia_dial = self.range_dial("Inertia",(1,100))



        controlLayout.addWidget(self.area_box)
        controlLayout.addWidget(self.threshold_box)
        controlLayout.addWidget(self.circul_dial)
        controlLayout.addWidget(self.convex_dial)
        controlLayout.addWidget(self.inertia_dial)
        #controlLayout.addWidget()
        
        controlFrame.setLayout(controlLayout)
       
        # btn1.clicked.connect(run_camThread)
        imageProcessingLayout = QGridLayout()
        imageProcessingFrame = QFrame()
        imageProcessingFrame.setLayout(imageProcessingLayout)

        blurLabel = QLabel("Blur : ")
        
        blurSlider = QSlider()
        blurSlider.setMinimum(0)
        blurSlider.setMaximum(20)
        blurSlider.setTickInterval(2)
        blurSlider.setOrientation(Qt.Horizontal)
        blurSlider.setSingleStep(2)

        
       

        blurSlider.valueChanged.connect(self.videoThread.set_blur)
        
        imageProcessingLayout.addWidget(blurLabel,0,0)
        imageProcessingLayout.addWidget(blurSlider,0,1)

        rotateBtn = QPushButton("Rotate")
        rotateBtn.setMaximumWidth(100)
        rotateBtn.clicked.connect(self.videoThread.set_rotate)
        

        contourSlider = QSlider()
        contourSlider.setMinimum(0)
        contourSlider.setMaximum(255)
        contourSlider.setTickInterval(1) 

        contourSlider.setOrientation(Qt.Horizontal)

        contourSlider.valueChanged.connect(self.videoThread.set_canny)

        contourLabel = QLabel("Contour : ")
    

        imageProcessingFrame.layout().addWidget(contourLabel,1,0)
        imageProcessingLayout.addWidget(contourSlider,1,1)
        imageProcessingLayout.addWidget(rotateBtn,2,0)
        

        pg.setConfigOption('background', 'w')
        self.scatter_graph = pg.PlotWidget()
        #self.plot = self.graph.plot()
        self.scatter = pg.ScatterPlotItem(pen=pg.mkPen(width=5, color='r'), symbol='o', size=25)
        self.scatter_graph.addItem(self.scatter)
        self.scatter_graph.setXRange(50,200)
        self.scatter_graph.setYRange(50,300)

        self.graph = pg.PlotWidget(axisItems={'bottom': pg.DateAxisItem()})
        self.graph.showGrid(x=True, y=True)
        self.plot = self.graph.plot(pen="k")
        self.graph.setYRange(0, 2, padding=0)

        self.voice_recorder_graph = pg.PlotWidget(axisItems={'bottom': pg.DateAxisItem()})
        self.voice_recorder_graph.showGrid(x=True, y=True)
        self.voice_recorder = self.voice_recorder_graph.plot(pen="b")

        ## TODO: change axis item to string
        self.pulse_graph_widget = pg.PlotWidget(axisItems={'bottom': pg.DateAxisItem()})
        self.pulse_graph_widget.showGrid(x=True, y=True)
        self.pulse_graph = self.pulse_graph_widget.plot(pen="b")
        
        self.time_stamps = []


        tabs.addTab(controlFrame, "Blob Detection Parameters")
        tabs.addTab(self.graph, "Pupil Diameter Plot")
        tabs.addTab(self.scatter_graph, "Pupil Position Plot")
        tabs.addTab(imageProcessingFrame, "Image Processing")
        tabs.addTab(self.voice_recorder_graph, "Voice Recorder Plot")
        tabs.addTab(self.pulse_graph_widget, "Pulse Plot")

        self.image_1_label = QLabel()
        # change
        self.image_1_label.setScaledContents(False)
        #self.image_2_label = QLabel()



        self.mainLayout.addWidget(self.image_1_label, 0, 0)
        #self.mainLayout.addWidget(self.image_2_label, 0, 1)

        
        ## Input Frame
        analysisLayout = QVBoxLayout()
        mediaLayout = QHBoxLayout()

        analysisFrame = QWidget()

        inputBox = QHBoxLayout()
        patientLabel = QLabel("Patient Identification Number: ")
        self.patientInput = QLineEdit()

        inputBox.addWidget(patientLabel)
        inputBox.addWidget(self.patientInput)


        inputFrame = QFrame()
        inputFrame.setLayout(inputBox)

        
        analysisLayout.addWidget(inputFrame)

        
        analysisFrame.setMinimumWidth(250)
        analysisFrame.setMaximumWidth(600)
        analysisFrame.setLayout(analysisLayout)
        
        recordBox = QGroupBox()
        recordBox.setFixedHeight(100)
        recordBox.setTitle("Record")
        recordBox.setLayout(mediaLayout)

        analysisLayout.addWidget(recordBox)
        self.playBtn = QPushButton("Start Recording")
        self.playBtn.setIcon(QIcon("./Icons/Play.png"))
        self.playBtn.clicked.connect(self.play)
        self.stopBtn = QPushButton("Stop Recording")
        self.stopBtn.setDisabled(True)
        self.stopBtn.clicked.connect(self.stop)
        self.stopBtn.setIcon(QIcon("./Icons/Stop.png"))

        calibrateBtn = QPushButton("Calibrate")

        calibrateBtn.clicked.connect(self.calibrate)



        # applyParamsBtn = QPushButton("Apply Parameters")
        # applyParamsBtn.clicked.connect(self.apply_params)

        self.timeLabel = QLabel("Recording Time : ")
        self.timeLabel.setFixedHeight(50)
        analysisLayout.addWidget(self.timeLabel)

         
        mediaLayout.addWidget(self.playBtn)
        mediaLayout.addWidget(self.stopBtn)
        #mediaLayout.addWidget(applyParamsBtn)
        mediaLayout.addWidget(calibrateBtn)

        infoBox = QGroupBox()
        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setHorizontalHeaderLabels(["Camera 1","Camera 2"])
        self.tableWidget.setRowCount(5)
        self.tableWidget.setVerticalHeaderLabels(["X","Y","Pupil Radius Change (%)","Heart Rate (BPM)","Blinks"])




        dataLayout = QVBoxLayout()
        
        infoBox.setTitle("Data")
        infoBox.setLayout(dataLayout)
        analysisLayout.addWidget(infoBox)
        dataLayout.addWidget(self.tableWidget)
    

       
        #playBtn.clicked.connect(self.record)

        self.mainLayout.addWidget(analysisFrame, 0, 2,2,1)
        self.mainLayout.addWidget(tabs, 1, 0,1,2)
        
        

        
        widget = QWidget(self)
        widget.setLayout(self.mainLayout)
        self.setCentralWidget(widget)

        self.dataX,self.dataY,self.r  =[],[],[]
        self.idx = 0
        self.pupil_radius = 1
        self.pupil_radius_ = 0

        self.initialize_gui()
       
        # connect its signal to the update_image slot
        self.videoThread.change_pixmap_signal.connect(self.update_image)
        self.videoThread.keypoints.connect(self.update_data)
        self.videoThread.keypoints.connect(self.update_scatter_graph)
        self.videoThread.keypoints.connect(self.update_plot)
        self.videoThread.blink_count.connect(self.update_blink_count)
        self.serielThread.serielData.connect(self.update_pulse)
        
        # start the thread
        self.videoThread.start()
        self.serielThread.start()

        # self.audioThread.voice_data.connect(self.update_voice_recorder)
        
  
        try:
            self.videoThread.start()
        except:
            self.videoThread.stop()
            retryBtn = QPushButton("Retry Connection")
            retryBtn.clicked.connect(self.retryConnection)
            self.mainLayout.addWidget(retryBtn, 0, 0)

   
        self.pulse_data = [0]
        self.pulse_timestamps = []

    def retryConnection(self):
        self.videoThread.start()

    @pyqtSlot(int)
    def update_blink_count(self,blink_count):
        self.tableWidget.setItem(4,0,QTableWidgetItem(f"{blink_count}"))

        
        
    @pyqtSlot(list)
    def update_pulse(self,data):
        
        if len(self.pulse_data)> 49:
            #self.pulse_timestamps.pop(0)
            self.pulse_data.pop(0)
            
        self.pulse_data.append(data[1])
        #self.pulse_timestamps.append(datetime.datetime.now().second)
        self.pulse_graph.setData(range(len(self.pulse_data)),self.pulse_data)
        self.tableWidget.setItem(3,0,QTableWidgetItem(f"{data[1]}"))
        



    @pyqtSlot(object)
    def update_voice_recorder(self,data):
        #print(data)
        self.voice_recorder.setData(range(len(data)),data)

    @pyqtSlot(tuple)
    def update_plot(self,data):
     
        try:
            self.plot.setData(self.time_stamps,[r/self.pupil_radius for r in self.r])
        except: pass
        
        

    @pyqtSlot(tuple)
    def update_scatter_graph(self, data):
        
        self.idx +=1

        if len(self.time_stamps) > 49:
            self.time_stamps.pop(0)
        # self.graph.clear()
        # self.plot.clear()
        self.time_stamps.append(self.idx)
        self.scatter.setData(self.dataX, self.dataY)
        #self.dataX.append(self.pupil_radius_)
        # for d in data:
        #     # self.dataX.append(d.pt[0])
        #     # self.dataY.append(d.pt[1])
        #     # self.r.append(d.size)
        #     self.dataX.append(d[0][0])
        #     self.dataY.append(d[0][1])
        #     self.r.append(d.size)
            
        #     self.scatter.setData(self.dataX, self.dataY)
        #     if len(self.dataX) > 50:
        #         self.dataX.pop(0)
        #         self.dataY.pop(0)
        #         self.r.pop(0)
                
                # self.time_stamps.pop(0)
            
    # @pyqtSlot(tuple)
    def calibrate(self):
        #for d in data:
        self.pupil_radius = self.pupil_radius_

    @pyqtSlot(tuple)
    def update_data(self, data):
        xys = []
        
        
        
        #(x,y) = d.pt
        (x,y) = data[0]

        #self.pupil_radius_ = d.size
        #self.pupil_radius_ = np.pi * data[1][0] * data[1][1]
        self.pupil_radius_ = self.calculate_perimeter(data[1][0],data[1][1])
        self.tableWidget.setItem(0,0,QTableWidgetItem(str(round(x,3))))
        self.tableWidget.setItem(1,0,QTableWidgetItem(str(round(y,3))))
        self.tableWidget.setItem(2,0,QTableWidgetItem(f"{(self.pupil_radius_/self.pupil_radius)*100:.1f}"))
        
        self.dataX.append(x)
        self.dataY.append(y)
        self.r.append(self.pupil_radius_)
        if len(self.dataX) > 50:
            self.dataX.pop(0)
            self.dataY.pop(0)
            self.r.pop(0)

        xys.append((x,y))
        # for idx,d in enumerate(data):
        #     print(d)
        #     #(x,y) = d.pt
        #     (x,y) = d[0]

        #     #self.pupil_radius_ = d.size
        #     self.pupil_radius_ = np.pi * d[1][0] * d[1][1]
        #     self.tableWidget.setItem(0,0,QTableWidgetItem(str(round(x,3))))
        #     self.tableWidget.setItem(1,0,QTableWidgetItem(str(round(y,3))))
        #     self.tableWidget.setItem(2,0,QTableWidgetItem(f"{(self.pupil_radius_/self.pupil_radius)*100:.1f}"))
            
        #     self.dataX.append(x)
        #     self.dataY.append(y)
        #     self.r.append(self.pupil_radius_)
        #     if len(self.dataX) > 50:
        #         self.dataX.pop(0)
        #         self.dataY.pop(0)
        #         self.r.pop(0)

        #     xys.append((x,y))
        
        #print(xys)

    def calculate_perimeter(self,a,b):
        perimeter = math.pi * ( 3*(a+b) - math.sqrt( (3*a + b) * (a + 3*b) ) )
        return perimeter


    @pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
        """Updates the image_label with a new opencv image"""
   
        qt_img = self.convert_cv_qt(cv_img)
        self.image_1_label.setPixmap(qt_img)
    
    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.image_1_label.width(), self.image_1_label.height(), Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)
     

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()