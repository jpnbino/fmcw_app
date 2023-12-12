from bms_constants import *

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
