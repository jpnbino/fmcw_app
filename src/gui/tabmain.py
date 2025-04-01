from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QComboBox, QPushButton, QStatusBar, QTextEdit, QLineEdit, QCheckBox
from PySide6.QtGui import QTextCursor
from gui.tabbms import BmsTab
from gui.userlog import UserLog
from serialbsp.protocol_fmcw import (
    CMD_DIGITAL_POTI_1, CMD_DIGITAL_POTI_2, CMD_DIGITAL_POTI_3, CMD_DIGITAL_POTI_4, CMD_FILTER_REQUEST, CMD_GET_BOOTLOADER_STATUS, CMD_GET_DEVICE_STATUS, CMD_GET_REMOTE_STATUS, CMD_GET_SDCARD_STATUS, CMD_LOG_IN, CMD_LOG_OUT, CMD_MODEM_AT_MONP, CMD_MODEM_AT_SMONC, CMD_MODEM_BATTERY, CMD_MODEM_OPERATOR, CMD_MODEM_RSSI, CMD_MODEM_TEMPERATURE, CMD_MODEM_TYPE, CMD_READ_ALL_MEMORY, CMD_READ_RAM, CMD_READ_USER_EEPROM, CMD_START_ADC_MEAS_ANTENNA_1, CMD_START_ADC_MEAS_ANTENNA_2, CMD_START_ADC_MEAS_ANTENNA_3, CMD_START_ADC_MEAS_ANTENNA_4, CMD_START_CALIBRATION, CMD_START_FFT_MEAS_ANTENNA_1, CMD_START_FFT_MEAS_ANTENNA_2, CMD_START_FFT_MEAS_ANTENNA_3, CMD_START_FFT_MEAS_ANTENNA_4, CMD_TEST, CMD_SET_RTC_CALIBRATION, CMD_SET_RTC_DAY, CMD_SET_RTC_DOW, CMD_SET_RTC_HOUR,
    CMD_SET_RTC_MINUTE, CMD_SET_RTC_MONTH, CMD_SET_RTC_SECOND, CMD_SET_RTC_YEAR, CMD_VAR1_UINT32_1, CMD_WRITE_EEPROM, CMD_WRITE_USER_EEPROM, SerialProtocolFmcw
)

REFRESH_RATE = 5000
MESSAGE_DURATION = 5000

class MainTab:
    def __init__(self, ui, bms_config):
        self.ui = ui
        self.serial_manager = self.ui.fmcw_serial_manager
        self.serial_protocol = None
        self.init_ui()
        self.user_log = UserLog(self.ui)
        self.bms_tab = BmsTab(ui, bms_config, self.user_log.append_message)

    def init_ui(self):
        self.statusBar = self.ui.findChild(QStatusBar, "statusBar")

        self.setup_serial_controls()
        self.setup_rtc_controls()
        self.setup_status_controls()
        self.setup_potis_controls()
        self.setup_measurement_controls()
        self.setup_modem_controls()
        self.setup_var32bits_controls()
        self.setup_remote_controls()
        self.setup_test_command()
        self.setup_serial_log()
        self.setup_timers()


    def setup_serial_controls(self):
        self.serialComboBox = self.ui.findChild(QComboBox, "serialComboBox")
        self.serialOpenCloseButton = self.ui.findChild(QPushButton, "serialOpenCloseButton")
        self.serialConnectedBox = self.ui.findChild(QCheckBox, "bitPortConnected")
        self.serialOpenCloseButton.clicked.connect(self.toggle_serial)
        self.update_serial_ports()

    def setup_rtc_controls(self):
        self.setup_rtc_year_controls()
        self.setup_rtc_month_controls()
        self.setup_rtc_day_controls()
        self.setup_rtc_dow_controls()
        self.setup_rtc_hour_controls()
        self.setup_rtc_minute_controls()
        self.setup_rtc_second_controls()
        self.setup_rtc_calibrate_controls()

    def setup_rtc_year_controls(self):
        self.rtcYearPushButton = self.ui.findChild(QPushButton, "sendRTCYearPushButton")
        self.rtcYearPushButton.clicked.connect(self.send_rtc_year)
        self.rtcYearComboBox = self.ui.findChild(QComboBox, "rtcYearComboBox")
        self.rtcYearComboBox.setStyleSheet("QComboBox { combobox-popup: 0; } QComboBox QAbstractItemView { max-height: 200px; }")
        for year in range(2025, 2100):
            self.rtcYearComboBox.addItem(str(year))

    def setup_rtc_month_controls(self):
        self.rtcMonthPushButton = self.ui.findChild(QPushButton, "sendRTCMonthPushButton")
        self.rtcMonthPushButton.clicked.connect(self.send_rtc_month)
        self.rtcMonthComboBox = self.ui.findChild(QComboBox, "rtcMonthComboBox")
        self.rtcMonthComboBox.addItems(["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])

    def setup_rtc_day_controls(self):
        self.rtcDayPushButton = self.ui.findChild(QPushButton, "sendRTCDayPushButton")
        self.rtcDayPushButton.clicked.connect(self.send_rtc_day)
        self.rtcDayComboBox = self.ui.findChild(QComboBox, "rtcDayComboBox")
        self.rtcDayComboBox.addItems([str(day) for day in range(1, 32)])

    def setup_rtc_dow_controls(self):
        self.rtcDowPushButton = self.ui.findChild(QPushButton, "sendRTCDowPushButton")
        self.rtcDowPushButton.clicked.connect(self.send_rtc_day_of_week)
        self.rtcDowComboBox = self.ui.findChild(QComboBox, "rtcDowComboBox")
        self.rtcDowComboBox.addItems(["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"])

    def setup_rtc_hour_controls(self):
        self.rtcHourPushButton = self.ui.findChild(QPushButton, "sendRTCHourPushButton")
        self.rtcHourPushButton.clicked.connect(self.send_rtc_hour)
        self.rtcHourComboBox = self.ui.findChild(QComboBox, "rtcHourComboBox")
        self.rtcHourComboBox.addItems([str(hour) for hour in range(0, 24)])
        self.rtcHourComboBox.setStyleSheet("QComboBox { combobox-popup: 0; } QComboBox QAbstractItemView { max-height: 200px; }")

    def setup_rtc_minute_controls(self):
        self.rtcMinutePushButton = self.ui.findChild(QPushButton, "sendRTCMinutePushButton")
        self.rtcMinutePushButton.clicked.connect(self.send_rtc_minute)
        self.rtcMinuteComboBox = self.ui.findChild(QComboBox, "rtcMinuteComboBox")
        self.rtcMinuteComboBox.addItems([str(minute) for minute in range(0, 60)])
        self.rtcMinuteComboBox.setStyleSheet("QComboBox { combobox-popup: 0; } QComboBox QAbstractItemView { max-height: 200px; }")

    def setup_rtc_second_controls(self):
        self.rtcSecondPushButton = self.ui.findChild(QPushButton, "sendRTCSecondPushButton")
        self.rtcSecondPushButton.clicked.connect(self.send_rtc_second)
        self.rtcSecondComboBox = self.ui.findChild(QComboBox, "rtcSecondComboBox")
        self.rtcSecondComboBox.addItems([str(second) for second in range(0, 60)])
        self.rtcSecondComboBox.setStyleSheet("QComboBox { combobox-popup: 0; } QComboBox QAbstractItemView { max-height: 200px; }")

    def setup_rtc_calibrate_controls(self):
        self.rtcCalibratePushButton = self.ui.findChild(QPushButton, "sendRTCCalibratePushButton")
        self.rtcCalibratePushButton.clicked.connect(self.send_rtc_calibrate)
        self.rtcCalibrateComboBox = self.ui.findChild(QComboBox, "rtcCalibrateComboBox")
        self.rtcCalibrateComboBox.addItems([str(cal) for cal in range(0, 31)])
        self.rtcCalibrateComboBox.setStyleSheet("QComboBox { combobox-popup: 0; } QComboBox QAbstractItemView { max-height: 200px; }")

    def setup_status_controls(self):
        self.setup_status_device_controls()
        self.setup_status_calibration_controls()
        self.setup_status_bootloader_controls()
        self.setup_status_sdcard_controls()
        self.setup_status_remote_controls()

    def setup_status_device_controls(self):
        self.statusDevicePushButton = self.ui.findChild(QPushButton, "readDeviceStatusPushButton")
        self.statusDevicePushButton.clicked.connect(self.read_device_status)

    def setup_status_calibration_controls(self):
        self.statusCalibrationPushButton = self.ui.findChild(QPushButton, "readCalibrationStatusPushButton")
        self.statusCalibrationPushButton.clicked.connect(self.read_calibration_status)

    def setup_status_bootloader_controls(self):
        self.statusBootloaderPushButton = self.ui.findChild(QPushButton, "readBootloaderStatusPushButton")
        self.statusBootloaderPushButton.clicked.connect(self.read_bootloader_status)

    def setup_status_sdcard_controls(self):
        self.statusSdcardPushButton = self.ui.findChild(QPushButton, "readSDCardStatusPushButton")
        self.statusSdcardPushButton.clicked.connect(self.read_sdcard_status)

    def setup_status_remote_controls(self):
        self.statusRemotePushButton = self.ui.findChild(QPushButton, "readRemoteStatusPushButton")
        self.statusRemotePushButton.clicked.connect(self.read_remote_status)

    def setup_potis_controls(self):
        self.poti1PushButton = self.ui.findChild(QPushButton, "poti1PushButton")
        self.poti2PushButton = self.ui.findChild(QPushButton, "poti2PushButton")
        self.poti3PushButton = self.ui.findChild(QPushButton, "poti3PushButton")
        self.poti4PushButton = self.ui.findChild(QPushButton, "poti4PushButton")
        self.readFilterConfigPushButton = self.ui.findChild(QPushButton, "readFilterConfigPushButton")


        self.poti1ComboBox = self.ui.findChild(QComboBox, "poti1ComboBox")
        self.poti2ComboBox = self.ui.findChild(QComboBox, "poti2ComboBox")
        self.poti3ComboBox = self.ui.findChild(QComboBox, "poti3ComboBox")
        self.poti4ComboBox = self.ui.findChild(QComboBox, "poti4ComboBox")

        self.poti1ComboBox.setStyleSheet("QComboBox { combobox-popup: 0; } QComboBox QAbstractItemView { max-height: 200px; }")
        self.poti2ComboBox.setStyleSheet("QComboBox { combobox-popup: 0; } QComboBox QAbstractItemView { max-height: 200px; }")
        self.poti3ComboBox.setStyleSheet("QComboBox { combobox-popup: 0; } QComboBox QAbstractItemView { max-height: 200px; }")
        self.poti4ComboBox.setStyleSheet("QComboBox { combobox-popup: 0; } QComboBox QAbstractItemView { max-height: 200px; }")

        self.poti1ComboBox.addItems([str(val) for val in range(0, 256)])
        self.poti2ComboBox.addItems([str(val) for val in range(0, 256)])
        self.poti3ComboBox.addItems([str(val) for val in range(0, 256)])
        self.poti4ComboBox.addItems([str(val) for val in range(0, 256)])

        self.poti1PushButton.clicked.connect(self.send_poti1)
        self.poti2PushButton.clicked.connect(self.send_poti2)
        self.poti3PushButton.clicked.connect(self.send_poti3)
        self.poti4PushButton.clicked.connect(self.send_poti4)
        self.readFilterConfigPushButton.clicked.connect(self.read_filter_config)

    def _execute_serial_command(self, command, data, log_message):
        if self.serial_manager and self.serial_manager.is_open():
            self.serial_protocol.send_command(command, data)
            self.user_log.append_message(log_message)
        else:
            self.user_log.append_message("Serial port not open")

    def send_poti1(self):
        value = int(self.poti1ComboBox.currentText())
        self._execute_serial_command(CMD_DIGITAL_POTI_1, [value], f"Sent POTI1 cmd with value: {value}\n")

    def send_poti2(self):
        value = int(self.poti2ComboBox.currentText())
        self._execute_serial_command(CMD_DIGITAL_POTI_2, [value], f"Sent POTI2 cmd with value: {value}\n")

    def send_poti3(self):
        value = int(self.poti3ComboBox.currentText())
        self._execute_serial_command(CMD_DIGITAL_POTI_3, [value], f"Sent POTI3 cmd with value: {value}\n")

    def send_poti4(self):
        value = int(self.poti4ComboBox.currentText())
        self._execute_serial_command(CMD_DIGITAL_POTI_4, [value], f"Sent POTI4 cmd with value: {value}\n")

    def read_filter_config(self):
        self._execute_serial_command(CMD_FILTER_REQUEST, [0], "Sent read filter config command\n")
    
    def setup_measurement_controls(self):
        self.measurement1ADCPushButton = self.ui.findChild(QPushButton, "sendAntenna1ADCPushButton")
        self.measurement2ADCPushButton = self.ui.findChild(QPushButton, "sendAntenna2ADCPushButton")
        self.measurement3ADCPushButton = self.ui.findChild(QPushButton, "sendAntenna3ADCPushButton")
        self.measurement4ADCPushButton = self.ui.findChild(QPushButton, "sendAntenna4ADCPushButton")
        self.measurement1FFTPushButton = self.ui.findChild(QPushButton, "sendAntenna1FFTPushButton")
        self.measurement2FFTPushButton = self.ui.findChild(QPushButton, "sendAntenna2FFTPushButton")
        self.measurement3FFTPushButton = self.ui.findChild(QPushButton, "sendAntenna3FFTPushButton")
        self.measurement4FFTPushButton = self.ui.findChild(QPushButton, "sendAntenna4FFTPushButton")
        self.measurementFFTSamplesComboBox = self.ui.findChild(QComboBox, "measurementFFTSamplesComboBox")

        self.measurement1ADCPushButton.clicked.connect(self.send_measurement1_adc)
        self.measurement2ADCPushButton.clicked.connect(self.send_measurement2_adc)
        self.measurement3ADCPushButton.clicked.connect(self.send_measurement3_adc)
        self.measurement4ADCPushButton.clicked.connect(self.send_measurement4_adc)
        self.measurement1FFTPushButton.clicked.connect(self.send_measurement1_fft)
        self.measurement2FFTPushButton.clicked.connect(self.send_measurement2_fft)
        self.measurement3FFTPushButton.clicked.connect(self.send_measurement3_fft)
        self.measurement4FFTPushButton.clicked.connect(self.send_measurement4_fft)

        self.measurementFFTSamplesComboBox.addItems([str(samples) for samples in range(1, 256)])
        self.measurementFFTSamplesComboBox.setStyleSheet("QComboBox { combobox-popup: 0; } QComboBox QAbstractItemView { max-height: 200px; }")
        self.measurementFFTSamplesComboBox.setCurrentIndex(0)

    def send_measurement_adc(self, antenna_cmd, antenna_number):
        self._execute_serial_command(antenna_cmd, [0], f"Sent measurement {antenna_number} ADC command\n")

    def send_measurement_fft(self, antenna_cmd, antenna_number):
        fft_samples = self.get_fft_samples()
        self._execute_serial_command(antenna_cmd, [fft_samples], f"Sent measurement {antenna_number} FFT command with {fft_samples} samples\n")

    def send_measurement1_adc(self):
        self.send_measurement_adc(CMD_START_ADC_MEAS_ANTENNA_1, 1)

    def send_measurement2_adc(self):
        self.send_measurement_adc(CMD_START_ADC_MEAS_ANTENNA_2, 2)

    def send_measurement3_adc(self):
        self.send_measurement_adc(CMD_START_ADC_MEAS_ANTENNA_3, 3)

    def send_measurement4_adc(self):
        self.send_measurement_adc(CMD_START_ADC_MEAS_ANTENNA_4, 4)

    def send_measurement1_fft(self):
        self.send_measurement_fft(CMD_START_FFT_MEAS_ANTENNA_1, 1)

    def send_measurement2_fft(self):
        self.send_measurement_fft(CMD_START_FFT_MEAS_ANTENNA_2, 2)

    def send_measurement3_fft(self):
        self.send_measurement_fft(CMD_START_FFT_MEAS_ANTENNA_3, 3)

    def send_measurement4_fft(self):
        self.send_measurement_fft(CMD_START_FFT_MEAS_ANTENNA_4, 4)

    def get_fft_samples(self):
        return int(self.measurementFFTSamplesComboBox.currentText())
    
    def setup_modem_controls(self):
        self.modemRSSIPushButton = self.ui.findChild(QPushButton, "modemRSSIPushButton")
        self.modemTempPushButton = self.ui.findChild(QPushButton, "modemTempPushButton")
        self.modemSupplyPushButton = self.ui.findChild(QPushButton, "modemSupplyPushButton")
        self.modemATMONPPushButton = self.ui.findChild(QPushButton, "modemATMONPPushButton")
        self.modemdATSMONCPushButton = self.ui.findChild(QPushButton, "modemATSMONCPushButton")
        self.modemATI1PushButton = self.ui.findChild(QPushButton, "modemATI1PushButton")
        self.modemATCOPSPushButton = self.ui.findChild(QPushButton, "modemATCOPSPushButton")

        self.modemRSSIPushButton.clicked.connect(self.send_modem_rssi)
        self.modemTempPushButton.clicked.connect(self.send_modem_temp)
        self.modemSupplyPushButton.clicked.connect(self.send_modem_supply)
        self.modemATMONPPushButton.clicked.connect(self.send_modem_atmonp)
        self.modemdATSMONCPushButton.clicked.connect(self.send_modem_atsmonc)
        self.modemATI1PushButton.clicked.connect(self.send_modem_ati1)
        self.modemATCOPSPushButton.clicked.connect(self.send_modem_atcops)
        
    def send_modem_command(self, command, log_message):
        self._execute_serial_command(command, [0], log_message)

    def send_modem_rssi(self):
        self.send_modem_command(CMD_MODEM_RSSI, "Sent modem RSSI command\n")

    def send_modem_temp(self):
        self.send_modem_command(CMD_MODEM_TEMPERATURE, "Sent modem temperature command\n")

    def send_modem_supply(self):
        self.send_modem_command(CMD_MODEM_BATTERY, "Sent modem supply command\n")

    def send_modem_atmonp(self):
        self.send_modem_command(CMD_MODEM_AT_MONP, "Sent modem ATMONP command\n")

    def send_modem_atsmonc(self):
        self.send_modem_command(CMD_MODEM_AT_SMONC, "Sent modem ATSMONC command\n")

    def send_modem_ati1(self):
        self.send_modem_command(CMD_MODEM_TYPE, "Sent modem ATI1 command\n")

    def send_modem_atcops(self):
        self.send_modem_command(CMD_MODEM_OPERATOR, "Sent modem ATCOPS command\n")

    def setup_var32bits_controls(self):
        self.var8PushButton = self.ui.findChild(QPushButton, "sendVarPushButton")
        self.var8LineEdit = self.ui.findChild(QLineEdit, "var8LineEdit")
        self.var8PushButton.clicked.connect(self.send_var8bits)

    def send_var8bits(self):
        if self.serial_manager and self.serial_manager.is_open():
            value = int(self.var8LineEdit.text())
            if 0 <= value <= 255:
                self.serial_protocol.send_command(CMD_VAR1_UINT32_1, [value])
                self.append_message(f"Sent 8-bit value: {value}\n")
            else:
                self.append_message("Value out of range (0-255)")
        else:
            self.append_message("Serial port not open")

    def setup_remote_controls(self):
        self.remoteLogInPushButton = self.ui.findChild(QPushButton, "remoteLogInPushButton")
        self.remoteLogOutPushButton = self.ui.findChild(QPushButton, "remoteLogOutPushButton")

        self.remoteLogInPushButton.clicked.connect(self.send_remote_log_in)
        self.remoteLogOutPushButton.clicked.connect(self.send_remote_log_out)

    def send_remote_log_in(self):
        if self.serial_manager and self.serial_manager.is_open():
            self.serial_protocol.send_command(CMD_LOG_IN, [0xff])
            self.append_message("Sent remote log in command\n")
        else:
            self.append_message("Serial port not open")

    def send_remote_log_out(self):
        if self.serial_manager and self.serial_manager.is_open():
            self.serial_protocol.send_command(CMD_LOG_OUT, [0xff])
            self.append_message("Sent remote log out command\n")
        else:
            self.append_message("Serial port not open")

    def setup_test_command(self):
        self.testPushButton = self.ui.findChild(QPushButton, "sendTestCmdPushButton")
        self.testPushButton.clicked.connect(self.send_test_command)

    def read_status(self, command, log_message):
        self._execute_serial_command(command, [0], log_message)

    def read_device_status(self):
        self.read_status(CMD_GET_DEVICE_STATUS, "Sent read device status command\n")

    def read_calibration_status(self):
        self.read_status(CMD_START_CALIBRATION, "Sent read calibration status command\n")

    def read_bootloader_status(self):
        self.read_status(CMD_GET_BOOTLOADER_STATUS, "Sent read bootloader status command\n")

    def read_sdcard_status(self):
        self.read_status(CMD_GET_SDCARD_STATUS, "Sent read SD card status command\n")

    def read_remote_status(self):
        self.read_status(CMD_GET_REMOTE_STATUS, "Sent read remote status command\n")
        
    def setup_serial_log(self):
        pass

    def setup_timers(self):
        self.timer = QTimer(self.ui)
        self.timer.timeout.connect(self.update_serial_ports)
        self.timer.start(REFRESH_RATE)

        self.data_timer = QTimer(self.ui)
        self.data_timer.timeout.connect(self.read_serial_data)

    def update_serial_ports(self):
        current_selection = self.serialComboBox.currentText()
        ports = self.serial_manager.get_available_ports()
        self.serialComboBox.clear()

        for device, description in ports:
            display_text = f"{device}: {description}"
            self.serialComboBox.addItem(display_text)

        index = self.serialComboBox.findText(current_selection)
        if index != -1:
            self.serialComboBox.setCurrentIndex(index)
        else:
            self.serialComboBox.setCurrentIndex(0)

    def toggle_serial(self):
        selected_item = self.serialComboBox.currentText()
        com_port = selected_item.split(":")[0].strip()

        if self.serialOpenCloseButton.text() == "Open":
            self.serial_manager.open_serial_port(com_port)
            if self.serial_manager.is_open():
                self.serialConnectedBox.setChecked(True)
                self.serialOpenCloseButton.setText("Close")
                self.serial_protocol = SerialProtocolFmcw(self.serial_manager, self.append_message)
                self.serial_protocol.start()
                self.bms_tab.set_serial_protocol(self.serial_protocol)
        else:
            if self.serial_protocol:
                self.serial_protocol.stop()
                self.serial_protocol = None
                self.bms_tab.set_serial_protocol(None)

            self.serialConnectedBox.setChecked(False)
            self.serial_manager.close_serial_port()
            self.serialOpenCloseButton.setText("Open")

    def send_test_command(self):
        if self.serial_manager and self.serial_manager.is_open():
            self.serial_protocol.send_command(CMD_TEST, [0xff])
            self.append_message("Sent test command\n")
        else:
            self.append_message("Serial port not open")

    def _int_to_bcd(self, value):
        return ((value // 10) << 4) | (value % 10)
    
    def send_rtc_year(self):
        selected_year = int(self.rtcYearComboBox.currentText())
        year_value = selected_year - 2000
        bcd_value = self._int_to_bcd(year_value)
        self._execute_serial_command(CMD_SET_RTC_YEAR, [bcd_value], f"Sent RTC year cmd with value: {selected_year} (BCD: {bcd_value:02X})\n")

    def send_rtc_month(self):
        month_map = {
            "Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4,
            "May": 5, "Jun": 6, "Jul": 7, "Aug": 8,
            "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12
        }
        selected_month = self.rtcMonthComboBox.currentText()
        month_value = month_map[selected_month]
        bcd_value = self._int_to_bcd(month_value)
        self._execute_serial_command(CMD_SET_RTC_MONTH, [bcd_value], f"Sent RTC month cmd with value: {selected_month} (BCD: {bcd_value:02X})\n")

    def send_rtc_day(self):
        selected_day = int(self.rtcDayComboBox.currentText())
        bcd_value = self._int_to_bcd(selected_day)
        self._execute_serial_command(CMD_SET_RTC_DAY, [bcd_value], f"Sent RTC day cmd with value: {selected_day} (BCD: {bcd_value:02X})\n")

    def send_rtc_day_of_week(self):
        day_map = {
            "Mon": 0, "Tue": 1, "Wed": 2, "Thu": 3,
            "Fri": 4, "Sat": 5, "Sun": 6
        }
        selected_day = self.rtcDowComboBox.currentText()
        day_value = day_map[selected_day]
        bcd_value = self._int_to_bcd(day_value)
        self._execute_serial_command(CMD_SET_RTC_DOW, [bcd_value], f"Sent RTC day of week cmd with value: {selected_day} (BCD: {bcd_value:02X})\n")

    def send_rtc_hour(self):
        selected_hour = int(self.rtcHourComboBox.currentText())
        bcd_value = self._int_to_bcd(selected_hour)
        self._execute_serial_command(CMD_SET_RTC_HOUR, [bcd_value], f"Sent RTC hour cmd with value: {selected_hour} (BCD: {bcd_value:02X})\n")

    def send_rtc_minute(self):
        selected_minute = int(self.rtcMinuteComboBox.currentText())
        bcd_value = self._int_to_bcd(selected_minute)
        self._execute_serial_command(CMD_SET_RTC_MINUTE, [bcd_value], f"Sent RTC minute cmd with value: {selected_minute} (BCD: {bcd_value:02X})\n")

    def send_rtc_second(self):
        selected_second = int(self.rtcSecondComboBox.currentText())
        bcd_value = self._int_to_bcd(selected_second)
        self._execute_serial_command(CMD_SET_RTC_SECOND, [bcd_value], f"Sent RTC second cmd with value: {selected_second} (BCD: {bcd_value:02X})\n")

    def send_rtc_calibrate(self):
        selected_cal = int(self.rtcCalibrateComboBox.currentText())
        self._execute_serial_command(CMD_SET_RTC_CALIBRATION, [selected_cal], f"Sent RTC calibrate cmd with value: {selected_cal}\n")

    def append_message(self, message, newline=True):
        if isinstance(message, bytes):
            try:
                message = message.decode('utf-8')
            except UnicodeDecodeError:
                message = repr(message)

        if newline:
            self.serial_log_text_edit.append(message)
        else:
            self.serial_log_text_edit.moveCursor(QTextCursor.End)
            self.serial_log_text_edit.insertPlainText(message)
            self.serial_log_text_edit.moveCursor(QTextCursor.End)

    def read_serial_data(self):
        if self.serial_manager and self.serial_manager.is_open():
            try:
                data = self.serial_manager.read_all()
                if data:
                    self.append_message(data.decode('utf-8'))
            except Exception as e:
                logging.error(f"Failed to read from serial port: {e}")
