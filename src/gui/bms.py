from PySide6.QtGui import QColor
from bms.constants import *
from bms.isl94203 import ISL94203
from serialbsp.protocol import *
import logging

class BMSGUI:
    def __init__(self, ui, bms_config):
        self.ui = ui
        self.bms_config = bms_config
        self.isl94203 = ISL94203()

        # Connect button click to Send Serial Command
        self.ui.readPackButton.clicked.connect(self.read_bms_config)
        self.ui.writePackButton.clicked.connect(self.write_bms_config)  

    def ui_update_fields(self):
        """Update the UI fields with the BMS configuration values."""
        self.ui_update_voltage_limits()
        self.ui_update_voltage_limits_timing()
        self.ui_update_timer_fields()
        self.ui_update_cell_balance_limits()
        self.ui_update_temperature_limits()
        self.ui_update_current_limits()
        self.ui_update_pack_option()
        self.ui_update_ram_values()
        self.ui_update_status_bits()

    def ui_update_voltage_limits(self):
        """Update voltage limits fields."""
        voltage_fields = [
            (self.ui.ovLockoutLineEdit, self.bms_config.ov_lockout),
            (self.ui.ovLineEdit, self.bms_config.ov),
            (self.ui.ovRecoverLineEdit, self.bms_config.ov_recover),
            (self.ui.eocVoltageLineEdit, self.bms_config.eoc_voltage),
            (self.ui.uvRecoverLineEdit, self.bms_config.uv_recover),
            (self.ui.underVoltageLineEdit, self.bms_config.under_voltage),
            (self.ui.sleepVoltageLineEdit, self.bms_config.sleep_voltage),
            (self.ui.LowVoltageChargeLineEdit, self.bms_config.low_voltage_charge),
            (self.ui.uvLockoutLineEdit, self.bms_config.uv_lockout)
        ]
        for line_edit, value in voltage_fields:
            line_edit.setText(f"{value:.2f}")

    def ui_update_voltage_limits_timing(self):
        """Update voltage limits timing fields and 
        Update the combo boxes with the selected values."""
        voltage_timing_fields = [
            (self.ui.ovDelayTimeoutLineEdit, self.bms_config.ov_delay_timeout),
            (self.ui.uvDelayTimeoutLineEdit, self.bms_config.uv_delay_timeout),
            (self.ui.sleepDelayLineEdit, self.bms_config.sleep_delay),
            (self.ui.openWireTimingLineEdit, self.bms_config.open_wire_timing)
        ]
        for line_edit, value in voltage_timing_fields:
            line_edit.setText(f"{int(value)}")

        combo_boxes = [
            (self.ui.ovDelayTimeoutCombo, self.bms_config.ov_delay_timeout_unit),
            (self.ui.uvDelayTimeoutCombo, self.bms_config.uv_delay_timeout_unit),
            (self.ui.sleepDelayUnitCombo, self.bms_config.sleep_delay_unit),
            (self.ui.openWireTimingCombo, self.bms_config.open_wire_timing_unit)
        ]
        for combo, value in combo_boxes:
            combo.setCurrentText(UNIT_MAPPING.get(int(value), 'Unknown'))

    def ui_update_timer_fields(self):
        """Update timer-related fields."""
        timer_fields = {
            self.ui.timerIdleDozeCombo: self.bms_config.timer_idle_doze,
            self.ui.timerSleepCombo: self.bms_config.timer_sleep,
        }
        for line_edit, value in timer_fields.items():
            line_edit.setCurrentText(f"{int(value)}")

        wdt_line_edit = self.ui.timerWDTLineEdit
        wdt_line_edit.setText(f"{int(self.bms_config.timer_wdt)}")

    def ui_update_cell_balance_limits(self):
        """Update cell balance limits fields."""
        self.ui.CellConfigurationLineEdit.setText(f"{int(CELL_CONFIG_MAPPING[self.bms_config.cell_config])}")
        
        cell_balance_limits = {
            self.ui.CBUpperLimLineEdit: self.bms_config.cb_upper_lim,
            self.ui.CBLowerLimLineEdit: self.bms_config.cb_lower_lim,
            self.ui.CBMaxDeltaLineEdit: self.bms_config.cb_max_delta,
            self.ui.CBMinDeltaLineEdit: self.bms_config.cb_min_delta,
            self.ui.CBOverTempLineEdit: self.bms_config.cb_over_temp,
            self.ui.CBOTRecoverLineEdit: self.bms_config.cb_ot_recover,
            self.ui.CBUTRecoverLineEdit: self.bms_config.cb_ut_recover,
            self.ui.CBUnderTempLineEdit: self.bms_config.cb_under_temp,
        }
        for line_edit, value in cell_balance_limits.items():
            line_edit.setText(f"{value:.2f}")    

        self.ui.CBOnTimeLineEdit.setText(f"{int(self.bms_config.cb_on_time)}")
        self.ui.CBOffTimeLineEdit.setText(f"{int(self.bms_config.cb_off_time)}")
        self.ui.CBOnTimeUnitLineEdit.setCurrentText(UNIT_MAPPING.get(int(self.bms_config.cb_on_time_unit), 'Unknown'))
        self.ui.CBOffTimeUnitLineEdit.setCurrentText(UNIT_MAPPING.get(int(self.bms_config.cb_off_time_unit), 'Unknown'))

    def ui_update_temperature_limits(self):
        """Update temperature limits fields."""
        temp_limits = {
            self.ui.TLChargeOverTempLineEdit: self.bms_config.tl_charge_over_temp,
            self.ui.TLChargeOTRecoverLineEdit: self.bms_config.tl_charge_ot_recover,
            self.ui.TLChargeUTRecoverLineEdit: self.bms_config.tl_charge_ut_recover,
            self.ui.TLChargeUnderTempLineEdit: self.bms_config.tl_charge_under_temp,
            self.ui.TLDiscOverTempLineEdit: self.bms_config.tl_disch_over_temp,
            self.ui.TLDischOTRecoverLineEdit: self.bms_config.tl_disch_ot_recover,
            self.ui.TLDischUTRecoverLineEdit: self.bms_config.tl_disch_ut_recover,
            self.ui.TLDischUnderTempLineEdit: self.bms_config.tl_disch_under_temp,
            self.ui.TLInternalOverTempLineEdit: self.bms_config.tl_internal_over_temp,
            self.ui.TLInternalOTRecoverLineEdit: self.bms_config.tl_internal_ot_recover
        }
        for line_edit, value in temp_limits.items():
            line_edit.setText(f"{value:.2f}") 

    def ui_update_current_limits(self):
        """Update current limits fields."""
        current_limits = {
            self.ui.CLDischargeOCVoltageCombo: (self.bms_config.disch_oc_voltage, DOC_MAPPING),
            self.ui.CLChargeOCVoltageCombo: (self.bms_config.charge_oc_voltage, COC_MAPPING),
            self.ui.CLDischargeSCVoltageCombo: (self.bms_config.disch_sc_voltage, DSC_MAPPING),
            self.ui.CLDischargeOCTimeoutCombo: (self.bms_config.disch_oc_timeout_unit, UNIT_MAPPING),
            self.ui.CLChargeOCTimeoutCombo: (self.bms_config.charge_oc_timeout_unit, UNIT_MAPPING),
            self.ui.CLDischargeSCTimeoutCombo: (self.bms_config.disch_sc_timeout_unit, UNIT_MAPPING)
        }
        for combo, (value, mapping) in current_limits.items():
            combo.setCurrentText(mapping.get(int(value), 'Unknown'))

        current_fields = {
            self.ui.CLDischargeOCTimeoutLineEdit: self.bms_config.disch_oc_timeout,
            self.ui.CLChargeOCTimeoutLineEdit: self.bms_config.charge_oc_timeout,
            self.ui.CLDischargeSCTimeoutLineEdit: self.bms_config.disch_sc_timeout
        }
        for line_edit, value in current_fields.items():
            line_edit.setText(f"{int(value)}")

        current_detect_fields = {
            self.ui.chargeDetectPulseCombo: self.bms_config.charge_detect_pulse_width,	
            self.ui.loadDetectPulseCombo: self.bms_config.load_detect_pulse_width
        }
        for combo, value in current_detect_fields.items():
            combo.setCurrentText(f"{int(value)}")
            
    def ui_update_pack_option(self):
        """Update pack option fields."""
        options = {
            self.ui.poT2MonitorsFETTempCheckBox: self.bms_config.bit_t2_monitors_fet,
            self.ui.poEnableCELLFpsdCheckBox: self.bms_config.bit_enable_cellf_psd,
            self.ui.poEnableOpenWirePSDCheckBox: self.bms_config.bit_enable_openwire_psd,
            self.ui.poEnableUVLOCheckBox: self.bms_config.bit_enable_uvlo_pd,
            self.ui.poEnableOpenWireScanCheckBox: self.bms_config.bit_enable_openwire_scan,
            self.ui.CBDuringChargeCheckBox: self.bms_config.bit_cb_during_charge,
            self.ui.CBDuringDischargeCheckBox: self.bms_config.bit_cb_during_discharge,
            self.ui.CBDuringEOCCheckBox: self.bms_config.bit_cb_during_eoc,
            self.ui.tGainCheckBox: self.bms_config.bit_tgain
            }
        for checkbox, value in options.items():
            checkbox.setChecked(value)

    def ui_update_ram_values(self):
        #RAM
        #Voltage values: Cells, Min, Max, Batt, Vrgo
        voltage_fields = [
            (self.ui.vcell1LineEdit, self.bms_config.vcell1),
            (self.ui.vcell2LineEdit, self.bms_config.vcell2),
            (self.ui.vcell3LineEdit, self.bms_config.vcell3),
            (self.ui.vcell4LineEdit, self.bms_config.vcell4),
            (self.ui.vcell5LineEdit, self.bms_config.vcell5),
            (self.ui.vcell6LineEdit, self.bms_config.vcell6),
            (self.ui.vcell7LineEdit, self.bms_config.vcell7),
            (self.ui.vcell8LineEdit, self.bms_config.vcell8),
            (self.ui.vcellMinLineEdit, self.bms_config.vcell_min),
            (self.ui.vcellMaxLineEdit, self.bms_config.vcell_max),
            (self.ui.vcellBattLineEdit, self.bms_config.vbatt),
            (self.ui.vcellVrgoLineEdit, self.bms_config.vrgo),
        ]
        for line_edit, value in voltage_fields:
            line_edit.setText(f"{value:.2f}")


        #Temperature      
        gain = 0
        if(self.bms_config.bit_tgain):
            gain = 1
            self.ui.TemperatureGainLabel.setText("Now the gain is 1x")
        else:
            gain = 2
            self.ui.TemperatureGainLabel.setText("Now the gain is 2x")
            
        self.ui.tempITVoltaqeLineEdit.setText(f"{self.bms_config.temp_internal:.2f}")
        internal_temp_celsius = ((self.bms_config.temp_internal *1000)/(gain*0.92635)) - 273.15
        self.ui.tempITDegLineEdit.setText(f"{internal_temp_celsius:.2f}")

        self.ui.tempXT1VoltaqeLineEdit.setText(f"{self.bms_config.temp_xt1:.2f}")
        self.ui.tempXT2VoltaqeLineEdit.setText(f"{self.bms_config.temp_xt2:.2f}")

        #Current
        resistor = float(self.ui.ResistorLineEdit.text())/1000
        current = float(self.bms_config.v_sense/resistor)
        voltage = self.bms_config.v_sense

        self.ui.CSGainLineEdit.setText(f"{int(self.bms_config.i_gain)}")
        self.ui.packCurrentVLineEdit.setText(f"{voltage*1000:.4f}") #in millivolts
        self.ui.packCurrentALineEdit.setText(f"{int(current*1000)}") # in milliamperes
        
    def ui_update_status_bits(self):
        status_mapping = {
            # address 0x80
            self.ui.bitOVlabel: self.bms_config.bit_ov,
            self.ui.bitOVLOlabel: self.bms_config.bit_ovlo,
            self.ui.bitUVlabel: self.bms_config.bit_uv,
            self.ui.bitUVLOlabel: self.bms_config.bit_uvlo,
            self.ui.bitDOTlabel: self.bms_config.bit_dot,
            self.ui.bitDUTlabel: self.bms_config.bit_dut,
            self.ui.bitCOTlabel: self.bms_config.bit_cot,
            self.ui.bitCUTlabel: self.bms_config.bit_cut,
            # address 0x81
            self.ui.bitIOTlabel: self.bms_config.bit_iot,
            self.ui.bitCOClabel: self.bms_config.bit_coc,
            self.ui.bitDOClabel: self.bms_config.bit_doc,
            self.ui.bitDSClabel: self.bms_config.bit_dsc,
            self.ui.bitCELLFlabel: self.bms_config.bit_cellf,
            self.ui.bitOPENlabel: self.bms_config.bit_open,
            self.ui.bitEOCHGlabel: self.bms_config.bit_eochg,
            # address 0x82
            self.ui.bitLDPRSNTlabel: self.bms_config.bit_ld_prsnt,
            self.ui.bitCHPRSNTlabel: self.bms_config.bit_ch_prsnt,
            self.ui.bitCHINGlabel: self.bms_config.bit_ching,
            self.ui.bitDCHINGlabel: self.bms_config.bit_dching,
            self.ui.bitLVCHRGlabel: self.bms_config.bit_lvchg,
            # address 0x83
            self.ui.bitCBOTlabel: self.bms_config.bit_cbot,
            self.ui.bitCBUTlabel: self.bms_config.bit_cbut,
            self.ui.bitCBOVlabel: self.bms_config.bit_cbov,
            self.ui.bitCBUVlabel: self.bms_config.bit_cbuv,
            self.ui.bitIDLElabel: self.bms_config.bit_in_idle,
            self.ui.bitDOZElabel: self.bms_config.bit_in_doze,
            self.ui.bitSLEEPlabel: self.bms_config.bit_in_sleep
        }

        for label, bit in status_mapping.items():
            self.ui_show_status_bit(label, bit)


    def ui_show_status_bit(self, label, bit_config ):
        if ( bit_config):
            self.set_label_background_color ( label, QColor(0, 255, 0))
        else:
            self.set_label_background_color ( label, QColor(255, 255, 255))


    def set_label_background_color(self, label, color):
        # Set the background color using style sheet
        current_style = label.styleSheet()
        label.setStyleSheet(f"{current_style} background-color: {color.name()};")


    def convert_to_hex(self, value, config_type):
        """
        Converts a given value to hexadecimal representation.

        Args:
            value (float or str): The value to be converted.

        Returns:
            int: The hexadecimal representation of the value.

        Raises:
            None

        """
        try:
            return int(float(value) / config_type)
        except ValueError:
            print(f"Error converting {value} to hex.")
            return 0
    
    def get_unit_from_combo(self, combo):
        """Read the combobox and return the unit chosen by user."""
        selected_text = combo.currentText()
        unit = next((code for code, text in UNIT_MAPPING.items() if text == selected_text), None)
        return unit
         
    def write_voltage_limits(self):
        voltage_values = [
            (self.ui.ovLineEdit.text(),     0x00),
            (self.ui.ovRecoverLineEdit.text(), 0x02),
            (self.ui.underVoltageLineEdit.text(), 0x04),
            (self.ui.uvRecoverLineEdit.text(), 0x06),
            (self.ui.ovLockoutLineEdit.text(), 0x08),
            (self.ui.uvLockoutLineEdit.text(), 0x0a),
            (self.ui.eocVoltageLineEdit.text(), 0x0c),
            (self.ui.LowVoltageChargeLineEdit.text(), 0x0e),
            (self.ui.sleepVoltageLineEdit.text(), 0x44)
        ]
        for value, address in voltage_values:
            hex_value = self.convert_to_hex(value, VOLTAGE_CELL_MULTIPLIER)
            self.isl94203.reg_write(address, hex_value, MASK_12BIT, 0x00)

    def write_voltage_limits_timing(self):
        # Extract values from QLineEdit fields
        ov_delay_timeout = int(self.ui.ovDelayTimeoutLineEdit.text())
        uv_delay_timeout = int(self.ui.uvDelayTimeoutLineEdit.text())
        open_wire_sample_time = int(self.ui.openWireTimingLineEdit.text())
        sleep_delay = int(self.ui.sleepDelayLineEdit.text())
    
        # Extract and shift units
        ov_delay_timeout_unit = self.get_unit_from_combo(self.ui.ovDelayTimeoutCombo) << 10
        uv_delay_timeout_unit = self.get_unit_from_combo(self.ui.uvDelayTimeoutCombo) << 10
        sleep_delay_unit = self.get_unit_from_combo(self.ui.sleepDelayUnitCombo) << 9
        open_wire_sample_time_unit = self.get_unit_from_combo(self.ui.openWireTimingCombo) << 9
    
        # Combine values and units, then write to registers
        self.isl94203.reg_write(0x10, ov_delay_timeout_unit | ov_delay_timeout, MASK_12BIT, 0)
        self.isl94203.reg_write(0x12, uv_delay_timeout_unit | uv_delay_timeout, MASK_12BIT, 0)
        self.isl94203.reg_write(0x14, open_wire_sample_time_unit | open_wire_sample_time, MASK_10BIT, 0)
        self.isl94203.reg_write(0x46, sleep_delay_unit | sleep_delay, MASK_11BIT, 0)


    def convert_time_to_hex(self, time, escaling):
        """Convert time to hex value."""
        return int(time)>> escaling
    
    def write_timers(self):

        timer_values = [
            (self.ui.timerWDTLineEdit.text(), 0x46, MASK_5BIT, 11, 0),
            (self.ui.timerIdleDozeCombo.currentText(), 0x48, MASK_4BIT, 0, 0),
            (self.ui.timerSleepCombo.currentText(), 0x48, MASK_4BIT, 4, 4)
        ]
        for value, address, mask, shift, scaling in timer_values:
            hex_value = self.convert_time_to_hex(value, scaling)
            self.isl94203.reg_write(address, hex_value, mask, shift)



    def write_cell_balance_registers(self):
        cell_balance_values = [
            (self.ui.CBLowerLimLineEdit.text(), 0x1c),
            (self.ui.CBUpperLimLineEdit.text(), 0x1e),
            (self.ui.CBMinDeltaLineEdit.text(), 0x20),
            (self.ui.CBMaxDeltaLineEdit.text(), 0x22),
            (self.ui.CBOnTimeLineEdit.text(), 0x24),
            (self.ui.CBOffTimeLineEdit.text(), 0x26)
        ]
        for value, address in cell_balance_values:
            hex_value = self.convert_to_hex(value, VOLTAGE_CELL_MULTIPLIER)
            self.isl94203.reg_write(address, hex_value, MASK_12BIT, 0x00)

        cell_balance_temp_values = [
                        (self.ui.CBUnderTempLineEdit.text(), 0x28),
            (self.ui.CBUTRecoverLineEdit.text(), 0x2a),
            (self.ui.CBOverTempLineEdit.text(), 0x2c),
            (self.ui.CBOTRecoverLineEdit.text(), 0x2e)
        ]
        for value, address in cell_balance_temp_values:
            hex_value = self.convert_to_hex(value, TEMPERATURE_MULTIPLIER)
            self.isl94203.reg_write(address, hex_value, MASK_12BIT, 0x00)
            
        # Extract and shift units
        cb_on_time_unit = self.get_unit_from_combo(self.ui.CBOnTimeUnitLineEdit) << 10
        cb_off_time_unit = self.get_unit_from_combo(self.ui.CBOffTimeUnitLineEdit) << 10

        # Combine values and units, then write to registers
        self.isl94203.reg_write(0x24, cb_on_time_unit | int(self.ui.CBOnTimeLineEdit.text()), MASK_12BIT, 0)
        self.isl94203.reg_write(0x26, cb_off_time_unit | int(self.ui.CBOffTimeLineEdit.text()), MASK_12BIT, 0)


    def write_temperature_registers(self):
        temp_values = [
            (self.ui.TLChargeOverTempLineEdit.text(), 0x30),
            (self.ui.TLChargeOTRecoverLineEdit.text(), 0x32),
            (self.ui.TLChargeUnderTempLineEdit.text(), 0x34),
            (self.ui.TLChargeUTRecoverLineEdit.text(), 0x36),
            (self.ui.TLDiscOverTempLineEdit.text(), 0x38),
            (self.ui.TLDischOTRecoverLineEdit.text(), 0x3a),
            (self.ui.TLDischUnderTempLineEdit.text(), 0x3C),
            (self.ui.TLDischUTRecoverLineEdit.text(), 0x3E),
            (self.ui.TLInternalOverTempLineEdit.text(), 0x40),
            (self.ui.TLInternalOTRecoverLineEdit.text(), 0x42)
        ]
        for value, address in temp_values:
            hex_value = self.convert_to_hex(value, TEMPERATURE_MULTIPLIER)
            self.isl94203.reg_write(address, hex_value, MASK_12BIT, 0x00)

    def write_current_registers(self):
        # Helper function to pack values into the register
        def pack_register_value(timeout, unit, voltage):
            # timeout is 10 bits (0-9), unit is 2 bits (10-11), voltage is 3 bits (12-14)
            return (timeout & 0x3FF) | ((unit & 0x3) << 10) | ((voltage & 0x7) << 12)

        # Define the mappings for the different selections
        register_mappings = [
            {
                'timeout_edit': self.ui.CLDischargeOCTimeoutLineEdit,
                'unit_combo': self.ui.CLDischargeOCTimeoutCombo,
                'voltage_combo': self.ui.CLDischargeOCVoltageCombo,
                'address': 0x16,
                'voltage_mapping': DOC_MAPPING
            },
            {
                'timeout_edit': self.ui.CLChargeOCTimeoutLineEdit,
                'unit_combo': self.ui.CLChargeOCTimeoutCombo,
                'voltage_combo': self.ui.CLChargeOCVoltageCombo,
                'address': 0x18,
                'voltage_mapping': COC_MAPPING
            },
            {
                'timeout_edit': self.ui.CLDischargeSCTimeoutLineEdit,
                'unit_combo': self.ui.CLDischargeSCTimeoutCombo,
                'voltage_combo': self.ui.CLDischargeSCVoltageCombo,
                'address': 0x1A,
                'voltage_mapping': DSC_MAPPING
            }
        ]

        # Iterate over each mapping and write the corresponding register value
        for reg in register_mappings:
            # Extract the timeout value
            timeout_value = int(reg['timeout_edit'].text())

            # Find the corresponding unit key from the unit mapping
            selected_unit = reg['unit_combo'].currentText()
            unit_key = next(key for key, value in UNIT_MAPPING.items() if value == selected_unit)

            # Find the corresponding voltage key from the voltage mapping
            selected_voltage = reg['voltage_combo'].currentText()
            voltage_key = next(key for key, value in reg['voltage_mapping'].items() if value == selected_voltage)

            # Pack the timeout, unit, and voltage into the register value
            packed_value = pack_register_value(timeout_value, unit_key, voltage_key)

            # Write the packed value to the register
            self.isl94203.reg_write(reg['address'], packed_value, MASK_15BIT, 0x00)

        # Extract the charge and load detect pulse widths
        charge_detect_pulse = int(self.ui.chargeDetectPulseCombo.currentText())
        load_detect_pulse = int(self.ui.loadDetectPulseCombo.currentText())

        # Write the charge and load detect pulse widths to the registers
        self.isl94203.reg_write(0x00, charge_detect_pulse, MASK_4BIT, 12)
        self.isl94203.reg_write(0x04, load_detect_pulse, MASK_4BIT, 12)


    def write_pack_option_registers(self):
        pack_options = [
            (self.ui.poT2MonitorsFETTempCheckBox.isChecked(), 0x4A, MASK_1BIT, 5), 
            (self.ui.poEnableCELLFpsdCheckBox.isChecked(), 0x4A, MASK_1BIT, 7),    
            (self.ui.poEnableOpenWirePSDCheckBox.isChecked(), 0x4A, MASK_1BIT, 0), 
            (self.ui.poEnableUVLOCheckBox.isChecked(), 0x4B, MASK_1BIT, 3),        
            (self.ui.poEnableOpenWireScanCheckBox.isChecked(), 0x4A, MASK_1BIT, 1),
            (self.ui.CBDuringChargeCheckBox.isChecked(), 0x4B, MASK_1BIT, 6),      
            (self.ui.CBDuringDischargeCheckBox.isChecked(), 0x4B, MASK_1BIT, 7),   
            (self.ui.CBDuringEOCCheckBox.isChecked(), 0x4B, MASK_1BIT, 0),         
            (self.ui.tGainCheckBox.isChecked(), 0x4A, MASK_1BIT, 4)               
        ]
        for value, address, mask, shift in pack_options:
            self.isl94203.reg_write(address, int(value), mask, shift)



    def send_serial_command(self, command, data):
        # Access the shared serial_setup
        serial_setup = self.ui.serial_setup

        try:
            if serial_setup and serial_setup.is_open():
                # Send the configuration data over serial
                serial_protocol = SerialProtocol(serial_setup)
                serial_protocol.send_command(command, data)
                packet = serial_protocol.read_packet()
                _ , response = packet
                print(f"response: {response}")
            else:
                logging.warning("Serial port is not open")
        except Exception as e:
            logging.error(f"Failed to send serial command: {e}")

    def write_bms_config(self):

        if self.ui.serial_setup and self.ui.serial_setup.is_open():
            register_cfg = ISL94203.registers
  
            self.write_voltage_limits()
            self.write_voltage_limits_timing()
            self.write_timers()
            self.write_cell_balance_registers()
            self.write_temperature_registers()
            self.write_current_registers()
            self.write_pack_option_registers()

            logging.info(f"write_bms_config():\n{' '.join(f'{value:02X}' for value in register_cfg)}")
            
            self.send_serial_command(CMD_WRITE_EEPROM, register_cfg)
        else: 
            logging.error("Serial port is not open")
            self.ui.statusBar.showMessage("Error: Serial port is not open.") 

    def read_bms_config(self):
        """Read the BMS configuration from the device."""
        serial_setup = self.ui.serial_setup        
        configuration = []
        try:
            if serial_setup and serial_setup.is_open():
                # Send the configuration data over serial
                serial_protocol = SerialProtocol(serial_setup)
                serial_protocol.send_command(CMD_READ_ALL_MEMORY, [])   
                packet = serial_protocol.read_packet()
                _ , configuration = packet

                self.bms_config.update_registers(list(configuration))
                self.ui_update_fields()

                logging.info(f"read_bms_config():\n{' '.join(f'{value:02X}' for value in configuration)}")
                self.ui.statusBar.showMessage("Configuration read successfully.")
            else:
                ERROR_MESSAGE = "Serial port is not open"
                logging.error(ERROR_MESSAGE)
                self.ui.statusBar.showMessage(f"Error: {ERROR_MESSAGE}.")
        except Exception as e:
            logging.error(f"Failed to read BMS configuration: {e}")
            self.ui.statusBar.showMessage(f"Error: {e}")
