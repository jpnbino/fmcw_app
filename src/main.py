import os
import sys
import logging


from PySide6.QtGui import QIcon, QFont, QFontDatabase
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QSpinBox, QStatusBar, QScrollArea, QCheckBox
from PySide6.QtCore import QFile, QIODevice, Qt

from config.app_config import WINDOW_TITLE, ICON_PATH, UI_FILE_PATH, get_resource_path
from bms.isl94203_driver import ISL94203Driver
from gui.tabbms import BmsTab
from gui.tabmain import MainTab
from gui.global_log_manager import log_manager
from gui.global_status_bar_manager import status_bar_manager
from gui.userlog import UserLog


from serialbsp.serial_manager import SerialManager
from serialbsp.protocol_fmcw import SerialProtocolFmcw

from logger.logging_config import configure_logging


def main():
    configure_logging()
    logging.info("Application started")

    # Set the Qt::AA_ShareOpenGLContexts attribute before creating the QApplication instance
    QApplication.setAttribute(Qt.AA_ShareOpenGLContexts)

    app = QApplication(sys.argv)

    # Load and set Roboto font
    stylesheet_path = get_resource_path("qt/resources/stylesheet.qss")

    with open(stylesheet_path, "r") as f:
            custom_stylesheet = f.read()
    app.setStyleSheet(app.styleSheet() + custom_stylesheet)

    font_path = get_resource_path("qt/fonts/Roboto/Roboto-Regular.ttf")

    if os.path.exists(font_path):
        print(f"Font file found at: {font_path}")
        font_id = QFontDatabase.addApplicationFont(font_path)
        if font_id != -1:
            font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
            roboto_font = QFont(font_family)
            roboto_font.setPointSize(9)
            app.setFont(roboto_font)
            print(f"Roboto font applied: {font_family}")
        else:
            print("Failed to load Roboto font")
    else:
        print(f"Font file not found at: {font_path}")

    try:
        # Load the UI file using QUiLoader
        ui_file = QFile(UI_FILE_PATH)
        if not ui_file.open(QIODevice.ReadOnly):
            print(f"Cannot open {UI_FILE_PATH}: {ui_file.errorString()}")
            sys.exit(-1)
        loader = QUiLoader()
        window = loader.load(ui_file)
        ui_file.close()
        if not window:
            print(loader.errorString())
            sys.exit(-1)

        checkbox_names = ["bitCharging","bitDischarging","bitEOC", 
                           "bitChargerOn","bitLoadOn",
                           "bitCOC", "bitDOC", "bitDSC", 
                           "bitOV", "bitUV", "bitOVLO", "bitUVLO",
                           "bitCBOV", "bitCBUV", "bitLVCHRG",
                           "bitCOT","bitCUT","bitCBOT","bitCBUT",
                           "bitDOT", "bitDUT", "bitIOT",
                           "bitIDLE", "bitDOZE", "bitSLEEP",
                           "bitCELLF", "bitOPEN", "bitPortConnected"]
        for name in checkbox_names:
            checkbox = window.findChild(QCheckBox, name)
            if checkbox:
                checkbox.setProperty("class", "bit-indicator")
                checkbox.setEnabled(False)
                
        # Set up the main window
        fmcw_app = FMCWApplication(window)
        fmcw_app.show()

        sys.exit(app.exec())
    except Exception as e:
        logging.error(f"Failed to start the application: {e}")
        sys.exit(1)

class FMCWApplication(QMainWindow):
    def __init__(self, window):
        super().__init__()
  
        self.setCentralWidget(window)
        self.setWindowTitle(WINDOW_TITLE)
        self.setWindowIcon(QIcon(ICON_PATH))

        # Enable scrolling
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(window)
        self.setCentralWidget(self.scroll_area)

        # Initialize SerialManager
        self.serial_manager = SerialManager()
        self.serial_protocol = SerialProtocolFmcw()

        # Connect SerialManager and SerialProtocolFmcw
        self.serial_manager.data_received.connect(self.serial_protocol.handle_raw_data)
        self.serial_protocol.log_message.connect(log_manager.log_message)


        # Initialize BMS configuration
        self.bms_config = ISL94203Driver()

        # Initialize UserLog and LogManager
        self.user_log = UserLog(window)
        log_manager.initialize(self.user_log)

        self.main_tab = MainTab(self, self.serial_manager, self.serial_protocol)
        self.bms_tab = BmsTab(self, self.serial_manager, self.serial_protocol, self.bms_config)

        self.logRateSpinBox = window.findChild(QSpinBox, "logRateSpinBox")
        self.logRateSpinBox.setMinimum(1)
        self.logRateSpinBox.setMaximum(3600)

        # Create and set up the status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        status_bar_manager.initialize_status_bar_manager(self.status_bar)   

if __name__ == '__main__':
    main()