from PySide6.QtGui import QColor
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QPushButton, QStatusBar, QLineEdit, QComboBox, QCheckBox, QLabel, QSpinBox

from bms.isl94203_constants import *

from gui.utility import convert_time_to_hex, convert_to_hex
from logger.log_handler import LogHandler
from bms.isl94203_factory import ISL94203Factory

import logging

from serialbsp.commands import CMD_READ_ALL_MEMORY, CMD_READ_RAM, CMD_WRITE_EEPROM


class BmsTab:
    def __init__(self, ui, bms_driver, log_callback):
        self.ui = ui
        self.resistor = 0.005
        self.isl94203_driver = bms_driver
        self.isl94203 = ISL94203Factory.create_instance()
        self.log_file_path = None
        self.log_callback = log_callback
        self.serial_setup = self.ui.fmcw_serial_manager
        self.serial_protocol = None
        


        # Connect button click to Send Serial Command
        self.ui.findChild(QPushButton, "readPackButton").clicked.connect(self.read_bms_config)
        self.ui.findChild(QPushButton, "writePackButton").clicked.connect(self.write_bms_config)
        self.ui.findChild(QPushButton, "readRamButton").clicked.connect(self.read_bms_ram_config)
        self.ui.findChild(QPushButton, "loadDefaultButton").clicked.connect(self.load_default_config)
        self.ui.findChild(QPushButton, "startStopLogButton").clicked.connect(self.log_bms_ram_config)

        self.statusBar = self.ui.findChild(QStatusBar, "statusBar")
        self.startStopLogButton = self.ui.findChild(QPushButton, "startStopLogButton")

        # Access QLineEdit elements using findChild
        self.ovLockoutLineEdit = self.ui.findChild(QLineEdit, "ovLockoutLineEdit")
        self.ovLineEdit = self.ui.findChild(QLineEdit, "ovLineEdit")
        self.ovRecoverLineEdit = self.ui.findChild(QLineEdit, "ovRecoverLineEdit")
        self.eocVoltageLineEdit = self.ui.findChild(QLineEdit, "eocVoltageLineEdit")
        self.uvRecoverLineEdit = self.ui.findChild(QLineEdit, "uvRecoverLineEdit")
        self.underVoltageLineEdit = self.ui.findChild(QLineEdit, "underVoltageLineEdit")
        self.sleepVoltageLineEdit = self.ui.findChild(QLineEdit, "sleepVoltageLineEdit")
        self.lowVoltageChargeLineEdit = self.ui.findChild(QLineEdit, "LowVoltageChargeLineEdit")
        self.uvLockoutLineEdit = self.ui.findChild(QLineEdit, "uvLockoutLineEdit")

        self.ovDelayTimeoutLineEdit = self.ui.findChild(QLineEdit, "ovDelayTimeoutLineEdit")
        self.uvDelayTimeoutLineEdit = self.ui.findChild(QLineEdit, "uvDelayTimeoutLineEdit")
        self.sleepDelayLineEdit = self.ui.findChild(QLineEdit, "sleepDelayLineEdit")
        self.openWireTimingLineEdit = self.ui.findChild(QLineEdit, "openWireTimingLineEdit")
        self.ovDelayTimeoutCombo = self.ui.findChild(QComboBox, "ovDelayTimeoutCombo")
        self.uvDelayTimeoutCombo = self.ui.findChild(QComboBox, "uvDelayTimeoutCombo")
        self.sleepDelayUnitCombo = self.ui.findChild(QComboBox, "sleepDelayUnitCombo")
        self.openWireTimingCombo = self.ui.findChild(QComboBox, "openWireTimingCombo")

        self.timerIdleDozeCombo = self.ui.findChild(QComboBox, "timerIdleDozeCombo")
        self.timerSleepCombo = self.ui.findChild(QComboBox, "timerSleepCombo")
        self.timerWDTLineEdit = self.ui.findChild(QLineEdit, "timerWDTLineEdit")

        self.CellConfigurationLineEdit = self.ui.findChild(QLineEdit, "CellConfigurationLineEdit")

        self.poT2MonitorsFETTempCheckBox = self.ui.findChild(QCheckBox, "poT2MonitorsFETTempCheckBox")
        self.poEnableCELLFpsdCheckBox = self.ui.findChild(QCheckBox, "poEnableCELLFpsdCheckBox")
        self.poEnableOpenWirePSDCheckBox = self.ui.findChild(QCheckBox, "poEnableOpenWirePSDCheckBox")
        self.poEnableUVLOCheckBox = self.ui.findChild(QCheckBox, "poEnableUVLOCheckBox")
        self.poEnableOpenWireScanCheckBox = self.ui.findChild(QCheckBox, "poEnableOpenWireScanCheckBox")

        self.CBUpperLimLineEdit = self.ui.findChild(QLineEdit, "CBUpperLimLineEdit")
        self.CBLowerLimLineEdit = self.ui.findChild(QLineEdit, "CBLowerLimLineEdit")
        self.CBMaxDeltaLineEdit = self.ui.findChild(QLineEdit, "CBMaxDeltaLineEdit")
        self.CBMinDeltaLineEdit = self.ui.findChild(QLineEdit, "CBMinDeltaLineEdit")
        self.CBOverTempLineEdit = self.ui.findChild(QLineEdit, "CBOverTempLineEdit")
        self.CBOTRecoverLineEdit = self.ui.findChild(QLineEdit, "CBOTRecoverLineEdit")
        self.CBUTRecoverLineEdit = self.ui.findChild(QLineEdit, "CBUTRecoverLineEdit")
        self.CBUnderTempLineEdit = self.ui.findChild(QLineEdit, "CBUnderTempLineEdit")
        self.CBOnTimeLineEdit = self.ui.findChild(QLineEdit, "CBOnTimeLineEdit")
        self.CBOffTimeLineEdit = self.ui.findChild(QLineEdit, "CBOffTimeLineEdit")
        self.CBOnTimeUnitLineEdit = self.ui.findChild(QComboBox, "CBOnTimeUnitLineEdit")
        self.CBOffTimeUnitLineEdit = self.ui.findChild(QComboBox, "CBOffTimeUnitLineEdit")

        self.CBDuringChargeCheckBox = self.ui.findChild(QCheckBox, "CBDuringChargeCheckBox")
        self.CBDuringDischargeCheckBox = self.ui.findChild(QCheckBox, "CBDuringDischargeCheckBox")
        self.CBDuringEOCCheckBox = self.ui.findChild(QCheckBox, "CBDuringEOCCheckBox")

        self.CLDischargeOCVoltageCombo = self.ui.findChild(QComboBox, "CLDischargeOCVoltageCombo")
        self.CLChargeOCVoltageCombo = self.ui.findChild(QComboBox, "CLChargeOCVoltageCombo")
        self.CLDischargeSCVoltageCombo = self.ui.findChild(QComboBox, "CLDischargeSCVoltageCombo")
        self.CLDischargeOCTimeoutCombo = self.ui.findChild(QComboBox, "CLDischargeOCTimeoutCombo")
        self.CLChargeOCTimeoutCombo = self.ui.findChild(QComboBox, "CLChargeOCTimeoutCombo")
        self.CLDischargeSCTimeoutCombo = self.ui.findChild(QComboBox, "CLDischargeSCTimeoutCombo")

        self.CLDischargeOCTimeoutLineEdit = self.ui.findChild(QLineEdit, "CLDischargeOCTimeoutLineEdit")
        self.CLChargeOCTimeoutLineEdit = self.ui.findChild(QLineEdit, "CLChargeOCTimeoutLineEdit")
        self.CLDischargeSCTimeoutLineEdit = self.ui.findChild(QLineEdit, "CLDischargeSCTimeoutLineEdit")

        self.chargeDetectPulseCombo = self.ui.findChild(QComboBox, "chargeDetectPulseCombo")
        self.loadDetectPulseCombo = self.ui.findChild(QComboBox, "loadDetectPulseCombo")

        self.TLChargeOverTempLineEdit = self.ui.findChild(QLineEdit, "TLChargeOverTempLineEdit")
        self.TLChargeOTRecoverLineEdit = self.ui.findChild(QLineEdit, "TLChargeOTRecoverLineEdit")
        self.TLChargeUTRecoverLineEdit = self.ui.findChild(QLineEdit, "TLChargeUTRecoverLineEdit")
        self.TLChargeUnderTempLineEdit = self.ui.findChild(QLineEdit, "TLChargeUnderTempLineEdit")
        self.TLDiscOverTempLineEdit = self.ui.findChild(QLineEdit, "TLDiscOverTempLineEdit")
        self.TLDischOTRecoverLineEdit = self.ui.findChild(QLineEdit, "TLDischOTRecoverLineEdit")
        self.TLDischUTRecoverLineEdit = self.ui.findChild(QLineEdit, "TLDischUTRecoverLineEdit")

        self.TLDischUnderTempLineEdit = self.ui.findChild(QLineEdit, "TLDischUnderTempLineEdit")
        self.TLInternalOverTempLineEdit = self.ui.findChild(QLineEdit, "TLInternalOverTempLineEdit")
        self.TLInternalOTRecoverLineEdit = self.ui.findChild(QLineEdit, "TLInternalOTRecoverLineEdit")

        self.tGainCheckBox = self.ui.findChild(QCheckBox, "tGainCheckBox")
        self.TemperatureGainLabel = self.ui.findChild(QLabel, "TemperatureGainLabel")

        self.vcell1LineEdit = self.ui.findChild(QLineEdit, "vcell1LineEdit")
        self.vcell2LineEdit = self.ui.findChild(QLineEdit, "vcell2LineEdit")
        self.vcell3LineEdit = self.ui.findChild(QLineEdit, "vcell3LineEdit")
        self.vcell4LineEdit = self.ui.findChild(QLineEdit, "vcell4LineEdit")
        self.vcell5LineEdit = self.ui.findChild(QLineEdit, "vcell5LineEdit")
        self.vcell6LineEdit = self.ui.findChild(QLineEdit, "vcell6LineEdit")
        self.vcell7LineEdit = self.ui.findChild(QLineEdit, "vcell7LineEdit")
        self.vcell8LineEdit = self.ui.findChild(QLineEdit, "vcell8LineEdit")
        self.vcellMinLineEdit = self.ui.findChild(QLineEdit, "vcellMinLineEdit")
        self.vcellMaxLineEdit = self.ui.findChild(QLineEdit, "vcellMaxLineEdit")
        self.vcellBattLineEdit = self.ui.findChild(QLineEdit, "vcellBattLineEdit")
        self.vcellVrgoLineEdit = self.ui.findChild(QLineEdit, "vcellVrgoLineEdit")

        self.CSGainLineEdit = self.ui.findChild(QLineEdit, "CSGainLineEdit")
        self.packCurrentVLineEdit = self.ui.findChild(QLineEdit, "packCurrentVLineEdit")
        self.packCurrentALineEdit = self.ui.findChild(QLineEdit, "packCurrentALineEdit")
        self.ResistorLineEdit = self.ui.findChild(QLineEdit, "ResistorLineEdit")

        self.tempITVoltaqeLineEdit = self.ui.findChild(QLineEdit, "tempITVoltaqeLineEdit")
        self.tempITDegLineEdit = self.ui.findChild(QLineEdit, "tempITDegLineEdit")
        self.tempXT1VoltaqeLineEdit = self.ui.findChild(QLineEdit, "tempXT1VoltaqeLineEdit")
        self.tempXT2VoltaqeLineEdit = self.ui.findChild(QLineEdit, "tempXT2VoltaqeLineEdit")

        self.bitOVlabel = self.ui.findChild(QLabel, "bitOVlabel")
        self.bitOVLOlabel = self.ui.findChild(QLabel, "bitOVLOlabel")
        self.bitUVlabel = self.ui.findChild(QLabel, "bitUVlabel")
        self.bitUVLOlabel = self.ui.findChild(QLabel, "bitUVLOlabel")
        self.bitDOTlabel = self.ui.findChild(QLabel, "bitDOTlabel")
        self.bitDUTlabel = self.ui.findChild(QLabel, "bitDUTlabel")
        self.bitCOTlabel = self.ui.findChild(QLabel, "bitCOTlabel")
        self.bitCUTlabel = self.ui.findChild(QLabel, "bitCUTlabel")
        self.bitIOTlabel = self.ui.findChild(QLabel, "bitIOTlabel")
        self.bitCOClabel = self.ui.findChild(QLabel, "bitCOClabel")
        self.bitDOClabel = self.ui.findChild(QLabel, "bitDOClabel")
        self.bitDSClabel = self.ui.findChild(QLabel, "bitDSClabel")
        self.bitCELLFlabel = self.ui.findChild(QLabel, "bitCELLFlabel")
        self.bitOPENlabel = self.ui.findChild(QLabel, "bitOPENlabel")
        self.bitEOCHGlabel = self.ui.findChild(QLabel, "bitEOCHGlabel")
        self.bitLDPRSNTlabel = self.ui.findChild(QLabel, "bitLDPRSNTlabel")
        self.bitCHPRSNTlabel = self.ui.findChild(QLabel, "bitCHPRSNTlabel")
        self.bitCHINGlabel = self.ui.findChild(QLabel, "bitCHINGlabel")
        self.bitDCHINGlabel = self.ui.findChild(QLabel, "bitDCHINGlabel")
        self.bitLVCHRGlabel = self.ui.findChild(QLabel, "bitLVCHRGlabel")
        self.bitCBOTlabel = self.ui.findChild(QLabel, "bitCBOTlabel")
        self.bitCBUTlabel = self.ui.findChild(QLabel, "bitCBUTlabel")
        self.bitCBOVlabel = self.ui.findChild(QLabel, "bitCBOVlabel")
        self.bitCBUVlabel = self.ui.findChild(QLabel, "bitCBUVlabel")
        self.bitIDLElabel = self.ui.findChild(QLabel, "bitIDLElabel")
        self.bitDOZElabel = self.ui.findChild(QLabel, "bitDOZElabel")
        self.bitSLEEPlabel = self.ui.findChild(QLabel, "bitSLEEPlabel")

        self.logRateSpinBox = self.ui.findChild(QSpinBox, "logRateSpinBox")

    def ui_update_ram_fields(self):
        self.ui_update_ram_values()
        self.ui_update_status_bits()

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
        voltage_limits = self.isl94203_driver.read_all_registers()
        voltage_fields = [
            (self.ovLockoutLineEdit, voltage_limits.get("overvoltage_lockout")),
            (self.ovLineEdit, voltage_limits.get("overvoltage_threshold")),
            (self.ovRecoverLineEdit, voltage_limits.get("overvoltage_recovery")),
            (self.eocVoltageLineEdit, voltage_limits.get("end_of_charge_voltage")),
            (self.uvRecoverLineEdit, voltage_limits.get("undervoltage_recovery")),
            (self.underVoltageLineEdit, voltage_limits.get("undervoltage_threshold")),
            (self.sleepVoltageLineEdit, voltage_limits.get("sleep_voltage")),
            (self.lowVoltageChargeLineEdit, voltage_limits.get("low_voltage_charge")),
            (self.uvLockoutLineEdit, voltage_limits.get("undervoltage_lockout"))
        ]
        for line_edit, value in voltage_fields:
            line_edit.setText(f"{value[0]:.2f}")

    def ui_update_voltage_limits_timing(self):
        """Update voltage limits timing fields and 
        Update the combo boxes with the selected values."""
        all_registers = self.isl94203_driver.read_all_registers()
        voltage_timing_fields = [
            (self.ovDelayTimeoutLineEdit, all_registers.get("ov_delay_timeout")),
            (self.uvDelayTimeoutLineEdit, all_registers.get("uv_delay_timeout")),
            (self.sleepDelayLineEdit, all_registers.get("sleep_delay")),
            (self.openWireTimingLineEdit, all_registers.get("open_wire_timing"))
        ]
        for line_edit, value in voltage_timing_fields:
            line_edit.setText(f"{int(value[0])}")

        combo_boxes = [
            (self.ovDelayTimeoutCombo, all_registers.get("ov_delay_timeout")),
            (self.uvDelayTimeoutCombo, all_registers.get("uv_delay_timeout")),
            (self.sleepDelayUnitCombo, all_registers.get("sleep_delay")),
            (self.openWireTimingCombo, all_registers.get("open_wire_timing"))
        ]
        for combo, value in combo_boxes:
            combo.setCurrentText(value[1])

    def ui_update_timer_fields(self):
        """Update timer-related fields."""
        all_registers = self.isl94203_driver.read_all_registers()

        timer_fields = {
            self.timerIdleDozeCombo: all_registers.get("timer_idle_doze"),
            self.timerSleepCombo: all_registers.get("timer_sleep"),
        }   

        for line_edit, value in timer_fields.items():
            line_edit.setCurrentText(f"{int(value[0])}")

        wdt_line_edit = self.timerWDTLineEdit
        wdt_line_edit.setText(f"{int(all_registers.get('timer_wdt')[0])}")

    def ui_update_cell_balance_limits(self):
        """Update cell balance limits fields."""
        all_registers = self.isl94203_driver.read_all_registers()

        cell_config = all_registers.get("cell_config")

        if cell_config == 0:
            self.CellConfigurationLineEdit.setText("0")
        else:
            self.CellConfigurationLineEdit.setText(f"{int(cell_config[0])}")

        cell_balance_limits = {
            self.CBUpperLimLineEdit: all_registers.get("cb_max_voltage"),
            self.CBLowerLimLineEdit: all_registers.get("cb_min_voltage"),
            self.CBMaxDeltaLineEdit: all_registers.get("cb_max_delta"),
            self.CBMinDeltaLineEdit: all_registers.get("cb_min_delta"),
            self.CBOverTempLineEdit: all_registers.get("cb_over_temp"),
            self.CBOTRecoverLineEdit: all_registers.get("cb_ot_recover"),
            self.CBUTRecoverLineEdit: all_registers.get("cb_ut_recover"),
            self.CBUnderTempLineEdit: all_registers.get("cb_under_temp")
        }
        for line_edit, value in cell_balance_limits.items():
            line_edit.setText(f"{value[0]:.2f}")

        cell_balance_timing = {
            self.CBOnTimeLineEdit: all_registers.get("cb_on_time"),
            self.CBOffTimeLineEdit: all_registers.get("cb_off_time")
        }
        for line_edit, value in cell_balance_timing.items():
            line_edit.setText(f"{int(value[0])}")  

        cell_balance_timing_units = {
            self.CBOnTimeUnitLineEdit: all_registers.get("cb_on_time"),
            self.CBOffTimeUnitLineEdit: all_registers.get("cb_off_time")
        }
        for combo, value in cell_balance_timing_units.items():
            combo.setCurrentText(value[1])

    def ui_update_temperature_limits(self):
        """Update temperature limits fields."""
        all_registers = self.isl94203_driver.read_all_registers()

        temp_limits = {
            self.TLChargeOverTempLineEdit: all_registers.get("tl_charge_ot"),
            self.TLChargeOTRecoverLineEdit: all_registers.get("tl_charge_ot_recover"),
            self.TLChargeUTRecoverLineEdit: all_registers.get("tl_charge_ut_recover"),
            self.TLChargeUnderTempLineEdit: all_registers.get("tl_charge_ut"),
            self.TLDiscOverTempLineEdit: all_registers.get("tl_discharge_ot"),
            self.TLDischOTRecoverLineEdit: all_registers.get("tl_discharge_ot_recover"),
            self.TLDischUTRecoverLineEdit: all_registers.get("tl_discharge_ut_recover"),
            self.TLDischUnderTempLineEdit: all_registers.get("tl_discharge_ut"),
            self.TLInternalOverTempLineEdit: all_registers.get("tl_internal_ot"),
            self.TLInternalOTRecoverLineEdit: all_registers.get("tl_internal_ot_recover")
        }

        for line_edit, value in temp_limits.items():
            line_edit.setText(f"{value[0]:.2f}")

    def ui_update_current_limits(self):
        """Update current limits fields."""
        
        all_registers = self.isl94203_driver.read_all_registers()

        current_limits = {
            self.CLDischargeOCVoltageCombo: all_registers.get("cl_discharge_oc"),
            self.CLChargeOCVoltageCombo: all_registers.get("cl_charge_oc"),
            self.CLDischargeSCVoltageCombo: all_registers.get("cl_discharge_sc"),
        }
        for combo, value in current_limits.items():
            combo.setCurrentText(value[0])


        current_fields = {
            self.CLDischargeOCTimeoutLineEdit: all_registers.get("cl_discharge_oc_delay"),
            self.CLChargeOCTimeoutLineEdit: all_registers.get("cl_charge_oc_delay"),
            self.CLDischargeSCTimeoutLineEdit: all_registers.get("cl_discharge_sc_delay")
        }
        for line_edit, value in current_fields.items():
            line_edit.setText(f"{int(value[0])}")

        current_timeout_units = {           
            self.CLDischargeOCTimeoutCombo: all_registers.get("cl_discharge_oc_delay"),
            self.CLChargeOCTimeoutCombo: all_registers.get("cl_charge_oc_delay"),
            self.CLDischargeSCTimeoutCombo: all_registers.get("cl_discharge_sc_delay")
        }
        for combo, value in current_timeout_units.items():
            combo.setCurrentText(value[1])

        current_detect_fields = {
            self.chargeDetectPulseCombo: all_registers.get("cl_pulse_width_charge"),
            self.loadDetectPulseCombo: all_registers.get("cl_pulse_width_load")
        }
        for combo, value in current_detect_fields.items():
            combo.setCurrentText(f"{value[0]}")

    def ui_update_pack_option(self):
        """Update pack option fields."""
        
        all_registers = self.isl94203_driver.read_all_registers()

        options = {
            self.poT2MonitorsFETTempCheckBox: all_registers.get("po_t2_monitors_fet"),
            self.poEnableCELLFpsdCheckBox: all_registers.get("po_enable_cellf_psd"),
            self.poEnableOpenWirePSDCheckBox: all_registers.get("po_enable_openwire_psd"),
            self.poEnableUVLOCheckBox: all_registers.get("po_enable_uvlo_pd"),
            self.poEnableOpenWireScanCheckBox: all_registers.get("po_enable_openwire_scan"),
            self.CBDuringChargeCheckBox: all_registers.get("cb_during_charge"),
            self.CBDuringDischargeCheckBox: all_registers.get("cb_during_discharge"),
            self.CBDuringEOCCheckBox: all_registers.get("cb_during_eoc"),
            self.tGainCheckBox: all_registers.get("tgain")
        }
        for checkbox, value in options.items():
            checkbox.setChecked(value[0])

    def ui_update_ram_values(self):
        # RAM
        # Voltage values: Cells, Min, Max, Batt, Vrgo
        all_registers = self.isl94203_driver.read_all_registers()

        voltage_fields = [
            (self.vcell1LineEdit, all_registers.get("vcell1")),
            (self.vcell2LineEdit, all_registers.get("vcell2")),
            (self.vcell3LineEdit, all_registers.get("vcell3")),
            (self.vcell4LineEdit, all_registers.get("vcell4")),
            (self.vcell5LineEdit, all_registers.get("vcell5")),
            (self.vcell6LineEdit, all_registers.get("vcell6")),
            (self.vcell7LineEdit, all_registers.get("vcell7")),
            (self.vcell8LineEdit, all_registers.get("vcell8")),
            (self.vcellMinLineEdit, all_registers.get("vcell_min")),
            (self.vcellMaxLineEdit, all_registers.get("vcell_max")),
            (self.vcellBattLineEdit, all_registers.get("vbatt")),
            (self.vcellVrgoLineEdit, all_registers.get("vrgo"))
        ]

        for line_edit, value in voltage_fields:
            line_edit.setText(f"{value[0]:.2f}")

        # Temperature
        bit_tgain = all_registers.get("tgain")[0]
        gain = 0
        if bit_tgain:
            gain = 1
            self.TemperatureGainLabel.setText("Now the gain is 1x")
        else:
            gain = 2
            self.TemperatureGainLabel.setText("Now the gain is 2x")

        self.tempITVoltaqeLineEdit.setText(f"{all_registers.get('temp_internal')[0]:.2f}")
        
        internal_temp_celsius = all_registers.get("temp_internal")[0] * gain
        self.tempITDegLineEdit.setText(f"{internal_temp_celsius:.2f}")

        self.tempXT1VoltaqeLineEdit.setText(f"{all_registers.get('temp_xt1')[0]:.2f}")
        self.tempXT2VoltaqeLineEdit.setText(f"{all_registers.get('temp_xt2')[0]:.2f}")

        current = all_registers.get("current_i")[0]
        voltage = current * self.resistor

        self.CSGainLineEdit.setText(f"{int(all_registers.get("i_gain")[0])}")
        self.packCurrentVLineEdit.setText(f"{voltage * 1000:.4f}")  # in millivolts
        self.packCurrentALineEdit.setText(f"{current * 1000:.4f}")  # in milliamperes

    def ui_update_status_bits(self):
        """Update the status bits in the UI."""
        all_registers = self.isl94203_driver.read_all_registers()

        status_mapping = {
            # address 0x80
            self.bitOVlabel: all_registers.get("bit_ov"),
            self.bitOVLOlabel: all_registers.get("bit_ovlo"),
            self.bitUVlabel: all_registers.get("bit_uv"),
            self.bitUVLOlabel: all_registers.get("bit_uvlo"),
            self.bitDOTlabel: all_registers.get("bit_dot"),
            self.bitDUTlabel: all_registers.get("bit_dut"),
            self.bitCOTlabel: all_registers.get("bit_cot"),
            self.bitCUTlabel: all_registers.get("bit_cut"),
            # address 0x81
            self.bitIOTlabel: all_registers.get("bit_iot"),
            self.bitCOClabel: all_registers.get("bit_coc"),
            self.bitDOClabel: all_registers.get("bit_doc"),
            self.bitDSClabel: all_registers.get("bit_dsc"),
            self.bitCELLFlabel: all_registers.get("bit_cellf"),
            self.bitOPENlabel: all_registers.get("bit_open"),
            self.bitEOCHGlabel: all_registers.get("bit_eochg"),
            # address 0x82
            self.bitLDPRSNTlabel: all_registers.get("bit_ld_prsnt"),
            self.bitCHPRSNTlabel: all_registers.get("bit_ch_prsnt"),
            self.bitCHINGlabel: all_registers.get("bit_ching"),
            self.bitDCHINGlabel: all_registers.get("bit_dching"),
            self.bitLVCHRGlabel: all_registers.get("bit_lvchg"),
            # address 0x83
            self.bitCBOTlabel: all_registers.get("bit_cbot"),
            self.bitCBUTlabel: all_registers.get("bit_cbut"),
            self.bitCBOVlabel: all_registers.get("bit_cbov"),
            self.bitCBUVlabel: all_registers.get("bit_cbuv"),
            self.bitIDLElabel: all_registers.get("bit_in_idle"),
            self.bitDOZElabel: all_registers.get("bit_in_doze"),
            self.bitSLEEPlabel: all_registers.get("bit_in_sleep")
        }

        for label, value in status_mapping.items():
            self.ui_show_status_bit(label, value[0])

    def ui_show_status_bit(self, label, bit_config):
        if bit_config:
            self.set_label_background_color(label, QColor(0, 255, 0))
        else:
            self.set_label_background_color(label, QColor(255, 255, 255))

    def set_label_background_color(self, label, color):
        # Set the background color using style sheet
        current_style = label.styleSheet()
        label.setStyleSheet(f"{current_style} background-color: {color.name()};")

    def get_unit_from_combo(self, combo):
        """Read the combobox and return the unit chosen by user."""
        selected_text = combo.currentText()
        unit = next((code for code, text in UNIT_MAPPING.items() if text == selected_text), None)
        return unit

    def write_voltage_limits(self):
        """Write voltage limits from UI to the driver."""
        voltage_limits = {
            "overvoltage_lockout": float(self.ovLockoutLineEdit.text()),
            "overvoltage_threshold": float(self.ovLineEdit.text()),
            "overvoltage_recovery": float(self.ovRecoverLineEdit.text()),
            "eoc_voltage": float(self.eocVoltageLineEdit.text()),
            "undervoltage_recovery": float(self.uvRecoverLineEdit.text()),
            "undervoltage_threshold": float(self.underVoltageLineEdit.text()),
            "sleep_voltage": float(self.sleepVoltageLineEdit.text()),
            "low_voltage_charge": float(self.lowVoltageChargeLineEdit.text()),
            "undervoltage_lockout": float(self.uvLockoutLineEdit.text())
        }
        self.isl94203_driver.write_voltage_limits(voltage_limits)
        
    def write_voltage_limits_timing(self):
        # Extract values from QLineEdit fields
        ov_delay_timeout = int(self.ovDelayTimeoutLineEdit.text())
        uv_delay_timeout = int(self.uvDelayTimeoutLineEdit.text())
        open_wire_sample_time = int(self.openWireTimingLineEdit.text())
        sleep_delay = int(self.sleepDelayLineEdit.text())

        # Extract and shift units
        ov_delay_timeout_unit = self.get_unit_from_combo(self.ovDelayTimeoutCombo)
        uv_delay_timeout_unit = self.get_unit_from_combo(self.uvDelayTimeoutCombo)
        sleep_delay_unit = self.get_unit_from_combo(self.sleepDelayUnitCombo)
        open_wire_sample_time_unit = self.get_unit_from_combo(self.openWireTimingCombo)

        timing_limits = {
            'ov_delay_timeout': (ov_delay_timeout, ov_delay_timeout_unit),
            'uv_delay_timeout': (uv_delay_timeout, uv_delay_timeout_unit),
            'open_wire_sample_time': (open_wire_sample_time, open_wire_sample_time_unit),
            'sleep_delay': (sleep_delay, sleep_delay_unit)
        }

        self.isl94203_driver.write_voltage_limits_timing(timing_limits)

    def write_timers(self):
        timer_values = {
            'timer_wdt': self.timerWDTLineEdit.text(),
            'timer_idle_doze': self.timerIdleDozeCombo.currentText(),
            'timer_sleep': self.timerSleepCombo.currentText()
        }
        self.isl94203_driver.write_timers(timer_values)

    def write_cell_balance_registers(self):
        cell_balance_values = {
            'CBLowerLim': self.CBLowerLimLineEdit.text(),
            'CBUpperLim': self.CBUpperLimLineEdit.text(),
            'CBMinDelta': self.CBMinDeltaLineEdit.text(),
            'CBMaxDelta': self.CBMaxDeltaLineEdit.text(),
            'CBOnTime': self.CBOnTimeLineEdit.text(),
            'CBOffTime': self.CBOffTimeLineEdit.text()
        }

        cell_balance_temp_values = {
            'CBUnderTemp': self.CBUnderTempLineEdit.text(),
            'CBUTRecover': self.CBUTRecoverLineEdit.text(),
            'CBOverTemp': self.CBOverTempLineEdit.text(),
            'CBOTRecover': self.CBOTRecoverLineEdit.text()
        }

        # Extract and shift units
        cb_on_time_unit = self.get_unit_from_combo(self.CBOnTimeUnitLineEdit)
        cb_off_time_unit = self.get_unit_from_combo(self.CBOffTimeUnitLineEdit)

        # Combine values and units
        cb_on_time = int(self.CBOnTimeLineEdit.text())
        cb_off_time = int(self.CBOffTimeLineEdit.text())

        self.isl94203_driver.write_cell_balance_registers(cell_balance_values, cell_balance_temp_values, cb_on_time, cb_off_time, cb_on_time_unit, cb_off_time_unit)
        
    def write_temperature_registers(self):
        temp_values = {
            'TLChargeOverTemp': self.TLChargeOverTempLineEdit.text(),
            'TLChargeOTRecover': self.TLChargeOTRecoverLineEdit.text(),
            'TLChargeUnderTemp': self.TLChargeUnderTempLineEdit.text(),
            'TLChargeUTRecover': self.TLChargeUTRecoverLineEdit.text(),
            'TLDiscOverTemp': self.TLDiscOverTempLineEdit.text(),
            'TLDischOTRecover': self.TLDischOTRecoverLineEdit.text(),
            'TLDischUnderTemp': self.TLDischUnderTempLineEdit.text(),
            'TLDischUTRecover': self.TLDischUTRecoverLineEdit.text(),
            'TLInternalOverTemp': self.TLInternalOverTempLineEdit.text(),
            'TLInternalOTRecover': self.TLInternalOTRecoverLineEdit.text()
        }
        self.isl94203_driver.write_temperature_registers(temp_values)
        
    def write_current_registers(self):

        current_limits = {
            'cl_discharge_oc': self.CLDischargeOCVoltageCombo.currentText(),
            'cl_charge_oc': self.CLChargeOCVoltageCombo.currentText(),
            'cl_discharge_sc': self.CLDischargeSCVoltageCombo.currentText(),
            'cl_discharge_oc_delay': (int(self.CLDischargeOCTimeoutLineEdit.text()), self.get_unit_from_combo(self.CLDischargeOCTimeoutCombo)),
            'cl_charge_oc_delay': (int(self.CLChargeOCTimeoutLineEdit.text()), self.get_unit_from_combo(self.CLChargeOCTimeoutCombo)),
            'cl_discharge_sc_delay': (int(self.CLDischargeSCTimeoutLineEdit.text()), self.get_unit_from_combo(self.CLDischargeSCTimeoutCombo)),
            'cl_pulse_width_charge': self.chargeDetectPulseCombo.currentText(), 
            'cl_pulse_width_load': self.loadDetectPulseCombo.currentText()
        }

        self.isl94203_driver.write_current_registers(current_limits)

    def write_pack_option_registers(self):
        options = {
            'poT2MonitorsFETTemp': self.poT2MonitorsFETTempCheckBox.isChecked(),
            'poEnableCELLFpsd': self.poEnableCELLFpsdCheckBox.isChecked(),
            'poEnableOpenWirePSD': self.poEnableOpenWirePSDCheckBox.isChecked(),
            'poEnableUVLO': self.poEnableUVLOCheckBox.isChecked(),
            'poEnableOpenWireScan': self.poEnableOpenWireScanCheckBox.isChecked(),
            'CBDuringCharge': self.CBDuringChargeCheckBox.isChecked(),
            'CBDuringDischarge': self.CBDuringDischargeCheckBox.isChecked(),
            'CBDuringEOC': self.CBDuringEOCCheckBox.isChecked(),
            'tGain': self.tGainCheckBox.isChecked()
        }
        self.isl94203_driver.write_pack_option_registers(options)

    def write_cell_config(self):
        cell_config = int(self.CellConfigurationLineEdit.text())
        self.isl94203_driver.write_cell_config(cell_config)

    def set_serial_protocol(self, serial_protocol):
        """Set or update the serial_protocol instance."""
        self.serial_protocol = serial_protocol

    def send_serial_command(self, command, data):
        """
        Send a command with data over the serial connection.

        Args:
            command (str): The command to send.
            data (list): The data to send with the command.
        """
        if self.serial_setup is None:
            logging.error("Serial setup is None")
            return

        if not self.serial_setup.is_open():
            logging.warning("Serial port is not open")
            return

        try:
            self.serial_protocol.send_command(command, data)
            #packet = self.serial_protocol.read_packet(MEMORY_SIZE)
            #_, response = packet
            #print(f"response: {response}")
        except Exception as e:
            logging.error(f"Failed to send serial command: {e}")

    def write_bms_config(self):
        if not self.serial_setup or not self.serial_setup.is_open():
            logging.error("Serial port is not open")
            #self.statusBar.showMessage("Error: Serial port is not open.")
            return

        register_cfg = self.isl94203.get_registers()

        self.write_voltage_limits()
        self.write_voltage_limits_timing()
        self.write_timers()
        self.write_cell_balance_registers()
        self.write_temperature_registers()
        self.write_current_registers()
        self.write_pack_option_registers()
        self.write_cell_config()

        logging.info(f"write_bms_config():\n{' '.join(f'{value:02X}' for value in register_cfg)}")

        self.send_serial_command(CMD_WRITE_EEPROM, register_cfg[ADDR_EEPROM_BEGIN:ADDR_EEPROM_END + 1])
        #self.statusBar.showMessage("Configuration written successfully.")

    def read_bms_config(self):
        """Read the BMS configuration from the device."""

        configuration = []

        if not self.serial_setup or not self.serial_setup.is_open():
            error_message = "Serial port is not open"
            logging.error(error_message)
            #self.statusBar.showMessage(f"Error: {error_message}.")
            return

        try:
            self.serial_protocol.pause()

            self.serial_setup.reset_input_buffer()
            self.serial_setup.reset_output_buffer()

            self.serial_protocol.send_command(CMD_READ_ALL_MEMORY, [0])
            packet = self.serial_protocol.read_packet(ISL94203_MEMORY_SIZE)
            _, configuration = packet

            self.isl94203.set_registers(list(configuration))
            self.ui_update_fields()
            register_cfg = self.isl94203.get_registers()
            logging.info(f"read_bms_config():\n{' '.join(f'{value:02X}' for value in register_cfg)}")
            #self.statusBar.showMessage("Configuration read successfully.")
        except Exception as e:
            logging.error(f"Failed to read BMS configuration: {e}")
            #self.statusBar.showMessage(f"Error: {e}")

    def read_bms_ram_config(self):
        """Read RAM memory configuration from the device via serial"""
        configuration = []

        if not self.serial_setup or not self.serial_setup.is_open():
            ERROR_MESSAGE = "Serial port is not open"
            logging.error(ERROR_MESSAGE)
            #self.statusBar.showMessage(f"Error: {ERROR_MESSAGE}.")
            return
        try:
            self.serial_protocol.pause()

            self.serial_setup.reset_input_buffer()
            self.serial_setup.reset_output_buffer()

            self.serial_protocol.send_command(CMD_READ_RAM, [0])
            packet = self.serial_protocol.read_packet(ISL94203_RAM_SIZE)
            _, configuration = packet

            self.isl94203.set_ram_registers(list(configuration))
            self.isl94203_driver.update_registers()
            self.ui_update_fields()

            logging.info(f"read_bms_ram_config():\n{' '.join(f'{value:02X}' for value in configuration)}")
            #self.statusBar.showMessage("RAM configuration read successfully.")

            return list(configuration)

        except Exception as e:
            logging.error(f"Failed to read BMS RAM configuration: {e}")
            #self.statusBar.showMessage(f"Error: {e}")

    def log_bms_ram_config(self):
        if self.startStopLogButton.isChecked():
            self.startStopLogButton.setText("Stop Log")
            self.ui.update_logging_status("Logging: In Progress")
            delay = self.logRateSpinBox.value()

            if not hasattr(self, 'ram_log_handler'):
                self.ram_log_handler = LogHandler(log_type='ram')

            self.ram_log_handler.start_log()

            ram_values = self.read_bms_ram_config()

            if ram_values:
                # Write to the RAM log file
                self.ram_log_handler.write_ram_log(ram_values)

                # Optionally: Parse values and log to the parsed log file
                parsed_values = self.parse_bms_values(ram_values)
                if not hasattr(self, 'parsed_log_handler'):
                    self.parsed_log_handler = LogHandler(log_type='parsed')
                self.parsed_log_handler.start_log()
                self.parsed_log_handler.write_parsed_log(parsed_values)

            QTimer.singleShot(delay * 1000, self.log_bms_ram_config)
        else:
            self.startStopLogButton.setText("Start Log")
            self.ui.update_logging_status("Logging: Not started")
            self.ram_log_handler.stop_log()
            if hasattr(self, 'parsed_log_handler'):
                self.parsed_log_handler.stop_log()

    def load_default_config(self):
        configuration = []
        self.isl94203.set_ram_registers(list(configuration))
        self.ui_update_fields()

    def parse_bms_values(self, ram_values):
        """Parse raw RAM values into meaningful values."""
        cell_values = ram_values[:3]  # Assume first 3 values are Cell1, Cell2, Cell3
        cell_min = min(cell_values)
        cell_max = max(cell_values)
        icurrent = ram_values[3]  # Assume 4th value is Icurrent
        status_bit0 = (ram_values[4] & 0x01)  # Assume 5th value is a status byte, bit 0
        status_bit1 = (ram_values[4] & 0x02) >> 1  # Assume 5th value, bit 1

        # Return a list of parsed values in the expected format
        return [cell_values[0], cell_values[1], cell_values[2], cell_min, cell_max, icurrent, status_bit0, status_bit1]
