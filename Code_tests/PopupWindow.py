
from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout

class MyPopup(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.layoutMain = QHBoxLayout()
        self.setLayout(self.layoutMain)

        self.buttonSave = QPushButton("Save")
        self.buttonSave.clicked.connect(self.save)
        self.layoutMain.addWidget(self.buttonSave)
        self.buttonClose = QPushButton("Close")
        self.buttonClose.clicked.connect(self.close)
        self.layoutMain.addWidget(self.buttonClose)

    def save(self):
        pass
    def close(self):
        pass
    