
from serial import Serial
import time
from datetime import datetime

# Replace 'COM3' with the appropriate port name for your system
serial_port = 'COM11'
baud_rate = 19200

# Establish a connection to the serial port
ser = Serial(serial_port, baud_rate, timeout=1)

try:
    while True:
        # Read data from the serial port
        data = ser.readline().decode('utf-8').strip()
        
        # If data received, print it
        if data:
            print(datetime.strptime(data[:18],"%d-%M-%Y %H:%M:%S"))
            print(f"date: {data[:18]}")
            print(f"SpO2: {data[21:24]}")
            try:print(f"BPM: {int(data[29:32])}")#
            except:pass
            print("Received data from serial port: ", data)

            # Give the device time to send data again
            time.sleep(0.5)
except KeyboardInterrupt:
    print("Closing the serial port.")
    ser.close()