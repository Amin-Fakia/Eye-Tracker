
from libraries_import import *
class RangeBox():

    def __new__(self,box_name=None,label1=None,label2=None,label1_value=(0,100),label2_value=(0,100),active=True):
        Layout = QVBoxLayout()
        self.Box = QGroupBox()
        self.Box.setTitle(box_name)
        self.Box.setLayout(Layout)
        self.Box.setCheckable(active)
        Layout.addWidget(QLabel(label1))
        valueMin = QSpinBox()
        valueMin.setRange(label1_value[0],label1_value[1])
        Layout.addWidget(valueMin)
        Layout.addWidget(QLabel(label2))
        valueMax = QSpinBox()
        valueMax.setRange(label2_value[0],label2_value[1])
        Layout.addWidget(valueMax)
        return self.Box
