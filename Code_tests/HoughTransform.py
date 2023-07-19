import typing
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPainter, QBrush, QPen,QPixmap,QColor
from PyQt5.QtCore import Qt, QSize
import sys
import pyqtgraph as pg

class PaintFrame(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMouseTracking(True)
        self.points = []

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        pen = QPen(Qt.white, 2)
        painter.setPen(pen)

        painter.fillRect(self.rect(), QColor("black"))

        for i in range(1, len(self.points)):
            painter.drawPoints(self.points[i - 1], self.points[i])
            
        

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.points.append(event.pos())
            self.update()
      

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            self.points.append(event.pos())
            self.update()

class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.title = "Hough Transform"
        
        self.InitWindow()

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QHBoxLayout(central_widget)

        frame1 = PaintFrame()
        

        # Create the second frame
        frame2 = QFrame()


        plot = pg.PlotWidget()
        plot.showAxis('bottom', False)  # Hide bottom axis
        plot.showAxis('left', False)  # Hide left axis

        frame2_layout = QHBoxLayout(frame2)
        frame2_layout.addWidget(plot)




        frame2.setMaximumWidth(400)
        


        # Add frames to the layout
        layout.addWidget(frame1)
        layout.addWidget(frame2)

   

    def InitWindow(self):
        self.setWindowTitle(self.title)
        self.setFixedWidth(700)
        self.setFixedHeight(500)
        self.show()



App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec())
