from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QComboBox, QPushButton, QStatusBar, QTextEdit
from PySide6.QtGui import QTextCursor
from serialbsp.protocol_fmcw import (
    CMD_GET_BOOTLOADER_STATUS, CMD_GET_DEVICE_STATUS, CMD_GET_REMOTE_STATUS, CMD_GET_SDCARD_STATUS, CMD_START_CALIBRATION, CMD_TEST, CMD_SET_RTC_CALIBRATION, CMD_SET_RTC_DAY, CMD_SET_RTC_DOW, CMD_SET_RTC_HOUR,
    CMD_SET_RTC_MINUTE, CMD_SET_RTC_MONTH, CMD_SET_RTC_SECOND, CMD_SET_RTC_YEAR, SerialProtocolFmcw
)

REFRESH_RATE = 5000
MESSAGE_DURATION = 5000

class MainTab:
    def __init__(self, ui):
        self.ui = ui
        self.serial_manager = self.ui.fmcw_serial_manager
        self.serial_protocol = None
        self.init_ui()

    def init_ui(self):
        self.setup_status_bar()
        self.setup_serial_controls()
        self.setup_rtc_controls()
        self.setup_serial_log()
        self.setup_timers()

    def setup_status_bar(self):
        self.statusBar = self.ui.findChild(QStatusBar, "statusBar")

    def setup_serial_controls(self):
        self.serialComboBox = self.ui.findChild(QComboBox, "serialComboBox")
        self.serialOpenCloseButton = self.ui.findChild(QPushButton, "serialOpenCloseButton")
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
        self.statusSdcardPushButton = self.ui.findChild(QPushButton, "readSdcardStatusPushButton")
        self.statusSdcardPushButton.clicked.connect(self.read_sdcard_status)

    def setup_status_remote_controls(self):
        self.statusRemotePushButton = self.ui.findChild(QPushButton, "readRemoteStatusPushButton")
        self.statusRemotePushButton.clicked.connect(self.read_remote_status)

    def read_device_status(self):
        if self.serial_manager and self.serial_manager.is_open():
            self.serial_protocol.send_command(CMD_GET_DEVICE_STATUS, [])
            self.append_serial_log("Sent read device status command\n")
        else:
            self.append_serial_log("Serial port not open")

    def read_calibration_status(self):
        if self.serial_manager and self.serial_manager.is_open():
            self.serial_protocol.send_command(CMD_START_CALIBRATION, [])
            self.append_serial_log("Sent read calibration status command\n")
        else:
            self.append_serial_log("Serial port not open")

    def read_bootloader_status(self):
        if self.serial_manager and self.serial_manager.is_open():
            self.serial_protocol.send_command(CMD_GET_BOOTLOADER_STATUS, [])
            self.append_serial_log("Sent read bootloader status command\n")

    def read_sdcard_status(self):
        if self.serial_manager and self.serial_manager.is_open():
            self.serial_protocol.send_command(CMD_GET_SDCARD_STATUS, [])
            self.append_serial_log("Sent read SD card status command\n")

    def read_remote_status(self):
        if self.serial_manager and self.serial_manager.is_open():
            self.serial_protocol.send_command(CMD_GET_REMOTE_STATUS, [])
            self.append_serial_log("Sent read remote status command\n")
        

    def setup_serial_log(self):
        self.serial_log_text_edit = self.ui.findChild(QTextEdit, "serialLogTextEdit")

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
                self.serialOpenCloseButton.setText("Close")
                self.serial_protocol = SerialProtocolFmcw(self.serial_manager, self.append_serial_log)
                self.serial_protocol.start()
        else:
            if self.serial_protocol:
                self.serial_protocol.stop()
            self.serial_manager.close_serial_port()
            self.serialOpenCloseButton.setText("Open")

    def send_test_command(self):
        if self.serial_manager and self.serial_manager.is_open():
            self.serial_protocol.send_command(CMD_TEST, [0xff])
            self.append_serial_log("Sent test command\n")
        else:
            self.append_serial_log("Serial port not open")

    def send_rtc_year(self):
        if self.serial_manager and self.serial_manager.is_open():
            selected_year = int(self.rtcYearComboBox.currentText())
            year_value = selected_year - 2000
            bcd_value = ((year_value // 10) << 4) | (year_value % 10)
            self.serial_protocol.send_command(CMD_SET_RTC_YEAR, [bcd_value])
            self.append_serial_log(f"Sent RTC year cmd with value: {selected_year} (BCD: {bcd_value:02X})\n")
        else:
            self.append_serial_log("Serial port not open")

    def send_rtc_month(self):
        if self.serial_manager and self.serial_manager.is_open():
            month_map = {
                "Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4,
                "May": 5, "Jun": 6, "Jul": 7, "Aug": 8,
                "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12
            }
            selected_month = self.rtcMonthComboBox.currentText()
            month_value = month_map[selected_month]
            bcd_value = ((month_value // 10) << 4) | (month_value % 10)
            self.serial_protocol.send_command(CMD_SET_RTC_MONTH, [bcd_value])
            self.append_serial_log(f"Sent RTC month cmd with value: {selected_month} (BCD: {bcd_value:02X})\n")
        else:
            self.append_serial_log("Serial port not open")

    def send_rtc_day(self):
        if self.serial_manager and self.serial_manager.is_open():
            selected_day = int(self.rtcDayComboBox.currentText())
            bcd_value = ((selected_day // 10) << 4) | (selected_day % 10)
            self.serial_protocol.send_command(CMD_SET_RTC_DAY, [bcd_value])
            self.append_serial_log(f"Sent RTC day cmd with value: {selected_day} (BCD: {bcd_value:02X})\n")
        else:
            self.append_serial_log("Serial port not open")

    def send_rtc_day_of_week(self):
        if self.serial_manager and self.serial_manager.is_open():
            day_map = {
                "Mon": 0, "Tue": 1, "Wed": 2, "Thu": 3,
                "Fri": 4, "Sat": 5, "Sun": 6
            }
            selected_day = self.rtcDowComboBox.currentText()
            day_value = day_map[selected_day]
            bcd_value = ((day_value // 10) << 4) | (day_value % 10)
            self.serial_protocol.send_command(CMD_SET_RTC_DOW, [bcd_value])
            self.append_serial_log(f"Sent RTC day of week cmd with value: {selected_day} (BCD: {bcd_value:02X})\n")
        else:
            self.append_serial_log("Serial port not open")

    def send_rtc_hour(self):
        if self.serial_manager and self.serial_manager.is_open():
            selected_hour = int(self.rtcHourComboBox.currentText())
            bcd_value = ((selected_hour // 10) << 4) | (selected_hour % 10)
            self.serial_protocol.send_command(CMD_SET_RTC_HOUR, [bcd_value])
            self.append_serial_log(f"Sent RTC hour cmd with value: {selected_hour} (BCD: {bcd_value:02X})\n")
        else:
            self.append_serial_log("Serial port not open")

    def send_rtc_minute(self):
        if self.serial_manager and self.serial_manager.is_open():
            selected_minute = int(self.rtcMinuteComboBox.currentText())
            bcd_value = ((selected_minute // 10) << 4) | (selected_minute % 10)
            self.serial_protocol.send_command(CMD_SET_RTC_MINUTE, [bcd_value])
            self.append_serial_log(f"Sent RTC minute cmd with value: {selected_minute} (BCD: {bcd_value:02X})\n")
        else:
            self.append_serial_log("Serial port not open")

    def send_rtc_second(self):
        if self.serial_manager and self.serial_manager.is_open():
            selected_second = int(self.rtcSecondComboBox.currentText())
            bcd_value = ((selected_second // 10) << 4) | (selected_second % 10)
            self.serial_protocol.send_command(CMD_SET_RTC_SECOND, [bcd_value])
            self.append_serial_log(f"Sent RTC second cmd with value: {selected_second} (BCD: {bcd_value:02X})\n")
        else:
            self.append_serial_log("Serial port not open")

    def send_rtc_calibrate(self):
        if self.serial_manager and self.serial_manager.is_open():
            selected_cal = int(self.rtcCalibrateComboBox.currentText())
            self.serial_protocol.send_command(CMD_SET_RTC_CALIBRATION, [selected_cal])
            self.append_serial_log(f"Sent RTC calibrate cmd with value: {selected_cal}\n")
        else:
            self.append_serial_log("Serial port not open")


    def append_serial_log(self, message, newline=True):
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
                    self.append_serial_log(data.decode('utf-8'))
            except Exception as e:
                logging.error(f"Failed to read from serial port: {e}")
