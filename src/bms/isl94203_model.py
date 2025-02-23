from dataclasses import dataclass, field
from bms.isl94203_constants import *


@dataclass
class ISL94203_Model:

    # Configuration values
    config_values_int: list = field(default_factory=list)
    
    # Voltage limits
    ov: float = 0.0
    ov_lockout: float = 0.0
    ov_recover: float = 0.0
    eoc_voltage: float = 0.0
    uv_recover: float = 0.0
    under_voltage: float = 0.0
    sleep_voltage: float = 0.0
    low_voltage_charge: float = 0.0
    uv_lockout: float = 0.0

    # In milliseconds
    charge_detect_pulse_width: int = 0
    load_detect_pulse_width: int = 0

    ov_delay_timeout: int = 0
    uv_delay_timeout: int = 0
    open_wire_timing: int = 0
    sleep_delay: int = 0

    ov_delay_timeout_unit: int = 0
    uv_delay_timeout_unit: int = 0
    open_wire_timing_unit: int = 0
    sleep_delay_unit: int = 0

    # Timers
    timer_idle_doze: int = 0
    timer_sleep: int = 0
    timer_wdt: int = 0

    # Cell configuration
    CELL_CONFIG_MAPPING: dict = field(default_factory=lambda: {
        0b10000011: 3,
        0b11000011: 4,
        0b11000111: 5,
        0b11100111: 6,
        0b11110111: 7,
        0b11111111: 8
    })
    cell_config: int = 0

    # Cell balance limits
    cb_upper_lim: int = 0
    cb_lower_lim: int = 0
    cb_max_delta: int = 0
    cb_min_delta: int = 0
    cb_over_temp: int = 0
    cb_ot_recover: int = 0
    cb_ut_recover: int = 0
    cb_under_temp: int = 0
    cb_on_time: int = 0
    cb_off_time: int = 0

    cb_on_time_unit: int = 0
    cb_off_time_unit: int = 0

    bit_cb_during_charge: bool = False
    bit_cb_during_discharge: bool = False
    bit_cb_during_eoc: bool = False

    # Temperature limits
    tl_charge_over_temp: int = 0
    tl_charge_ot_recover: int = 0
    tl_charge_ut_recover: int = 0
    tl_charge_under_temp: int = 0

    tl_disch_over_temp: int = 0
    tl_disch_ot_recover: int = 0
    tl_disch_ut_recover: int = 0
    tl_disch_under_temp: int = 0

    tl_internal_over_temp: int = 0
    tl_internal_ot_recover: int = 0

    # Pack options
    bit_t2_monitors_fet: bool = False
    bit_enable_cellf_psd: bool = False
    bit_enable_openwire_psd: bool = False
    bit_enable_uvlo_pd: bool = False
    bit_enable_openwire_scan: bool = False

    # Temperature gain
    bit_tgain: bool = False

    # Current limits
    disch_oc_voltage: int = 0
    disch_oc_timeout: int = 0
    disch_oc_timeout_unit: int = 0
    charge_oc_voltage: int = 0
    charge_oc_timeout: int = 0
    charge_oc_timeout_unit: int = 0
    disch_sc_voltage: int = 0
    disch_sc_timeout: int = 0
    disch_sc_timeout_unit: int = 0

    # RAM
    # Address 0x80
    bit_ov: bool = False
    bit_ovlo: bool = False
    bit_uv: bool = False
    bit_uvlo: bool = False
    bit_dot: bool = False
    bit_dut: bool = False
    bit_cot: bool = False
    bit_cut: bool = False

    # Address 0x81
    bit_iot: bool = False
    bit_coc: bool = False
    bit_doc: bool = False
    bit_dsc: bool = False
    bit_cellf: bool = False
    bit_open: bool = False
    bit_eochg: bool = False

    # Address 0x82
    bit_ld_prsnt: bool = False
    bit_ch_prsnt: bool = False
    bit_ching: bool = False
    bit_dching: bool = False
    bit_ecc_used: bool = False
    bit_ecc_fail: bool = False
    bit_int_scan: bool = False
    bit_lvchg: bool = False

    # Address 0x83
    bit_cbot: bool = False
    bit_cbut: bool = False
    bit_cbov: bool = False
    bit_cbuv: bool = False
    bit_in_idle: bool = False
    bit_in_doze: bool = False
    bit_in_sleep: bool = False

    # Current calculation
    # Create a dictionary mapping binary patterns current gains
    current_gain_code: dict = field(default_factory=lambda: {
        0b00: 50,
        0b01: 5,
        0b10: 500,
        0b11: 500
    })

    v_sense: float = 0.0  # Voltage over Sense Resistor
    i_pack: float = 0.0  # Current over Sense Resistor (Pack current)
    i_gain: int = 0

    # Temperature
    temp_internal: float = 0.0
    temp_xt1: float = 0.0
    temp_xt2: float = 0.0

    # Cell voltages
    vcell1: float = 0
    vcell2: float = 0
    vcell3: float = 0
    vcell4: float = 0
    vcell5: float = 0
    vcell6: float = 0
    vcell7: float = 0
    vcell8: float = 0
    vcell_min: float = 0
    vcell_max: float = 0
    vbatt: float = 0
    vrgo: float = 0

    # Mapping of codes to text values
    unit_mapping: dict = field(default_factory=lambda: {0: "μs", 1: "ms", 2: "s", 3: "min"})
    doc_mapping: dict = field(
        default_factory=lambda: {0: "4mV", 1: "8mV", 2: "16mV", 3: "24mV", 4: "32mV", 5: "48mV", 6: "64mV", 7: "96mV"})
    coc_mapping: dict = field(
        default_factory=lambda: {0: "1mV", 1: "2mV", 2: "4mV", 3: "6mV", 4: "8mV", 5: "12mV", 6: "16mV", 7: "24mV"})
    dsc_mapping: dict = field(
        default_factory=lambda: {0: "16mV", 1: "24mV", 2: "32mV", 3: "48mV", 4: "64mV", 5: "96mV", 6: "128mV",
                                 7: "256mV"})
