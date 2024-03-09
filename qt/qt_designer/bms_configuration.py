from bms_constants import *

class BMSConfiguration:
    
    def __init__(self):

        #Default from datasheet:      1E2A  0DD4  18FF  09FF  0E7F  0600  0DFF  07AA  0801  0801  0214  44A0  44A0  60C8  0A55  0D70  0010  01AB  0802  0802  0BF2  0A93  04B6  053E  04B6  053E  0BF2  0A93  04B6  053E  0BF2  0A93  067C  0621  06AA  FC0F  83FF       |USER EEPROM  8bytes    |0000  2240  0000  0003  0000  0A8F  0ABE  0015  0A91  0ABE  0000  0000  0000  0000  0A8F  0A92  027B  04D2  04D2  0368  0B09  002A              
        self.configuration_default = "2A,1E,D4,0D,FF,18,FF,09,7F,0E,00,06,FF,0D,AA,07,01,08,01,08,14,02,A0,44,A0,44,C8,60,55,0A,70,0D,10,00,AB,01,02,08,02,08,F2,0B,93,0A,B6,04,3E,05,B6,04,3E,05,F2,0B,93,0A,B6,04,3E,05,F2,0B,93,0A,7C,06,21,06,AA,06,0F,FC,FF,83,00,00,00,00,00,00,00,00,00,00,40,22,00,00,03,00,00,00,8F,0A,BE,0A,15,00,91,0A,BE,0A,00,00,00,00,00,00,00,00,8F,0A,92,0A,7B,02,D2,04,D2,04,68,03,09,0B,2A,00,"

        # Mapping of codes to text values
        self.unit_mapping = {0: "μs", 1: "ms", 2: "s", 3: "min"}
        self.doc_mapping = {0: "4mV", 1: "8mV", 2: "16mV", 3: "24mV", 4: "32mV", 5: "48mV", 6: "64mV", 7: "96mV"}
        self.coc_mapping = {0: "1mV", 1: "2mV", 2: "4mV", 3: "6mV", 4: "8mV", 5: "12mV", 6: "16mV", 7: "24mV"}
        self.dsc_mapping = {0: "16mV", 1: "24mV", 2: "32mV", 3: "48mV", 4: "64mV", 5: "96mV", 6: "128mV", 7: "256mV"}

        # Split the input line by commas and remove spaces
        self.config_values = [val.strip() for val in self.configuration_default.split(',')[:] if val.strip()]
        self.config_values_int = []
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
        return self.configuration_default

    def get_config(self):
        return self.config_values

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
        print( hex(address_index), values[address_index],values[address_index+1] )
        return int(''.join(values[address_index:address_index+2][::-1]), 16)
    
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
        if ( byte_address >= ADDR_RAM_BEGIN):
            real_address = byte_address - ADDR_RAM_BEGIN + ADDR_RAM_OFFSET
        else:
            real_address = byte_address

        byte_value = int(''.join(values[real_address]), 16)
        return bool((byte_value >> bit_position) & MASK_1BIT)

    def update_registers(self,values):
        self.config_values = values
        self.config_values_int = [int(val,16) for val in values]
        print(values)

        # Extract values for the specified fields

        #Voltage Limits
        self.ov =            self.calculate_voltage(values, 0x00)
        self.ov_recover =    self.calculate_voltage(values, 0x02)
        self.under_voltage = self.calculate_voltage(values, 0x04)
        self.uv_recover =    self.calculate_voltage(values, 0x06)
        self.ov_lockout =    self.calculate_voltage(values, 0x08)
        self.uv_lockout =    self.calculate_voltage(values, 0x0A)
        self.eoc_voltage =   self.calculate_voltage(values, 0x0C)
        self.low_voltage_charge = self.calculate_voltage(values, 0x0E)
        self.sleep_voltage = self.calculate_voltage(values, 0x44)

        
        self.ov_delay_timeout =     self.get_reg_val(values, 0x10, 0, MASK_10BIT) 
        self.ov_delay_timeout_unit= self.get_reg_val(values, 0x10, 10,MASK_2BIT)  

        self.uv_delay_timeout =      self.get_reg_val(values, 0x12, 0, MASK_10BIT)
        self.uv_delay_timeout_unit = self.get_reg_val(values, 0x12, 10,MASK_2BIT) 

        self.open_wire_timing =      self.get_reg_val(values, 0x14, 0, MASK_9BIT)
        self.open_wire_timing_unit = self.get_reg_val(values, 0x14, 9, MASK_1BIT)

        self.sleep_delay =           self.get_reg_val(values, 0x46, 0, MASK_9BIT)
        self.sleep_delay_unit =      self.get_reg_val(values, 0x46, 9,MASK_2BIT) 
        
        #Timers
        self.timer_wdt = self.get_reg_val(values, 0x46, 11, MASK_5BIT)
        self.timer_idle_doze = self.get_reg_val(values, 0x48, 0, MASK_4BIT)
        self.timer_sleep = self.get_reg_val(values, 0x48, 0, MASK_8BIT)
        
        #Cell Configutarion
        self.cell_config = self.get_reg_val(values, 0x48, 8, MASK_8BIT)

        #Pack Options
        self.bit_enable_openwire_psd = self.get_boolean_value( values, 0x4A, 0)
        self.bit_enable_openwire_scan = self.get_boolean_value( values, 0x4A, 1)
        #bit2:PCFETE
        #bit3:Reserved
        #bit4:TGAIN
        self.bit_t2_monitors_fet = self.get_boolean_value(values, 0x4A, 5)
        #bit6:Reserved
        self.bit_enable_cellf_psd = self.get_boolean_value(values, 0x4A, 7)


        self.bit_cb_during_eoc =  self.get_boolean_value(values, 0x4B, 0)
        #bit1:Reserved
        #bit2:Reserved
        self.bit_enable_uvlo_pd = self.get_boolean_value(values, 0x4B, 3)
        #bit4:CFET
        #bit5:DFET
        self.bit_cb_during_charge = self.get_boolean_value(values, 0x4B, 6)
        self.bit_cb_during_discharge = self.get_boolean_value(values, 0x4B, 7)
        

        #Cell Balance Limits
        self.cb_lower_lim =  self.calculate_voltage(values, 0x1C)
        self.cb_upper_lim =  self.calculate_voltage(values, 0x1E)
        self.cb_min_delta =  self.calculate_voltage(values, 0x20)
        self.cb_max_delta =  self.calculate_voltage(values, 0x22)

        self.cb_on_time =      self.get_reg_val(values, 0x24, 0,MASK_10BIT)
        self.cb_on_time_unit = self.get_reg_val(values, 0x24, 10,MASK_2BIT)

        self.cb_off_time =      self.get_reg_val(values, 0x26, 0,MASK_10BIT)
        self.cb_off_time_unit = self.get_reg_val(values, 0x26, 10,MASK_2BIT)

        self.cb_under_temp = self.apply_mask_and_multiplier_temp(int(''.join(values[0x28:0x2A][::-1]), 16))
        self.cb_ut_recover = self.apply_mask_and_multiplier_temp(int(''.join(values[0x2A:0x2C][::-1]), 16))  
        self.cb_over_temp =  self.apply_mask_and_multiplier_temp(int(''.join(values[0x2C:0x2E][::-1]), 16)) 
        self.cb_ot_recover = self.apply_mask_and_multiplier_temp(int(''.join(values[0x2E:0x30][::-1]), 16))   
        
        #Current Limits

        self.disch_oc_voltage =       self.get_reg_val(values, 0x16, 12, MASK_3BIT)
        self.disch_oc_timeout =       self.get_reg_val(values, 0x16, 0, MASK_10BIT)
        self.disch_oc_timeout_unit =  self.get_reg_val(values, 0x16, 10, MASK_2BIT)

        self.charge_oc_voltage =      self.get_reg_val(values, 0x18, 12, MASK_3BIT)
        self.charge_oc_timeout =      self.get_reg_val(values, 0x18, 0, MASK_10BIT)
        self.charge_oc_timeout_unit = self.get_reg_val(values, 0x18, 10, MASK_2BIT)

        self.disch_sc_voltage =       self.get_reg_val(values, 0x1A, 12, MASK_3BIT)
        self.disch_sc_timeout =       self.get_reg_val(values, 0x1A, 0, MASK_10BIT)
        self.disch_sc_timeout_unit =  self.get_reg_val(values, 0x1A, 10, MASK_2BIT)   

        #Temperature Limits
        self.tl_charge_over_temp  =  self.calculate_temp_voltage(values, 0x30)
        self.tl_charge_ot_recover =  self.calculate_temp_voltage(values, 0x32)
        self.tl_charge_under_temp =  self.calculate_temp_voltage(values, 0x34)
        self.tl_charge_ut_recover =  self.calculate_temp_voltage(values, 0x36)

        self.tl_disch_over_temp  =   self.calculate_temp_voltage(values, 0x38)
        self.tl_disch_ot_recover =   self.calculate_temp_voltage(values, 0x3A)
        self.tl_disch_under_temp  =  self.calculate_temp_voltage(values, 0x3C)
        self.tl_disch_ut_recover =   self.calculate_temp_voltage(values, 0x3E)

        self.tl_internal_over_temp = self.calculate_temp_voltage(values, 0x40)
        self.tl_internal_ot_recover = self.calculate_temp_voltage(values, 0x42)

        #RAM
        self.i_gain =  self.current_gain_code[self.get_reg_val(values, 0x85, 4,MASK_2BIT)]
        self.v_sense = self.apply_mask_and_multiplier_pack_current(self.get_ram_16bits(0x8E,values),self.i_gain)
        self.vcell1 =  self.apply_mask_and_multiplier(self.get_ram_16bits(0x90,values)) 
        self.vcell2 =  self.apply_mask_and_multiplier(self.get_ram_16bits(0x92,values)) 
        self.vcell3 =  self.apply_mask_and_multiplier(self.get_ram_16bits(0x94,values)) 
        self.vcell4 =  self.apply_mask_and_multiplier(self.get_ram_16bits(0x96,values)) 
        self.vcell5 =  self.apply_mask_and_multiplier(self.get_ram_16bits(0x98,values)) 
        self.vcell6 =  self.apply_mask_and_multiplier(self.get_ram_16bits(0x9A,values)) 
        self.vcell7 =  self.apply_mask_and_multiplier(self.get_ram_16bits(0x9C,values)) 
        self.vcell8 =  self.apply_mask_and_multiplier(self.get_ram_16bits(0x9E,values)) 

        self.vcell_min = self.apply_mask_and_multiplier(self.get_ram_16bits(0x8A,values))
        self.vcell_max = self.apply_mask_and_multiplier(self.get_ram_16bits(0x8C,values))

        self.vbatt = self.apply_mask_and_multiplier_pack(self.get_ram_16bits(0xA6,values))
        self.vrgo =  self.apply_mask_and_multiplier_vrgo(self.get_ram_16bits(0xA8,values))


        #adress 0x80
        self.bit_ov   =   self.get_boolean_value(values, 0x80, 0)
        self.bit_ovlo =   self.get_boolean_value(values, 0x80, 1)
        self.bit_uv   =   self.get_boolean_value(values, 0x80, 2)
        self.bit_uvlo =   self.get_boolean_value(values, 0x80, 3)
        self.bit_dot  =   self.get_boolean_value(values, 0x80, 4)
        self.bit_dut  =   self.get_boolean_value(values, 0x80, 5)
        self.bit_cot  =   self.get_boolean_value(values, 0x80, 6)
        self.bit_cut  =   self.get_boolean_value(values, 0x80, 7)

        #adress 0x81
        self.bit_iot   =   self.get_boolean_value(values, 0x81, 0)
        self.bit_coc   =   self.get_boolean_value(values, 0x81, 1)
        self.bit_doc   =   self.get_boolean_value(values, 0x81, 2)
        self.bit_dsc   =   self.get_boolean_value(values, 0x81, 3)
        self.bit_cellf =   self.get_boolean_value(values, 0x81, 4)
        self.bit_open  =   self.get_boolean_value(values, 0x81, 5)
        self.bit_eochg =   self.get_boolean_value(values, 0x81, 7)

        #adress 0x82
        self.bit_ld_prsnt = self.get_boolean_value(values, 0x82, 0)
        self.bit_ch_prsnt = self.get_boolean_value(values, 0x82, 1)
        self.bit_ching =    self.get_boolean_value(values, 0x82, 2)
        self.bit_dching =   self.get_boolean_value(values, 0x82, 3)
        self.bit_ecc_used = self.get_boolean_value(values, 0x82, 4)
        self.bit_ecc_fail = self.get_boolean_value(values, 0x82, 5)
        self.bit_int_scan = self.get_boolean_value(values, 0x82, 6)
        self.bit_lvchg =    self.get_boolean_value(values, 0x82, 7)
        
        #adress 0x83
        self.bit_cbot =     self.get_boolean_value(values, 0x83, 0)
        self.bit_cbut =     self.get_boolean_value(values, 0x83, 1)
        self.bit_cbov =     self.get_boolean_value(values, 0x83, 2)
        self.bit_cbuv =     self.get_boolean_value(values, 0x83, 3)
        self.bit_in_idle =  self.get_boolean_value(values, 0x83, 4)
        self.bit_in_doze =  self.get_boolean_value(values, 0x83, 5)
        self.bit_in_sleep = self.get_boolean_value(values, 0x83, 6)





    def read_from_values(self, values):
        # Assuming the input format is a comma-separated string
        # Split the input line by commas and remove spaces
        values = [val.strip() for val in values.split(',') if val.strip()]

        #convert to int
        self.config_values_int = [int(val) for val in values]

        
    # Assuming the values get 16bits, therefore, operations are over two consecutives addresses 
    # example:

    def reg_write( self, address, value , mask, shift):

        byte0 = int(self.config_values_int[address])
        byte1 = int(self.config_values_int[address+1] ) 
        
        tmp = (byte1 << 8)|  byte0

        tmp = (tmp << shift) & ~mask
        tmp = tmp | (value << shift)

        self.config_values_int[address] = tmp & 0xff
        self.config_values_int[address + 1] = (tmp>> 8 ) & 0xff

        self.config_values = [hex(val)[2:].zfill(2).upper() for val in self.config_values_int]

    def write_to_values(self):

        return 0

    def calculate_voltage(self, values, address):
        """
        Calculate voltage based on values and address.

        Parameters:
        - values (list): The list of values from which to extract the voltage.
        - address (int): The starting address.

        Returns:
        - float: The calculated voltage.
        """
        return self.apply_mask_and_multiplier(int(''.join(values[address:address+2][::-1]), 16))

    def calculate_temp_voltage(self, values, address):
        """
        Calculate voltage based on values and address.

        Parameters:
        - values (list): The list of values from which to extract the voltage.
        - address (int): The starting address.

        Returns:
        - float: The calculated voltage.
        """
        return self.apply_mask_and_multiplier_temp(int(''.join(values[address:address+2][::-1]), 16))
       
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
        if ( start_address >= ADDR_RAM_BEGIN):
            start_address = start_address - ADDR_RAM_BEGIN + ADDR_RAM_OFFSET

        raw_value = int(''.join(values[start_address:start_address+2][::-1]), 16)
        value = (raw_value >> bit_shift) & bit_mask
        return value