START_BYTE = 0xAA

CMD_READ_ALL_MEMORY = 0x01
CMD_READ_EEPROM = 0x02
CMD_WRITE_EEPROM = 0x03
CMD_READ_RAM = 0x04
CMD_WRITE_USER_EEPROM = 0x05
CMD_READ_USER_EEPROM = 0x06


class SerialProtocol:
    def __init__(self, serial_setup):
        self.serial_setup = serial_setup
        self.serial_setup.ser.timeout = 1  # Set a timeout of 1 second

    def calculate_checksum(self, data):
        checksum = 0
        for byte in data:
            checksum ^= byte
        return checksum

    def send_command(self, cmd, data):
        packet = [START_BYTE, cmd, len(data)] + data
        checksum = self.calculate_checksum(packet[1:])
        packet.append(checksum)
        self.serial_setup.ser.write(bytearray(packet))

    def read_packet(self):
        ser = self.serial_setup.ser
        while True:
            byte = ser.read(1)
            if not byte:
                return None
            if byte[0] == START_BYTE:
                break

        cmd = ser.read(1)
        if not cmd:
            print("Timeout waiting for command byte")
            return None
        cmd = cmd[0]

        data_length = ser.read(1)
        if not data_length:
            print("Timeout waiting for data length byte")
            return None
        data_length = data_length[0]

        data = ser.read(data_length)
        if len(data) != data_length:
            print("Timeout or incomplete data received")
            return None

        checksum = ser.read(1)
        if not checksum:
            print("Timeout waiting for checksum byte")
            return None
        checksum = checksum[0]

        packet = [cmd, data_length] + list(data)
        if self.calculate_checksum(packet) != checksum:
            print("Checksum mismatch")
            return None

        return (cmd, data)

    def process_received_data(self, cmd, data):
        hex_data = ' '.join(f'{value:02X}' for value in data)
        if cmd == CMD_READ_ALL_MEMORY:
            print(f"Memory Data:\n {hex_data}")
        elif cmd == CMD_READ_EEPROM:
            print(f"EEPROM Data:\n {hex_data}")
        elif cmd == CMD_WRITE_EEPROM:
            print(f"Write EEPROM Acknowledgment:\n {hex_data}")
        elif cmd == CMD_READ_RAM:
            print(f"RAM Data:\n {hex_data}")
        else:
            print(f"Unknown Command {cmd} with Data:\n {hex_data}")

    def run(self):
        self.send_command(CMD_READ_ALL_MEMORY, [])

        while True:
            packet = self.read_packet()
            if packet:
                cmd, data = packet
                self.process_received_data(cmd, data)
