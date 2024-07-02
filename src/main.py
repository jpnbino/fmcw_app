
import sys
import logging

from PySide6.QtUiTools import loadUiType
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtGui import QIcon

from config import WINDOW_TITLE, ICON_PATH, UI_FILE_PATH
from bms.configuration import BMSConfiguration
from gui.bms import BMSGUI
from gui.serial import SerialWidget

WINDOW_WIDTH = 1126
WINDOW_HEIGHT = 885

Ui_MainWindow, _ = loadUiType(UI_FILE_PATH) 

def configure_logging():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def main():
    configure_logging()
    logging.info("Application started")
    app = QApplication(sys.argv)

    try:
        fmcw_app = FMCWApplication(UI_FILE_PATH)
        fmcw_app.show()
        sys.exit(app.exec())
    except Exception as e:
        logging.error(f"Failed to start the application: {e}")
        sys.exit(1)

class FMCWApplication(QMainWindow, Ui_MainWindow ):
    def __init__(self, ui_file_name):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle(WINDOW_TITLE)
        self.setWindowIcon(QIcon(ICON_PATH))
        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)
        
        self.bms_config = BMSConfiguration()
        self.gui = BMSGUI(self, self.bms_config)
        self.serial_widget = SerialWidget(self)

        self.serial_setup = None

if __name__ == '__main__':
    main()
