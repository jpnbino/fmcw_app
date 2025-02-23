import os
import sys

import serial
import random

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from bms.isl94203_constants import ADDR_EEPROM_BEGIN, ADDR_EEPROM_END, ADDR_USER_EEPROM_BEGIN, ADDR_USER_EEPROM_END, \
    DEFAULT_CONFIG, ADDR_RAM_OFFSET, ADDR_RAM_BEGIN, ADDR_RAM_END, ISL94203_EEPROM_SIZE
from serialbsp.protocol_fmcw import SerialProtocolFmcw

START_BYTE = 0xAA

CMD_READ_ALL_MEMORY = 0x01
CMD_READ_EEPROM = 0x02
CMD_WRITE_EEPROM = 0x03
CMD_READ_RAM = 0x04
CMD_WRITE_USER_EEPROM = 0x05
CMD_READ_USER_EEPROM = 0x06

CMD_NAMES = {
    CMD_READ_ALL_MEMORY: "CMD_READ_ALL_MEMORY",
    CMD_READ_EEPROM: "CMD_READ_EEPROM",
    CMD_WRITE_EEPROM: "CMD_WRITE_EEPROM",
    CMD_READ_RAM: "CMD_READ_RAM",
    CMD_WRITE_USER_EEPROM: "CMD_WRITE_USER_EEPROM",
    CMD_READ_USER_EEPROM: "CMD_READ_USER_EEPROM"
}


class SimulatedDevice:
    def __init__(self, port, baudrate):
        self.ser = serial.Serial(port, baudrate, timeout=1)
        if not self.ser.is_open:
            self.ser.open()
            print(f"Opened serial port {port} at {baudrate} baud")
        else:
            print(f"Serial port {port} is already open")

        self.config = DEFAULT_CONFIG
        self.protocol = SerialProtocolFmcw(self)

    def calculate_checksum(self, data):
        checksum = 0
        for byte in data:
            checksum ^= byte
        return checksum

    def send_response(self, cmd, data):
        if isinstance(data, bytes):
            data = list(data)
        packet = [START_BYTE, cmd, len(data)] + data
        checksum = self.calculate_checksum(packet[1:])
        packet.append(checksum)
        self.ser.write(bytearray(packet))

    def handle_command(self, cmd, data):
        response_data = []

        if cmd == CMD_READ_ALL_MEMORY:
            response_data = self.config
        elif cmd == CMD_READ_EEPROM:
            eeprom_values = self.config[ADDR_EEPROM_BEGIN:(ADDR_EEPROM_END + 1)]
            response_data = eeprom_values
        elif cmd == CMD_WRITE_EEPROM:
            if len(data) != ISL94203_EEPROM_SIZE:
                print(f"Error: Data length {len(data)} bytes does not match EEPROM size {ISL94203_EEPROM_SIZE} bytes")
                response_data = [0xFF]  # Error response
            else:
                self.config[ADDR_EEPROM_BEGIN:ADDR_EEPROM_END + 1] = data
                response_data = [0x00]  # Acknowledge write operation
        elif cmd == CMD_READ_RAM:
            ram_size = ADDR_RAM_END - ADDR_RAM_BEGIN + 1
            response_data = [random.randint(0, 255) for _ in range(ram_size)]
            # ram_values = self.config[ADDR_RAM_OFFSET:ADDR_RAM_OFFSET + (ADDR_RAM_END - ADDR_RAM_BEGIN + 1)]
            # response_data = ram_values
        elif cmd == CMD_READ_USER_EEPROM:
            user_eeprom_values = self.config[ADDR_USER_EEPROM_BEGIN:(ADDR_USER_EEPROM_END + 1)]
            response_data = user_eeprom_values
        elif cmd == CMD_WRITE_USER_EEPROM:
            if len(data) > (ADDR_USER_EEPROM_END - ADDR_USER_EEPROM_BEGIN + 1):
                print(
                    f"Error: Data length {len(data)} bytes exceeds User EEPROM size {(ADDR_USER_EEPROM_END - ADDR_USER_EEPROM_BEGIN + 1)} bytes")
                response_data = [0xFF]  # Error response
            else:
                self.config[ADDR_USER_EEPROM_BEGIN:ADDR_USER_EEPROM_BEGIN + len(data)] = data
                response_data = [0x00]  # Acknowledge write operation
        else:
            print(f"Unknown Command {cmd}")

        return response_data

    def run(self):
        while True:
            packet = self.protocol.read_packet()
            if packet:
                cmd, data = packet
                if len(data) > 0:
                    data_str = ' '.join(format(byte, '02X') for byte in data)  # Convert data to a string of hex values
                else:
                    data_str = "No data"

                cmd_name = CMD_NAMES.get(cmd, f"Unknown Command ({cmd})")
                print(f"Received command: {cmd_name}")
                print(f"data in ({len(data)} bytes): \n{data_str}")

                response_data = self.handle_command(cmd, data)
                response_data_str = ' '.join(format(byte, '02X') for byte in response_data)
                self.send_response(cmd, response_data)
                print(f"data out ({len(response_data)} bytes):\n{response_data_str}\n")


if __name__ == '__main__':
    simulated_device = SimulatedDevice(port='COM8', baudrate=9600)
    print("Simulated device running...")
    simulated_device.run()
