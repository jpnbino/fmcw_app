import serial
from serial.tools import list_ports

class SerialManager:

    def __init__(self):
        self.ser = serial.Serial()
        self.current_port = None  
        
    def list_ports(self):
        ports = list(list_ports.comports())
        for port in ports:
            print(f"Port: {port.device}")

    def get_available_ports(self):
        ports = list_ports.comports()
        return [(port.device, port.description) for port in ports]

    def open_serial_port(self, port, baudrate=9600, timeout=2):
        self.ser.port = port
        self.ser.baudrate = baudrate
        self.ser.timeout = timeout
        self.current_port = port

        try:
            self.ser.open()
            print(f"Serial port {port} opened\n")
            return self.ser
        except serial.SerialException as e:
            print(f"Error opening serial port: {e}\n")
            return None

    def close_serial_port(self):
        if self.ser.is_open:
            self.ser.close()
            print(f"Serial port {self.current_port} closed\n")

    def is_open(self):
        return self.ser.is_open
    
    def reset_input_buffer(self):
        self.ser.reset_input_buffer()

    def reset_output_buffer(self):
        self.ser.reset_output_buffer()
        