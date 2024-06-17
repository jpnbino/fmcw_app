import serial
import time

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
        packet = [START_BYTE, cmd, len(data)] + data
        checksum = self.calculate_checksum(packet[1:])
        packet.append(checksum)
        self.ser.write(bytearray(packet))

    def run(self):
        while True:
            packet = self.read_packet()
            if packet:
                cmd, data = packet
                data_str = ' '.join(format(byte, '02X') for byte in data)  # Convert data to a string of hex values
                print(f"Received command: {cmd}, data: {data_str}")

                if cmd == CMD_READ_ALL_MEMORY:
                    response_data = [0x10, 0x20, 0x30, 0x40]  # Example data
                    self.send_response(cmd, response_data)
                elif cmd == CMD_READ_EEPROM:
                    response_data = [0x50, 0x60, 0x70, 0x80]  # Example data
                    self.send_response(cmd, response_data)
                elif cmd == CMD_WRITE_EEPROM:
                    # Acknowledge the write command
                    self.send_response(cmd, [])
                elif cmd == CMD_READ_RAM:
                    response_data = [0x90, 0xA0, 0xB0, 0xC0]  # Example data
                    self.send_response(cmd, response_data)
                else:
                    print(f"Unknown Command {cmd}")

if __name__ == '__main__':
    simulated_device = SimulatedDevice(port='COM22', baudrate=9600)
    print("Simulated device running...")
    simulated_device.run()
