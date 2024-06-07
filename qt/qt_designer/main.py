from PySide6.QtUiTools import loadUiType
from qtpy.QtWidgets import QApplication, QMainWindow 
from qtpy.QtGui import QIcon


from bms_configuration import BMSConfiguration
from bms_gui import BMSGUI
from serial_widget import SerialWidget

import sys

Ui_MainWindow, _ = loadUiType("app/qt/qt_designer/fmcw.ui") 

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
