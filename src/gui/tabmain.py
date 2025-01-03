from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QComboBox, QPushButton, QStatusBar, QTextEdit
from PySide6.QtGui import QTextCursor
from serialbsp.protocol_fmcw import CMD_TEST, SET_RTC_YEAR, SerialProtocolFmcw


REFRESH_RATE = 5000
MESSAGE_DURATION = 5000


class MainTab:
    def __init__(self, ui):
        self.ui = ui
        self.serial_manager = self.ui.fmcw_serial_manager
        self.serial_protocol = None
        self.init_ui()


    def init_ui(self):
        self.statusBar = self.ui.findChild(QStatusBar, "statusBar")
        self.serialComboBox = self.ui.findChild(QComboBox, "serialComboBox")
        self.serialOpenCloseButton = self.ui.findChild(QPushButton, "serialOpenCloseButton")

        self.update_serial_ports()

        self.serialOpenCloseButton.clicked.connect(self.toggle_serial)

        self.timer = QTimer(self.ui)
        self.timer.timeout.connect(self.update_serial_ports)
        self.timer.start(REFRESH_RATE)

        self.rtcYearPushButton = self.ui.findChild(QPushButton, "sendRTCYearPushButton")
        self.rtcYearPushButton.clicked.connect(self.send_rtc_year)

        self.serial_log_text_edit = self.ui.findChild(QTextEdit, "serialLogTextEdit")

        # Set up a timer to periodically check for new data
        self.data_timer = QTimer(self.ui)
        self.data_timer.timeout.connect(self.read_serial_data)

    def update_serial_ports(self):
        current_selection = self.serialComboBox.currentText()
        ports = self.serial_manager.get_available_ports()
        self.serialComboBox.clear()

        # Repopulate the combo box
        for device, description in ports:
            display_text = f"{device}: {description}"
            self.serialComboBox.addItem(display_text)

        # Restore the previous selection if it still exists
        index = self.serialComboBox.findText(current_selection)
        if index != -1:
            self.serialComboBox.setCurrentIndex(index)
        else:
            self.serialComboBox.setCurrentIndex(0)

    def toggle_serial(self):
        selected_item = self.serialComboBox.currentText()
        com_port = selected_item.split(":")[0].strip()  # Extract the port device name

        if self.serialOpenCloseButton.text() == "Open":
            self.serial_manager.open_serial_port(com_port)
            if self.serial_manager.is_open():
                self.serialOpenCloseButton.setText("Close")
                self.serial_protocol = SerialProtocolFmcw(self.serial_manager,  self.append_serial_log)
                self.serial_protocol.start()
                #self.statusBar.showMessage(f"Serial port {com_port} opened successfully.", MESSAGE_DURATION)
        else:
            if self.serial_protocol:
                self.serial_protocol.stop()
            self.serial_manager.close_serial_port()
            self.serialOpenCloseButton.setText("Open")
            #self.statusBar.showMessage(f"Serial port {com_port} closed successfully.", MESSAGE_DURATION)

    def send_rtc_year(self):
        if self.serial_manager and self.serial_manager.is_open():
            
            self.serial_protocol.send_command(CMD_TEST, [0xff])
            self.append_serial_log("Sent RTC year command")
        else:
            self.append_serial_log("Serial port not open")

    def append_serial_log(self, message, newline=True):
        if isinstance(message, bytes):
            message = message.decode('utf-8')  # Decode bytes to string
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
