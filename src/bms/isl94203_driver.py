import logging
from bms.isl94203_constants import *
from bms.isl94203_factory import ISL94203Factory
from gui.utility import convert_to_hex

from . import cfg_voltage_registers  as VoltageReg
from . import cfg_cell_balance_registers  as CellBalReg
from . import cfg_temperature_registers as TempReg
from . import cfg_cell_num_register as CellConfigReg
from . import cfg_timers_registers as TimerReg
from . import cfg_timeout_registers  as TimeoutReg
from . import cfg_bit_registers  as BitReg

from . import ram_current_registers as CurrentReg
from . import ram_voltage_status_registers as RamVoltageReg
from . import ram_temperature_status_registers as RamTempReg
from . import ram_status_register as RamStatusReg

logging.basicConfig(level=logging.DEBUG)


class ISL94203Driver:
    """This class provides operations to read and update the configuration values of the ISL94203 battery management system IC. It can translate back and fourth the raw values from the registers to the actual configuration values based on the datasheet.
    """     
    def __init__(self):
        """Initialize the BMSConfiguration instance with an ISL94203 instance."""
        self.isl94203_hal = ISL94203Factory.create_instance()

        # Voltage Limits
        self.config_registers = {
            "overvoltage_threshold": VoltageReg.reg["overvoltage_threshold"],
            "overvoltage_recovery": VoltageReg.reg["overvoltage_recovery"],
            "undervoltage_threshold": VoltageReg.reg["undervoltage_threshold"],
            "undervoltage_recovery": VoltageReg.reg["undervoltage_recovery"],
            "overvoltage_lockout": VoltageReg.reg["overvoltage_lockout"],
            "undervoltage_lockout": VoltageReg.reg["undervoltage_lockout"],
            "end_of_charge_voltage": VoltageReg.reg["end_of_charge_voltage"],
            "low_voltage_charge": VoltageReg.reg["low_voltage_charge"],
            "sleep_voltage": VoltageReg.reg["sleep_voltage"],
        
            "cb_min_voltage": CellBalReg.v_reg["cell_balance_min_voltage"],
            "cb_max_voltage": CellBalReg.v_reg["cell_balance_max_voltage"],
            "cb_min_delta": CellBalReg.v_reg["cell_balance_min_delta"],
            "cb_max_delta": CellBalReg.v_reg["cell_balance_max_delta"],
            "cb_on_time": CellBalReg.t_reg["cell_balance_on_time"],
            "cb_off_time": CellBalReg.t_reg["cell_balance_off_time"],
            "cb_under_temp": CellBalReg.v_reg["cell_balance_min_temp"],
            "cb_ut_recover": CellBalReg.v_reg["cell_balance_min_temp_recovery"],
            "cb_over_temp": CellBalReg.v_reg["cell_balance_max_temp"],
            "cb_ot_recover": CellBalReg.v_reg["cell_balance_max_temp_recovery"],

            "tl_charge_ot": TempReg.reg["Charge OT Voltage"],
            "tl_charge_ot_recover": TempReg.reg["Charge OT Recovery"],
            "tl_charge_ut": TempReg.reg["Charge UT Voltage"],
            "tl_charge_ut_recover": TempReg.reg["Charge UT Recovery"],
            "tl_discharge_ov": TempReg.reg["Discharge OV Voltage"],
            "tl_discharge_ov_recover": TempReg.reg["Discharge OV Recovery"],
            "tl_discharge_ut": TempReg.reg["Discharge UT Voltage"],
            "tl_discharge_ut_recover": TempReg.reg["Discharge UT Recovery"],
            "tl_internal_ov": TempReg.reg["Internal OV Voltage"],
            "tl_internal_ov_recover": TempReg.reg["Internal OV Recovery"],
        
            "cell_config": CellConfigReg.reg,

            "timer_idle_doze": TimerReg.reg["idle_doze_timer"],
            "timer_sleep": TimerReg.reg["sleep_mode_timer"],
            "timer_wdt": TimerReg.reg["watchdog_timer"],

            "charge_detect_pulse_width": TimeoutReg.reg["charge_detect_pulse_width"],
            "load_detect_pulse_width": TimeoutReg.reg["load_detect_pulse_width"],
            "ov_delay_timeout": TimeoutReg.reg["overvoltage_delay_timeout"],
            "uv_delay_timeout": TimeoutReg.reg["undervoltage_delay_timeout"],
            "open_wire_timing": TimeoutReg.reg["open_wire_timeout"],
            
            "xt2m": BitReg.reg["xt2m"],
            "cfpsd": BitReg.reg["cfpsd"],
            "owpsd": BitReg.reg["owpsd"],
            "uvlopd": BitReg.reg["uvlopd"],
            "dowd": BitReg.reg["dowd"],
            "cbdc": BitReg.reg["cbdc"],
            "cbdd": BitReg.reg["cbdd"],
            "cb_eoc": BitReg.reg["cb_eoc"],
            "tgain": BitReg.reg["tgain"]
        }

        self.ram_registers = {        
            "cut": RamStatusReg.status_bit_reg["cut"],
            "cot": RamStatusReg.status_bit_reg["cot"],
            "dut": RamStatusReg.status_bit_reg["dut"],
            "dot": RamStatusReg.status_bit_reg["dot"],
            "uvlo": RamStatusReg.status_bit_reg["uvlo"],
            "uv": RamStatusReg.status_bit_reg["uv"],
            "ovlo": RamStatusReg.status_bit_reg["ovlo"],
            "ov": RamStatusReg.status_bit_reg["ov"],
            "eochg": RamStatusReg.status_bit_reg["eochg"],
            "open": RamStatusReg.status_bit_reg["open"],
            "cellf": RamStatusReg.status_bit_reg["cellf"],
            "dsc": RamStatusReg.status_bit_reg["dsc"],
            "doc": RamStatusReg.status_bit_reg["doc"],
            "coc": RamStatusReg.status_bit_reg["coc"],
            "iot": RamStatusReg.status_bit_reg["iot"],
            "lvchg": RamStatusReg.status_bit_reg["lvchg"],
            "int_scan": RamStatusReg.status_bit_reg["int_scan"],
            "ecc_fail": RamStatusReg.status_bit_reg["ecc_fail"],
            "ecc_used": RamStatusReg.status_bit_reg["ecc_used"],
            "dching": RamStatusReg.status_bit_reg["dching"],
            "ching": RamStatusReg.status_bit_reg["ching"],
            "ch_prsnt": RamStatusReg.status_bit_reg["ch_prsnt"],
            "ld_prsnt": RamStatusReg.status_bit_reg["ld_prsnt"],
            "in_sleep": RamStatusReg.status_bit_reg["in_sleep"],
            "in_doze": RamStatusReg.status_bit_reg["in_doze"],
            "in_idle": RamStatusReg.status_bit_reg["in_idle"],
            "cbuv": RamStatusReg.status_bit_reg["cbuv"],
            "cbov": RamStatusReg.status_bit_reg["cbov"],
            "cbut": RamStatusReg.status_bit_reg["cbut"],
            "cbot": RamStatusReg.status_bit_reg["cbot"],
            "cb1on": RamStatusReg.cb_bit_reg["cb1on"],
            "cb2on": RamStatusReg.cb_bit_reg["cb2on"],
            "cb3on": RamStatusReg.cb_bit_reg["cb3on"],
            "cb4on": RamStatusReg.cb_bit_reg["cb4on"],
            "cb5on": RamStatusReg.cb_bit_reg["cb5on"],
            "cb6on": RamStatusReg.cb_bit_reg["cb6on"],
            "cb7on": RamStatusReg.cb_bit_reg["cb7on"],
            "cb8on": RamStatusReg.cb_bit_reg["cb8on"],

            "current_gain": CurrentReg.current_gain,

            "vcell_min": RamVoltageReg.reg["vcell_min"],
            "vcell_max": RamVoltageReg.reg["vcell_max"],
            "vcell1": RamVoltageReg.reg["vcell1"],
            "vcell2": RamVoltageReg.reg["vcell2"],
            "vcell3": RamVoltageReg.reg["vcell3"],
            "vcell4": RamVoltageReg.reg["vcell4"],
            "vcell5": RamVoltageReg.reg["vcell5"],
            "vcell6": RamVoltageReg.reg["vcell6"],
            "vcell7": RamVoltageReg.reg["vcell7"],
            "vcell8": RamVoltageReg.reg["vcell8"],
            "vbatt": RamVoltageReg.reg["vbatt"],
            "vrgo": RamVoltageReg.reg["vrgo"],

            "temp_internal": RamTempReg.reg["internal_temperature"],
            "temp_xt1": RamTempReg.reg["external_temperature1"],
            "temp_xt2": RamTempReg.reg["external_temperature2"],
        }


    def read_register(self, register_name: str):
        """Read a register value using the register name."""
        if register_name in self.config_registers:
            field = self.config_registers[register_name]
        elif register_name in self.ram_registers:
            field = self.ram_registers[register_name]
        else:
            raise ValueError(f"Register {register_name} not found.")
        
        raw_value = self.isl94203_hal.reg_read(field.address, field.bit_position, field.bit_mask)
        if hasattr(field, 'mapping') and field.mapping is not None:
            if raw_value in field.mapping:
                return field.mapping[raw_value]
        elif hasattr(field, 'from_raw'):
            return field.from_raw(raw_value)
        return raw_value

    def write_register(self, register_name: str, value):
        """Write a value to a register using the register name."""
        if register_name in self.config_registers:
            field = self.config_registers[register_name]
        elif register_name in self.ram_registers:
            field = self.ram_registers[register_name]
        else:
            raise ValueError(f"Register {register_name} not found.")
        
        raw_value = field.to_raw(value)
        self.isl94203_hal.reg_write(field.address, raw_value, field.bit_mask, field.bit_position)

    def get_register_list(self):
        """Return a single dictionary of all registers."""
        all_registers_dict = {**self.config_registers, **self.ram_registers}
        all_registers = {}
        for register_name, field in all_registers_dict.items():
            all_registers[register_name] = self.read_register(register_name)
        return all_registers
    
    def write_voltage_limits(self, voltage_limits):
        """
        Write the voltage limits to the ISL94203 device.

        Args:
            voltage_limits (dict): A dictionary containing the voltage limit name and its value.
        """
        voltage_addresses = {
            'ov': 0x00,
            'ov_recover': 0x02,
            'under_voltage': 0x04,
            'uv_recover': 0x06,
            'ov_lockout': 0x08,
            'uv_lockout': 0x0A,
            'eoc_voltage': 0x0C,
            'low_voltage_charge': 0x0E,
            'sleep_voltage': 0x44
        }

        for limit, value in voltage_limits.items():
            if limit in voltage_addresses:
                address = voltage_addresses[limit]
                hex_value = convert_to_hex(value, VOLTAGE_CELL_MULTIPLIER)
                self.isl94203_hal.reg_write(address, hex_value, Mask.MASK_12BIT, 0x00)

    def write_voltage_limits_timing(self, timing_limits):
        """
        Write the voltage limits timing to the ISL94203 device.

        Args:
            timing_limits (dict): A dictionary containing the timing limit name and its value.
        """
        timing_addresses = {
            'ov_delay_timeout': (0x10, Mask.MASK_12BIT, 0),
            'uv_delay_timeout': (0x12, Mask.MASK_12BIT, 0),
            'open_wire_sample_time': (0x14, Mask.MASK_10BIT, 0),
            'sleep_delay': (0x46, Mask.MASK_11BIT, 0)
        }

        for limit, (value, unit) in timing_limits.items():
            if limit in timing_addresses:
                address, mask, shift = timing_addresses[limit]
                combined_value = (unit << 9) | value if 'sample_time' in limit else (unit << 10) | value
                self.isl94203_hal.reg_write(address, combined_value, mask, shift)

    def write_timers(self, timer_values):
        """
        Write the timer values to the ISL94203 device.

        Args:
            timer_values (dict): A dictionary containing the timer name and its value.
        """
        timer_addresses = {
            'timer_wdt': (0x46, Mask.MASK_5BIT, 11, 0),
            'timer_idle_doze': (0x48, Mask.MASK_4BIT, 0, 0),
            'timer_sleep': (0x48, Mask.MASK_4BIT, 4, 4)
        }

        for timer, value in timer_values.items():
            if timer in timer_addresses:
                address, mask, shift, scaling = timer_addresses[timer]
                hex_value = convert_time_to_hex(value, scaling)
                self.isl94203_hal.reg_write(address, hex_value, mask, shift)

    def write_cell_balance_registers(self, cell_balance_values, cell_balance_temp_values, cb_on_time, cb_off_time, cb_on_time_unit, cb_off_time_unit):
        """
        Write the cell balance registers to the ISL94203 device.

        Args:
            cell_balance_values (list): A list of tuples containing the value and address for cell balance limits.
            cell_balance_temp_values (list): A list of tuples containing the value and address for cell balance temperature limits.
            cb_on_time (int): The on time value for cell balancing.
            cb_off_time (int): The off time value for cell balancing.
            cb_on_time_unit (int): The unit for the on time value.
            cb_off_time_unit (int): The unit for the off time value.
        """
        cell_balance_addresses = {
            'CBLowerLim': 0x1c,
            'CBUpperLim': 0x1e,
            'CBMinDelta': 0x20,
            'CBMaxDelta': 0x22,
            'CBOnTime': 0x24,
            'CBOffTime': 0x26
        }

        cell_balance_temp_addresses = {
            'CBUnderTemp': 0x28,
            'CBUTRecover': 0x2a,
            'CBOverTemp': 0x2c,
            'CBOTRecover': 0x2e
        }

        for key, value in cell_balance_values.items():
            if key in cell_balance_addresses:
                address = cell_balance_addresses[key]
                hex_value = convert_to_hex(value, VOLTAGE_CELL_MULTIPLIER)
                self.isl94203_hal.reg_write(address, hex_value, Mask.MASK_12BIT, 0x00)

        for key, value in cell_balance_temp_values.items():
            if key in cell_balance_temp_addresses:
                address = cell_balance_temp_addresses[key]
                hex_value = convert_to_hex(value, TEMPERATURE_MULTIPLIER)
                self.isl94203_hal.reg_write(address, hex_value, Mask.MASK_12BIT, 0x00)

        # Combine values and units, then write to registers
        self.isl94203_hal.reg_write(0x24, (cb_on_time_unit << 10) | cb_on_time, Mask.MASK_12BIT, 0)
        self.isl94203_hal.reg_write(0x26, (cb_off_time_unit << 10) | cb_off_time, Mask.MASK_12BIT, 0)

    def write_temperature_registers(self, temp_values):
        """
        Write the temperature registers to the ISL94203 device.

        Args:
            temp_values (dict): A dictionary containing the temperature limit name and its value.
        """
        temp_addresses = {
            'TLChargeOverTemp': 0x30,
            'TLChargeOTRecover': 0x32,
            'TLChargeUnderTemp': 0x34,
            'TLChargeUTRecover': 0x36,
            'TLDiscOverTemp': 0x38,
            'TLDischOTRecover': 0x3a,
            'TLDischUnderTemp': 0x3C,
            'TLDischUTRecover': 0x3E,
            'TLInternalOverTemp': 0x40,
            'TLInternalOTRecover': 0x42
        }

        for limit, value in temp_values.items():
            if limit in temp_addresses:
                address = temp_addresses[limit]
                hex_value = convert_to_hex(value, TEMPERATURE_MULTIPLIER)
                self.isl94203_hal.reg_write(address, hex_value, Mask.MASK_12BIT, 0x00)

    def write_current_detect_pulse(self, pulse_values):
        """
        Write the current detect pulse width to the ISL94203 device.

        Args:
            pulse_values (dict): A dictionary containing the pulse name and its value.
        """
        pulse_addresses = {
            'charge_detect_pulse_width': 0x00,
            'load_detect_pulse_width': 0x04
        }

        for pulse, value in pulse_values.items():
            if pulse in pulse_addresses:
                address = pulse_addresses[pulse]
                self.isl94203_hal.reg_write(address, value, Mask.MASK_4BIT, 0x00)

    def write_cell_config(self, cell_config):
        """
        Write the cell configuration to the ISL94203 device.

        Args:
            cell_config (int): The cell configuration value to write.
        """

        self.isl94203_hal.reg_write(0x48, int(CELL_CONFIG_INT2CODE_MAPPING[cell_config]), Mask.MASK_8BIT, 8)

    def write_pack_option_registers(self, options):
        """
        Write the pack option registers to the ISL94203 device.

        Args:
            options (dict): A dictionary containing the option name and its value.
        """
        pack_options = {
            'poT2MonitorsFETTemp': XT2M_FIELD,
            'poEnableCELLFpsd': CFPSD_FIELD,
            'poEnableOpenWirePSD': OWPSD_FIELD,
            'poEnableUVLO': UVLOPD_FIELD,
            'poEnableOpenWireScan': DOWD_FIELD,
            'CBDuringCharge': CBDC_FIELD,
            'CBDuringDischarge': CBDD_FIELD,
            'CBDuringEOC': CB_EOC_FIELD,
            'tGain': TGAIN_FIELD,
        }

        for option, value in options.items():
            if option in pack_options:
                field = pack_options[option]
                self.isl94203_hal.reg_write_bit(field.address, int(bool(value)), field.bit_position)

    def read_voltage_limits(self):
        """Reads voltage limits from registers and returns a dictionary."""
        voltage_limits = {}
        for field_name, field in self.config_registers.items():
            voltage_limits[field_name] = self.read_register(field_name)
        return voltage_limits

    def write_voltage_limits(self, voltage_limits):
        """Writes voltage limits to registers from a dictionary."""
        for field_name, value in voltage_limits.items():
            if field_name in self.config_registers:
                self.write_config_field(field_name, value)
    
    def read_cell_balance_limits(self):
        """Reads cell balance limits from registers and returns a dictionary."""
        cell_balance_limits = {}
        for field_name, field in self.config_registers.items():
            cell_balance_limits[field_name] = self.read_config_field(field_name)
        return cell_balance_limits
    
if __name__ == "__main__":
    isl9420x = ISL94203Driver()
    
    # Read the default configuration values
    config = isl9420x.isl94203_hal.get_default_registers()
    isl9420x.isl94203_hal.set_registers(config)
    
    print("\nPrint Raw values")
    print("----------------")
    print("EEPROM Registers ( 0x00 - 0x4B )")
    print("addr " + f"{' '.join(f'{value:02X}' for value in range(0x00, 0x4C))}")
    print("val  " + f"{' '.join(f'{value:02X}' for value in config[:ISL94203_EEPROM_SIZE])}")
    print("USER EEPROM Registers ( 0x50 - 0x57 )")
    print("addr " + f"{' '.join(f'{value:02X}' for value in range(0x50, 0x58))}")
    print("val  " + f"{' '.join(f'{value:02X}' for value in config[ADDR_USER_EEPROM_OFFSET:ADDR_RAM_OFFSET])}")
    print("RAM Registers ( 0x80 - 0xAB )")
    print("addr " + f"{' '.join(f'{value:02X}' for value in range(0x80, 0xAC))}")
    print("val  " + f"{' '.join(f'{value:02X}' for value in config[ADDR_RAM_OFFSET:])}")


    print("\nPrint Parsed Registers values")
    print("-----------------------------")
    registers_list = isl9420x.get_register_list()
    max_key_length = max(len(key) for key in registers_list.keys())
    for limit, value in registers_list.items():
        if isinstance(value, float):
            print(f"{limit:<{max_key_length}}: {value:.2f}")
        else:
            print(f"{limit:<{max_key_length}}: {value}")
    


