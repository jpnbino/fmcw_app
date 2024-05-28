import serial
from serial.tools import list_ports

class SerialSetup:
    def __init__(self):
        self.ser = serial.Serial()
        self.current_port = None  # Store the current port name

    def list_ports(self):
        ports = list(list_ports.comports())
        for port in ports:
            print(f"Port: {port.device}")

    def open_serial(self, port, baudrate=9600, timeout=2):
        self.ser.port = port
        self.ser.baudrate = baudrate
        self.ser.timeout = timeout
        self.current_port = port  # Store the current port name

        try:
            self.ser.open()
            print(f"Serial port {port} opened\n")
        except serial.SerialException as e:
            print(f"Error opening serial port: {e}\n")

    def close_serial(self):
        if self.ser.is_open:
            self.ser.close()
            print(f"Serial port {self.current_port} closed\n")  # Print the current port name
