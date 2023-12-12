from PySide6.QtUiTools import loadUiType
from qtpy.QtWidgets import QApplication, QMainWindow

from qtpy.QtCore import QFile, QIODevice
from qtpy.QtGui import QIcon
import sys

from bms_configuration import BMSConfiguration
from bms_gui import BMSGUI

Ui_MainWindow, _ = loadUiType("app/qt/qt_designer/fmcw.ui") 

class FMCWApplication(QMainWindow, Ui_MainWindow ):
    def __init__(self, ui_file_name):
        super().__init__()

        #Setup the user interface
        self.setupUi(self)

        # Set the window title
        self.setWindowTitle("FMCW Application")

        # Set the application icon for the window and taskbar
        icon_path = "images/icons/icon_circle.png"  # Replace this with the path to your icon file
        self.setWindowIcon(QIcon(icon_path))
                           
        # Set the initial size of the window
        self.resize(800, 600)

        # Initialize bms_config as an instance of BMSConfiguration
        self.bms_config = BMSConfiguration()
        
        # Initialize BMSGUI
        self.gui = BMSGUI(self, self.bms_config)

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
