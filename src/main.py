import atexit
import os
import sys
import logging
from logging_config import configure_logging

from PySide6.QtGui import QIcon, QFont, QFontDatabase
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QSpinBox, QStatusBar
from PySide6.QtCore import QFile, QIODevice, Qt

from app_config import WINDOW_TITLE, ICON_PATH, UI_FILE_PATH
from bms.isl94203_driver import BMSConfiguration
from gui.tabbms import BmsTab
from gui.tabmain import MainTab

from serialbsp.serial_manager import SerialManager

def main():
    configure_logging()
    logging.info("Application started")

    # Set the Qt::AA_ShareOpenGLContexts attribute before creating the QApplication instance
    QApplication.setAttribute(Qt.AA_ShareOpenGLContexts)

    app = QApplication(sys.argv)

    # Load and set Roboto font
    root_directory = os.path.dirname(os.path.abspath(__file__))
    font_path = os.path.join(root_directory, "../qt/fonts/Roboto/Roboto-Regular.ttf")

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
        app.setStyle("Fusion")

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

        # Set up the main window
        fmcw_app = FMCWApplication(window)
        fmcw_app.show()

        # Register cleanup function
        atexit.register(fmcw_app.cleanup)

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

        self.fmcw_serial_manager = SerialManager()
        self.bms_config = BMSConfiguration()

        self.main_tab = MainTab(self, self.bms_config)

        self.logRateSpinBox = window.findChild(QSpinBox, "logRateSpinBox")
        self.logRateSpinBox.setMinimum(1)
        self.logRateSpinBox.setMaximum(3600)

        # Create and set up the status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        # Create a QLabel for logging status
        self.logging_status_label = QLabel("Logging: Not started")
        self.logging_status_label.setStyleSheet("padding-right: 10px;")
        self.status_bar.addPermanentWidget(self.logging_status_label)

        # Correctly set the alignment flags
        self.logging_status_label.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)

    def cleanup(self):
        logging.info("Cleaning up resources")
        # Ensure all threads are stopped
        if hasattr(self.main_tab, 'serial_protocol') and self.main_tab.serial_protocol:
            self.main_tab.serial_protocol.stop()
        logging.info("Cleanup complete")

    def update_logging_status(self, message):
        self.logging_status_label.setText(message)

if __name__ == '__main__':
    main()