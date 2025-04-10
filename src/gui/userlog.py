from PySide6.QtWidgets import (
    QWidget,
    QTextEdit,
    QPushButton,
)
from PySide6.QtCore import Signal, Slot

class UserLog(QWidget):
    message_received = Signal(str)

    def __init__(self, ui, parent=None):
        super().__init__(parent)
        self.ui = ui
        self.init_ui()
        self.init_connections()

    def init_ui(self):
        self.serial_log_text_edit = self.ui.findChild(QTextEdit, "serialLogTextEdit")
        self.serial_log_clear_button = self.ui.findChild(QPushButton, "serialLogClearPushButton")
        self.serial_log_clear_button.clicked.connect(self.serial_log_text_edit.clear)


    def init_connections(self):
        self.serial_log_clear_button.clicked.connect(self.clear_log)
        self.message_received.connect(self.append_message)

    @Slot(str)
    def append_message(self, message):
        self.serial_log_text_edit.append(message)

    @Slot()
    def clear_log(self):
        self.serial_log_text_edit.clear()