
import sys
import os

# Add the project directories to the sys.path
base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
src_path = os.path.join(base_path, 'src')
sys.path.append(src_path)
sys.path.append(os.path.join(src_path, 'bms'))
sys.path.append(os.path.join(src_path, 'gui'))
sys.path.append(os.path.join(src_path, 'serialbsp'))

from PySide6.QtUiTools import loadUiType
from qtpy.QtWidgets import QApplication, QMainWindow 
from qtpy.QtGui import QIcon

from bms.configuration import BMSConfiguration
from gui.bms import BMSGUI
from gui.serial import SerialWidget


Ui_MainWindow, _ = loadUiType("app/qt/fmcw.ui") 

class FMCWApplication(QMainWindow, Ui_MainWindow ):
    def __init__(self, ui_file_name):
        super().__init__()

        self.setupUi(self)
        self.setWindowTitle("FMCW Application")
        icon_path = "app/images/icons/icon_circle.png"
        self.setWindowIcon(QIcon(icon_path))
        self.resize(1200,800)

        self.bms_config = BMSConfiguration()
        self.gui = BMSGUI(self, self.bms_config)
        self.serial_widget = SerialWidget(self)

        self.serial_setup = None

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui_file_name = "qt/qt_designer/fmcw.ui"
    fmcw_app = FMCWApplication(ui_file_name)
    fmcw_app.show()
    sys.exit(app.exec_())
