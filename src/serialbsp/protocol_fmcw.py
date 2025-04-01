import threading
import serial
from serialbsp.crc8 import calculate_crc, check_crc
from serialbsp.commands import *

class SerialProtocolFmcw:
    def __init__(self, serial_manager, log_callback):
        self.serial_manager = serial_manager
        self.serial_manager.ser.timeout = 2 # Set a timeout of 1 second
        self.serial_manager.ser.write_timeout = 1
        self.log_callback = log_callback
        self.pause_event = threading.Event()  # Add an event to control pausing
        self.pause_event.set()  # Initially, the thread is not paused

    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self.read_data)
        self.thread.start()
        
    def stop(self):
        self.running = False
        self.thread.join()

    def pause(self):
        """Pause the read_data thread."""
        self.pause_event.clear()

    def resume(self):
        """Resume the read_data thread."""
        self.pause_event.set()

    def read_data(self):
        while self.running:
            self.pause_event.wait()
            if self.serial_manager.is_open():
                try:
                    data = self.serial_manager.ser.read(50)
                    if not data:
                        continue
                    self.log_callback(data, newline=False)
                except serial.SerialException as e:
                    self.log_callback(f"Serial exception: {e}")
                    self.running = False
            else:
                self.log_callback("Serial port closed")
                self.running = False               

    def read_packet(self, data_length):
        ser = self.serial_manager.ser

        if not ser or not ser.is_open:
            self.log_callback("Serial port not open")
            return None

        cmd = ser.read(2)
        if not cmd:
            return None
        cmd = cmd[0]

        data = ser.read(data_length)
        if len(data) != data_length:
            self.log_callback("Timeout or incomplete data received")
            return None

        checksum = ser.read(1)
        if not checksum:
            self.log_callback("Timeout waiting for checksum byte")
            return None
        checksum = checksum[0]

        packet = [cmd, data_length] + list(data)
        if check_crc(packet) != checksum:
            self.log_callback("Checksum mismatch")
            #return None

        return (cmd, data)

    def send_command(self, cmd, data):
        packet = [cmd] + data
        checksum =calculate_crc(packet + [0])
        packet.append(checksum)
        self.serial_manager.ser.write(bytearray(packet))
        self.log_callback(f"Sent packet: {packet}")
        