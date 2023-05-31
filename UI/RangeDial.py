from libraries_import import *

class RangeDial():
    def __new__(self,dial_name=None,label_value=(0,100)):
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
    def update(value,label):
        label.setText(f'Value : {value}')
        