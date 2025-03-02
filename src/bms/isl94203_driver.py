import logging
from bms.isl94203_constants import *
from bms.isl94203_factory import ISL94203Factory
from gui.utility import convert_to_hex

from . import cfg_voltage_registers  as VoltageReg
from . import cfg_cell_balance_registers  as CellBalReg
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

            "vcell_min": RamVoltageReg.reg["cell_min_voltage"],
            "vcell_max": RamVoltageReg.reg["cell_max_voltage"],
            "vcell1": RamVoltageReg.reg["vcell1"],
            "vcell2": RamVoltageReg.reg["vcell2"],
            "vcell3": RamVoltageReg.reg["vcell3"],
            "vcell4": RamVoltageReg.reg["vcell4"],
            "vcell5": RamVoltageReg.reg["vcell5"],
            "vcell6": RamVoltageReg.reg["vcell6"],
            "vcell7": RamVoltageReg.reg["vcell7"],
            "vcell8": RamVoltageReg.reg["vcell8"],
            "vbatt": RamVoltageReg.reg["vbatt_voltage"],
            "vrgo": RamVoltageReg.reg["vrgon_voltage"],

            "temp_internal": RamTempReg.internal_temperature,
            "temp_xt1": RamTempReg.external_temperature1,
            "temp_xt2": RamTempReg.external_temperature2,
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
        if hasattr(field, 'from_raw'):
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

    
    def update_registers(self):
        """
        Update the parameters values after reading from registers.
        This method retrieves the current register values from the ISL94203 device
        and logs them. It then updates various configuration parameters such as
        voltage limits, timing, cell configuration, pack options, cell balance,
        current limits, temperature limits, RAM values, and feature controls.
        
        Raises:
            Exception: If any error occurs during the update of configuration parameters.
        """
        registers = self.isl94203_hal.get_registers()
        logging.info(f"update_registers()\n{' '.join(f'{value:02X}' for value in registers)}")

        try:
            self.update_voltage_limits()
            self.update_timing()
            self.cell_configuration()
            self.update_pack_options()
            self.update_cell_balance()
            self.update_current_limits()
            self.update_temperature_limits()
            self.update_ram_values()
            self.update_feature_controls()
        except Exception as e:
            print(f"Error updating configuration: {e}")

    def update_voltage_limits(self):
        """Reads voltage values from specific registers and updates the corresponding attributes of the object."""
        voltage_mapping = {
            "overvoltage_threshold": "ov",
            "overvoltage_recovery": "ov_recover",
            "undervoltage_threshold": "under_voltage",
            "undervoltage_recovery": "uv_recover",
            "overvoltage_lockout": "ov_lockout",
            "undervoltage_lockout": "uv_lockout",
            "end_of_charge_voltage": "eoc_voltage",
            "low_voltage_charge": "low_voltage_charge",
            "sleep_voltage": "sleep_voltage"
        }
        for register_name, attr in voltage_mapping.items():
            try:
                value = self.read_register(register_name)
                setattr(self, attr, value)
            except Exception as e:
                print(f"Error updating voltage limits: {e}")

    def update_timing(self):
        """
        This method reads timing values from specific registers and updates the 
        corresponding attributes of the object. The timing values are read using 
        the `isl94203.reg_read` method and are mapped to attributes based on a 
        predefined mapping.

        Attributes Updated:
            - ov_delay_timeout (int): Overvoltage delay timeout.
            - uv_delay_timeout (int): Undervoltage delay timeout.
            - open_wire_timing (int): Open wire timing.
            - timer_idle_doze (int): Timer idle doze.
            - timer_sleep (int): Timer sleep.
            - timer_wdt (int): Timer watchdog timeout.

        Raises:
            Exception: If there is an error reading from the registers.
        """
        timing_mapping = {
            "ov_delay_timeout": "ov_delay_timeout",
            "uv_delay_timeout": "uv_delay_timeout",
            "open_wire_timing": "open_wire_timing",
            "timer_idle_doze": "timer_idle_doze",
            "timer_sleep": "timer_sleep",
            "timer_wdt": "timer_wdt"
        }
        for register_name, attr in timing_mapping.items():
            try:
                value = self.read_register(register_name)
                setattr(self, attr, value)
            except Exception as e:
                print(f"Error updating timing: {e}")

    def cell_configuration(self):
        # Cell Configuration
        self.cell_config = self.isl94203_hal.reg_read(0x48, 8, Mask.MASK_8BIT)

    def update_pack_options(self):
        """
        Update the pack options (Addresses 0x4A and 0x4B) attributes based on the given values.
        This method reads specific bits from the ISL94203 device and updates the corresponding
        attributes of the class instance.
        
        **Attributes Updated**:
            - bit_enable_openwire_psd (bool): Enable open wire PSD.
            - bit_enable_openwire_scan (bool): Enable open wire scan.
            - bit_tgain (bool): TGAIN bit.
            - bit_t2_monitors_fet (bool): T2 monitors FET bit.
            - bit_enable_cellf_psd (bool): Enable cell F PSD.
            - bit_cb_during_eoc (bool): CB during EOC bit.
            - bit_enable_uvlo_pd (bool): Enable UVLO PD bit.
            - bit_cb_during_charge (bool): CB during charge bit.
            - bit_cb_during_discharge (bool): CB during discharge bit.

        Raises:
            Exception: If there is an error reading a bit from the ISL94203 device.
        """
        pack_options_mapping = {
            (0x4A, 0): 'bit_enable_openwire_psd',
            (0x4A, 1): 'bit_enable_openwire_scan',
            (0x4A, 4): 'bit_tgain',
            (0x4A, 5): 'bit_t2_monitors_fet',
            (0x4A, 7): 'bit_enable_cellf_psd',
            (0x4B, 0): 'bit_cb_during_eoc',
            (0x4B, 3): 'bit_enable_uvlo_pd',
            (0x4B, 6): 'bit_cb_during_charge',
            (0x4B, 7): 'bit_cb_during_discharge'
        }

        for (addr, bit_pos), attr in pack_options_mapping.items():
            try:
                setattr(self, attr, self.isl94203_hal.read_bit(addr, bit_pos))
            except Exception as e:
                print(f"Error updating pack options: {e}")

    def update_cell_balance(self):
        """
        Update various cell balance attributes by reading values from specific addresses
        and applying necessary calculations.

        This method handles three main categories of attributes:
            - cell balance limits
            - cell balance timing
            - cell balance temperature.

        Cell balance limits are updated using a predefined mapping of addresses to attribute
        names. The values are calculated using the `calculate_voltage` method.

        Cell balance timing attributes are updated using a predefined mapping of address,
        bit shift, and bit mask to attribute names. The values are read using the `isl94203.reg_read` method.

        Cell balance temperature attributes are updated using a predefined mapping of low and high byte
        addresses to attribute names. The values are calculated using the `calculate_temperature_from_raw_value` method.

        Attributes Updated:
            - cb_lower_lim (float): Cell balance lower limit.
            - cb_upper_lim (float): Cell balance upper limit.
            - cb_min_delta (float): Cell balance minimum delta.
            - cb_max_delta (float): Cell balance maximum delta.
            - cb_on_time (int): Cell balance on time.
            - cb_on_time_unit (int): Cell balance on time unit.
            - cb_off_time (int): Cell balance off time.
            - cb_off_time_unit (int): Cell balance off time unit.
            - cb_under_temp (float): Cell balance under temperature.
            - cb_ut_recover (float): Cell balance under temperature recover.
            - cb_over_temp (float): Cell balance over temperature.

        Exceptions are caught and printed for each update operation to ensure that errors do not interrupt
        the entire update process.

        Raises:
            Exception: If there is an error updating any of the cell balance attributes.
        """
        cell_balance_mapping = {
            0x1C: 'cb_lower_lim',
            0x1E: 'cb_upper_lim',
            0x20: 'cb_min_delta',
            0x22: 'cb_max_delta'
        }

        for addr, attr in cell_balance_mapping.items():
            try:
                setattr(self, attr, self.calculate_voltage(addr))
            except Exception as e:
                print(f"Error updating cell balance: {e}")

        cell_balance_timing_mapping = {
            (0x24, 0, Mask.MASK_10BIT): 'cb_on_time',
            (0x24, 10, Mask.MASK_2BIT): 'cb_on_time_unit',
            (0x26, 0, Mask.MASK_10BIT): 'cb_off_time',
            (0x26, 10, Mask.MASK_2BIT): 'cb_off_time_unit'
        }

        for (addr, bit_shift, bit_mask), attr in cell_balance_timing_mapping.items():
            try:
                value = self.isl94203_hal.reg_read(addr, bit_shift, bit_mask)
                setattr(self, attr, value)
            except Exception as e:
                print(f"Error updating cell balance timing: {e}")

        temperature_mapping = {
            (0x28, 0x29): 'cb_under_temp',
            (0x2A, 0x2B): 'cb_ut_recover',
            (0x2C, 0x2D): 'cb_over_temp',
            (0x2E, 0x2F): 'cb_ot_recover'
        }

        for (low_byte, high_byte), attr in temperature_mapping.items():
            try:
                registers = self.isl94203_hal.get_registers()
                value = self.calculate_temperature_from_raw_value((registers[high_byte] << 8) | registers[low_byte])
                setattr(self, attr, value)
            except Exception as e:
                print(f"Error updating cell balance temperature: {e}")

    def update_current_limits(self):
        """
        Update the current limit attributes based on the given values.
        This method reads specific registers from the ISL94203 device and updates
        the corresponding attributes of the instance with the read values. The
        mapping of registers to attributes is defined in the `current_limits_mapping`
        dictionary.

        Raises:
            Exception: If there is an error reading from the ISL94203 device.
        
        Attributes Updated:
            - disch_oc_voltage (int): Discharge overcurrent voltage.
            - disch_oc_timeout (int): Discharge overcurrent timeout.
            - disch_oc_timeout_unit (int): Discharge overcurrent timeout unit.
            - charge_oc_voltage (int): Charge overcurrent voltage.
            - charge_oc_timeout (int): Charge overcurrent timeout.
            - charge_oc_timeout_unit (int): Charge overcurrent timeout unit.
            - disch_sc_voltage (int): Discharge short-circuit voltage.
            - disch_sc_timeout (int): Discharge short-circuit timeout.
            - disch_sc_timeout_unit (int): Discharge short-circuit timeout unit.
            - charge_detect_pulse_width (int): Charge detect pulse width.
            - load_detect_pulse_width (int): Load detect pulse width.

        """
        current_limits_mapping = {
            (0x16, 12, Mask.MASK_3BIT): 'disch_oc_voltage',
            (0x16, 0, Mask.MASK_10BIT): 'disch_oc_timeout',
            (0x16, 10, Mask.MASK_2BIT): 'disch_oc_timeout_unit',
            (0x18, 12, Mask.MASK_3BIT): 'charge_oc_voltage',
            (0x18, 0, Mask.MASK_10BIT): 'charge_oc_timeout',
            (0x18, 10, Mask.MASK_2BIT): 'charge_oc_timeout_unit',
            (0x1A, 12, Mask.MASK_3BIT): 'disch_sc_voltage',
            (0x1A, 0, Mask.MASK_10BIT): 'disch_sc_timeout',
            (0x1A, 10, Mask.MASK_2BIT): 'disch_sc_timeout_unit',
            (0x00, 12, Mask.MASK_4BIT): 'charge_detect_pulse_width',
            (0x04, 12, Mask.MASK_4BIT): 'load_detect_pulse_width'
        }

        for (addr, bit_shift, bit_mask), attr in current_limits_mapping.items():
            try:
                value = self.isl94203_hal.reg_read(addr, bit_shift, bit_mask)
                setattr(self, attr, value)
            except Exception as e:
                print(f"Error updating current limits: {e}")

    def update_temperature_limits(self):
        """Update the temperature limit attributes based on the given values.
        This method maps specific addresses to temperature limit attributes and updates
        these attributes by calculating the temperature voltage for each address.
        
        Raises:
            Exception: If there is an error updating any of the temperature limits.
        """
        temperature_limits_mapping = {
            0x30: 'tl_charge_over_temp',
            0x32: 'tl_charge_ot_recover',
            0x34: 'tl_charge_under_temp',
            0x36: 'tl_charge_ut_recover',
            0x38: 'tl_disch_over_temp',
            0x3A: 'tl_disch_ot_recover',
            0x3C: 'tl_disch_under_temp',
            0x3E: 'tl_disch_ut_recover',
            0x40: 'tl_internal_over_temp',
            0x42: 'tl_internal_ot_recover'
        }

        for addr, attr in temperature_limits_mapping.items():
            try:
                setattr(self, attr, self.calculate_temp_voltage(addr))
            except Exception as e:
                print(f"Error updating temperature limits: {e}")

    def update_ram_values(self):
        """
        Update the RAM attributes based on the given values.
        This method reads various RAM addresses and updates the corresponding 
        attributes of the object with the processed values. The values are 
        processed based on the type of attribute being updated.

        Attributes Updated:
            - v_sense: Pack current sense voltage
            - vcell1 to vcell8: Cell voltages
            - vcell_min: Minimum cell voltage
            - vcell_max: Maximum cell voltage
            - temp_internal: Internal temperature
            - temp_xt1: External temperature sensor 1
            - temp_xt2: External temperature sensor 2
            - vbatt: Battery voltage
            - vrgo: Regulator output voltage

        Raises:
            Exception: If there is an error reading or processing the RAM values.
        """
        self.i_gain = CURRENT_GAIN_MAPPING[self.isl94203_hal.reg_read(0x85, 4, Mask.MASK_12BIT)]
        ram_addresses = {
            0x8E: 'v_sense',
            0x90: 'vcell1',
            0x92: 'vcell2',
            0x94: 'vcell3',
            0x96: 'vcell4',
            0x98: 'vcell5',
            0x9A: 'vcell6',
            0x9C: 'vcell7',
            0x9E: 'vcell8',
            0x8A: 'vcell_min',
            0x8C: 'vcell_max',
            0xA0: 'temp_internal',
            0xA2: 'temp_xt1',
            0xA4: 'temp_xt2',
            0xA6: 'vbatt',
            0xA8: 'vrgo'
        }

        for addr, attr in ram_addresses.items():
            try:
                value = 0
                if 'temp' in attr:
                    value = self.calculate_temperature_from_raw_value(self.isl94203_hal.reg_read(addr))
                elif 'vcell' in attr:
                    value = self.apply_mask_and_multiplier(self.isl94203_hal.reg_read(addr))
                elif attr == 'v_sense':
                    value = self.apply_mask_and_multiplier_pack_current(self.isl94203_hal.reg_read(addr), self.i_gain)
                elif attr == 'vbatt':
                    value = self.apply_mask_and_multiplier_pack(self.isl94203_hal.reg_read(addr))
                elif attr == 'vrgo':
                    value = self.calculate_vrgo_from_raw_value(self.isl94203_hal.reg_read(addr))

                setattr(self, attr, value)
            except Exception as e:
                print(f"Error updating RAM values: {e}")

    def update_feature_controls(self):
        """
        Update the feature control attributes based on the given values.
        This method reads specific bits from the ISL94203 device and updates the corresponding
        attributes of the class instance. The mapping of (address, bit position) to attribute
        names is predefined in the `bit_mapping` dictionary.
        
        Raises:
            Exception: If there is an error reading a bit from the ISL94203 device, an exception is caught and an error message is printed.
        """
        # Define the mapping of (address, bit position) to attribute names
        bit_mapping = {
            (0x80, 0): 'bit_ov',
            (0x80, 1): 'bit_ovlo',
            (0x80, 2): 'bit_uv',
            (0x80, 3): 'bit_uvlo',
            (0x80, 4): 'bit_dot',
            (0x80, 5): 'bit_dut',
            (0x80, 6): 'bit_cot',
            (0x80, 7): 'bit_cut',
            (0x81, 0): 'bit_iot',
            (0x81, 1): 'bit_coc',
            (0x81, 2): 'bit_doc',
            (0x81, 3): 'bit_dsc',
            (0x81, 4): 'bit_cellf',
            (0x81, 5): 'bit_open',
            (0x81, 7): 'bit_eochg',
            (0x82, 0): 'bit_ld_prsnt',
            (0x82, 1): 'bit_ch_prsnt',
            (0x82, 2): 'bit_ching',
            (0x82, 3): 'bit_dching',
            (0x82, 4): 'bit_ecc_used',
            (0x82, 5): 'bit_ecc_fail',
            (0x82, 6): 'bit_int_scan',
            (0x82, 7): 'bit_lvchg',
            (0x83, 0): 'bit_cbot',
            (0x83, 1): 'bit_cbut',
            (0x83, 2): 'bit_cbov',
            (0x83, 3): 'bit_cbuv',
            (0x83, 4): 'bit_in_idle',
            (0x83, 5): 'bit_in_doze',
            (0x83, 6): 'bit_in_sleep'
        }

        # Iterate through the mapping and set the attributes
        for (address, bit_position), attr_name in bit_mapping.items():
            try:
                value = self.isl94203_hal.read_bit(address, bit_position)
                setattr(self, attr_name, value)
            except Exception as e:
                print(f"Error updating feature controls: {e}")

    def apply_mask_and_multiplier_generic(self, value, multiplier, gain=1):
        """
        Apply a mask and a multiplier to the given value.

        Args:
            value (int): The raw value to be processed.
            multiplier (float): The multiplier to be applied.
            gain (float): The gain to be applied (default is 1).

        Returns:
            float: The processed value.
        """
        masked_value = value & Mask.MASK_12BIT.value
        result = masked_value * multiplier / gain
        return result

    def apply_mask_and_multiplier(self, value):
        """
        Apply a mask and a multiplier to the given value for cell voltage.

        Args:
            value (int): The raw value to be processed.

        Returns:
            float: The processed value.
        """
        return self.apply_mask_and_multiplier_generic(value, VOLTAGE_CELL_MULTIPLIER)

    def apply_mask_and_multiplier_pack_current(self, value, gain):
        """
        Apply a mask and a multiplier to the given value for pack current.

        Args:
            value (int): The raw value to be processed.
            gain (float): The gain to be applied.

        Returns:
            float: The processed value.
        """
        return self.apply_mask_and_multiplier_generic(value, CURRENT_CELL_MULTIPLIER, gain)

    def apply_mask_and_multiplier_pack(self, value):
        """
        Apply a mask and a multiplier to the given value for pack voltage.

        Args:
            value (int): The raw value to be processed.

        Returns:
            float: The processed value.
        """
        return self.apply_mask_and_multiplier_generic(value, VOLTAGE_PACK_MULTIPLIER)

    def calculate_vrgo_from_raw_value(self, value):
        """
        Calculates the VRGO (Voltage regulator output) based on the raw value. Should be around 2.5V.

        Args:
            value (int): Voltage raw value as stored in the register.

        Returns:
            float: Real voltage calculated from the raw value. (e.g. 2.5 V)
        """
        return self.apply_mask_and_multiplier_generic(value, VOLTAGE_VRGO_MULTIPLIER)

    def calculate_temperature_from_raw_value(self, value):
        """
        Calculates the temperature from the raw value.

        Args:
            value (int): The raw value to calculate the temperature from.

        Returns:
            float: The calculated temperature in volts. For Celsius, use thermistor datasheet.
        """
        return self.apply_mask_and_multiplier_generic(value, TEMPERATURE_MULTIPLIER)

    def calculate_voltage(self, address):
        """
        Calculate voltage based on values and address.

        Args:
            address (int): The starting address.

        Returns:
            float: The calculated voltage.
        """
        # Extract the two bytes from values starting from the given address
        registers = self.isl94203_hal.get_registers()
        byte0 = registers[address]
        byte1 = registers[address + 1]

        # Combine bytes into a single 16-bit value (little-endian format)
        combined_value = (byte1 << 8) | byte0

        # Apply mask and multiplier and return the calculated voltage
        return self.apply_mask_and_multiplier(combined_value)

    def calculate_temp_voltage(self, address):
        """
        Calculate voltage based on values and address.

        Args:
            address (int): The starting address.

        Returns:
            float: The calculated voltage.
        """
        registers = self.isl94203_hal.get_registers()
        # Extract the 16-bit value from 'values' starting at 'address'
        raw_value = (registers[address + 1] << 8) | registers[address]

        # Apply mask and multiplier to calculate the voltage
        return self.calculate_temperature_from_raw_value(raw_value)


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
    # Add any test or initialization code here
    config = isl9420x.isl94203_hal.get_default_registers()
    isl9420x.isl94203_hal.set_registers(config)
    isl9420x.update_registers()

    print("Voltage Limits:")
    voltage_limits = isl9420x.read_voltage_limits()
    for limit, value in voltage_limits.items():
        print(f"{limit}: {value}")

    for i in range(1, 9):
        print(getattr(isl9420x, f'vcell{i}'))
