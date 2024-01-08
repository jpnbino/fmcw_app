from PySide6.QtUiTools import loadUiType
from qtpy.QtWidgets import QApplication, QMainWindow
from qtpy.QtCore import QFile, QIODevice
from qtpy.QtGui import QIcon
import sys

from bms_configuration import BMSConfiguration
from bms_gui import BMSGUI
from serial_communication import SerialCommunication

from serial.tools import list_ports

Ui_MainWindow, _ = loadUiType("app/qt/qt_designer/fmcw.ui") 

class SerialGUI():
    def __init__(self,  ui):
        self.ui = ui
        self.update_serial_ports()
        self.ui.serialOpenCloseButton.clicked.connect(self.toggle_serial)

        # Create a serial communication instance
        self.serial_comm = SerialCommunication()

    def update_serial_ports(self):
        ports = list_ports.comports()
        self.ui.serialComboBox.clear()
        for port in ports:
            description = port.description if port.description else "No description"
            self.ui.serialComboBox.addItem(f"{port.device}: {description}")

        

    def toggle_serial(self):
        selected_item = self.ui.serialComboBox.currentText()
        com_port = selected_item.split(":")[0].strip()

        if self.ui.serialOpenCloseButton.text() == "Open":
            try:
                self.serial_comm.open_serial(com_port)
                self.ui.serialOpenCloseButton.setText("Close")
            except Exception as e:
                print(f"Error opening serial port: {e}")
        else:
            self.serial_comm.close_serial()
            self.ui.serialOpenCloseButton.setText("Open")


class FMCWApplication(QMainWindow, Ui_MainWindow ):
    def __init__(self, ui_file_name):
        super().__init__()

        #Setup the user interface
        self.setupUi(self)

        # Set the window title
        self.setWindowTitle("FMCW Application")

        # Set the application icon for the window and taskbar
        icon_path = "app/images/icons/icon_circle.png"  # Replace this with the path to your icon file
        self.setWindowIcon(QIcon(icon_path))
                           
        # Initialize bms_config as an instance of BMSConfiguration
        self.bms_config = BMSConfiguration()
        
        # Initialize BMSGUI
        self.gui = BMSGUI(self, self.bms_config)


        # Serial Configuration Widget
        self.serial_widget = SerialGUI(self)

        # Set the initial size of the window
        self.resize(1200,800)

        # Adjust the window size to fit its contents
        #self.adjustSize()

        # Set the central widget and show the main window
        #self.setCentralWidget(self.ui)
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Some code to obtain the form file name, ui_file_name
    ui_file_name = "qt/qt_designer/fmcw.ui"

    # Create an instance of the FMCWApplication class
    fmcw_app = FMCWApplication(ui_file_name)

    sys.exit(app.exec_())
