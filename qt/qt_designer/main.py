from qtpy.QtWidgets import QApplication, QMainWindow, QLineEdit, QPushButton
from qtpy.QtUiTools import QUiLoader
from qtpy.QtCore import QFile, QIODevice
from qtpy.QtGui import QIcon
import sys

MASK_1BIT = 0x0001
MASK_2BIT = 0x0003
MASK_10BIT = 0x03FF
MASK_11BIT = 0x07FF
MASK_12BIT = 0x0FFF

VOLTAGE_CELL_MULTIPLIER = (1.8 * 8.0) / (4095.0 * 3.0) # 0,0011721611721612

class ISL94203:

    EEPROM_ADDR_INIT = 0x00
    EEPROM_ADDR_END = 0x4B
    USER_EEPROM_ADDR_INIT = 0x50
    USER_EEPROM_ADDR_END = 0x57
    RAM_ADDR_INIT = 0x80
    RAM_ADDR_END = 0xAB

    NUM_REGISTERS = 5

    def __init__(self):
        self.registers = {}

    def initialize_registers(self, start_address, end_address, initial_value):
        for address in range(start_address, end_address + 1):
            self.registers[address] = initial_value

    def get_register_value(self, address):
        return self.registers.get(address, None)

    def set_register_value(self, address, new_value):
        if address in self.registers:
            self.registers[address] = new_value
            print(f"Register {hex(address)} set to {hex(new_value)}")
        else:
            print(f"Invalid register address: {hex(address)}")


class BMSConfiguration:
    
    def __init__(self):

        #Default from datasheet:      1E2A  0DD4  18FF  09FF  0E7F  0600  0DFF  07AA  0801  0801  0214  44A0  44A0  60C8  0A55  0D70  0010  01AB  0802  0802  0BF2  0A93  04B6  053E  04B6  053E  0BF2  0A93  4B6   053E  0BF2  0A93  67C   621H  06AA  FC0F  83FF       |USER EEPROM  8bytes    |0000  2240  0000  0003  0000  0A8F  0ABE  0015  0A91  0ABE  0000  0000  0000  0000  0A8F  0A92  027B  04D2  04D2  0368  0B09  002A              
        self.configuration_default = "2A,1E,D4,0D,FF,18,FF,09,7F,0E,00,06,FF,0D,AA,07,01,08,01,08,14,02,C8,54,C8,74,C8,40,55,08,2A,0C,11,00,AB,02,3C,0C,B4,0C,00,00,00,00,00,00,00,00,22,02,50,02,71,0C,16,0C,22,02,50,02,71,0C,16,0C,64,06,10,06,AA,06,01,FC,F8,C3,B9,21,00,00,00,00,00,00,00,00,00,00,40,22,00,00,03,00,00,00,8F,0A,BE,0A,15,00,91,0A,BE,0A,00,00,00,00,00,00,00,00,8F,0A,92,0A,7B,02,D2,04,D2,04,68,03,09,0B,2A,00,"
 
        # Split the input line by commas and remove spaces
        self.config_values = [val.strip() for val in self.configuration_default.split(',')[:] if val.strip()]
        self.config_values_int = []
        self.ov_lockout = 0.0
        self.ov_recover = 0.0
        self.eoc_voltage = 0.0
        self.uv_recover = 0.0
        self.under_voltage = 0.0
        self.sleep_voltage = 0.0
        self.low_voltage_charge = 0.0
        self.uv_lockout = 0.0

        #in milliseconds
        self.charge_detect_pulse_width = 0
        self.load_detect_pulse_width = 0

        self.ov_delay_timeout = 0          
        self.uv_delay_timeout = 0      
        self.open_wire_timing = 0
        self.sleep_delay = 0
        
        self.ov_delay_timeout_unit = 0
        self.uv_delay_timeout_unit = 0
        self.open_wire_timing_unit = 0
        self.sleep_delay_unit = 0

        # Mapping of codes to text values
        self.unit_mapping = {00: "μs", 1: "ms", 2: "s", 3: "min"}

    def get_default_config(self):
        return self.configuration_default

    def get_config(self):
        return self.config_values
    
    def update_registers(self,values):
        self.config_values = values
        self.config_values_int = [int(val,16) for val in values]
        print(values)

        # Extract values for the specified fields

        #Voltage levels
        self.ov =            self.apply_mask_and_multiplier(int(''.join(values[0:2][::-1]), 16))
        self.ov_recover =    self.apply_mask_and_multiplier(int(''.join(values[2:4][::-1]), 16))
        self.under_voltage = self.apply_mask_and_multiplier(int(''.join(values[4:6][::-1]), 16))
        self.uv_recover =    self.apply_mask_and_multiplier(int(''.join(values[6:8][::-1]), 16))
        self.ov_lockout =    self.apply_mask_and_multiplier(int(''.join(values[8:10][::-1]), 16))
        self.uv_lockout =    self.apply_mask_and_multiplier(int(''.join(values[10:12][::-1]), 16))
        self.eoc_voltage =    self.apply_mask_and_multiplier(int(''.join(values[12:14][::-1]), 16))
        self.low_voltage_charge = self.apply_mask_and_multiplier(int(''.join(values[14:16][::-1]), 16))
        self.sleep_voltage = self.apply_mask_and_multiplier(int(''.join(values[68:70][::-1]), 16))

        #Timing
        self.ov_delay_timeout =     ((int(''.join(values[0x10:0x12][::-1]), 16)) >> 0)  & MASK_10BIT
        self.ov_delay_timeout_unit= ((int(''.join(values[0x10:0x12][::-1]), 16)) >> 10)  & MASK_2BIT

        self.uv_delay_timeout =     ((int(''.join(values[0x12:0x14][::-1]), 16)) >> 0)  & MASK_10BIT
        self.uv_delay_timeout_unit = ((int(''.join(values[0x12:0x14][::-1]), 16)) >> 10)  & MASK_2BIT

        self.open_wire_timing =     ((int(''.join(values[0x14:0x16][::-1]), 16)) >> 0)  & 0x01ff
        self.open_wire_timing_unit = ((int(''.join(values[0x14:0x16][::-1]), 16)) >> 9)  & MASK_1BIT

        self.sleep_delay =          ((int(''.join(values[0x46:0x48][::-1]), 16)) >> 0)  & 0x01ff
        self.sleep_delay_unit =     ((int(''.join(values[0x46:0x48][::-1]), 16)) >> 9)  & MASK_2BIT
        
    
    def read_from_values(self, values):
        # Assuming the input format is a comma-separated string
        # Split the input line by commas and remove spaces
        values = [val.strip() for val in values.split(',') if val.strip()]

        #convert to int
        self.config_values_int = [int(val) for val in values]

        
    # Assuming the values get 16bits, therefore, operations are over two consecutives addresses 
    # example:

    def reg_write( self, address, value , mask, shift):

        byte0 = int(self.config_values_int[address])
        byte1 = int(self.config_values_int[address+1] ) 
        
        tmp = (byte1 << 8)|  byte0

        tmp = (tmp << shift) & ~mask
        tmp = tmp | (value << shift)

        self.config_values_int[address] = tmp & 0xff
        self.config_values_int[address + 1] = (tmp>> 8 ) & 0xff

        self.config_values = [hex(val)[2:].zfill(2).upper() for val in self.config_values_int]

    def write_to_values(self):

        return 0
    
    def apply_mask_and_multiplier(self, value):
        # Apply masking
        masked_value = value & MASK_12BIT
        # Apply multiplier
        result = masked_value * VOLTAGE_CELL_MULTIPLIER
        return result
    
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
            self.ui.ovDelayTimeoutLineEdit,

        ]:
            line_edit.textChanged.connect(self.on_line_edit_changed)

    #read the combobox and return the unit chosen by user
    def get_unit_from_combo(self, combo):
        selected_text = combo.currentText()
        unit = next((code for code, text in self.bms_config.unit_mapping.items() if text == selected_text), None)
        return unit
    
    def read_bms_config(self):

        #@todo: Implemetar para usar a serial.
        # Serial read
        # save values
        # mostra na tela
        configuration =   self.bms_config.get_config()   

        self.bms_config.update_registers(configuration)

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

        self.ui.ovDelayTimeoutLineEdit.setText(f"{int(self.bms_config.ov_delay_timeout)}")
        self.ui.uvDelayTimeoutLineEdit.setText(f"{int(self.bms_config.uv_delay_timeout)}")
        self.ui.sleepDelayLineEdit.setText(f"{int(self.bms_config.sleep_delay)}")
        self.ui.openWireTimingLineEdit.setText(f"{int(self.bms_config.open_wire_timing)}")

        # Update the combo box with the selected value
        self.ui.ovDelayTimeoutCombo.setCurrentText(self.bms_config.unit_mapping.get(int(self.bms_config.ov_delay_timeout_unit), 'Unknown'))
        self.ui.uvDelayTimeoutCombo.setCurrentText(self.bms_config.unit_mapping.get(int(self.bms_config.uv_delay_timeout_unit), 'Unknown'))
        self.ui.sleepDelayUnitCombo.setCurrentText(self.bms_config.unit_mapping.get(int(self.bms_config.sleep_delay_unit), 'Unknown'))
        self.ui.openWireTimingCombo.setCurrentText(self.bms_config.unit_mapping.get(int(self.bms_config.open_wire_timing_unit), 'Unknown'))

        

    def write_bms_config(self):

        register_cfg = self.bms_config.get_config()

        print("enter write_bms_config:", register_cfg)

#Convert Editline values to HEX

        # Get the values from the QLineEdit fields
        ov = float(self.ui.ovLineEdit.text()) #reg00
        ov_recover = float(self.ui.ovRecoverLineEdit.text())
        
        uv = float(self.ui.underVoltageLineEdit.text())        
        uv_recover = float(self.ui.uvRecoverLineEdit.text())

        ov_lockout = float(self.ui.ovLockoutLineEdit.text())
        uv_lockout = float(self.ui.uvLockoutLineEdit.text())

        eoc_voltage = float(self.ui.eocVoltageLineEdit.text())
        low_voltage_charge = float(self.ui.LowVoltageChargeLineEdit.text())

        sleep_voltage = float(self.ui.sleepVoltageLineEdit.text())
        
        
        # Convert the integer
        ov_hex = int(ov / VOLTAGE_CELL_MULTIPLIER)
        ov_recover_hex = int(ov_recover / VOLTAGE_CELL_MULTIPLIER)
        
        uv_hex = int(uv / VOLTAGE_CELL_MULTIPLIER)
        uv_recover_hex = int(uv_recover / VOLTAGE_CELL_MULTIPLIER)

        ov_lockout_hex = int(ov_lockout / VOLTAGE_CELL_MULTIPLIER)
        uv_lockout_hex = int(uv_lockout / VOLTAGE_CELL_MULTIPLIER)

        eoc_voltage_hex = int(eoc_voltage / VOLTAGE_CELL_MULTIPLIER)
        low_voltage_charge_hex = int(low_voltage_charge / VOLTAGE_CELL_MULTIPLIER)
        
        sleep_voltage_hex = int(sleep_voltage / VOLTAGE_CELL_MULTIPLIER)
        
        self.bms_config.reg_write( 0x00, ov_hex, MASK_12BIT, 0x00)
        self.bms_config.reg_write( 0x02, ov_recover_hex, MASK_12BIT, 0x00)
        self.bms_config.reg_write( 0x04, uv_hex, MASK_12BIT, 0x00)
        self.bms_config.reg_write( 0x06, uv_recover_hex, MASK_12BIT, 0x00)
        self.bms_config.reg_write( 0x08, ov_lockout_hex, MASK_12BIT, 0x00)
        self.bms_config.reg_write( 0x0a, uv_lockout_hex, MASK_12BIT, 0x00)
        self.bms_config.reg_write( 0x0c, eoc_voltage_hex, MASK_12BIT, 0x00)
        self.bms_config.reg_write( 0x0e, low_voltage_charge_hex, MASK_12BIT, 0x00)
        self.bms_config.reg_write( 0x44, sleep_voltage_hex, MASK_12BIT, 0x00)
        
        #time register
         # Get the values from the QLineEdit fields
        ov_delay_timeout = int(self.ui.ovDelayTimeoutLineEdit.text()) #reg00
        uv_delay_timeout = int(self.ui.uvDelayTimeoutLineEdit.text())
        
        open_wire_sample_time = int(self.ui.openWireTimingLineEdit.text())
        sleep_delay = int(self.ui.sleepDelayLineEdit.text())        
        
        #Read unit and shift the values according to position in the register
        ov_delay_timeout_unit = self.get_unit_from_combo(self.ui.ovDelayTimeoutCombo) << 10
        uv_delay_timeout_unit = self.get_unit_from_combo(self.ui.uvDelayTimeoutCombo) << 10
        sleep_delay_unit = self.get_unit_from_combo(self.ui.sleepDelayUnitCombo) << 9
        open_wire_sample_time_unit = self.get_unit_from_combo(self.ui.openWireTimingCombo) << 9

        #Joins values and units, and write the configuration
        self.bms_config.reg_write( 0x10, ov_delay_timeout_unit|ov_delay_timeout, MASK_12BIT, 0)
        self.bms_config.reg_write( 0x12, uv_delay_timeout_unit|uv_delay_timeout, MASK_12BIT, 0)
        self.bms_config.reg_write( 0x14, open_wire_sample_time_unit |open_wire_sample_time, MASK_10BIT, 0)
        self.bms_config.reg_write( 0x46, sleep_delay_unit | sleep_delay, MASK_11BIT, 0)  


        register_cfg = self.bms_config.get_config()
        print("exit write_bms_config:", register_cfg)

#Write values in the correct position
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

        # Set the application icon for the window and taskbar
        icon_path = "images/icons/icon_circle.png"  # Replace this with the path to your icon file
        self.setWindowIcon(QIcon(icon_path))
                           
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
    ui_file_name = "qt/qt_designer/fmcw.ui"

    # Create an instance of the FMCWApplication class
    fmcw_app = FMCWApplication(ui_file_name)

    sys.exit(app.exec_())
