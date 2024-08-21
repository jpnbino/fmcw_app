import serial
import time
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from bms.constants import DEFAULT_CONFIG

START_BYTE = 0xAA

CMD_READ_ALL_MEMORY = 0x01
CMD_READ_EEPROM = 0x02
CMD_WRITE_EEPROM = 0x03
CMD_READ_RAM = 0x04


class SimulatedDevice:
    def __init__(self, port, baudrate):
        self.ser = serial.Serial(port, baudrate, timeout=1)
        if not self.ser.is_open:
            self.ser.open()
            print(f"Opened serial port {port} at {baudrate} baud")
        else:
            print(f"Serial port {port} is already open")

        self.config = DEFAULT_CONFIG

    def calculate_checksum(self, data):
        checksum = 0
        for byte in data:
            checksum ^= byte
        return checksum

    def read_packet(self):
        ser = self.ser
        while True:
            byte = ser.read(1)
            if byte and byte[0] == START_BYTE:
                break

        cmd = ser.read(1)
        if not cmd:
            return None
        cmd = cmd[0]

        data_length = ser.read(1)
        if not data_length:
            return None
        data_length = data_length[0]

        data = ser.read(data_length)
        if len(data) != data_length:
            return None

        checksum = ser.read(1)
        if not checksum:
            return None
        checksum = checksum[0]

        packet = [cmd, data_length] + list(data)
        if self.calculate_checksum(packet) != checksum:
            print("Checksum mismatch")
            return None

        return (cmd, data)

    def send_response(self, cmd, data):
        if isinstance(data, bytes):
            data = list(data)
        packet = [START_BYTE, cmd, len(data)] + data
        checksum = self.calculate_checksum(packet[1:])
        packet.append(checksum)
        self.ser.write(bytearray(packet))

    def run(self):
        while True:
            packet = self.read_packet()
            if packet:
                cmd, data = packet
                if len(data) > 0:
                    data_str = ' '.join(format(byte, '02X') for byte in data)  # Convert data to a string of hex values
                else:
                    data_str = "No data"

                print(f"Received command: {cmd}, data: {data_str}")

                response_data = []

                if cmd == CMD_READ_ALL_MEMORY:
                    response_data = self.config  # Example data
                    self.send_response(cmd, response_data)
                elif cmd == CMD_READ_EEPROM:
                    response_data = [0x50, 0x60, 0x70, 0x80]  # Example data
                    self.send_response(cmd, response_data)
                elif cmd == CMD_WRITE_EEPROM:
                    print(f"self.config: \n{' '.join(f'{value:02X}' for value in self.config)}")
                    self.config = list(data)
                    print(f"self.config: \n{' '.join(f'{value:02X}' for value in self.config)}")
                    print(f"EEPROM data written: {data}")
                    # Acknowledge the write command
                    # response_data = [0x11, 0x22, 0x33, 0x44]
                    self.send_response(cmd, [])
                elif cmd == CMD_READ_RAM:
                    response_data = self.config
                    self.send_response(cmd, response_data)
                else:
                    print(f"Unknown Command {cmd}")

                print(f"Device response: {response_data}")


if __name__ == '__main__':
    simulated_device = SimulatedDevice(port='COM22', baudrate=9600)
    print("Simulated device running...")
    simulated_device.run()
