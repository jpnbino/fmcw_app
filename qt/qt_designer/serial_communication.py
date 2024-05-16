import serial
from serial.tools import list_ports

class SerialCommunication:
    def __init__(self):
        self.ser = serial.Serial()

    def open_serial(self, port):
        self.ser.port = port
        self.ser.baudrate = 9600  # Adjust the baudrate as needed
        self.ser.timeout = 2
        
        try:
            self.ser.open()
            print(f"Serial port {port} opened\n")
        except serial.SerialException as e:
            print(f"Error opening serial port: {e}\n")

    def close_serial(self):
        self.ser.close()
        print(f"Serial port closed\n")

    def read_data(self):
        # Placeholder for reading data from the device
        print("Reading data...\n")

    def write_data(self):
        # Placeholder for writing data to the device
        print("Writing data...\n")
