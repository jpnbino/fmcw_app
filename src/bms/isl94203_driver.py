import logging
from bms.isl94203_constants import *
from bms.isl94203_factory import ISL94203Factory

from . import cfg_voltage_registers  as VoltageReg
from . import cfg_cell_balance_registers  as CellBalReg
from . import cfg_temperature_registers as TempReg
from . import cfg_cell_num_register as CellConfigReg
from . import cfg_timers_registers as TimerReg
from . import cfg_timeout_registers  as TimeoutReg
from . import cfg_bit_registers  as BitReg
from . import cfg_current_limits_registers as CurrentReg

from . import ram_current_registers as RamCurrentReg
from . import ram_voltage_status_registers as RamVoltageReg
from . import ram_temperature_status_registers as RamTempReg
from . import ram_status_register as RamStatusReg

logging.basicConfig(level=logging.DEBUG)


class ISL94203Driver:
    """This class provides operations to read and update the configuration values of the ISL94203 battery management system IC. It can translate back and fourth the raw values from the registers to the actual configuration values based on the datasheet.
    """     
    def __init__(self, resistor: float = 0.005):
        """Initialize the BMSConfiguration instance with an ISL94203 instance."""
        self.isl94203_hal = ISL94203Factory.create_instance()
        self.resistor = resistor # Current sense resistor value in mOhm

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

            # Charge and Discharge Current Limits
            "cl_discharge_oc": CurrentReg.reg["discharge_oc_current"],
            "cl_charge_oc": CurrentReg.reg["charge_oc_current"],
            "cl_discharge_sc": CurrentReg.reg["discharge_sc_current"],

            "cl_discharge_oc_delay": CurrentReg.reg["discharge_oc_delay"],
            "cl_charge_oc_delay": CurrentReg.reg["charge_oc_delay"],
            "cl_discharge_sc_delay": CurrentReg.reg["discharge_sc_delay"],
    

            "cl_pulse_width_charge": CurrentReg.reg["charge_detect_pulse_width"],
            "cl_pulse_width_load": CurrentReg.reg["discharge_detect_pulse_width"],
            
            "tl_charge_ot": TempReg.reg["Charge OT Voltage"],
            "tl_charge_ot_recover": TempReg.reg["Charge OT Recovery"],
            "tl_charge_ut": TempReg.reg["Charge UT Voltage"],
            "tl_charge_ut_recover": TempReg.reg["Charge UT Recovery"],
            "tl_discharge_ot": TempReg.reg["Discharge OV Voltage"],
            "tl_discharge_ot_recover": TempReg.reg["Discharge OV Recovery"],
            "tl_discharge_ut": TempReg.reg["Discharge UT Voltage"],
            "tl_discharge_ut_recover": TempReg.reg["Discharge UT Recovery"],
            "tl_internal_ot": TempReg.reg["Internal OV Voltage"],
            "tl_internal_ot_recover": TempReg.reg["Internal OV Recovery"],
        
            "cell_config": CellConfigReg.reg,

            "timer_idle_doze": TimerReg.reg["idle_doze_timer"],
            "timer_sleep": TimerReg.reg["sleep_mode_timer"],
            "timer_wdt": TimerReg.reg["watchdog_timer"],

            "charge_detect_pulse_width": TimeoutReg.reg["charge_detect_pulse_width"],
            "load_detect_pulse_width": TimeoutReg.reg["load_detect_pulse_width"],
            "ov_delay_timeout": TimeoutReg.reg["overvoltage_delay_timeout"],
            "uv_delay_timeout": TimeoutReg.reg["undervoltage_delay_timeout"],
            "open_wire_timing": TimeoutReg.reg["open_wire_timeout"],
            "sleep_delay": TimeoutReg.reg["sleep_delay"],
            
            "po_t2_monitors_fet": BitReg.reg["xt2m"],
            "po_enable_cellf_psd": BitReg.reg["cfpsd"],
            "po_enable_openwire_psd": BitReg.reg["owpsd"],
            "po_enable_uvlo_pd": BitReg.reg["uvlopd"],
            "po_enable_openwire_scan": BitReg.reg["dowd"],
            "cb_during_charge": BitReg.reg["cbdc"],
            "cb_during_discharge": BitReg.reg["cbdd"],
            "cb_during_eoc": BitReg.reg["cb_eoc"],
            "tgain": BitReg.reg["tgain"]
        }

        self.ram_registers = {        
            "bit_cut": RamStatusReg.status_bit_reg["cut"],
            "bit_cot": RamStatusReg.status_bit_reg["cot"],
            "bit_dut": RamStatusReg.status_bit_reg["dut"],
            "bit_dot": RamStatusReg.status_bit_reg["dot"],
            "bit_uvlo": RamStatusReg.status_bit_reg["uvlo"],
            "bit_uv": RamStatusReg.status_bit_reg["uv"],
            "bit_ovlo": RamStatusReg.status_bit_reg["ovlo"],
            "bit_ov": RamStatusReg.status_bit_reg["ov"],
            "bit_eochg": RamStatusReg.status_bit_reg["eochg"],
            "bit_open": RamStatusReg.status_bit_reg["open"],
            "bit_cellf": RamStatusReg.status_bit_reg["cellf"],
            "bit_dsc": RamStatusReg.status_bit_reg["dsc"],
            "bit_doc": RamStatusReg.status_bit_reg["doc"],
            "bit_coc": RamStatusReg.status_bit_reg["coc"],
            "bit_iot": RamStatusReg.status_bit_reg["iot"],
            "bit_lvchg": RamStatusReg.status_bit_reg["lvchg"],
            "bit_int_scan": RamStatusReg.status_bit_reg["int_scan"],
            "bit_ecc_fail": RamStatusReg.status_bit_reg["ecc_fail"],
            "bit_ecc_used": RamStatusReg.status_bit_reg["ecc_used"],
            "bit_dching": RamStatusReg.status_bit_reg["dching"],
            "bit_ching": RamStatusReg.status_bit_reg["ching"],
            "bit_ch_prsnt": RamStatusReg.status_bit_reg["ch_prsnt"],
            "bit_ld_prsnt": RamStatusReg.status_bit_reg["ld_prsnt"],
            "bit_in_sleep": RamStatusReg.status_bit_reg["in_sleep"],
            "bit_in_doze": RamStatusReg.status_bit_reg["in_doze"],
            "bit_in_idle": RamStatusReg.status_bit_reg["in_idle"],
            "bit_cbuv": RamStatusReg.status_bit_reg["cbuv"],
            "bit_cbov": RamStatusReg.status_bit_reg["cbov"],
            "bit_cbut": RamStatusReg.status_bit_reg["cbut"],
            "bit_cbot": RamStatusReg.status_bit_reg["cbot"],
            "bit_cb1on": RamStatusReg.cb_bit_reg["cb1on"],
            "bit_cb2on": RamStatusReg.cb_bit_reg["cb2on"],
            "bit_cb3on": RamStatusReg.cb_bit_reg["cb3on"],
            "bit_cb4on": RamStatusReg.cb_bit_reg["cb4on"],
            "bit_cb5on": RamStatusReg.cb_bit_reg["cb5on"],
            "bit_cb6on": RamStatusReg.cb_bit_reg["cb6on"],
            "bit_cb7on": RamStatusReg.cb_bit_reg["cb7on"],
            "bit_cb8on": RamStatusReg.cb_bit_reg["cb8on"],

            "i_gain": RamCurrentReg.reg["gain"],
            "current_i": RamCurrentReg.reg["i"],

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

    def _lookup_register_info(self, register_name):
        if register_name in self.config_registers:
            field = self.config_registers[register_name]
        elif register_name in self.ram_registers:
            field = self.ram_registers[register_name]
        else:
            raise ValueError(f"Register {register_name} not found.")
        return field

    def read_register(self, register_name: str):
        """Read a register value using the register name."""    
        unit_str = self._read_units_from_register(register_name)
        value = self._read_value_from_register(register_name)

        return value, unit_str
    
    def _read_units_from_register(self, register_name: str) -> str:
        """Read the units from a register using the register name."""
        field = self._lookup_register_info(register_name)
        
        if hasattr(field, 'unit_mapping') and field.unit_mapping is not None:
            unit_raw_value = self.isl94203_hal.reg_read(field.address, field.bit_position, field.bit_mask)
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
            if register_name == "current_i":
                gain_raw_value = self.isl94203_hal.reg_read(RamCurrentReg.reg["gain"].address, RamCurrentReg.reg["gain"].bit_position, RamCurrentReg.reg["gain"].bit_mask)
                gain = CURRENT_GAIN_MAPPING[gain_raw_value]
                value = field.from_raw(raw_value, self.resistor, gain)    
            else:
                value = field.from_raw(raw_value)

        return value

    def write_register(self, register_name: str, value, value_unit=None):
        """Write a value to a register using the register name."""
        field = self._lookup_register_info(register_name)
        
        if hasattr(field, 'to_raw') and field.to_raw is not None:
            if hasattr(field, 'mapping') and field.mapping is not None:
                raw_value = field.to_raw(value, field.mapping)
            else:
                raw_value = field.to_raw(value)
        else:
            raise ValueError(f"Field {register_name} does not have a 'to_raw' method.")
        
        self.isl94203_hal.reg_write(field.address, raw_value, field.bit_mask, field.bit_position)

    def get_register_list(self):
        """Return a single dictionary of all registers."""
        all_registers_dict = {**self.config_registers, **self.ram_registers}
        all_registers = {}
        for register_name, field in all_registers_dict.items():
            all_registers[register_name] = self.read_register(register_name)
        return all_registers

    def read_all_registers(self):
        """Reads all configuration and RAM registers and returns a dictionary."""
        all_registers = {}
        for field_name in self.config_registers.keys():
            try:
                all_registers[field_name] = self.read_register(field_name)
            except Exception as e:
                logging.error(f"Error reading config register {field_name}: {e}")
                all_registers[field_name] = None
        for field_name in self.ram_registers.keys():
            try:
                all_registers[field_name] = self.read_register(field_name)
            except Exception as e:
                logging.error(f"Error reading RAM register {field_name}: {e}")
                all_registers[field_name] = None
        return all_registers

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
                self.write_register(field_name, value)
 
    def write_voltage_limits_timing(self, timing_limits):
        """Writes voltage limits timing to registers from a dictionary."""
        for field_name, value in timing_limits.items():
            if isinstance(value, tuple):
                value, value_unit = value
            else:
                value_unit = None
            if field_name in self.config_registers:
                self.write_register(field_name, value, value_unit)
            else:
                raise ValueError(f"Field {field_name} not found in config registers.")
                
    def write_timers(self, timer_values):
        """Writes timer values to registers from a dictionary."""
        for field_name, value in timer_values.items():
            if field_name in self.config_registers:
                self.write_register(field_name, value)
            else:
                raise ValueError(f"Field {field_name} not found in config registers.")

    def write_cell_balance_registers(self, cell_balance_values):
        for field_name, value in cell_balance_values.items():
            if isinstance(value, tuple):
                value, value_unit = value
            else:
                value_unit = None
            if field_name in self.config_registers:
                self.write_register(field_name, value, value_unit)
            else:
                raise ValueError(f"Field {field_name} not found in config registers.")
    
    def write_temperature_registers(self, temp_values):
        for field_name, value in temp_values.items():
            if field_name in self.config_registers:
                self.write_register(field_name, value)
    
    def write_current_registers(self, current_values):
        for field_name, value in current_values.items():
            if isinstance(value, tuple):
                value, value_unit = value
            else:
                value_unit = None
            if field_name in self.config_registers:
                self.write_register(field_name, value, value_unit)
            else:
                raise ValueError(f"Field {field_name} not found in config registers.")

    def write_cell_config(self, cell_config):

        self.write_register("cell_config", cell_config)

    def write_pack_option_registers(self, options):
        for field_name, value in options.items():
            if field_name in self.config_registers:
                self.write_register(field_name, value)
            else:
                raise ValueError(f"Field {field_name} not found in config registers.")

    def read_cell_balance_limits(self):
        """Reads cell balance limits from registers and returns a dictionary."""
        cell_balance_limits = {}
        for field_name, field in self.config_registers.items():
            cell_balance_limits[field_name] = self.read_config_field(field_name)
        return cell_balance_limits
    
    def set_resistor_value(self, resistor_value):
        """Set the current sense resistor value."""
        self.resistor = resistor_value
        logging.debug(f"Current sense resistor value set to: {self.resistor} Ohm")

    def get_resistor_value(self):
        """Get the current sense resistor value."""
        return self.resistor
    
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
    


