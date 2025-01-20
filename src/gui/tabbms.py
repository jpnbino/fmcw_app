from PySide6.QtGui import QColor
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QPushButton, QStatusBar, QLineEdit, QComboBox, QCheckBox, QLabel, QSpinBox

from bms.constants import *

from gui.utility import convert_time_to_hex, convert_to_hex
from logger.log_handler import LogHandler
from bms.isl94203_factory import ISL94203Factory

import logging

from serialbsp.commands import CMD_READ_ALL_MEMORY, CMD_READ_RAM, CMD_WRITE_EEPROM
from serialbsp.protocol_fmcw import SerialProtocolFmcw


class BmsTab:
    def __init__(self, ui, bms_config, log_callback):
        self.ui = ui
        self.bms_config = bms_config
        self.isl94203 = ISL94203Factory.create_instance()
        self.log_file_path = None
        self.log_callback = log_callback
        self.serial_setup = self.ui.fmcw_serial_manager
        self.serial_protocol = None


        # Connect button click to Send Serial Command
        self.ui.findChild(QPushButton, "readPackButton").clicked.connect(self.read_bms_config)
        self.ui.findChild(QPushButton, "writePackButton").clicked.connect(self.write_bms_config)
        self.ui.findChild(QPushButton, "readRamButton").clicked.connect(self.read_bms_ram_config)
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
        voltage_fields = [
            (self.ovLockoutLineEdit, self.bms_config.ov_lockout),
            (self.ovLineEdit, self.bms_config.ov),
            (self.ovRecoverLineEdit, self.bms_config.ov_recover),
            (self.eocVoltageLineEdit, self.bms_config.eoc_voltage),
            (self.uvRecoverLineEdit, self.bms_config.uv_recover),
            (self.underVoltageLineEdit, self.bms_config.under_voltage),
            (self.sleepVoltageLineEdit, self.bms_config.sleep_voltage),
            (self.lowVoltageChargeLineEdit, self.bms_config.low_voltage_charge),
            (self.uvLockoutLineEdit, self.bms_config.uv_lockout)
        ]
        for line_edit, value in voltage_fields:
            line_edit.setText(f"{value:.2f}")

    def ui_update_voltage_limits_timing(self):
        """Update voltage limits timing fields and 
        Update the combo boxes with the selected values."""
        voltage_timing_fields = [
            (self.ovDelayTimeoutLineEdit, self.bms_config.ov_delay_timeout),
            (self.uvDelayTimeoutLineEdit, self.bms_config.uv_delay_timeout),
            (self.sleepDelayLineEdit, self.bms_config.sleep_delay),
            (self.openWireTimingLineEdit, self.bms_config.open_wire_timing)
        ]
        for line_edit, value in voltage_timing_fields:
            line_edit.setText(f"{int(value)}")

        combo_boxes = [
            (self.ovDelayTimeoutCombo, self.bms_config.ov_delay_timeout_unit),
            (self.uvDelayTimeoutCombo, self.bms_config.uv_delay_timeout_unit),
            (self.sleepDelayUnitCombo, self.bms_config.sleep_delay_unit),
            (self.openWireTimingCombo, self.bms_config.open_wire_timing_unit)
        ]
        for combo, value in combo_boxes:
            combo.setCurrentText(UNIT_MAPPING.get(int(value), 'Unknown'))

    def ui_update_timer_fields(self):
        """Update timer-related fields."""
        timer_fields = {
            self.timerIdleDozeCombo: self.bms_config.timer_idle_doze,
            self.timerSleepCombo: self.bms_config.timer_sleep,
        }
        for line_edit, value in timer_fields.items():
            line_edit.setCurrentText(f"{int(value)}")

        wdt_line_edit = self.timerWDTLineEdit
        wdt_line_edit.setText(f"{int(self.bms_config.timer_wdt)}")

    def ui_update_cell_balance_limits(self):
        """Update cell balance limits fields."""
        if self.bms_config.cell_config == 0:
            self.CellConfigurationLineEdit.setText("0")
        else:
            self.CellConfigurationLineEdit.setText(f"{int(CELL_CONFIG_MAPPING[self.bms_config.cell_config])}")

        cell_balance_limits = {
            self.CBUpperLimLineEdit: self.bms_config.cb_upper_lim,
            self.CBLowerLimLineEdit: self.bms_config.cb_lower_lim,
            self.CBMaxDeltaLineEdit: self.bms_config.cb_max_delta,
            self.CBMinDeltaLineEdit: self.bms_config.cb_min_delta,
            self.CBOverTempLineEdit: self.bms_config.cb_over_temp,
            self.CBOTRecoverLineEdit: self.bms_config.cb_ot_recover,
            self.CBUTRecoverLineEdit: self.bms_config.cb_ut_recover,
            self.CBUnderTempLineEdit: self.bms_config.cb_under_temp,
        }
        for line_edit, value in cell_balance_limits.items():
            line_edit.setText(f"{value:.2f}")

        self.CBOnTimeLineEdit.setText(f"{int(self.bms_config.cb_on_time)}")
        self.CBOffTimeLineEdit.setText(f"{int(self.bms_config.cb_off_time)}")
        self.CBOnTimeUnitLineEdit.setCurrentText(UNIT_MAPPING.get(int(self.bms_config.cb_on_time_unit), 'Unknown'))
        self.CBOffTimeUnitLineEdit.setCurrentText(UNIT_MAPPING.get(int(self.bms_config.cb_off_time_unit), 'Unknown'))

    def ui_update_temperature_limits(self):
        """Update temperature limits fields."""
        temp_limits = {
            self.TLChargeOverTempLineEdit: self.bms_config.tl_charge_over_temp,
            self.TLChargeOTRecoverLineEdit: self.bms_config.tl_charge_ot_recover,
            self.TLChargeUTRecoverLineEdit: self.bms_config.tl_charge_ut_recover,
            self.TLChargeUnderTempLineEdit: self.bms_config.tl_charge_under_temp,
            self.TLDiscOverTempLineEdit: self.bms_config.tl_disch_over_temp,
            self.TLDischOTRecoverLineEdit: self.bms_config.tl_disch_ot_recover,
            self.TLDischUTRecoverLineEdit: self.bms_config.tl_disch_ut_recover,
            self.TLDischUnderTempLineEdit: self.bms_config.tl_disch_under_temp,
            self.TLInternalOverTempLineEdit: self.bms_config.tl_internal_over_temp,
            self.TLInternalOTRecoverLineEdit: self.bms_config.tl_internal_ot_recover
        }
        for line_edit, value in temp_limits.items():
            line_edit.setText(f"{value:.2f}")

    def ui_update_current_limits(self):
        """Update current limits fields."""
        current_limits = {
            self.CLDischargeOCVoltageCombo: (self.bms_config.disch_oc_voltage, DOC_MAPPING),
            self.CLChargeOCVoltageCombo: (self.bms_config.charge_oc_voltage, COC_MAPPING),
            self.CLDischargeSCVoltageCombo: (self.bms_config.disch_sc_voltage, DSC_MAPPING),
            self.CLDischargeOCTimeoutCombo: (self.bms_config.disch_oc_timeout_unit, UNIT_MAPPING),
            self.CLChargeOCTimeoutCombo: (self.bms_config.charge_oc_timeout_unit, UNIT_MAPPING),
            self.CLDischargeSCTimeoutCombo: (self.bms_config.disch_sc_timeout_unit, UNIT_MAPPING)
        }
        for combo, (value, mapping) in current_limits.items():
            combo.setCurrentText(mapping.get(int(value), 'Unknown'))

        current_fields = {
            self.CLDischargeOCTimeoutLineEdit: self.bms_config.disch_oc_timeout,
            self.CLChargeOCTimeoutLineEdit: self.bms_config.charge_oc_timeout,
            self.CLDischargeSCTimeoutLineEdit: self.bms_config.disch_sc_timeout
        }
        for line_edit, value in current_fields.items():
            line_edit.setText(f"{int(value)}")

        current_detect_fields = {
            self.chargeDetectPulseCombo: self.bms_config.charge_detect_pulse_width,
            self.loadDetectPulseCombo: self.bms_config.load_detect_pulse_width
        }
        for combo, value in current_detect_fields.items():
            combo.setCurrentText(f"{int(value)}")

    def ui_update_pack_option(self):
        """Update pack option fields."""
        options = {
            self.poT2MonitorsFETTempCheckBox: self.bms_config.bit_t2_monitors_fet,
            self.poEnableCELLFpsdCheckBox: self.bms_config.bit_enable_cellf_psd,
            self.poEnableOpenWirePSDCheckBox: self.bms_config.bit_enable_openwire_psd,
            self.poEnableUVLOCheckBox: self.bms_config.bit_enable_uvlo_pd,
            self.poEnableOpenWireScanCheckBox: self.bms_config.bit_enable_openwire_scan,
            self.CBDuringChargeCheckBox: self.bms_config.bit_cb_during_charge,
            self.CBDuringDischargeCheckBox: self.bms_config.bit_cb_during_discharge,
            self.CBDuringEOCCheckBox: self.bms_config.bit_cb_during_eoc,
            self.tGainCheckBox: self.bms_config.bit_tgain
        }
        for checkbox, value in options.items():
            checkbox.setChecked(value)

    def ui_update_ram_values(self):
        # RAM
        # Voltage values: Cells, Min, Max, Batt, Vrgo
        voltage_fields = [
            (self.vcell1LineEdit, self.bms_config.vcell1),
            (self.vcell2LineEdit, self.bms_config.vcell2),
            (self.vcell3LineEdit, self.bms_config.vcell3),
            (self.vcell4LineEdit, self.bms_config.vcell4),
            (self.vcell5LineEdit, self.bms_config.vcell5),
            (self.vcell6LineEdit, self.bms_config.vcell6),
            (self.vcell7LineEdit, self.bms_config.vcell7),
            (self.vcell8LineEdit, self.bms_config.vcell8),
            (self.vcellMinLineEdit, self.bms_config.vcell_min),
            (self.vcellMaxLineEdit, self.bms_config.vcell_max),
            (self.vcellBattLineEdit, self.bms_config.vbatt),
            (self.vcellVrgoLineEdit, self.bms_config.vrgo),
        ]
        for line_edit, value in voltage_fields:
            line_edit.setText(f"{value:.2f}")

        # Temperature
        gain = 0
        if self.bms_config.bit_tgain:
            gain = 1
            self.TemperatureGainLabel.setText("Now the gain is 1x")
        else:
            gain = 2
            self.TemperatureGainLabel.setText("Now the gain is 2x")

        self.tempITVoltaqeLineEdit.setText(f"{self.bms_config.temp_internal:.2f}")
        internal_temp_celsius = ((self.bms_config.temp_internal * 1000) / (gain * 0.92635)) - 273.15
        self.tempITDegLineEdit.setText(f"{internal_temp_celsius:.2f}")

        self.tempXT1VoltaqeLineEdit.setText(f"{self.bms_config.temp_xt1:.2f}")
        self.tempXT2VoltaqeLineEdit.setText(f"{self.bms_config.temp_xt2:.2f}")

        # Current
        resistor = float(self.ResistorLineEdit.text()) / 1000
        current = float(self.bms_config.v_sense / resistor)
        voltage = self.bms_config.v_sense

        self.CSGainLineEdit.setText(f"{int(self.bms_config.i_gain)}")
        self.packCurrentVLineEdit.setText(f"{voltage * 1000:.4f}")  # in millivolts
        self.packCurrentALineEdit.setText(f"{int(current * 1000)}")  # in milliamperes

    def ui_update_status_bits(self):
        status_mapping = {
            # address 0x80
            self.bitOVlabel: self.bms_config.bit_ov,
            self.bitOVLOlabel: self.bms_config.bit_ovlo,
            self.bitUVlabel: self.bms_config.bit_uv,
            self.bitUVLOlabel: self.bms_config.bit_uvlo,
            self.bitDOTlabel: self.bms_config.bit_dot,
            self.bitDUTlabel: self.bms_config.bit_dut,
            self.bitCOTlabel: self.bms_config.bit_cot,
            self.bitCUTlabel: self.bms_config.bit_cut,
            # address 0x81
            self.bitIOTlabel: self.bms_config.bit_iot,
            self.bitCOClabel: self.bms_config.bit_coc,
            self.bitDOClabel: self.bms_config.bit_doc,
            self.bitDSClabel: self.bms_config.bit_dsc,
            self.bitCELLFlabel: self.bms_config.bit_cellf,
            self.bitOPENlabel: self.bms_config.bit_open,
            self.bitEOCHGlabel: self.bms_config.bit_eochg,
            # address 0x82
            self.bitLDPRSNTlabel: self.bms_config.bit_ld_prsnt,
            self.bitCHPRSNTlabel: self.bms_config.bit_ch_prsnt,
            self.bitCHINGlabel: self.bms_config.bit_ching,
            self.bitDCHINGlabel: self.bms_config.bit_dching,
            self.bitLVCHRGlabel: self.bms_config.bit_lvchg,
            # address 0x83
            self.bitCBOTlabel: self.bms_config.bit_cbot,
            self.bitCBUTlabel: self.bms_config.bit_cbut,
            self.bitCBOVlabel: self.bms_config.bit_cbov,
            self.bitCBUVlabel: self.bms_config.bit_cbuv,
            self.bitIDLElabel: self.bms_config.bit_in_idle,
            self.bitDOZElabel: self.bms_config.bit_in_doze,
            self.bitSLEEPlabel: self.bms_config.bit_in_sleep
        }

        for label, bit in status_mapping.items():
            self.ui_show_status_bit(label, bit)

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
        voltage_values = [
            (self.ovLineEdit.text(), 0x00),
            (self.ovRecoverLineEdit.text(), 0x02),
            (self.underVoltageLineEdit.text(), 0x04),
            (self.uvRecoverLineEdit.text(), 0x06),
            (self.ovLockoutLineEdit.text(), 0x08),
            (self.uvLockoutLineEdit.text(), 0x0a),
            (self.eocVoltageLineEdit.text(), 0x0c),
            (self.lowVoltageChargeLineEdit.text(), 0x0e),
            (self.sleepVoltageLineEdit.text(), 0x44)
        ]
        for value, address in voltage_values:
            hex_value: int = convert_to_hex(value, VOLTAGE_CELL_MULTIPLIER)
            self.isl94203.reg_write(address, hex_value, Mask.MASK_12BIT, 0x00)

    def write_voltage_limits_timing(self):
        # Extract values from QLineEdit fields
        ov_delay_timeout = int(self.ovDelayTimeoutLineEdit.text())
        uv_delay_timeout = int(self.uvDelayTimeoutLineEdit.text())
        open_wire_sample_time = int(self.openWireTimingLineEdit.text())
        sleep_delay = int(self.sleepDelayLineEdit.text())

        # Extract and shift units
        ov_delay_timeout_unit = self.get_unit_from_combo(self.ovDelayTimeoutCombo) << 10
        uv_delay_timeout_unit = self.get_unit_from_combo(self.uvDelayTimeoutCombo) << 10
        sleep_delay_unit = self.get_unit_from_combo(self.sleepDelayUnitCombo) << 9
        open_wire_sample_time_unit = self.get_unit_from_combo(self.openWireTimingCombo) << 9

        # Combine values and units, then write to registers
        self.isl94203.reg_write(0x10, ov_delay_timeout_unit | ov_delay_timeout, Mask.MASK_12BIT, 0)
        self.isl94203.reg_write(0x12, uv_delay_timeout_unit | uv_delay_timeout, Mask.MASK_12BIT, 0)
        self.isl94203.reg_write(0x14, open_wire_sample_time_unit | open_wire_sample_time, Mask.MASK_10BIT, 0)
        self.isl94203.reg_write(0x46, sleep_delay_unit | sleep_delay, Mask.MASK_11BIT, 0)

    def write_timers(self):

        timer_values = [
            (self.timerWDTLineEdit.text(), 0x46, Mask.MASK_5BIT, 11, 0),
            (self.timerIdleDozeCombo.currentText(), 0x48, Mask.MASK_4BIT, 0, 0),
            (self.timerSleepCombo.currentText(), 0x48, Mask.MASK_4BIT, 4, 4)
        ]
        for value, address, mask, shift, scaling in timer_values:
            hex_value = convert_time_to_hex(value, scaling)
            self.isl94203.reg_write(address, hex_value, mask, shift)

    def write_cell_balance_registers(self):
        cell_balance_values = [
            (self.CBLowerLimLineEdit.text(), 0x1c),
            (self.CBUpperLimLineEdit.text(), 0x1e),
            (self.CBMinDeltaLineEdit.text(), 0x20),
            (self.CBMaxDeltaLineEdit.text(), 0x22),
            (self.CBOnTimeLineEdit.text(), 0x24),
            (self.CBOffTimeLineEdit.text(), 0x26)
        ]
        for value, address in cell_balance_values:
            hex_value = convert_to_hex(value, VOLTAGE_CELL_MULTIPLIER)
            self.isl94203.reg_write(address, hex_value, Mask.MASK_12BIT, 0x00)

        cell_balance_temp_values = [
            (self.CBUnderTempLineEdit.text(), 0x28),
            (self.CBUTRecoverLineEdit.text(), 0x2a),
            (self.CBOverTempLineEdit.text(), 0x2c),
            (self.CBOTRecoverLineEdit.text(), 0x2e)
        ]
        for value, address in cell_balance_temp_values:
            hex_value = convert_to_hex(value, TEMPERATURE_MULTIPLIER)
            self.isl94203.reg_write(address, hex_value, Mask.MASK_12BIT, 0x00)

        # Extract and shift units
        cb_on_time_unit = self.get_unit_from_combo(self.CBOnTimeUnitLineEdit) << 10
        cb_off_time_unit = self.get_unit_from_combo(self.CBOffTimeUnitLineEdit) << 10

        # Combine values and units, then write to registers
        self.isl94203.reg_write(0x24, cb_on_time_unit | int(self.CBOnTimeLineEdit.text()), Mask.MASK_12BIT, 0)
        self.isl94203.reg_write(0x26, cb_off_time_unit | int(self.CBOffTimeLineEdit.text()), Mask.MASK_12BIT, 0)

    def write_temperature_registers(self):
        temp_values = [
            (self.TLChargeOverTempLineEdit.text(), 0x30),
            (self.TLChargeOTRecoverLineEdit.text(), 0x32),
            (self.TLChargeUnderTempLineEdit.text(), 0x34),
            (self.TLChargeUTRecoverLineEdit.text(), 0x36),
            (self.TLDiscOverTempLineEdit.text(), 0x38),
            (self.TLDischOTRecoverLineEdit.text(), 0x3a),
            (self.TLDischUnderTempLineEdit.text(), 0x3C),
            (self.TLDischUTRecoverLineEdit.text(), 0x3E),
            (self.TLInternalOverTempLineEdit.text(), 0x40),
            (self.TLInternalOTRecoverLineEdit.text(), 0x42)
        ]
        for value, address in temp_values:
            hex_value = convert_to_hex(value, TEMPERATURE_MULTIPLIER)
            self.isl94203.reg_write(address, hex_value, Mask.MASK_12BIT, 0x00)

    def write_current_registers(self):
        # Helper function to pack values into the register
        def pack_register_value(timeout, unit, voltage):
            # timeout is 10 bits (0-9), unit is 2 bits (10-11), voltage is 3 bits (12-14)
            return (timeout & 0x3FF) | ((unit & 0x3) << 10) | ((voltage & 0x7) << 12)

        # Define the mappings for the different selections
        register_mappings = [
            {
                'timeout_edit': self.CLDischargeOCTimeoutLineEdit,
                'unit_combo': self.CLDischargeOCTimeoutCombo,
                'voltage_combo': self.CLDischargeOCVoltageCombo,
                'address': 0x16,
                'voltage_mapping': DOC_MAPPING
            },
            {
                'timeout_edit': self.CLChargeOCTimeoutLineEdit,
                'unit_combo': self.CLChargeOCTimeoutCombo,
                'voltage_combo': self.CLChargeOCVoltageCombo,
                'address': 0x18,
                'voltage_mapping': COC_MAPPING
            },
            {
                'timeout_edit': self.CLDischargeSCTimeoutLineEdit,
                'unit_combo': self.CLDischargeSCTimeoutCombo,
                'voltage_combo': self.CLDischargeSCVoltageCombo,
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
            self.isl94203.reg_write(reg['address'], packed_value, Mask.MASK_15BIT, 0x00)

        # Extract the charge and load detect pulse widths
        charge_detect_pulse = int(self.chargeDetectPulseCombo.currentText())
        load_detect_pulse = int(self.loadDetectPulseCombo.currentText())

        # Write the charge and load detect pulse widths to the registers
        self.isl94203.reg_write(0x00, charge_detect_pulse, Mask.MASK_4BIT, 12)
        self.isl94203.reg_write(0x04, load_detect_pulse, Mask.MASK_4BIT, 12)

    def write_pack_option_registers(self):
        pack_options = [
            (self.poT2MonitorsFETTempCheckBox.isChecked(), 0x4A, Mask.MASK_1BIT, 5),
            (self.poEnableCELLFpsdCheckBox.isChecked(), 0x4A, Mask.MASK_1BIT, 7),
            (self.poEnableOpenWirePSDCheckBox.isChecked(), 0x4A, Mask.MASK_1BIT, 0),
            (self.poEnableUVLOCheckBox.isChecked(), 0x4B, Mask.MASK_1BIT, 3),
            (self.poEnableOpenWireScanCheckBox.isChecked(), 0x4A, Mask.MASK_1BIT, 1),
            (self.CBDuringChargeCheckBox.isChecked(), 0x4B, Mask.MASK_1BIT, 6),
            (self.CBDuringDischargeCheckBox.isChecked(), 0x4B, Mask.MASK_1BIT, 7),
            (self.CBDuringEOCCheckBox.isChecked(), 0x4B, Mask.MASK_1BIT, 0),
            (self.tGainCheckBox.isChecked(), 0x4A, Mask.MASK_1BIT, 4)
        ]
        for value, address, mask, shift in pack_options:
            self.isl94203.reg_write(address, int(value), mask, shift)

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
            packet = self.serial_protocol.read_packet(MEMORY_SIZE)
            _, response = packet
            print(f"response: {response}")
        except Exception as e:
            logging.error(f"Failed to send serial command: {e}")

    def write_bms_config(self):
        if not self.serial_setup or not self.serial_setup.is_open():
            logging.error("Serial port is not open")
            self.statusBar.showMessage("Error: Serial port is not open.")
            return

        register_cfg = self.isl94203.get_registers()

        self.write_voltage_limits()
        self.write_voltage_limits_timing()
        self.write_timers()
        self.write_cell_balance_registers()
        self.write_temperature_registers()
        self.write_current_registers()
        self.write_pack_option_registers()

        logging.info(f"write_bms_config():\n{' '.join(f'{value:02X}' for value in register_cfg)}")

        self.send_serial_command(CMD_WRITE_EEPROM, register_cfg[ADDR_EEPROM_BEGIN:ADDR_EEPROM_END + 1])
        self.statusBar.showMessage("Configuration written successfully.")

    def read_bms_config(self):
        """Read the BMS configuration from the device."""

        configuration = []

        if not self.serial_setup or not self.serial_setup.is_open():
            error_message = "Serial port is not open"
            logging.error(error_message)
            self.statusBar.showMessage(f"Error: {error_message}.")
            return

        try:
            self.serial_protocol.pause()

            self.serial_setup.reset_input_buffer()
            self.serial_setup.reset_output_buffer()

            self.serial_protocol.send_command(CMD_READ_ALL_MEMORY, [0])
            packet = self.serial_protocol.read_packet(MEMORY_SIZE)
            _, configuration = packet

            self.isl94203.set_registers(list(configuration))
            self.bms_config.update_registers()
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
            self.statusBar.showMessage(f"Error: {ERROR_MESSAGE}.")
            return None
        try:
            serial_protocol = SerialProtocolFmcw(self.serial_setup, self.log_callback)
            serial_protocol.send_command(CMD_READ_RAM, [0])
            packet = serial_protocol.read_packet(RAM_SIZE)
            _, configuration = packet

            self.isl94203.set_ram_values(list(configuration))
            self.bms_config.update_registers()
            self.ui_update_fields()

            logging.info(f"read_bms_ram_config():\n{' '.join(f'{value:02X}' for value in configuration)}")
            self.statusBar.showMessage("RAM configuration read successfully.")

            return list(configuration)

        except Exception as e:
            logging.error(f"Failed to read BMS RAM configuration: {e}")
            self.statusBar.showMessage(f"Error: {e}")
            return None

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
