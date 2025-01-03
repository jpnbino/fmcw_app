import threading
import queue
import serial
from serialbsp.crc8 import calculate_crc, check_crc

STATUS_REQUEST = 0x08
ERROR_BYTE = 0x09
BOARD_TRIGGERED = 0x0A
START_CALIBRATION = 0x0B
START_FFT_MEAS_ANTENNA_1 = 0x10
START_ADC_MEAS_ANTENNA_1 = 0x11
START_FFT_MEAS_ANTENNA_2 = 0x12
START_ADC_MEAS_ANTENNA_2 = 0x13
START_FFT_MEAS_ANTENNA_3 = 0x14
START_ADC_MEAS_ANTENNA_3 = 0x15
START_FFT_MEAS_ANTENNA_4 = 0x16
START_ADC_MEAS_ANTENNA_4 = 0x17
SET_RTC_YEAR = 0x18
SET_RTC_MONTH = 0x19
SET_RTC_DAY = 0x1A
SET_RTC_HOUR = 0x1B
SET_RTC_MINUTE = 0x1C
SET_RTC_SECOND = 0x1D
DIGITAL_POTI_1 = 0x20
DIGITAL_POTI_2 = 0x21
DIGITAL_POTI_3 = 0x22
DIGITAL_POTI_4 = 0x23
FILTER_REQUEST = 0x24
RESET_TUSB3410 = 0x28
RESET_ISM = 0x29
RESET_RS485 = 0x2A
RESET = 0x2B
TABLE_FIRST_ENTRY = 0x30
TABLE_ENTRY = 0x31
TABLE_LAST_ENTRY = 0x32
CMD_TEST = 0xFF

class SerialProtocolFmcw:
    def __init__(self, serial_manager, log_callback):
        self.serial_manager = serial_manager
        self.serial_manager.ser.timeout = 1  # Set a timeout of 1 second
        self.serial_manager.ser.write_timeout = 1
        self.log_callback = log_callback


    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self.read_data)
        self.thread.start()
        
    def stop(self):
        self.running = False
        self.read_thread.join()

    def read_data(self):
        while self.running:
            if self.serial_manager.is_open():
                try:
                    data = self.serial_manager.ser.read(5)
                    if not data:
                        continue
                    self.log_callback(data, newline=False)
                except serial.SerialException as e:
                    self.log_callback(f"Serial exception: {e}")
                    self.running = False
            else:
                self.log_callback("Serial port closed")
                self.running = False
                

    def read_packet(self):
        ser = self.serial_manager.ser

        if not ser or not ser.is_open:
            self.log_callback("Serial port not open")
            return None

        cmd = ser.read(1)
        if not cmd:
            return None
        cmd = cmd[0]

        data_length = ser.read(1)
        if not data_length:
            self.log_callback("Timeout waiting for data length byte")
            return None
        data_length = data_length[0]

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
            return None

        return (cmd, data)

    def send_command(self, cmd, data):
        packet = [cmd] + data
        checksum =calculate_crc(packet + [0])
        packet.append(checksum)
        self.serial_manager.ser.write(bytearray(packet))
        self.log_callback(f"Sent packet: {packet}")


        
    def process_received_data(self, cmd, data):
        hex_data = ' '.join(f'{value:02X}' for value in data)
        if cmd == STATUS_REQUEST:
            self.log_callback(f"Status Request:\n {hex_data}")
        elif cmd == ERROR_BYTE:
            self.log_callback(f"Error Byte:\n {hex_data}")
        elif cmd == BOARD_TRIGGERED:
            self.log_callback(f"Board Triggered:\n {hex_data}")
        elif cmd == START_CALIBRATION:
            self.log_callback(f"Start Calibration:\n {hex_data}")
        elif cmd in [START_FFT_MEAS_ANTENNA_1, START_FFT_MEAS_ANTENNA_2, START_FFT_MEAS_ANTENNA_3, START_FFT_MEAS_ANTENNA_4]:
            self.log_callback(f"Start FFT Measurement Antenna {cmd - START_FFT_MEAS_ANTENNA_1 + 1}:\n {hex_data}")
        elif cmd in [START_ADC_MEAS_ANTENNA_1, START_ADC_MEAS_ANTENNA_2, START_ADC_MEAS_ANTENNA_3, START_ADC_MEAS_ANTENNA_4]:
            self.log_callback(f"Start ADC Measurement Antenna {cmd - START_ADC_MEAS_ANTENNA_1 + 1}:\n {hex_data}")
        elif cmd in [SET_RTC_YEAR, SET_RTC_MONTH, SET_RTC_DAY, SET_RTC_HOUR, SET_RTC_MINUTE, SET_RTC_SECOND]:
            self.log_callback(f"Set RTC {cmd - SET_RTC_YEAR + 1}:\n {hex_data}")
        elif cmd in [DIGITAL_POTI_1, DIGITAL_POTI_2, DIGITAL_POTI_3, DIGITAL_POTI_4]:
            self.log_callback(f"Digital Poti {cmd - DIGITAL_POTI_1 + 1}:\n {hex_data}")
        elif cmd == FILTER_REQUEST:
            self.log_callback(f"Filter Request:\n {hex_data}")
        elif cmd in [RESET_TUSB3410, RESET_ISM, RESET_RS485, RESET]:
            self.log_callback(f"Reset {cmd - RESET_TUSB3410 + 1}:\n {hex_data}")
        elif cmd == TABLE_FIRST_ENTRY:
            self.log_callback(f"Table First Entry:\n {hex_data}")
        elif cmd == TABLE_ENTRY:
            self.log_callback(f"Table Entry:\n {hex_data}")
        elif cmd == TABLE_LAST_ENTRY:
            self.log_callback(f"Table Last Entry:\n {hex_data}")
        else:
            self.log_callback(f"Unknown Command {cmd} with Data:\n {hex_data}")