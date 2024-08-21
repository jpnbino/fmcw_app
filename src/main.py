import os
import sys
import logging

from PySide6.QtUiTools import loadUiType
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel
from PySide6.QtGui import QIcon, QFont, QFontDatabase
from PySide6.QtCore import Qt

from config import WINDOW_TITLE, ICON_PATH, UI_FILE_PATH
from bms.configuration import BMSConfiguration
from gui.bms import BMSGUI
from gui.serial import SerialWidget

Ui_MainWindow, _ = loadUiType(UI_FILE_PATH)


def configure_logging():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def main():
    configure_logging()
    logging.info("Application started")
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
        fmcw_app = FMCWApplication(UI_FILE_PATH)
        fmcw_app.show()
        sys.exit(app.exec())
    except Exception as e:
        logging.error(f"Failed to start the application: {e}")
        sys.exit(1)


class FMCWApplication(QMainWindow, Ui_MainWindow):
    def __init__(self, ui_file_name):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle(WINDOW_TITLE)
        self.setWindowIcon(QIcon(ICON_PATH))

        self.bms_config = BMSConfiguration()
        self.gui = BMSGUI(self, self.bms_config)
        self.serial_widget = SerialWidget(self)

        self.serial_setup = None

        self.logRateSpinBox.setMinimum(1)
        self.logRateSpinBox.setMaximum(3600)

        # Create a QLabel for logging status
        self.logging_status_label = QLabel("Logging: Not started")
        self.logging_status_label.setStyleSheet("padding-right: 10px;") 
        self.statusBar.addPermanentWidget(self.logging_status_label)

    def update_logging_status(self, message):
        self.logging_status_label.setText(message)


if __name__ == '__main__':
    main()
