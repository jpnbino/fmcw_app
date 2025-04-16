import os
import yaml
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QPushButton, QLineEdit, QComboBox, QCheckBox, QLabel, QSpinBox

from bms.isl94203_constants import *

from logger.log_handler import LogHandler
from bms.isl94203_factory import ISL94203Factory

import logging

from serialbsp.commands import *
from gui.global_log_manager import log_manager
from gui.global_status_bar_manager import status_bar_manager

class BmsTab:
    def __init__(self, ui, serial_manager, serial_protocol, bms_driver):
        self.ui = ui
        self.serial_manager = serial_manager
        self.serial_protocol = serial_protocol
        
        self.resistor = 0.005
        self.isl94203_driver = bms_driver
        self.isl94203 = ISL94203Factory.create_instance()
        self.log_file_path = None

        self.cmd_read_all_memory = get_command_by_name("CMD_READ_ALL_MEMORY")
        self.cmd_read_ram = get_command_by_name("CMD_READ_RAM")
        self.cmd_write_eeprom = get_command_by_name("CMD_WRITE_EEPROM")

        self.serial_protocol.data_received.connect(self.process_bms_read_config_response)
        self.serial_protocol.data_received.connect(self.process_bms_ram_read_config_response)

        # Connect button click to Send Serial Command
        self.ui.findChild(QPushButton, "readPackButton").clicked.connect(self.read_bms_config)
        self.ui.findChild(QPushButton, "writePackButton").clicked.connect(self.write_bms_config)
        self.ui.findChild(QPushButton, "readRamButton").clicked.connect(self.read_bms_ram_config)
        self.ui.findChild(QPushButton, "loadDefaultButton").clicked.connect(self.load_default_config)
        self.ui.findChild(QPushButton, "startStopLogButton").clicked.connect(self.log_bms_ram_config)

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

        self.CellConfigurationCombo = self.ui.findChild(QComboBox, "cellConfigurationCombo")

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
        self.CBOnTimeUnitCombo = self.ui.findChild(QComboBox, "CBOnTimeUnitCombo")
        self.CBOffTimeUnitCombo = self.ui.findChild(QComboBox, "CBOffTimeUnitCombo")

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

        self.bitOV = self.ui.findChild(QLabel, "bitOVlabel")
        self.bitOVLO = self.ui.findChild(QLabel, "bitOVLOlabel")
        self.bitUV = self.ui.findChild(QLabel, "bitUVlabel")
        self.bitUVLO = self.ui.findChild(QLabel, "bitUVLOlabel")
        self.bitDOT = self.ui.findChild(QLabel, "bitDOTlabel")
        self.bitDUT = self.ui.findChild(QLabel, "bitDUTlabel")
        self.bitCOT = self.ui.findChild(QLabel, "bitCOTlabel")
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
            self.CellConfigurationCombo.setCurrentText("0")
        else:
            self.CellConfigurationCombo.setCurrentText(f"{int(cell_config[0])}")

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
            self.CBOnTimeUnitCombo: all_registers.get("cb_on_time"),
            self.CBOffTimeUnitCombo: all_registers.get("cb_off_time")
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

    def update_bit_indicators(self, data):
        for name, state in data.items():
            checkbox = self.ui.findChild(QCheckBox, name)
            if checkbox:
                checkbox.setChecked(state[0])

    def ui_update_status_bits(self):
        """Update the status bits in the UI."""
        all_registers = self.isl94203_driver.read_all_registers()

        bits_mapping = {
            # Current/Charging status bits
            "bitCharging": all_registers.get("bit_ching"),
            "bitDischarging": all_registers.get("bit_dching"),
            "bitEOC": all_registers.get("bit_eochg"),   
            "bitChargerOn": all_registers.get("bit_ch_prsnt"),
            "bitLoadOn": all_registers.get("bit_ld_prsnt"),
            "bitCOC": all_registers.get("bit_coc"),
            "bitDOC": all_registers.get("bit_doc"),
            "bitDSC": all_registers.get("bit_dsc"),
            # Voltage status bits
            "bitOV": all_registers.get("bit_ov"),
            "bitUV": all_registers.get("bit_uv"),
            "bitOVLO": all_registers.get("bit_ovlo"),
            "bitUVLO": all_registers.get("bit_uvlo"),
            "bitCBOV": all_registers.get("bit_cbov"),
            "bitCBUV": all_registers.get("bit_cbuv"),
            "bitLVCHRG": all_registers.get("bit_lvchg"),
            # Temperature status bits
            "bitCOT": all_registers.get("bit_cot"),
            "bitCUT": all_registers.get("bit_cut"),
            "bitCBOT": all_registers.get("bit_cbot"),
            "bitCBUT": all_registers.get("bit_cbut"),
            "bitDOT": all_registers.get("bit_dot"),
            "bitDUT": all_registers.get("bit_dut"),
            "bitIOT": all_registers.get("bit_iot"),
            # Operating mode status bits
            "bitIDLE": all_registers.get("bit_in_idle"),
            "bitDOZE": all_registers.get("bit_in_doze"),
            "bitSLEEP": all_registers.get("bit_in_sleep"),
            # Fault status bits
            "bitCELLF": all_registers.get("bit_cellf"),
            "bitOPEN": all_registers.get("bit_open"),
        }

        self.update_bit_indicators(bits_mapping)

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
            "end_of_charge_voltage": float(self.eocVoltageLineEdit.text()),
            "undervoltage_recovery": float(self.uvRecoverLineEdit.text()),
            "undervoltage_threshold": float(self.underVoltageLineEdit.text()),
            "sleep_voltage": float(self.sleepVoltageLineEdit.text()),
            "low_voltage_charge": float(self.lowVoltageChargeLineEdit.text()),
            "undervoltage_lockout": float(self.uvLockoutLineEdit.text())
        }
        self.isl94203_driver.write_voltage_limits(voltage_limits)

        
    def write_voltage_limits_timing(self):
        # Extract values from QLineEdit fields
        voltage_limits_timing = {
            "ov_delay_timeout": (int(self.ovDelayTimeoutLineEdit.text()), self.ovDelayTimeoutCombo.currentText()),
            "uv_delay_timeout": (int(self.uvDelayTimeoutLineEdit.text()), self.uvDelayTimeoutCombo.currentText()),
            "sleep_delay": (int(self.sleepDelayLineEdit.text()), self.sleepDelayUnitCombo.currentText()),
            "open_wire_timing": (int(self.openWireTimingLineEdit.text()), self.openWireTimingCombo.currentText())
        }
        self.isl94203_driver.write_voltage_limits_timing(voltage_limits_timing)

    def write_timers(self):
        timer_values = {
            'timer_wdt': int(self.timerWDTLineEdit.text()),
            'timer_idle_doze': int(self.timerIdleDozeCombo.currentText()),
            'timer_sleep': int(self.timerSleepCombo.currentText())
        }
        self.isl94203_driver.write_timers(timer_values)

    def write_cell_balance_registers(self):
        cell_balance_values = {
            'cb_min_voltage': float(self.CBLowerLimLineEdit.text()),
            'cb_max_voltage': float(self.CBUpperLimLineEdit.text()),
            'cb_min_delta': float(self.CBMinDeltaLineEdit.text()),
            'cb_max_delta': float(self.CBMaxDeltaLineEdit.text()),
            'cb_under_temp': float(self.CBUnderTempLineEdit.text()),
            'cb_ut_recover': float(self.CBUTRecoverLineEdit.text()),
            'cb_over_temp': float(self.CBOverTempLineEdit.text()),
            'cb_ot_recover': float(self.CBOTRecoverLineEdit.text()),
            'cb_on_time': (int(self.CBOnTimeLineEdit.text()), self.CBOnTimeUnitCombo.currentText()),
            'cb_off_time': (int(self.CBOffTimeLineEdit.text()), self.CBOffTimeUnitCombo.currentText())
        }

        self.isl94203_driver.write_cell_balance_registers(cell_balance_values)
        
    def write_temperature_registers(self):
        temp_limits = {
            'tl_charge_ot': float(self.TLChargeOverTempLineEdit.text()),
            'tl_charge_ot_recover': float(self.TLChargeOTRecoverLineEdit.text()),
            'tl_charge_ut': float(self.TLChargeUnderTempLineEdit.text()),
            'tl_charge_ut_recover': float(self.TLChargeUTRecoverLineEdit.text()),
            'tl_discharge_ot': float(self.TLDiscOverTempLineEdit.text()),
            'tl_discharge_ot_recover': float(self.TLDischOTRecoverLineEdit.text()),
            'tl_discharge_ut': float(self.TLDischUnderTempLineEdit.text()),
            'tl_discharge_ut_recover': float(self.TLDischUTRecoverLineEdit.text()),
            'tl_internal_ot': float(self.TLInternalOverTempLineEdit.text()),
            'tl_internal_ot_recover': float(self.TLInternalOTRecoverLineEdit.text())
        }
        self.isl94203_driver.write_temperature_registers(temp_limits)
        
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
            'po_t2_monitors_fet': self.poT2MonitorsFETTempCheckBox.isChecked(),
            'po_enable_cellf_psd': self.poEnableCELLFpsdCheckBox.isChecked(),
            'po_enable_openwire_psd': self.poEnableOpenWirePSDCheckBox.isChecked(),
            'po_enable_uvlo_pd': self.poEnableUVLOCheckBox.isChecked(),
            'po_enable_openwire_scan': self.poEnableOpenWireScanCheckBox.isChecked(),
            'cb_during_charge': self.CBDuringChargeCheckBox.isChecked(),
            'cb_during_discharge': self.CBDuringDischargeCheckBox.isChecked(),
            'cb_during_eoc': self.CBDuringEOCCheckBox.isChecked(),
            'tgain': self.tGainCheckBox.isChecked()
        }
        self.isl94203_driver.write_pack_option_registers(options)

    def write_cell_config(self):
        cell_config = int(self.CellConfigurationCombo.currentText())
        self.isl94203_driver.write_cell_config(cell_config)

    def write_bms_config(self):
        if not self.serial_manager or not self.serial_manager.is_open():
            logging.error("Serial port is not open")

            status_bar_manager.update_message("Serial port is not open.",category="error")
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

        self._encode_and_send(self.cmd_write_eeprom, register_cfg[ADDR_EEPROM_BEGIN:ADDR_EEPROM_END + 1], self.cmd_write_eeprom.description)
        status_bar_manager.update_message("Configuration written successfully.", category="success")

    def _encode_and_send(self, command: Command, data: list[int], log_message: str) -> None:
        """
        Encodes the command and data, sends it via the serial manager, and logs the message.
        """
        if self.serial_manager.is_open():
            log_manager.log_message(log_message)
            self.serial_protocol.encode_command(command, data)
            
        else:
            log_manager.log_message("Serial port not open")

    def process_bms_read_config_response(self, packet: bytes) -> None:
        """
        Process the response packet from the BMS.
        """
        try:
            if packet[0] != self.cmd_read_all_memory.code:
                return
            print("packet:", " ".join(f"0x{byte:02x}" for byte in packet))
            print("packet length:", len(packet))
            self.isl94203.set_registers(list(packet[2:-1]))
            self.ui_update_fields()
            register_cfg = self.isl94203.get_registers()
            logging.info(f"read_bms_config():\n{' '.join(f'{value:02X}' for value in register_cfg)}")
            status_bar_manager.update_message("Configuration read successfully.", category="success")
        except Exception as e:
            logging.error(f"Failed to process BMS response: {e}")
            status_bar_manager.update_message(f"Error: {e}", category="error")

    def read_bms_config(self):
        """Read the BMS configuration from the device."""

        if not self.serial_manager or not self.serial_manager.is_open():
            error_message = "Serial port is not open"
            logging.error(error_message)
            status_bar_manager.update_message(f"Error: {error_message}.", category="error")
            return

        try:
            self.serial_manager.reset_input_buffer()
            self.serial_manager.reset_output_buffer()
            self._encode_and_send(self.cmd_read_all_memory, [0], self.cmd_read_all_memory.description)

        except Exception as e:
            logging.error(f"Failed to send command to read BMS configuration: {e}")
            status_bar_manager.update_message(f"Error: {e}", category="error")
            

    def process_bms_ram_read_config_response(self, packet: bytes) -> None:
        """
        Process the response packet from the BMS RAM read command.
        """
        try:
            if packet[0] != self.cmd_read_ram.code:
                return
            print("packet:", " ".join(f"0x{byte:02x}" for byte in packet))
            print("packet length:", len(packet))
            self.isl94203.set_ram_registers(list(packet[2:-1]))
            self.ui_update_ram_fields()
            ram_values = self.isl94203.get_ram_registers()
            logging.info(f"read_bms_ram_config():\n{' '.join(f'{value:02X}' for value in ram_values)}")
            status_bar_manager.update_message("RAM configuration read successfully.", category="success")
        except Exception as e:
            logging.error(f"Failed to process BMS RAM response: {e}")
            status_bar_manager.update_message(f"Error: {e}", category="error")

    def read_bms_ram_config(self):
        """Read RAM memory configuration from the device via serial"""
        configuration = []

        if not self.serial_manager or not self.serial_manager.is_open():
            ERROR_MESSAGE = "Serial port is not open"
            logging.error(ERROR_MESSAGE)
            status_bar_manager.update_message(f"Error: {ERROR_MESSAGE}.", category="error")
            return
        try:
            self.serial_manager.reset_input_buffer()
            self.serial_manager.reset_output_buffer()
            self._encode_and_send(self.cmd_read_ram, [0], self.cmd_read_ram.description)

        except Exception as e:
            logging.error(f"Failed to read BMS RAM configuration: {e}")
            status_bar_manager.update_message(f"Error: {e}", category="error")

    def log_bms_ram_config(self):
        if self.startStopLogButton.isChecked():
            self.startStopLogButton.setText("Stop Log")
            status_bar_manager.update_logging_status(True)
            delay = self.logRateSpinBox.value()

            if not hasattr(self, 'ram_log_handler'):
                self.ram_log_handler = LogHandler(log_type='ram')

            self.ram_log_handler.start_log()

            self.read_bms_ram_config()

            ram_values =  self.isl94203.get_ram_registers()

            if ram_values:
                # Parse the raw data
                parsed_values = self.parse_bms_values(ram_values)

                # Write the log entry (raw + parsed data)
                self.ram_log_handler.write_log_entry(raw_data=ram_values, parsed_data=parsed_values)

            QTimer.singleShot(delay * 1000, self.log_bms_ram_config)
        else:
            self.startStopLogButton.setText("Start Log")
            status_bar_manager.update_logging_status(False)
            if hasattr(self, 'ram_log_handler'):
                self.ram_log_handler.stop_log()

    def load_default_config(self):
        config_path = os.path.join(os.path.dirname(__file__), '../..', 'config', 'default_config.yaml')
        try:
            with open(config_path, 'r') as file:
                configuration = yaml.safe_load(file)

            # Update UI fields with the loaded configuration
            voltage_limits = configuration.get('voltage limits', {})
            self.ovLockoutLineEdit.setText(str(voltage_limits.get('ov lockout', '')))
            self.ovLineEdit.setText(str(voltage_limits.get('over voltage', '')))
            self.ovRecoverLineEdit.setText(str(voltage_limits.get('ov recover', '')))
            self.eocVoltageLineEdit.setText(str(voltage_limits.get('end of charge', '')))
            self.uvRecoverLineEdit.setText(str(voltage_limits.get('uv recover', '')))
            self.underVoltageLineEdit.setText(str(voltage_limits.get('under voltage', '')))
            self.sleepVoltageLineEdit.setText(str(voltage_limits.get('sleep voltage', '')))
            self.lowVoltageChargeLineEdit.setText(str(voltage_limits.get('low v charge', '')))
            self.uvLockoutLineEdit.setText(str(voltage_limits.get('uv lockout', '')))

            voltage_timing = configuration.get('voltage timeouts', {})
            self.ovDelayTimeoutLineEdit.setText(str(voltage_timing.get('ov delay', '')))
            self.ovDelayTimeoutCombo.setCurrentText(str(voltage_timing.get('ov delay unit', '')))
            self.uvDelayTimeoutLineEdit.setText(str(voltage_timing.get('uv delay', '')))
            self.uvDelayTimeoutCombo.setCurrentText(str(voltage_timing.get('uv delay unit', '')))
            self.sleepDelayLineEdit.setText(str(voltage_timing.get('sleep delay', '')))
            self.sleepDelayUnitCombo.setCurrentText(str(voltage_timing.get('sleep delay unit', '')))
            self.openWireTimingLineEdit.setText(str(voltage_timing.get('open wire', '')))
            self.openWireTimingCombo.setCurrentText(str(voltage_timing.get('open wire unit', '')))

            current_limits = configuration.get('current limits', {})
            self.CLDischargeOCVoltageCombo.setCurrentText(str(current_limits.get('discharge oc', '')))
            self.CLDischargeOCTimeoutLineEdit.setText(str(current_limits.get('doc delay', '')))
            self.CLDischargeOCTimeoutCombo.setCurrentText(str(current_limits.get('doc delay unit', '')))

            self.CLChargeOCVoltageCombo.setCurrentText(str(current_limits.get('charge oc', '')))
            self.CLChargeOCTimeoutLineEdit.setText(str(current_limits.get('coc delay', '')))
            self.CLChargeOCTimeoutCombo.setCurrentText(str(current_limits.get('coc delay unit', '')))
            
            self.CLDischargeSCVoltageCombo.setCurrentText(str(current_limits.get('discharge sc', '')))            
            self.CLDischargeSCTimeoutLineEdit.setText(str(current_limits.get('dsc delay', '')))
            self.CLDischargeSCTimeoutCombo.setCurrentText(str(current_limits.get('dsc delay unit', '')))
            
            self.chargeDetectPulseCombo.setCurrentText(str(current_limits.get('detect pulse width', {}).get('charge', '')))
            self.loadDetectPulseCombo.setCurrentText(str(current_limits.get('detect pulse width', {}).get('load', '')))

            timers = configuration.get('timers', {})
            self.timerIdleDozeCombo.setCurrentText(str(timers.get('idle/doze mode timer', '')))
            self.timerSleepCombo.setCurrentText(str(timers.get('sleep mode timer', '')))
            self.timerWDTLineEdit.setText(str(timers.get('wd timer', '')))

            cb_limits = configuration.get('cell balance limits', {})
            self.CBUpperLimLineEdit.setText(str(cb_limits.get('cb upper lim', '')))
            self.CBLowerLimLineEdit.setText(str(cb_limits.get('cb lower lim', '')))
            self.CBMaxDeltaLineEdit.setText(str(cb_limits.get('cb max delta', '')))
            self.CBMinDeltaLineEdit.setText(str(cb_limits.get('cb min delta', '')))
            self.CBOverTempLineEdit.setText(str(cb_limits.get('cb over temp', '')))
            self.CBOTRecoverLineEdit.setText(str(cb_limits.get('cb ot recover', '')))
            self.CBUTRecoverLineEdit.setText(str(cb_limits.get('cb ut recover', '')))
            self.CBUnderTempLineEdit.setText(str(cb_limits.get('cb under temp', '')))
            self.CBOnTimeLineEdit.setText(str(cb_limits.get('cb on time', '')))
            self.CBOffTimeLineEdit.setText(str(cb_limits.get('cb off time', '')))
            self.CBOnTimeUnitCombo.setCurrentText(str(cb_limits.get('cb on time unit', '')))
            self.CBOffTimeUnitCombo.setCurrentText(str(cb_limits.get('cb off time unit', '')))
            self.CBDuringChargeCheckBox.setChecked(cb_limits.get('cb during charge', False))
            self.CBDuringDischargeCheckBox.setChecked(cb_limits.get('cb during discharge', False))
            self.CBDuringEOCCheckBox.setChecked(cb_limits.get('cb during eoc', False))

            temp_limits = configuration.get('temperature limits', {})
            self.TLChargeOverTempLineEdit.setText(str(temp_limits.get('charge over temp', '')))
            self.TLChargeOTRecoverLineEdit.setText(str(temp_limits.get('charge ot recover', '')))
            self.TLChargeUTRecoverLineEdit.setText(str(temp_limits.get('charge ut recover', '')))
            self.TLChargeUnderTempLineEdit.setText(str(temp_limits.get('charge under temp', '')))
            self.TLDiscOverTempLineEdit.setText(str(temp_limits.get('discharge over temp', '')))
            self.TLDischOTRecoverLineEdit.setText(str(temp_limits.get('discharge ot recover', '')))
            self.TLDischUTRecoverLineEdit.setText(str(temp_limits.get('discharge ut recover', '')))
            self.TLDischUnderTempLineEdit.setText(str(temp_limits.get('discharge under temp', '')))
            self.TLInternalOverTempLineEdit.setText(str(temp_limits.get('internal over temp', '')))
            self.TLInternalOTRecoverLineEdit.setText(str(temp_limits.get('internal ot recover', '')))

            cell_config = configuration.get('cell configuration', {})
            self.CellConfigurationCombo.setCurrentText(str(cell_config.get('number of cells', '')))

            pack_option = configuration.get('pack options', {})
            self.poT2MonitorsFETTempCheckBox.setChecked(pack_option.get('xt2 monitors fet temp', False))
            self.poEnableCELLFpsdCheckBox.setChecked(pack_option.get('enable cellf psd action', False))
            self.poEnableOpenWirePSDCheckBox.setChecked(pack_option.get('enable open wire psd', False))
            self.poEnableUVLOCheckBox.setChecked(pack_option.get('enable uvlo power down', False))
            self.poEnableOpenWireScanCheckBox.setChecked(pack_option.get('enable open wire scan', False))

            temp_config = configuration.get('temp reading', {})
            self.tGainCheckBox.setChecked(temp_config.get('tgain', ''))

            logging.info("Default configuration loaded successfully from %s.", config_path)
            status_bar_manager.update_message("Default configuration loaded successfully.", category="success")
        except FileNotFoundError:
            logging.error("Default configuration file not found: %s", config_path)
        except yaml.YAMLError as e:
            logging.error("Error parsing YAML configuration file: %s", e)
        except Exception as e:
            logging.error("Failed to load default configuration: %s", e)
