import threading
import serial
from serialbsp.crc8 import calculate_crc, check_crc

ERROR_BYTE = 0x09
BOARD_TRIGGERED = 0x0A

# FMCW Commands
CMD_GET_DEVICE_STATUS = 0x08
CMD_START_CALIBRATION = 0x0B
CMD_GET_BOOTLOADER_STATUS = 0x0C
CMD_GET_SDCARD_STATUS = 0x0D
CMD_GET_REMOTE_STATUS = 0x0E

CMD_START_FFT_MEAS_ANTENNA_1 = 0x10
CMD_START_ADC_MEAS_ANTENNA_1 = 0x11
CMD_START_FFT_MEAS_ANTENNA_2 = 0x12
CMD_START_ADC_MEAS_ANTENNA_2 = 0x13
CMD_START_FFT_MEAS_ANTENNA_3 = 0x14
CMD_START_ADC_MEAS_ANTENNA_3 = 0x15
CMD_START_FFT_MEAS_ANTENNA_4 = 0x16
CMD_START_ADC_MEAS_ANTENNA_4 = 0x17

CMD_SET_RTC_YEAR = 0x18
CMD_SET_RTC_MONTH = 0x19
CMD_SET_RTC_DAY = 0x1A
CMD_SET_RTC_DOW = 0x1B
CMD_SET_RTC_HOUR = 0x1C
CMD_SET_RTC_MINUTE = 0x1D
CMD_SET_RTC_SECOND = 0x1E
CMD_SET_RTC_CALIBRATION = 0x1F

CMD_DIGITAL_POTI_1 = 0x20
CMD_DIGITAL_POTI_2 = 0x21
CMD_DIGITAL_POTI_3 = 0x22
CMD_DIGITAL_POTI_4 = 0x23
CMD_FILTER_REQUEST = 0x24

CMD_RESET_TUSB3410 = 0x28
CMD_RESET_ISM = 0x29
CMD_RESET_RS485 = 0x2A
CMD_RESET = 0x2B
CMD_TABLE_FIRST_ENTRY = 0x30
CMD_TABLE_ENTRY = 0x31
CMD_TABLE_LAST_ENTRY = 0x32

#Modem Commands
CMD_MODEM_RSSI = 0x38
CMD_MODEM_TEMPERATURE = 0x39
CMD_MODEM_BATTERY = 0x3A
CMD_MODEM_AT_MONP = 0x3B
CMD_MODEM_AT_SMONC = 0x3C
CMD_MODEM_TYPE = 0x3D
CMD_MODEM_OPERATOR = 0x3E

#Variables
CMD_VAR1_UINT32_1 = 0x40 #LSB
CMD_VAR1_UINT32_2 = 0x41
CMD_VAR1_UINT32_3 = 0x42
CMD_VAR1_UINT32_4 = 0x43 #MSB
CMD_VAR2_UINT32_1 = 0x44 #LSB
CMD_VAR2_UINT32_2 = 0x45
CMD_VAR2_UINT32_3 = 0x46
CMD_VAR2_UINT32_4 = 0x47 #MSB

#Remote commands
CMD_LOG_OUT = 0x48
CMD_LOG_IN = 0x49
CMD_FW_UPGRADE = 0x4A
CMD_SDCARD_WRITE = 0x4B
CMD_SDCARD_READ = 0x4C
CMD_SDCARD_DELETE = 0x4D
#Test Command
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
        self.thread.join()

    def read_data(self):
        while self.running:
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
        elif cmd in [CMD_SET_RTC_YEAR, CMD_SET_RTC_MONTH, CMD_SET_RTC_DAY, CMD_SET_RTC_HOUR, CMD_SET_RTC_MINUTE, CMD_SET_RTC_SECOND]:
            self.log_callback(f"Set RTC {cmd - CMD_SET_RTC_YEAR + 1}:\n {hex_data}")
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