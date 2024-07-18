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

        #Default from datasheet:      
        # 1E2A  0DD4  18FF  09FF  0E7F 
        # 0600  0DFF  07AA  0801  0801 
        # 0214  44A0  44A0  60C8  0A55
        # 0D70  0010  01AB  0802  0802
        # 0BF2  0A93  04B6  053E  04B6 
        # 053E  0BF2  0A93  04B6  053E 
        # 0BF2  0A93  067C  0621  06AA 
        # FC0F  83FF  
        # |USER EEPROM  8bytes    |
        # 0000  2240  0000  0003  0000
        # 0A8F  0ABE  0015  0A91  0ABE 
        # 0000  0000  0000  0000  0A8F
        # 0A92  027B  04D2  04D2  0368
        # 0B09  002A              
        #self.configuration_default = "2A,1E,D4,0D,FF,18,FF,09,7F,0E,00,06,FF,0D,AA,07,01,08,01,08,14,02,A0,44,A0,44,C8,60,55,0A,70,0D,10,00,AB,01,02,08,02,08,F2,0B,93,0A,B6,04,3E,05,B6,04,3E,05,F2,0B,93,0A,B6,04,3E,05,F2,0B,93,0A,7C,06,21,06,AA,06,0F,FC,FF,83,00,00,00,00,00,00,00,00,00,00,40,22,00,00,03,00,00,00,8F,0A,BE,0A,15,00,91,0A,BE,0A,00,00,00,00,00,00,00,00,8F,0A,92,0A,7B,02,D2,04,D2,04,68,03,09,0B,2A,00,"
        self.configuration_default = [
            0x2A, 0x1E, 0xD4, 0x0D, 0xFF, 0x18, 0xFF, 0x09, 0x7F, 0x0E,
            0x00, 0x06, 0xFF, 0x0D, 0xAA, 0x07, 0x01, 0x08, 0x01, 0x08, 
            0x14, 0x02, 0xA0, 0x44, 0xA0, 0x44, 0xC8, 0x60, 0x55, 0x0A,
            0x70, 0x0D, 0x10, 0x00, 0xAB, 0x01, 0x02, 0x08, 0x02, 0x08,
            0xF2, 0x0B, 0x93, 0x0A, 0xB6, 0x04, 0x3E, 0x05, 0xB6, 0x04,
            0x3E, 0x05, 0xF2, 0x0B, 0x93, 0x0A, 0xB6, 0x04, 0x3E, 0x05,
            0xF2, 0x0B, 0x93, 0x0A, 0x7C, 0x06, 0x21, 0x06, 0xAA, 0x06,
            0x0F, 0xFC, 0xFF, 0x83, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x40, 0x22, 0x00, 0x00, 0x03, 0x00,
            0x00, 0x00, 0x8F, 0x0A, 0xBE, 0x0A, 0x15, 0x00, 0x91, 0x0A,
            0xBE, 0x0A, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x8F, 0x0A, 0x92, 0x0A, 0x7B, 0x02, 0xD2, 0x04, 0xD2, 0x04,
            0x68, 0x03, 0x09, 0x0B, 0x2A, 0x00
        ]

        self.config = self.configuration_default

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
                    print(f"self.config: {self.config}")
                    self.config = list(data)
                    print(f"self.config: {self.config}")
                    print(f"EEPROM data written: {data}")
                    # Acknowledge the write command
                    #response_data = [0x11, 0x22, 0x33, 0x44]
                    self.send_response(cmd, [])
                elif cmd == CMD_READ_RAM:
                    response_data = [0x90, 0xA0, 0xB0, 0xC0]  # Example data
                    self.send_response(cmd, response_data)
                else:
                    print(f"Unknown Command {cmd}")

                print(f"Device response: {response_data}")

if __name__ == '__main__':
    simulated_device = SimulatedDevice(port='COM22', baudrate=9600)
    print("Simulated device running...")
    simulated_device.run()
