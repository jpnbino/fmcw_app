from qtpy.QtWidgets import QApplication, QMainWindow, QLineEdit, QPushButton
from qtpy.QtUiTools import QUiLoader
from qtpy.QtCore import QFile, QIODevice
import sys

MASK_12BIT = 0x0FFF
VOLTAGE_CELL_MULTIPLIER = (1.8 * 8.0) / (4095.0 * 3.0) # 0,0011721611721612

class BMSConfiguration:
    def __init__(self):
        self.ov_lockout = 0.0
        self.ov_recover = 0.0
        self.eoc_voltage = 0.0
        self.uv_recover = 0.0
        self.under_voltage = 0.0
        self.sleep_voltage = 0.0
        self.low_voltage_charge = 0.0
        self.uv_lockout = 0.0

    def read_from_values(self, values):
        # Assuming the input format is a comma-separated string
        # Split the input line by commas and remove spaces
        values = [val.strip() for val in values.split(',') if val.strip()]

        # Ensure that there are at least 20 fields in the input line
        if len(values) >= 20:
            # Extract values for the specified fields and convert to appropriate types
            self.ov_lockout = self.apply_mask_and_multiplier(int(''.join(values[2:4]), 16))
            self.ov_recover = self.apply_mask_and_multiplier(int(''.join(values[4:6]), 16))
            self.eoc_voltage = self.apply_mask_and_multiplier(int(''.join(values[6:8]), 16))
            self.uv_recover = self.apply_mask_and_multiplier(int(''.join(values[8:10]), 16))
            self.under_voltage = self.apply_mask_and_multiplier(int(''.join(values[10:12]), 16))
            self.sleep_voltage = self.apply_mask_and_multiplier(int(''.join(values[12:14]), 16))
            self.low_voltage_charge = self.apply_mask_and_multiplier(int(''.join(values[14:16]), 16))
            self.uv_lockout = self.apply_mask_and_multiplier(int(''.join(values[16:18]), 16))


    def write_to_values(self):
        ov_lockout_hex = f"{int(self.ov_lockout / VOLTAGE_CELL_MULTIPLIER):04X}"
        ov_recover_hex = f"{int(self.ov_recover / VOLTAGE_CELL_MULTIPLIER):04X}"
        eoc_voltage_hex = f"{int(self.eoc_voltage / VOLTAGE_CELL_MULTIPLIER):04X}"
        uv_recover_hex = f"{int(self.uv_recover / VOLTAGE_CELL_MULTIPLIER):04X}"
        under_voltage_hex = f"{int(self.under_voltage / VOLTAGE_CELL_MULTIPLIER):04X}"
        sleep_voltage_hex = f"{int(self.sleep_voltage / VOLTAGE_CELL_MULTIPLIER):04X}"
        low_voltage_charge_hex = f"{int(self.low_voltage_charge / VOLTAGE_CELL_MULTIPLIER):04X}"
        uv_lockout_hex = f"{int(self.uv_lockout / VOLTAGE_CELL_MULTIPLIER):04X}"

        # Construct the updated input line
        updated_input_line = (
            f"2023-11-13 02:39:20, "
            f"{ov_lockout_hex[0:2]},{ov_lockout_hex[2:4]},"
            f"{ov_recover_hex[0:2]},{ov_recover_hex[2:4]},"
            f"{eoc_voltage_hex[0:2]},{eoc_voltage_hex[2:4]},"
            f"{uv_recover_hex[0:2]},{uv_recover_hex[2:4]},"
            f"{under_voltage_hex[0:2]},{under_voltage_hex[2:4]},"
            f"{sleep_voltage_hex[0:2]},{sleep_voltage_hex[2:4]},"
            f"{low_voltage_charge_hex[0:2]},{low_voltage_charge_hex[2:4]},"
            f"{uv_lockout_hex[0:2]},{uv_lockout_hex[2:4]},"
        )

        return updated_input_line

class BMSGUI:
    def __init__(self, ui, bms_config):
        self.ui = ui
        self.bms_config = bms_config

        # Connect button click to custom functions
        self.ui.readPackButton.clicked.connect(self.read_bms_config)
        self.ui.writeEepromButton.clicked.connect(self.write_bms_config)

        # Connect QLineEdit signals to a common slot
        for line_edit in [
            self.ui.ovLockoutLineEdit,
            self.ui.ovLineEdit,
            self.ui.ovRecoverLineEdit,
            self.ui.eocVoltageLineEdit,
            self.ui.uvRecoverLineEdit,
            self.ui.underVoltageLineEdit,
            self.ui.sleepVoltageLineEdit,
            self.ui.LowVoltageChargeLineEdit,
            self.ui.uvLockoutLineEdit,
        ]:
            line_edit.textChanged.connect(self.on_line_edit_changed)

    def apply_mask_and_multiplier(self, value):
        # Apply masking
        masked_value = value & MASK_12BIT
        # Apply multiplier
        result = masked_value * VOLTAGE_CELL_MULTIPLIER
        return result

    def read_bms_config(self):

    
        #Default from datasheet:           1E2A  0DD4  18FF  09FF  0E7F  0600  0DFF  07AA  0801  0801  0214  44A0  44A0  60C8  0A55  0D70  0010  01AB  0802  0802  0BF2  0A93  04B6  053E  04B6  053E  0BF2  0A93  4B6   053E  0BF2  0A93  67C   621H  06AA  FC0F  83FF       |USER EEPROM  8bytes    |              
        input_line = "2023-11-13 02:39:20, 2A,1E,D4,0D,FF,18,FF,09,7F,0E,00,06,FF,0D,AA,07,01,08,01,08,14,02,C8,54,C8,74,C8,40,55,08,2A,0C,11,00,AB,02,3C,0C,B4,0C,00,00,00,00,00,00,00,00,22,02,50,02,71,0C,16,0C,22,02,50,02,71,0C,16,0C,64,06,10,06,AA,06,01,FC,F8,C3,B9,21,00,00,00,00,00,00,00,00,00,00,40,22,00,00,03,00,00,00,8F,0A,BE,0A,15,00,91,0A,BE,0A,00,00,00,00,00,00,00,00,8F,0A,92,0A,7B,02,D2,04,D2,04,68,03,09,0B,2A,00,"

        # Split the input line by commas and remove spaces
        values = [val.strip() for val in input_line.split(',')[1:] if val.strip()]

        # Ensure that there are at least 9 fields in the input line
        if len(values) >= 9:
            # Extract values for the specified fields
            self.bms_config.ov =            self.apply_mask_and_multiplier(int(''.join(values[0:2][::-1]), 16))
            self.bms_config.ov_recover =    self.apply_mask_and_multiplier(int(''.join(values[2:4][::-1]), 16))
            self.bms_config.under_voltage = self.apply_mask_and_multiplier(int(''.join(values[4:6][::-1]), 16))
            self.bms_config.uv_recover =    self.apply_mask_and_multiplier(int(''.join(values[6:8][::-1]), 16))
            self.bms_config.ov_lockout =    self.apply_mask_and_multiplier(int(''.join(values[8:10][::-1]), 16))
            self.bms_config.uv_lockout =    self.apply_mask_and_multiplier(int(''.join(values[10:12][::-1]), 16))
            self.bms_config.eoc_voltage =    self.apply_mask_and_multiplier(int(''.join(values[12:14][::-1]), 16))
            self.bms_config.low_voltage_charge = self.apply_mask_and_multiplier(int(''.join(values[14:16][::-1]), 16))
            self.bms_config.sleep_voltage = self.apply_mask_and_multiplier(int(''.join(values[68:70][::-1]), 16))

            print(hex(int(''.join(values[0:2][::-1]), 16)))
            print(hex(int(''.join(values[2:4][::-1]), 16)))
            print(hex(int(''.join(values[4:6][::-1]), 16)))
            print(hex(int(''.join(values[6:8][::-1]), 16)))
            print(hex(int(''.join(values[8:10][::-1]), 16)))
            print(hex(int(''.join(values[10:12][::-1]), 16)))
            print(hex(int(''.join(values[12:14][::-1]), 16)))
            print(hex(int(''.join(values[20:22][::-1]), 16)))
            print(hex (int(''.join(values[0x44:0x46][::-1]), 16)))

            # ... (update other configuration parameters)

            # Set the values in the corresponding QLineEdit fields with formatting to three decimal places
            self.ui.ovLockoutLineEdit.setText(f"{self.bms_config.ov_lockout:.2f}")
            self.ui.ovLineEdit.setText(f"{self.bms_config.ov:.2f}")
            self.ui.ovRecoverLineEdit.setText(f"{self.bms_config.ov_recover:.2f}")
            self.ui.eocVoltageLineEdit.setText(f"{self.bms_config.eoc_voltage:.2f}")
            self.ui.uvRecoverLineEdit.setText(f"{self.bms_config.uv_recover:.2f}")
            self.ui.underVoltageLineEdit.setText(f"{self.bms_config.under_voltage:.2f}")
            self.ui.sleepVoltageLineEdit.setText(f"{self.bms_config.sleep_voltage:.2f}")
            self.ui.LowVoltageChargeLineEdit.setText(f"{self.bms_config.low_voltage_charge:.2f}")
            self.ui.uvLockoutLineEdit.setText(f"{self.bms_config.uv_lockout:.2f}")
            # ... (update other QLineEdit fields)

    def write_bms_config(self):
        # Get the values from the QLineEdit fields
        ov_lockout = float(self.ui.ovLockoutLineEdit.text())
        print( ov_lockout)
        print(VOLTAGE_CELL_MULTIPLIER)
        ov = float(self.ui.ovLineEdit.text())
        ov_recover = float(self.ui.ovRecoverLineEdit.text())
        eoc_voltage = float(self.ui.eocVoltageLineEdit.text())
        uv_recover = float(self.ui.uvRecoverLineEdit.text())
        under_voltage = float(self.ui.underVoltageLineEdit.text())
        sleep_voltage = float(self.ui.sleepVoltageLineEdit.text())
        low_voltage_charge = float(self.ui.LowVoltageChargeLineEdit.text())
        uv_lockout = float(self.ui.uvLockoutLineEdit.text())

        # Convert the values back to the format used in the input line
        ov_lockout_hex = f"{int(ov_lockout / VOLTAGE_CELL_MULTIPLIER):04X}"
        print( ov_lockout_hex)
        ov_hex = f"{int(ov / VOLTAGE_CELL_MULTIPLIER):04X}"
        ov_recover_hex = f"{int(ov_recover / VOLTAGE_CELL_MULTIPLIER):04X}"
        eoc_voltage_hex = f"{int(eoc_voltage / VOLTAGE_CELL_MULTIPLIER):04X}"
        uv_recover_hex = f"{int(uv_recover / VOLTAGE_CELL_MULTIPLIER):04X}"
        under_voltage_hex = f"{int(under_voltage / VOLTAGE_CELL_MULTIPLIER):04X}"
        sleep_voltage_hex = f"{int(sleep_voltage / VOLTAGE_CELL_MULTIPLIER):04X}"
        low_voltage_charge_hex = f"{int(low_voltage_charge / VOLTAGE_CELL_MULTIPLIER):04X}"
        uv_lockout_hex = f"{int(uv_lockout / VOLTAGE_CELL_MULTIPLIER):04X}"

        # Construct the updated input line
        updated_input_line = "2023-11-13 02:39:20, {},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},".format(
            ov_lockout_hex[0:2], ov_lockout_hex[2:4],
            ov_hex[0:2], ov_hex[2:4],
            ov_recover_hex[0:2], ov_recover_hex[2:4],
            eoc_voltage_hex[0:2], eoc_voltage_hex[2:4],
            uv_recover_hex[0:2], uv_recover_hex[2:4],
            under_voltage_hex[0:2], under_voltage_hex[2:4],
            sleep_voltage_hex[0:2], sleep_voltage_hex[2:4],
            low_voltage_charge_hex[0:2], low_voltage_charge_hex[2:4],
            uv_lockout_hex[0:2], uv_lockout_hex[2:4]
        )

        # Do something with the updated input line (print for now)
        print("Updated Input Line:", updated_input_line)

    def on_line_edit_changed(self, text):
        print(f"Line Edit Changed: {text}")
        # Add your desired actions here

class FMCWApplication(QMainWindow):
    def __init__(self, ui_file_name):
        super().__init__()

        # Load the UI file
        ui_file = QFile(ui_file_name)
        if not ui_file.open(QIODevice.ReadOnly):
            print(f"Cannot open {ui_file_name}: {ui_file.errorString()}")
            sys.exit(-1)

        loader = QUiLoader()
        self.ui = loader.load(ui_file, None)
        ui_file.close()

        if not self.ui:
            print(loader.errorString())
            sys.exit(-1)

        # Set the window title
        self.setWindowTitle("FMCW Application")

        # Set the initial size of the window
        self.resize(800, 600)

        # Initialize bms_config as an instance of BMSConfiguration
        self.bms_config = BMSConfiguration()
        
        # Initialize BMSGUI
        self.gui = BMSGUI(self.ui, self.bms_config)

        # Set the central widget and show the main window
        self.setCentralWidget(self.ui)
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Some code to obtain the form file name, ui_file_name
    ui_file_name = "fmcw.ui"

    # Create an instance of the FMCWApplication class
    fmcw_app = FMCWApplication(ui_file_name)

    sys.exit(app.exec_())
