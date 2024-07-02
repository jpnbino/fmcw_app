from bms.constants import *
import logging

class BMSConfiguration:
    
    def __init__(self):
        # Mapping of codes to text values
        self.unit_mapping = {0: "μs", 1: "ms", 2: "s", 3: "min"}
        self.doc_mapping = {0: "4mV", 1: "8mV", 2: "16mV", 3: "24mV", 4: "32mV", 5: "48mV", 6: "64mV", 7: "96mV"}
        self.coc_mapping = {0: "1mV", 1: "2mV", 2: "4mV", 3: "6mV", 4: "8mV", 5: "12mV", 6: "16mV", 7: "24mV"}
        self.dsc_mapping = {0: "16mV", 1: "24mV", 2: "32mV", 3: "48mV", 4: "64mV", 5: "96mV", 6: "128mV", 7: "256mV"}

        # Split the input line by commas and remove spaces
        self.config_values_int = []
        self.ov = 0.0
        self.ov_lockout = 0.0
        self.ov_recover = 0.0
        self.eoc_voltage = 0.0
        self.uv_recover = 0.0
        self.under_voltage = 0.0
        self.sleep_voltage = 0.0
        self.low_voltage_charge = 0.0
        self.uv_lockout = 0.0

        #in milliseconds
        self.charge_detect_pulse_width = 0
        self.load_detect_pulse_width = 0

        self.ov_delay_timeout = 0          
        self.uv_delay_timeout = 0      
        self.open_wire_timing = 0
        self.sleep_delay = 0
        
        self.ov_delay_timeout_unit = 0
        self.uv_delay_timeout_unit = 0
        self.open_wire_timing_unit = 0
        self.sleep_delay_unit = 0

        #Timers 
        self.timer_idle_doze = 0
        self.timer_sleep = 0
        self.timer_wdt = 0
        
        #Cell Configuration
        # Create a dictionary mapping binary patterns to connected cell counts
        self.cell_config_code = {
            0b10000011: 3,
            0b11000011: 4,
            0b11000111: 5,
            0b11100111: 6,
            0b11110111: 7,
            0b11111111: 8
            }
        self.cell_config = 0

        #Cell Balance Limits
        self.cb_upper_lim = 0 
        self.cb_lower_lim = 0 
        self.cb_max_delta = 0 
        self.cb_min_delta = 0 
        self.cb_over_temp = 0 
        self.cb_ot_recover = 0 
        self.cb_ut_recover = 0 
        self.cb_under_temp = 0 
        self.cb_on_time = 0 
        self.cb_off_time = 0 
        
        self.cb_on_time_unit = 0 
        self.cb_off_time_unit = 0 

        self.bit_cb_during_charge = False
        self.bit_cb_during_discharge = False
        self.bit_cb_during_eoc = False

        #Temperature Limits
        self.tl_charge_over_temp = 0
        self.tl_charge_ot_recover = 0
        self.tl_charge_ut_recover = 0
        self.tl_charge_under_temp = 0

        self.tl_disch_over_temp = 0
        self.tl_disch_ot_recover = 0
        self.tl_disch_ut_recover = 0
        self.tl_disch_under_temp = 0

        self.tl_internal_over_temp = 0
        self.tl_internal_ot_recover = 0

        #Pack Options
        self.bit_t2_monitors_fet = False
        self.bit_enable_cellf_psd = False
        self.bit_enable_openwire_psd = False
        self.bit_enable_uvlo_pd = False
        self.bit_enable_openwire_scan = False

        #Temperature gain
        self.bit_tgain = False
        
        #Current Limits
        self.disch_oc_voltage = 0
        self.disch_oc_timeout = 0
        self.disch_oc_timeout_unit = 0
        self.charge_oc_voltage = 0
        self.charge_oc_timeout = 0
        self.charge_oc_timeout_unit = 0
        self.disch_sc_voltage = 0
        self.disch_sc_timeout = 0
        self.disch_sc_timeout_unit = 0

        #Ram
        #adress 0x80
        self.bit_ov = False
        self.bit_ovlo = False
        self.bit_uv = False
        self.bit_uvlo = False
        self.bit_dot = False
        self.bit_dut = False
        self.bit_cot = False
        self.bit_cut = False

        #adress 0x81
        self.bit_iot = False
        self.bit_coc = False
        self.bit_doc = False
        self.bit_dsc = False
        self.bit_cellf = False
        self.bit_open = False
        self.bit_eochg = False

        #adress 0x82
        self.bit_ld_prsnt = False
        self.bit_ch_prsnt = False
        self.bit_ching = False
        self.bit_dching = False
        self.bit_ecc_used = False
        self.bit_ecc_fail = False
        self.bit_int_scan = False
        self.bit_lvchg = False
        
        #adress 0x83
        self.bit_cbot = False
        self.bit_cbut = False
        self.bit_cbov = False
        self.bit_cbuv = False
        self.bit_in_idle = False
        self.bit_in_doze = False
        self.bit_in_sleep = False

        #Current calculation
        #Create a dictionary mapping binary patterns current gains
        self.current_gain_code = {
            0b00: 50,
            0b01: 5,
            0b10: 500,
            0b11: 500
            }
        
        self.v_sense = 0.0 #voltage over Sense Resistor
        self.i_pack = 0.0 #current over Sense Resistor (Pack current)
        self.i_gain = 0

        #Temperature
        self.temp_internal = 0.0
        self.temp_xt1 = 0.0
        self.temp_xt2 = 0.0

        #Cell voltages
        self.vcell1 = 0
        self.vcell2 = 0
        self.vcell3 = 0
        self.vcell4 = 0
        self.vcell5 = 0
        self.vcell6 = 0
        self.vcell7 = 0
        self.vcell8 = 0
        self.vcell_min = 0
        self.vcell_max = 0
        self.vbatt = 0
        self.vrgo = 0        

    def get_default_config(self):
        return DEFAULT_CONFIG

    def get_config(self):
        return self.config_values_int

    def update_registers(self,values):
        self.config_values_int = values
        logging.info(f"Updating registers with values: {values}")

        try:
            self.update_voltage_limits(values)
            self.update_timing(values)
            self.cell_configuration(values)
            self.update_pack_options(values)
            self.update_cell_balance(values)
            self.update_current_limits(values)
            self.update_temperature_limits(values)
            self.update_ram_values(values)
            self.update_feature_controls(values)
        except Exception as e:
            print(f"Error updating configuration: {e}")

        
    def update_voltage_limits(self, values):
        #Voltage Limits
        voltage_mappping = {
            0x00: 'ov',
            0x02: 'ov_recover',
            0x04: 'under_voltage',
            0x06: 'uv_recover',
            0x08: 'ov_lockout',
            0x0A: 'uv_lockout',
            0x0C: 'eoc_voltage',
            0x0E: 'low_voltage_charge',
            0x44: 'sleep_voltage'
        }
        for addr, attr in voltage_mappping.items():
            try:
                value = self.calculate_voltage(values, addr)
                setattr(self, attr, value)
            except Exception as e:
                print(f"Error updating voltage limits: {e}")
            
    def update_timing(self, values):
        '''Update the timing attributes based on the given values.
        Parameters:
        - values (list): The list of values from which to extract the timing attributes.
        '''
        timing_mapping = {
            (0x10,0, MASK_10BIT): 'ov_delay_timeout',
            (0x10,10,MASK_2BIT): 'ov_delay_timeout_unit',
            (0x12,0, MASK_10BIT): 'uv_delay_timeout',
            (0x12,10,MASK_2BIT): 'uv_delay_timeout_unit',
            (0x14,0, MASK_9BIT): 'open_wire_timing',
            (0x14,9, MASK_1BIT): 'open_wire_timing_unit',
            (0x46,0, MASK_9BIT): 'sleep_delay',
            (0x46,9, MASK_2BIT): 'sleep_delay_unit',
            (0x46,11, MASK_5BIT): 'timer_wdt',
            (0x48,0, MASK_4BIT): 'timer_idle_doze',
            (0x48,4, MASK_8BIT): 'timer_sleep',
            (0x48,8, MASK_8BIT): 'cell_config'
         }
        for (addr, bit_shift, bit_mask),attr in timing_mapping.items():
            try:
                value = self.get_reg_val(values, addr, bit_shift, bit_mask)
                setattr(self,attr, value)
            except Exception as e:
                print(f"Error updating timing: {e}")

    def cell_configuration(self, values):    
        #Cell Configuration
        self.cell_config = self.get_reg_val(values, 0x48, 8, MASK_8BIT)

    def update_pack_options(self, values):
        '''Update the pack options( Addresses 0x4A and 0x4B) attributes based on the given values.
        Parameters:
        - values (list): The list of values from which to extract the pack options attributes.
        '''
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
                setattr(self, attr, self.get_boolean_value(values, addr, bit_pos))
            except Exception as e:
                print(f"Error updating pack options: {e}")
        
    def update_cell_balance(self, values):
        '''Update the cell balance attributes based on the given values.
        Parameters:
        - values (list): The list of values from which to extract the cell balance attributes.
        '''    
        cell_balance_mapping = {
            0x1C: 'cb_lower_lim',
            0x1E: 'cb_upper_lim',
            0x20: 'cb_min_delta',
            0x22: 'cb_max_delta'
        }

        for addr, attr in cell_balance_mapping.items():
            try:
                setattr(self, attr, self.calculate_voltage(values, addr))
            except Exception as e:
                print(f"Error updating cell balance: {e}")

        cell_balance_timing_mapping = {
            (0x24, 0, MASK_10BIT): 'cb_on_time',
            (0x24, 10, MASK_2BIT): 'cb_on_time_unit',
            (0x26, 0, MASK_10BIT): 'cb_off_time',
            (0x26, 10, MASK_2BIT): 'cb_off_time_unit'
        }

        for (addr, bit_shift, bit_mask), attr in cell_balance_timing_mapping.items():
            try:
                value = self.get_reg_val(values, addr, bit_shift, bit_mask)
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
                value = self.apply_mask_and_multiplier_temp((values[high_byte] << 8) | values[low_byte])               
                setattr(self, attr, value)
            except Exception as e:
                print(f"Error updating cell balance temperature: {e}")
    
    def update_current_limits(self, values):
        '''Update the current limit attributes based on the given values.
        Parameters:
        - values (list): The list of values from which to extract the current limit attributes.
        '''     
        current_limits_mapping = {
            (0x16, 12, MASK_3BIT): 'disch_oc_voltage',
            (0x16, 0, MASK_10BIT): 'disch_oc_timeout',
            (0x16, 10, MASK_2BIT): 'disch_oc_timeout_unit',
            (0x18, 12, MASK_3BIT): 'charge_oc_voltage',
            (0x18, 0, MASK_10BIT): 'charge_oc_timeout',
            (0x18, 10, MASK_2BIT): 'charge_oc_timeout_unit',
            (0x1A, 12, MASK_3BIT): 'disch_sc_voltage',
            (0x1A, 0, MASK_10BIT): 'disch_sc_timeout',
            (0x1A, 10, MASK_2BIT): 'disch_sc_timeout_unit'
        }

        for (addr, bit_shift, bit_mask), attr in current_limits_mapping.items():
            try:
                value = self.get_reg_val(values, addr, bit_shift, bit_mask)
                setattr(self, attr, value)
            except Exception as e:
                print(f"Error updating current limits: {e}")

    def update_temperature_limits(self, values):
        """ Update the temperature limit attributes based on the given values.
        Parameters:
        - values (list): The list of values from which to extract the temperature limit attributes.
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
                setattr(self, attr, self.calculate_temp_voltage(values, addr))
            except Exception as e:
                print(f"Error updating temperature limits: {e}")

    def update_ram_values(self, values):
        """ Update the RAM attributes based on the given values.
        Parameters:
        - values (list): The list of values from which to extract the RAM attributes.
        """
        self.i_gain = self.current_gain_code[self.get_reg_val(values, 0x85, 4, MASK_2BIT)]
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
                if 'temp' in attr:
                    value = self.apply_mask_and_multiplier_temp(self.get_ram_16bits(addr, values))
                elif 'vcell' in attr:
                    value = self.apply_mask_and_multiplier(self.get_ram_16bits(addr, values))
                elif attr == 'v_sense':
                    value = self.apply_mask_and_multiplier_pack_current(self.get_ram_16bits(addr, values), self.i_gain)
                elif attr == 'vbatt':
                    value =  self.apply_mask_and_multiplier_pack(self.get_ram_16bits(addr, values))
                elif attr == 'vrgo':
                    value= self.apply_mask_and_multiplier_vrgo(self.get_ram_16bits(addr, values))

                setattr(self, attr, value)
            except Exception as e:
                print(f"Error updating RAM values: {e}")


    def update_feature_controls(self, values):
        """ Update the feature control attributes based on the given values.    
        Parameters:
        - values (list): The list of values from which to extract the feature control attributes.
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
                value = self.get_boolean_value(values, address, bit_position)
                setattr(self, attr_name, value)
            except Exception as e:
                print(f"Error updating feature controls: {e}")


    # Assuming the values get 16bits, therefore, operations are over two consecutives addresses 
    # example:

    def reg_write( self, address, value , mask, shift):
        """
        Write a value to a register based on the specified address, mask, and shift.

        Parameters:
        - address (int): The address of the register.
        - value (int): The value to write to the register.
        - mask (int): The mask to apply to the value.
        - shift (int): The shift to apply to the value.

        Returns:
        - int: The new value of the register.
        """
        byte0 = int(self.config_values_int[address])
        byte1 = int(self.config_values_int[address+1] ) 
        
        tmp = (byte1 << 8)|  byte0

        tmp = (tmp << shift) & ~mask
        tmp = tmp | (value << shift)

        self.config_values_int[address] = tmp & 0xff
        self.config_values_int[address + 1] = (tmp>> 8 ) & 0xff

    def calculate_voltage(self, values, address):
        """
        Calculate voltage based on values and address.

        Parameters:
        - values (list): The list of values from which to extract the voltage.
        - address (int): The starting address.

        Returns:
        - float: The calculated voltage.
        """
        # Extract the two bytes from values starting from the given address
        byte0 = values[address]
        byte1 = values[address + 1]

        # Combine bytes into a single 16-bit value (little-endian format)
        combined_value = (byte1 << 8) | byte0

        # Apply mask and multiplier and return the calculated voltage
        return self.apply_mask_and_multiplier(combined_value)

    def calculate_temp_voltage(self, values, address):
        """
        Calculate voltage based on values and address.

        Parameters:
        - values (list): The list of values from which to extract the voltage.
        - address (int): The starting address.

        Returns:
        - float: The calculated voltage.
        """
        # Extract the 16-bit value from 'values' starting at 'address'
        raw_value = (values[address + 1] << 8) | values[address]

        # Apply mask and multiplier to calculate the voltage
        return self.apply_mask_and_multiplier_temp(raw_value)

    def get_reg_val(self, values, start_address, bit_shift, bit_mask):
        """
        Extract a value from 'values' based on the specified parameters.

        Parameters:
        - values (list): The list of values from which to extract the value.
        - start_address (int): The starting address.
        - bit_shift (int): The bit shift for the value.
        - bit_mask (int): The bitmask for the value.

        Returns:
        - int: The extracted value.
        """
        if start_address >= ADDR_RAM_BEGIN:
            start_address = start_address - ADDR_RAM_BEGIN + ADDR_RAM_OFFSET

        # Assuming start_address points to the index in values directly
        raw_value = (values[start_address + 1] << 8) | values[start_address]
        value = (raw_value >> bit_shift) & bit_mask
        return value
          
    def apply_mask_and_multiplier(self, value):
        # Apply masking
        masked_value = value & MASK_12BIT
        # Apply multiplier
        result = masked_value * VOLTAGE_CELL_MULTIPLIER
        return result

    def apply_mask_and_multiplier_pack_current(self, value, gain):
        # Apply masking
        masked_value = value & MASK_12BIT
        # Apply multiplier
        result = masked_value * CURRENT_CELL_MULTIPLIER / (gain)
        return result

    def apply_mask_and_multiplier_pack(self, value):
        # Apply masking
        masked_value = value & MASK_12BIT
        # Apply multiplier
        result = masked_value * VOLTAGE_PACK_MULTIPLIER
        return result

    def apply_mask_and_multiplier_vrgo(self, value):
        # Apply masking
        masked_value = value & MASK_12BIT
        # Apply multiplier
        result = masked_value * VOLTAGE_VRGO_MULTIPLIER
        return result
    
    def apply_mask_and_multiplier_temp(self, value):
        # Apply masking
        masked_value = value & MASK_12BIT
        # Apply multiplier
        result = masked_value * TEMPERATURE_MULTIPLIER
        return result
    
    def get_ram_16bits(self, address, values):
        """
        Extracts a 16-bit value from 'values' starting at the specified 'address'.

        Parameters:
        - address (int): The starting address.
        - values (list): The list of values from which to extract the 16 bits.

        Returns:
        - int: The 16-bit integer value.
        """
        address_index = address - ADDR_RAM_BEGIN + ADDR_RAM_OFFSET
        # Extract the 16-bit value from 'values' starting at 'address_index'
        # Assuming little-endian byte order (LSB first)
        raw_value = (values[address_index + 1] << 8) | values[address_index]
        return raw_value
    

    def get_boolean_value(self, values, byte_address, bit_position):
        """
        Extracts a boolean value from 'values' based on the specified byte address and bit position.

        Parameters:
        - values (list): The list of values from which to extract the boolean value.
        - byte_address (int): The byte address.
        - bit_position (int): The bit position within the byte.

        Returns:
        - bool: The boolean value.
        """
        if byte_address >= ADDR_RAM_BEGIN:
            real_address = byte_address - ADDR_RAM_BEGIN + ADDR_RAM_OFFSET
        else:
            real_address = byte_address

        # Extract the byte value from values
        byte_value = values[real_address]

        # Calculate the boolean value based on the bit position
        return bool((byte_value >> bit_position) & 0x01)