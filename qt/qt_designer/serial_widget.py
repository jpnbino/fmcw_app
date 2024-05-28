from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QTimer
from serial_manager import get_available_ports, open_serial_port, close_serial_port

class SerialWidget:
    def __init__(self, ui):
        self.ui = ui
        self.init_ui()

    def init_ui(self):
        self.serialComboBox = self.ui.serialComboBox
        self.serialOpenCloseButton = self.ui.serialOpenCloseButton

        self.update_serial_ports()

        self.serialOpenCloseButton.clicked.connect(self.toggle_serial)

        self.timer = QTimer(self.ui)
        self.timer.timeout.connect(self.update_serial_ports)
        self.timer.start(5000)

    def update_serial_ports(self):
        current_selection = self.serialComboBox.currentText()
        ports = get_available_ports()
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
            self.ui.serial_comm = open_serial_port(com_port)
            if self.ui.serial_comm:
                self.serialOpenCloseButton.setText("Close")
        else:
            close_serial_port(self.ui.serial_comm)
            self.serialOpenCloseButton.setText("Open")
