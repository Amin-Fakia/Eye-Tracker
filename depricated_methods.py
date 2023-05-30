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
