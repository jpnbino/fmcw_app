from PySide6.QtCore import QTimer, QByteArray, Slot
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QLineEdit,
    QPushButton,
    QStatusBar,
)
from PySide6.QtGui import QTextCursor
from gui.tabbms import BmsTab
from gui.userlog import UserLog
from gui.global_log_manager import log_manager
from serialbsp.commands import *
from serialbsp.protocol_fmcw import SerialProtocolFmcw

REFRESH_RATE = 5000
MESSAGE_DURATION = 5000

class MainTab:
    def __init__(self, ui, bms_config):
        self.ui = ui
        self.serial_manager = self.ui.fmcw_serial_manager
        self.serial_protocol = SerialProtocolFmcw()
        self.init_ui()
        self.bms_tab = BmsTab(ui, bms_config, log_manager.log_message)

        self.cmd_start_adc_meas_antenna_1 = get_command_by_name("CMD_START_ADC_MEAS_ANTENNA_1")
        self.cmd_start_adc_meas_antenna_2 = get_command_by_name("CMD_START_ADC_MEAS_ANTENNA_2")
        self.cmd_start_adc_meas_antenna_3 = get_command_by_name("CMD_START_ADC_MEAS_ANTENNA_3")
        self.cmd_start_adc_meas_antenna_4 = get_command_by_name("CMD_START_ADC_MEAS_ANTENNA_4")
        self.cmd_start_fft_meas_antenna_1 = get_command_by_name("CMD_START_FFT_MEAS_ANTENNA_1")
        self.cmd_start_fft_meas_antenna_2 = get_command_by_name("CMD_START_FFT_MEAS_ANTENNA_2")
        self.cmd_start_fft_meas_antenna_3 = get_command_by_name("CMD_START_FFT_MEAS_ANTENNA_3")
        self.cmd_start_fft_meas_antenna_4 = get_command_by_name("CMD_START_FFT_MEAS_ANTENNA_4")

        self.cmd_var1_uint32_1 = get_command_by_name("CMD_VAR1_UINT32_1")

        self.cmd_modem_rssi = get_command_by_name("CMD_MODEM_RSSI")
        self.cmd_modem_temperature = get_command_by_name("CMD_MODEM_TEMPERATURE")
        self.cmd_modem_battery = get_command_by_name("CMD_MODEM_BATTERY")
        self.cmd_modem_at_monp = get_command_by_name("CMD_MODEM_AT_MONP")
        self.cmd_modem_at_smonc = get_command_by_name("CMD_MODEM_AT_SMONC")
        self.cmd_modem_type = get_command_by_name("CMD_MODEM_TYPE")
        self.cmd_modem_operator = get_command_by_name("CMD_MODEM_OPERATOR")

        self.cmd_start_calibration = get_command_by_name("CMD_START_CALIBRATION")    
        self.cmd_digital_poti_1 = get_command_by_name("CMD_DIGITAL_POTI_1")
        self.cmd_digital_poti_2 = get_command_by_name("CMD_DIGITAL_POTI_2")
        self.cmd_digital_poti_3 = get_command_by_name("CMD_DIGITAL_POTI_3")
        self.cmd_digital_poti_4 = get_command_by_name("CMD_DIGITAL_POTI_4")
        self.cmd_filter_request = get_command_by_name("CMD_FILTER_REQUEST")
        self.cmd_get_device_status = get_command_by_name("CMD_GET_DEVICE_STATUS")
        self.cmd_get_bootloader_status = get_command_by_name("CMD_GET_BOOTLOADER_STATUS")
        self.cmd_get_sdcard_status = get_command_by_name("CMD_GET_SDCARD_STATUS")
        self.cmd_get_remote_status = get_command_by_name("CMD_GET_REMOTE_STATUS")
        self.cmd_log_in = get_command_by_name("CMD_LOG_IN")
        self.cmd_log_out = get_command_by_name("CMD_LOG_OUT")
        self.cmd_test = get_command_by_name("CMD_TEST")
        self.cmd_set_rtc_year = get_command_by_name("CMD_SET_RTC_YEAR")
        self.cmd_set_rtc_month = get_command_by_name("CMD_SET_RTC_MONTH")
        self.cmd_set_rtc_day = get_command_by_name("CMD_SET_RTC_DAY")
        self.cmd_set_rtc_dow = get_command_by_name("CMD_SET_RTC_DOW")
        self.cmd_set_rtc_hour = get_command_by_name("CMD_SET_RTC_HOUR")
        self.cmd_set_rtc_minute = get_command_by_name("CMD_SET_RTC_MINUTE")
        self.cmd_set_rtc_second = get_command_by_name("CMD_SET_RTC_SECOND")
        self.cmd_set_rtc_calibration = get_command_by_name("CMD_SET_RTC_CALIBRATION")
        self.cmd_set_rtc_dow = get_command_by_name("CMD_SET_RTC_DOW")

        #  Connect SerialManager's data_received to the protocol handler
        self.serial_manager.data_received.connect(
            self.serial_protocol.handle_raw_data
        )
        #  Connect protocol's command_encoded signal to SerialManager's send_data
        self.serial_protocol.command_encoded.connect(self.serial_manager.send_data)
        self.serial_protocol.command_encoded.connect(self._send_encoded_data)
        self.serial_protocol.log_message.connect(log_manager.log_message)
      
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
        self.setup_timers()


    def setup_serial_controls(self):
        self.serialComboBox = self.ui.findChild(QComboBox, "serialComboBox")
        self.serialOpenCloseButton = self.ui.findChild(QPushButton, "serialOpenCloseButton")
        self.serialConnectedBox = self.ui.findChild(QCheckBox, "bitPortConnected")
        self.serialOpenCloseButton.clicked.connect(self.toggle_serial)
        self.update_serial_ports()
        self.serial_manager.connection_status_changed.connect(self.update_connection_status)
        self.serial_manager.error_occurred.connect(self.log_serial_error)

    @Slot(bytes)
    def handle_serial_data(self, raw_data: bytes):
        """
        Handles raw data received from the SerialManager.

        This method is connected to the SerialManager's data_received signal.
        It passes the data to the SerialProtocolFmcw for processing.
        """
        self.serial_protocol.handle_raw_data(raw_data)

    @Slot(bool)
    def update_connection_status(self, is_connected: bool):
        """Updates the UI based on the serial connection status."""
        self.serialConnectedBox.setChecked(is_connected)
        if is_connected:
            self.serialOpenCloseButton.setText("Close")
            self.serialComboBox.setEnabled(False)
            self.statusBar.showMessage("Serial port connected", MESSAGE_DURATION)
        else:
            self.serialOpenCloseButton.setText("Open")
            self.serialComboBox.setEnabled(True)
            self.statusBar.showMessage("Serial port disconnected", MESSAGE_DURATION)

    @Slot(str)
    def log_serial_error(self, error_message: str):
        """Logs serial port errors to the user log."""
        log_manager.log_message(f"Serial Error: {error_message}")

    @Slot(QByteArray)
    def _send_encoded_data(self, encoded_data: QByteArray):
        """
        Sends the already encoded data (including CRC) via the serial manager.
        This slot is connected to the serial_protocol's command_encoded signal.
        """
        self.serial_manager.send_data(bytes(encoded_data))
        hex_values = " ".join(f"0x{byte:02X}" for byte in bytes(encoded_data))
        log_manager.log_message(f"Sent encoded data: {hex_values}\n")

    def setup_timers(self):
        self.timer = QTimer(self.ui)
        self.timer.timeout.connect(self.update_serial_ports)
        self.timer.start(REFRESH_RATE)

    def update_serial_ports(self):
        """Populates the serial port combo box with available ports."""
        available_ports = self.serial_manager.get_available_ports()
        self.serialComboBox.clear()
        for port, description in available_ports:
            self.serialComboBox.addItem(f"{port} - {description}", port)

    def toggle_serial(self):
        """Opens or closes the serial port based on its current state."""
        if self.serial_manager.is_open():
            self.serial_manager.close_serial_port()
        else:
            selected_port = self.serialComboBox.currentData()
            if selected_port:
                self.serial_manager.open_serial_port(selected_port)
            else:
                self.statusBar.showMessage("No serial port selected", MESSAGE_DURATION)
     
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

        self.poti1ComboBox.addItems([str(val) for val in range(0, 256)])
        self.poti2ComboBox.addItems([str(val) for val in range(0, 256)])
        self.poti3ComboBox.addItems([str(val) for val in range(0, 256)])
        self.poti4ComboBox.addItems([str(val) for val in range(0, 256)])

        self.poti1PushButton.clicked.connect(self.send_poti1)
        self.poti2PushButton.clicked.connect(self.send_poti2)
        self.poti3PushButton.clicked.connect(self.send_poti3)
        self.poti4PushButton.clicked.connect(self.send_poti4)
        self.readFilterConfigPushButton.clicked.connect(self.read_filter_config)

    def _encode_and_send(self, command: Command, data: list[int], log_message: str) -> None:
        """
        Encodes the command and data, sends it via the serial manager, and logs the message.
        """
        if self.serial_manager.is_open():
            self.serial_protocol.encode_command(command, data)
            log_manager.log_message(log_message)
        else:
            log_manager.log_message("Serial port not open")

    def send_poti1(self):
        value = int(self.poti1ComboBox.currentText())
        self._encode_and_send(self.cmd_digital_poti_1, [value], f"Sent POTI1 cmd with value: {value}\n")

    def send_poti2(self):
        value = int(self.poti2ComboBox.currentText())
        self._encode_and_send(self.cmd_digital_poti_2, [value], f"Sent POTI2 cmd with value: {value}\n")

    def send_poti3(self):
        value = int(self.poti3ComboBox.currentText())
        self._encode_and_send(self.cmd_digital_poti_3, [value], f"Sent POTI3 cmd with value: {value}\n")

    def send_poti4(self):
        value = int(self.poti4ComboBox.currentText())
        self._encode_and_send(self.cmd_digital_poti_4, [value], f"Sent POTI4 cmd with value: {value}\n")

    def read_filter_config(self):
        self._encode_and_send(self.cmd_filter_request, [0], "Sent read filter config command\n")
    
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
        self._encode_and_send(antenna_cmd, [0], f"Sent measurement {antenna_number} ADC command\n")

    def send_measurement_fft(self, antenna_cmd, antenna_number):
        fft_samples = self.get_fft_samples()
        self._encode_and_send(antenna_cmd, [fft_samples], f"Sent measurement {antenna_number} FFT command with {fft_samples} samples\n")

    def send_measurement1_adc(self):
        self.send_measurement_adc(self.cmd_start_adc_meas_antenna_1, 1)

    def send_measurement2_adc(self):
        self.send_measurement_adc(self.cmd_start_adc_meas_antenna_2, 2)

    def send_measurement3_adc(self):
        self.send_measurement_adc(self.cmd_start_adc_meas_antenna_3, 3)

    def send_measurement4_adc(self):
        self.send_measurement_adc(self.cmd_start_adc_meas_antenna_4, 4)

    def send_measurement1_fft(self):
        self.send_measurement_fft(self.cmd_start_fft_meas_antenna_1, 1)

    def send_measurement2_fft(self):
        self.send_measurement_fft(self.cmd_start_fft_meas_antenna_2, 2)

    def send_measurement3_fft(self):
        self.send_measurement_fft(self.cmd_start_fft_meas_antenna_3, 3)

    def send_measurement4_fft(self):
        self.send_measurement_fft(self.cmd_start_fft_meas_antenna_4, 4)

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
        self._encode_and_send(command, [0], log_message)

    def send_modem_rssi(self):
        self.send_modem_command(self.cmd_modem_rssi, "Sent modem RSSI command\n")

    def send_modem_temp(self):
        self.send_modem_command(self.cmd_modem_temperature, "Sent modem temperature command\n")

    def send_modem_supply(self):
        self.send_modem_command(self.cmd_modem_battery, "Sent modem supply command\n")

    def send_modem_atmonp(self):
        self.send_modem_command(self.cmd_modem_at_monp, "Sent modem ATMONP command\n")

    def send_modem_atsmonc(self):
        self.send_modem_command(self.cmd_modem_at_smonc, "Sent modem ATSMONC command\n")

    def send_modem_ati1(self):
        self.send_modem_command(self.cmd_modem_type, "Sent modem ATI1 command\n")

    def send_modem_atcops(self):
        self.send_modem_command(self.cmd_modem_operator, "Sent modem ATCOPS command\n")

    def setup_var32bits_controls(self):
        self.var8PushButton = self.ui.findChild(QPushButton, "sendVarPushButton")
        self.var8LineEdit = self.ui.findChild(QLineEdit, "var8LineEdit")
        self.var8PushButton.clicked.connect(self.send_var8bits)

    def send_var8bits(self):
        value = int(self.var8LineEdit.text())
        if 0 <= value <= 255:
            self._encode_and_send(self.cmd_var1_uint32_1, [value])
            log_manager.log_message(f"Sent 8-bit value: {value}\n")
        else:
            log_manager.log_message("Value out of range (0-255)")

    def setup_remote_controls(self):
        self.remoteLogInPushButton = self.ui.findChild(QPushButton, "remoteLogInPushButton")
        self.remoteLogOutPushButton = self.ui.findChild(QPushButton, "remoteLogOutPushButton")
        self.remoteLogInPushButton.clicked.connect(self.send_remote_log_in)
        self.remoteLogOutPushButton.clicked.connect(self.send_remote_log_out)

    def send_remote(self, command, log_message):
            self._encode_and_send(command, [0xff])
            log_manager.log_message(log_message)

    def send_remote_log_in(self):
        self.send_remote(CMD_LOG_IN, "Sent remote log in command\n")

    def send_remote_log_out(self):
        self.send_remote(CMD_LOG_OUT, "Sent remote log out command\n")

    def setup_test_command(self):
        self.testPushButton = self.ui.findChild(QPushButton, "sendTestCmdPushButton")
        self.testPushButton.clicked.connect(self.send_test_command)

    def read_status(self, command: Command, log_message):
        self._encode_and_send(command, [0], log_message)

    def read_device_status(self):
        self.read_status(self.cmd_get_device_status, "Sent read device status command\n")

    def read_calibration_status(self):
        self.read_status(self.cmd_start_calibration, "Sent read calibration status command\n")

    def read_bootloader_status(self):
        self.read_status(self.cmd_get_bootloader_status, "Sent read bootloader status command\n")

    def read_sdcard_status(self):
        self.read_status(self.cmd_get_sdcard_status, "Sent read SD card status command\n")

    def read_remote_status(self):
        self.read_status(self.cmd_get_remote_status, "Sent read remote status command\n")

    def send_test_command(self):
        self._encode_and_send(self.cmd_test, [0xff], "Sent test command\n")

    def _int_to_bcd(self, value):
        return ((value // 10) << 4) | (value % 10)
    
    def send_rtc_year(self):
        selected_year = int(self.rtcYearComboBox.currentText())
        year_value = selected_year - 2000
        bcd_value = self._int_to_bcd(year_value)
        self._encode_and_send(self.cmd_set_rtc_year, [bcd_value], f"Sent RTC year cmd with value: {selected_year} (BCD: {bcd_value:02X})\n")

    def send_rtc_month(self):
        month_map = {
            "Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4,
            "May": 5, "Jun": 6, "Jul": 7, "Aug": 8,
            "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12
        }
        selected_month = self.rtcMonthComboBox.currentText()
        month_value = month_map[selected_month]
        bcd_value = self._int_to_bcd(month_value)
        self._encode_and_send(self.cmd_set_rtc_month, [bcd_value], f"Sent RTC month cmd with value: {selected_month} (BCD: {bcd_value:02X})\n")

    def send_rtc_day(self):
        selected_day = int(self.rtcDayComboBox.currentText())
        bcd_value = self._int_to_bcd(selected_day)
        self._encode_and_send(self.cmd_set_rtc_day, [bcd_value], f"Sent RTC day cmd with value: {selected_day} (BCD: {bcd_value:02X})\n")

    def send_rtc_day_of_week(self):
        day_map = {
            "Mon": 0, "Tue": 1, "Wed": 2, "Thu": 3,
            "Fri": 4, "Sat": 5, "Sun": 6
        }
        selected_day = self.rtcDowComboBox.currentText()
        day_value = day_map[selected_day]
        bcd_value = self._int_to_bcd(day_value)
        self._encode_and_send(self.cmd_set_rtc_dow, [bcd_value], f"Sent RTC day of week cmd with value: {selected_day} (BCD: {bcd_value:02X})\n")

    def send_rtc_hour(self):
        selected_hour = int(self.rtcHourComboBox.currentText())
        bcd_value = self._int_to_bcd(selected_hour)
        self._encode_and_send(self.cmd_set_rtc_hour, [bcd_value], f"Sent RTC hour cmd with value: {selected_hour} (BCD: {bcd_value:02X})\n")

    def send_rtc_minute(self):
        selected_minute = int(self.rtcMinuteComboBox.currentText())
        bcd_value = self._int_to_bcd(selected_minute)
        self._encode_and_send(self.cmd_set_rtc_minute, [bcd_value], f"Sent RTC minute cmd with value: {selected_minute} (BCD: {bcd_value:02X})\n")

    def send_rtc_second(self):
        selected_second = int(self.rtcSecondComboBox.currentText())
        bcd_value = self._int_to_bcd(selected_second)
        self._encode_and_send(self.cmd_set_rtc_second, [bcd_value], f"Sent RTC second cmd with value: {selected_second} (BCD: {bcd_value:02X})\n")

    def send_rtc_calibrate(self):
        selected_cal = int(self.rtcCalibrateComboBox.currentText())
        self._encode_and_send(self.cmd_set_rtc_year, [selected_cal], f"Sent RTC calibrate cmd with value: {selected_cal}\n")
    