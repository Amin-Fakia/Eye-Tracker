from libraries_import import *

class SerialReceiver(QThread):
    serielData = pyqtSignal(list)
    
    def __init__(self, com_port="COM1",baud_rate=19200) -> None:
        super(SerialReceiver,self).__init__()
        self.serial_port = com_port
        self.baud_rate = baud_rate
        
        self.pulse = 0
        self._isRunning = True
    def run(self):
        try:
            self.ser = Serial(self.serial_port, self.baud_rate, timeout=1)
        except: 
            print(f"Couldn't connect to serial port {self.serial_port}")
            self._isRunning = False

        while self._isRunning:
            # Read data from the serial port
            data = self.ser.readline().decode('utf-8').strip()
            
            # If data received, print it
            if data:
                try: self.serielData.emit([data[:18],int(data[29:32])])
                except:pass
                # print(f"date: {data[:18]}")
                # print(f"SpO2: {data[21:24]}")
                # print(f"BPM: {data[29:32]}")
                # print("Received data from serial port: ", data)
                # Give the device time to send data again
    def close(self):
        self._isRunning = False
        self.ser.close()

