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
        unit_str = self._read_units_from_register(register_name)
        value = self._read_value_from_register(register_name)

        return value, unit_str
    
    def _read_units_from_register(self, register_name: str) -> str:
        """Read the units from a register using the register name."""
        field = self._lookup_register_info(register_name)
        
        if hasattr(field, 'unit_mapping') and field.unit_mapping is not None:
            unit_raw_value = self.isl94203_hal.reg_read(field.address, field.unit_bit_position, field.unit_bit_mask)
            unit_str = field.unit_mapping.get(unit_raw_value, "")	
        elif hasattr(field, 'unit') and field.unit is not None:
            unit_str = field.unit
        else:
            unit_str = None
        
        return unit_str
    
    def _read_value_from_register(self, register_name: str):
        """Read a value from a register using the register name."""       
        field = self._lookup_register_info(register_name)

        raw_value = self.isl94203_hal.reg_read(field.address, field.bit_position, field.bit_mask)

        if hasattr(field, 'mapping') and field.mapping is not None:
            if raw_value in field.mapping:
                value= field.mapping[raw_value]
        elif hasattr(field, 'from_raw') and field.from_raw is not None:
            value = field.from_raw(raw_value)

        return value

    def _lookup_register_info(self, register_name):
        if register_name in self.config_registers:
            field = self.config_registers[register_name]
        elif register_name in self.ram_registers:
            field = self.ram_registers[register_name]
        else:
            raise ValueError(f"Register {register_name} not found.")
        return field

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
        pass
    def write_voltage_limits_timing(self, timing_limits):
        pass
    def write_timers(self, timer_values):
        pass
    def write_cell_balance_registers(self, cell_balance_values, cell_balance_temp_values, cb_on_time, cb_off_time, cb_on_time_unit, cb_off_time_unit):
        pass
    def write_temperature_registers(self, temp_values):
        pass
    def write_current_detect_pulse(self, pulse_values):
        pass
    def write_cell_config(self, cell_config):
        pass
    def write_pack_option_registers(self, options):
        pass

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
    for limit, (value, unit) in registers_list.items():
        if isinstance(value, float):
            print(f"{limit:<{max_key_length}}: {value:.2f} {unit if unit else ''}")
        else:
            print(f"{limit:<{max_key_length}}: {value} {unit if unit else ''}")
    


