from bms_constants import *
from PyQt5.QtGui import QPalette, QColor

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

        #Voltage Limits
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

        #-- Update the combo box with the selected value
        self.ui.ovDelayTimeoutCombo.setCurrentText(self.bms_config.unit_mapping.get(int(self.bms_config.ov_delay_timeout_unit), 'Unknown'))
        self.ui.uvDelayTimeoutCombo.setCurrentText(self.bms_config.unit_mapping.get(int(self.bms_config.uv_delay_timeout_unit), 'Unknown'))
        self.ui.sleepDelayUnitCombo.setCurrentText(self.bms_config.unit_mapping.get(int(self.bms_config.sleep_delay_unit), 'Unknown'))
        self.ui.openWireTimingCombo.setCurrentText(self.bms_config.unit_mapping.get(int(self.bms_config.open_wire_timing_unit), 'Unknown'))

        #Timers
        self.ui.timerIdleDozeLineEdit.setText(f"{int(self.bms_config.timer_idle_doze)}")
        self.ui.timerSleepLineEdit.setText(f"{int(self.bms_config.timer_sleep)}")
        self.ui.timerWDTLineEdit.setText(f"{int(self.bms_config.timer_idle_doze)}")

        #Cell Configuration 
        self.ui.CellConfigurationLineEdit.setText(f"{int(self.bms_config.cell_config_code[self.bms_config.cell_config])}")
        
        #Cell Balance Limits
        self.ui.CBUpperLimLineEdit.setText(f"{self.bms_config.cb_upper_lim:.2f}")
        self.ui.CBLowerLimLineEdit.setText(f"{self.bms_config.cb_lower_lim:.2f}")
        self.ui.CBMaxDeltaLineEdit.setText(f"{self.bms_config.cb_max_delta:.2f}")
        self.ui.CBMinDeltaLineEdit.setText(f"{self.bms_config.cb_min_delta:.2f}")
        self.ui.CBOverTempLineEdit.setText(f"{self.bms_config.cb_over_temp:.2f}")
        self.ui.CBOTRecoverLineEdit.setText(f"{self.bms_config.cb_ot_recover:.2f}")
        self.ui.CBUTRecoverLineEdit.setText(f"{self.bms_config.cb_ut_recover:.2f}")
        self.ui.CBUnderTempLineEdit.setText(f"{self.bms_config.cb_under_temp:.2f}")
       
        self.ui.CBOnTimeLineEdit.setText(f"{int(self.bms_config.cb_on_time)}")
        self.ui.CBOffTimeLineEdit.setText(f"{int(self.bms_config.cb_off_time)}")
        self.ui.CBOnTimeUnitLineEdit.setCurrentText(self.bms_config.unit_mapping.get(int(self.bms_config.cb_on_time_unit), 'Unknown'))
        self.ui.CBOffTimeUnitLineEdit.setCurrentText(self.bms_config.unit_mapping.get(int(self.bms_config.cb_off_time_unit), 'Unknown'))

        #Temperature Limits
        self.ui.TLChargeOverTempLineEdit.setText(f"{self.bms_config.tl_charge_over_temp:.2f}")
        self.ui.TLChargeOTRecoverLineEdit.setText(f"{self.bms_config.tl_charge_ot_recover:.2f}")
        self.ui.TLChargeUTRecoverLineEdit.setText(f"{self.bms_config.tl_charge_ut_recover:.2f}")
        self.ui.TLChargeUnderTempLineEdit.setText(f"{self.bms_config.tl_charge_under_temp:.2f}")

        self.ui.TLDiscOverTempLineEdit.setText(f"{self.bms_config.tl_disch_over_temp:.2f}")
        self.ui.TLDischOTRecoverLineEdit.setText(f"{self.bms_config.tl_charge_ot_recover:.2f}")
        self.ui.TLDischUTRecoverLineEdit.setText(f"{self.bms_config.tl_disch_ut_recover:.2f}")
        self.ui.TLDischUnderTempLineEdit.setText(f"{self.bms_config.tl_disch_under_temp:.2f}")
        self.ui.TLInternalOverTempLineEdit.setText(f"{self.bms_config.tl_internal_over_temp:.2f}")
        self.ui.TLInternalOTRecoverLineEdit.setText(f"{self.bms_config.tl_internal_ot_recover:.2f}")
        

        #Current Limit
        self.ui.CLDischargeOCVoltageCombo.setCurrentText(self.bms_config.doc_mapping.get(int(self.bms_config.disch_oc_voltage), 'Unknown'))
        self.ui.CLChargeOCVoltageCombo.setCurrentText(self.bms_config.coc_mapping.get(int(self.bms_config.charge_oc_voltage), 'Unknown'))
        self.ui.CLDischargeSCVoltageCombo.setCurrentText(self.bms_config.dsc_mapping.get(int(self.bms_config.disch_sc_voltage), 'Unknown'))

        self.ui.CLDischargeOCTimeoutCombo.setCurrentText(self.bms_config.unit_mapping.get(int(self.bms_config.disch_oc_timeout_unit), 'Unknown'))
        self.ui.CLChargeOCTimeoutCombo.setCurrentText(self.bms_config.unit_mapping.get(int(self.bms_config.charge_oc_timeout_unit), 'Unknown'))
        self.ui.CLDischargeSCTimeoutCombo.setCurrentText(self.bms_config.unit_mapping.get(int(self.bms_config.disch_sc_timeout_unit), 'Unknown'))

        self.ui.CLDischargeOCTimeoutLineEdit.setText(f"{int(self.bms_config.disch_oc_timeout)}")
        self.ui.CLChargeOCTimeoutLineEdit.setText(f"{int(self.bms_config.charge_oc_timeout)}")
        self.ui.CLDischargeSCTimeoutLineEdit.setText(f"{int(self.bms_config.disch_sc_timeout)}")
        
        #Pack Option
        self.ui.poT2MonitorsFETTempCheckBox.setChecked(self.bms_config.bit_t2_monitors_fet)
        self.ui.poEnableCELLFpsdCheckBox.setChecked(self.bms_config.bit_enable_cellf_psd)
        self.ui.poEnableOpenWirePSDCheckBox.setChecked(self.bms_config.bit_enable_openwire_psd)
        self.ui.poEnableUVLOCheckBox.setChecked(self.bms_config.bit_enable_uvlo_pd)
        self.ui.poEnableOpenWireScanCheckBox.setChecked(self.bms_config.bit_enable_openwire_scan)
        self.ui.poCascadeCheckBox.setChecked(True)
        
        self.ui.CBDuringChargeCheckBox.setChecked(self.bms_config.bit_cb_during_charge)
        self.ui.CBDuringDischargeCheckBox.setChecked(self.bms_config.bit_cb_during_discharge)
        self.ui.CBDuringEOCCheckBox.setChecked(self.bms_config.bit_cb_during_eoc)

        #RAM
        self.ui.vcell1LineEdit.setText(f"{self.bms_config.vcell1:.2f}")
        self.ui.vcell2LineEdit.setText(f"{self.bms_config.vcell2:.2f}")
        self.ui.vcell3LineEdit.setText(f"{self.bms_config.vcell3:.2f}")
        self.ui.vcell4LineEdit.setText(f"{self.bms_config.vcell4:.2f}")
        self.ui.vcell5LineEdit.setText(f"{self.bms_config.vcell5:.2f}")
        self.ui.vcell6LineEdit.setText(f"{self.bms_config.vcell6:.2f}")
        self.ui.vcell7LineEdit.setText(f"{self.bms_config.vcell7:.2f}")
        self.ui.vcell8LineEdit.setText(f"{self.bms_config.vcell8:.2f}")
        
        self.ui.vcellMinLineEdit.setText(f"{self.bms_config.vcell_min:.2f}")
        self.ui.vcellMaxLineEdit.setText(f"{self.bms_config.vcell_max:.2f}")
        
        self.ui.vcellBattLineEdit.setText(f"{self.bms_config.vbatt:.2f}")
        self.ui.vcellVrgoLineEdit.setText(f"{self.bms_config.vrgo:.2f}")

        #Current
        resistor = float(self.ui.ResistorLineEdit.text())/1000
        current = float(self.bms_config.v_sense/resistor)
        voltage = self.bms_config.v_sense

        self.ui.CSGainLineEdit.setText(f"{int(self.bms_config.i_gain)}")
        self.ui.packCurrentVLineEdit.setText(f"{voltage*1000:.4f}") #in millivolts
        self.ui.packCurrentALineEdit.setText(f"{int(current*1000)}") # in milliamperes
        
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

#Write values in the correct position
    def on_line_edit_changed(self, text):
        print(f"Line Edit Changed: {text}")
        # Add your desired actions here
