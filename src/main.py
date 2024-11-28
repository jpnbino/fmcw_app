import os
import sys
import logging
from logging_config import configure_logging

from PySide6.QtGui import QIcon, QFont, QFontDatabase
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QSpinBox, QPushButton
from PySide6.QtCore import QFile, QIODevice, Qt

from app_config import WINDOW_TITLE, ICON_PATH, UI_FILE_PATH
from bms.configuration import BMSConfiguration
from gui.bms import BMSGUI
from gui.serial import SerialWidget

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

        self.bms_config = BMSConfiguration()
        self.gui = BMSGUI(self, self.bms_config)
        self.serial_widget = SerialWidget(self)

        self.serial_setup = None

        self.logRateSpinBox = window.findChild(QSpinBox, "logRateSpinBox")
        self.logRateSpinBox.setMinimum(1)
        self.logRateSpinBox.setMaximum(3600)


        # Create a QLabel for logging status
        self.logging_status_label = QLabel("Logging: Not started")
        self.logging_status_label.setStyleSheet("padding-right: 10px;")
        self.statusBar().addPermanentWidget(self.logging_status_label)

        # Correctly set the alignment flags
        self.logging_status_label.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)

    def update_logging_status(self, message):
        self.logging_status_label.setText(message)

if __name__ == '__main__':
    main()