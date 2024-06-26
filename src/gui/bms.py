from PyQt5.QtGui import QColor
from bms.constants import *
from serialbsp.protocol import *

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

    def get_unit_from_combo(self, combo):
        """Read the combobox and return the unit chosen by user."""
        selected_text = combo.currentText()
        unit = next((code for code, text in self.bms_config.unit_mapping.items() if text == selected_text), None)
        return unit
    
    def read_bms_config(self):

        #@todo: Implemetar para usar a serial.
        # Serial read
        # save values
        # mostra na tela
        # Access the shared serial_setup
        serial_setup = self.ui.serial_setup        
        register_cfg_int = []
        if serial_setup and serial_setup.is_open():
            # Send the configuration data over serial
            serial_protocol = SerialProtocol(serial_setup)
            serial_protocol.send_command(CMD_READ_ALL_MEMORY, [])   
            packet = serial_protocol.read_packet()
            _ , register_cfg_int = packet
        else:
            print("Serial port is not open")

        configuration =  register_cfg_int

        self.bms_config.update_registers(list(configuration))

        print(f"read_bms_config: {list(configuration)}")

        self.update_ui_fields()

    def update_ui_fields(self):

        """Updates the UI fields with the current BMS configuration."""
        #Voltage Limits
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

        self.ui.ovDelayTimeoutLineEdit.setText(f"{int(self.bms_config.ov_delay_timeout)}")
        self.ui.uvDelayTimeoutLineEdit.setText(f"{int(self.bms_config.uv_delay_timeout)}")
        self.ui.sleepDelayLineEdit.setText(f"{int(self.bms_config.sleep_delay)}")
        self.ui.openWireTimingLineEdit.setText(f"{int(self.bms_config.open_wire_timing)}")

        self.update_combo_boxes()
        self.update_timer_fields()
        self.update_cell_balance_limits()
        self.update_temperature_limits()
        self.update_current_limits()
        self.update_pack_option()
        self.update_ram_values()
        self.update_status_bits()

    
    def update_combo_boxes(self):
        """Update the combo boxes with the selected values."""
        combo_boxes = [
            (self.ui.ovDelayTimeoutCombo, self.bms_config.ov_delay_timeout_unit),
            (self.ui.uvDelayTimeoutCombo, self.bms_config.uv_delay_timeout_unit),
            (self.ui.sleepDelayUnitCombo, self.bms_config.sleep_delay_unit),
            (self.ui.openWireTimingCombo, self.bms_config.open_wire_timing_unit)
        ]
        for combo, value in combo_boxes:
            combo.setCurrentText(self.bms_config.unit_mapping.get(int(value), 'Unknown'))

    def update_timer_fields(self):
        """Update timer-related fields."""
        timer_fields = {
            self.ui.timerIdleDozeLineEdit: self.bms_config.timer_idle_doze,
            self.ui.timerSleepLineEdit: self.bms_config.timer_sleep,
            self.ui.timerWDTLineEdit: self.bms_config.timer_idle_doze
        }
        for line_edit, value in timer_fields.items():
            line_edit.setText(f"{int(value)}")

    def update_cell_balance_limits(self):
        """Update cell balance limits fields."""
        self.ui.CellConfigurationLineEdit.setText(f"{int(self.bms_config.cell_config_code[self.bms_config.cell_config])}")
        
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
        self.ui.CBOnTimeUnitLineEdit.setCurrentText(self.bms_config.unit_mapping.get(int(self.bms_config.cb_on_time_unit), 'Unknown'))
        self.ui.CBOffTimeUnitLineEdit.setCurrentText(self.bms_config.unit_mapping.get(int(self.bms_config.cb_off_time_unit), 'Unknown'))

    def update_temperature_limits(self):
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

    def update_current_limits(self):
        """Update current limits fields."""
        current_limits = {
            self.ui.CLDischargeOCVoltageCombo: (self.bms_config.disch_oc_voltage, self.bms_config.doc_mapping),
            self.ui.CLChargeOCVoltageCombo: (self.bms_config.charge_oc_voltage, self.bms_config.coc_mapping),
            self.ui.CLDischargeSCVoltageCombo: (self.bms_config.disch_sc_voltage, self.bms_config.dsc_mapping),
            self.ui.CLDischargeOCTimeoutCombo: (self.bms_config.disch_oc_timeout_unit, self.bms_config.unit_mapping),
            self.ui.CLChargeOCTimeoutCombo: (self.bms_config.charge_oc_timeout_unit, self.bms_config.unit_mapping),
            self.ui.CLDischargeSCTimeoutCombo: (self.bms_config.disch_sc_timeout_unit, self.bms_config.unit_mapping)
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

    def update_pack_option(self):
        """Update pack option fields."""
        options = {
            self.ui.poT2MonitorsFETTempCheckBox: self.bms_config.bit_t2_monitors_fet,
            self.ui.poEnableCELLFpsdCheckBox: self.bms_config.bit_enable_cellf_psd,
            self.ui.poEnableOpenWirePSDCheckBox: self.bms_config.bit_enable_openwire_psd,
            self.ui.poEnableUVLOCheckBox: self.bms_config.bit_enable_uvlo_pd,
            self.ui.poEnableOpenWireScanCheckBox: self.bms_config.bit_enable_openwire_scan,
            self.ui.poCascadeCheckBox: True,
            self.ui.CBDuringChargeCheckBox: self.bms_config.bit_cb_during_charge,
            self.ui.CBDuringDischargeCheckBox: self.bms_config.bit_cb_during_discharge,
            self.ui.CBDuringEOCCheckBox: self.bms_config.bit_cb_during_eoc,
            self.ui.tGainCheckBox: self.bms_config.bit_tgain
            }
        for checkbox, value in options.items():
            checkbox.setChecked(value)

    def update_ram_values(self):
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
        
    def update_status_bits(self):
        #Status Bits from addresses 0x80, 0x81, 0x82, 0x83
        self.show_status_bit(self.ui.bitOVlabel,    self.bms_config.bit_ov)
        self.show_status_bit(self.ui.bitOVLOlabel,  self.bms_config.bit_ovlo)
        self.show_status_bit(self.ui.bitEOCHGlabel, self.bms_config.bit_uv)
        self.show_status_bit(self.ui.bitOVlabel,    self.bms_config.bit_uvlo)
        self.show_status_bit(self.ui.bitOVLOlabel,  self.bms_config.bit_dot)
        self.show_status_bit(self.ui.bitEOCHGlabel, self.bms_config.bit_dut)        
        self.show_status_bit(self.ui.bitOVlabel,    self.bms_config.bit_cot)
        self.show_status_bit(self.ui.bitOVlabel,    self.bms_config.bit_cut)
        
        #address 0x81
        self.show_status_bit(self.ui.bitIOTlabel,   self.bms_config.bit_iot)
        self.show_status_bit(self.ui.bitCOClabel,   self.bms_config.bit_coc)
        self.show_status_bit(self.ui.bitDOClabel,   self.bms_config.bit_doc)
        self.show_status_bit(self.ui.bitDSClabel,   self.bms_config.bit_dsc)
        self.show_status_bit(self.ui.bitCELLFlabel, self.bms_config.bit_cellf)
        self.show_status_bit(self.ui.bitOPENlabel,  self.bms_config.bit_open)
        self.show_status_bit(self.ui.bitEOCHGlabel, self.bms_config.bit_eochg)
     
        #address 0x82
        self.show_status_bit(self.ui.bitLDPRSNTlabel, self.bms_config.bit_ld_prsnt)
        self.show_status_bit(self.ui.bitCHPRSNTlabel, self.bms_config.bit_ch_prsnt)
        self.show_status_bit(self.ui.bitCHINGlabel,   self.bms_config.bit_ching)
        self.show_status_bit(self.ui.bitDCHINGlabel,  self.bms_config.bit_dching)
        #self.show_status_bit(self.ui.bitlabel,  self.bms_config.bit_ecc_used)
        #self.show_status_bit(self.ui.bitlabel, self.bms_config.bit_ecc_fail)        
        #self.show_status_bit(self.ui.bitlabel,    self.bms_config.bit_int_scan)
        self.show_status_bit(self.ui.bitLVCHRGlabel,    self.bms_config.bit_lvchg)        
        
        #address 0x83
        self.show_status_bit(self.ui.bitCBOTlabel,  self.bms_config.bit_cbot)
        self.show_status_bit(self.ui.bitCBUTlabel,  self.bms_config.bit_cbut)
        self.show_status_bit(self.ui.bitCBOVlabel,  self.bms_config.bit_cbov)
        self.show_status_bit(self.ui.bitCBUVlabel,  self.bms_config.bit_cbuv)
        self.show_status_bit(self.ui.bitIDLElabel,  self.bms_config.bit_in_idle)
        self.show_status_bit(self.ui.bitDOZElabel,  self.bms_config.bit_in_doze)
        self.show_status_bit(self.ui.bitSLEEPlabel, self.bms_config.bit_in_sleep)

    def show_status_bit(self, label, bit_config ):
        if ( bit_config):
            self.set_label_background_color ( label, QColor(0, 255, 0))
        else:
            self.set_label_background_color ( label, QColor(255, 255, 255))


    def set_label_background_color(self, label, color):
        # Set the background color using style sheet
        current_style = label.styleSheet()
        label.setStyleSheet(f"{current_style} background-color: {color.name()};")

    def write_bms_config(self):

        register_cfg = self.bms_config.get_config()

        print("entered write_bms_config:", register_cfg)

        # Convert Editline values to HEX
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

        register_cfg_int = [int(val, 16) for val in register_cfg]

        # Access the shared serial_setup
        serial_setup = self.ui.serial_setup

        if serial_setup and serial_setup.is_open():
            # Send the configuration data over serial
            serial_protocol = SerialProtocol(serial_setup)
            serial_protocol.send_command(CMD_WRITE_EEPROM, register_cfg_int)    
        else:
            print("Serial port is not open")
 
    def on_line_edit_changed(self, text):
        print(f"Line Edit Changed: {text}")