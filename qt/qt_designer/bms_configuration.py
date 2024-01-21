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
    
    def update_registers(self,values):
        self.config_values = values
        self.config_values_int = [int(val,16) for val in values]
        print(values)

        # Extract values for the specified fields

        #Voltage Limits
        self.ov =            self.apply_mask_and_multiplier(int(''.join(values[0:2][::-1]), 16))
        self.ov_recover =    self.apply_mask_and_multiplier(int(''.join(values[2:4][::-1]), 16))
        self.under_voltage = self.apply_mask_and_multiplier(int(''.join(values[4:6][::-1]), 16))
        self.uv_recover =    self.apply_mask_and_multiplier(int(''.join(values[6:8][::-1]), 16))
        self.ov_lockout =    self.apply_mask_and_multiplier(int(''.join(values[8:10][::-1]), 16))
        self.uv_lockout =    self.apply_mask_and_multiplier(int(''.join(values[10:12][::-1]), 16))
        self.eoc_voltage =    self.apply_mask_and_multiplier(int(''.join(values[12:14][::-1]), 16))
        self.low_voltage_charge = self.apply_mask_and_multiplier(int(''.join(values[14:16][::-1]), 16))
        self.sleep_voltage = self.apply_mask_and_multiplier(int(''.join(values[68:70][::-1]), 16))

        
        self.ov_delay_timeout =     ((int(''.join(values[0x10:0x12][::-1]), 16)) >> 0)  & MASK_10BIT
        self.ov_delay_timeout_unit= ((int(''.join(values[0x10:0x12][::-1]), 16)) >> 10)  & MASK_2BIT

        self.uv_delay_timeout =     ((int(''.join(values[0x12:0x14][::-1]), 16)) >> 0)  & MASK_10BIT
        self.uv_delay_timeout_unit = ((int(''.join(values[0x12:0x14][::-1]), 16)) >> 10)  & MASK_2BIT

        self.open_wire_timing =     ((int(''.join(values[0x14:0x16][::-1]), 16)) >> 0)  & 0x01ff
        self.open_wire_timing_unit = ((int(''.join(values[0x14:0x16][::-1]), 16)) >> 9)  & MASK_1BIT

        self.sleep_delay =          ((int(''.join(values[0x46:0x48][::-1]), 16)) >> 0)  & 0x01ff
        self.sleep_delay_unit =     ((int(''.join(values[0x46:0x48][::-1]), 16)) >> 9)  & MASK_2BIT
        
        #Timers
        self.timer_wdt = ((int(''.join(values[0x46:0x48][::-1]), 16)) >> 11)  & 0x001f
        self.timer_idle_doze = ((int(''.join(values[0x48:0x4A][::-1]), 16)) >> 0)  & 0x000f
        self.timer_sleep = ((int(''.join(values[0x48:0x4A][::-1]), 16)) >> 0)  & 0x00ff
        
        #Cell Configutarion
        self.cell_config = ((int(''.join(values[0x48:0x4A][::-1]), 16)) >> 8)  & 0x00ff

        #Pack Options

        
        self.bit_enable_openwire_psd = bool(((int(''.join(values[0x4A]), 16)) >> 0) & MASK_1BIT)
        self.bit_enable_openwire_scan = bool(((int(''.join(values[0x4A]), 16)) >> 1) & MASK_1BIT)
        #bit2:PCFETE
        #bit3:Reserved
        #bit4:TGAIN
        self.bit_t2_monitors_fet =  bool(((int(''.join(values[0x4A]), 16)) >> 5) & MASK_1BIT)
        #bit6:Reserved
        self.bit_enable_cellf_psd = bool(((int(''.join(values[0x4A]), 16)) >> 7) & MASK_1BIT)


        self.bit_cb_during_eoc =  bool(((int(''.join(values[0x4B]), 16)) >> 0) & MASK_1BIT)   
        #bit1:Reserved
        #bit2:Reserved
        self.bit_enable_uvlo_pd = bool(((int(''.join(values[0x4B]), 16)) >> 3) & MASK_1BIT) 
        #bit4:CFET
        #bit5:DFET
        self.bit_cb_during_charge = bool(((int(''.join(values[0x4B]), 16)) >> 6) & MASK_1BIT)
        self.bit_cb_during_discharge = bool(((int(''.join(values[0x4B]), 16)) >> 7) & MASK_1BIT)
        

        #Cell Balance Limits
        self.cb_lower_lim =  self.apply_mask_and_multiplier(int(''.join(values[0x1C:0x1E][::-1]), 16))
        self.cb_upper_lim =  self.apply_mask_and_multiplier(int(''.join(values[0x1E:0x20][::-1]), 16)) 
        self.cb_min_delta =  self.apply_mask_and_multiplier(int(''.join(values[0x20:0x22][::-1]), 16)) 
        self.cb_max_delta =  self.apply_mask_and_multiplier(int(''.join(values[0x22:0x24][::-1]), 16)) 

        self.cb_on_time =    ((int(''.join(values[0x24:0x26][::-1]), 16))>> 0)  & MASK_10BIT
        self.cb_on_time_unit = ((int(''.join(values[0x24:0x26][::-1]), 16))>> 10) & MASK_2BIT 

        self.cb_off_time =   ((int(''.join(values[0x26:0x28][::-1]), 16))>> 0) & MASK_10BIT         
        self.cb_off_time_unit = ((int(''.join(values[0x26:0x28][::-1]), 16))>> 10)  & MASK_2BIT

        self.cb_under_temp = self.apply_mask_and_multiplier_temp(int(''.join(values[0x28:0x2A][::-1]), 16))
        self.cb_ut_recover = self.apply_mask_and_multiplier_temp(int(''.join(values[0x2A:0x2C][::-1]), 16))  
        self.cb_over_temp =  self.apply_mask_and_multiplier_temp(int(''.join(values[0x2C:0x2E][::-1]), 16)) 
        self.cb_ot_recover = self.apply_mask_and_multiplier_temp(int(''.join(values[0x2E:0x30][::-1]), 16))   
        
        #Current Limits
        self.disch_oc_voltage = ((int(''.join(values[0x16:0x18][::-1]), 16)) >> 12)  & MASK_3BIT
        self.disch_oc_timeout = ((int(''.join(values[0x16:0x18][::-1]), 16)) >> 0)  & MASK_10BIT
        self.disch_oc_timeout_unit = ((int(''.join(values[0x16:0x18][::-1]), 16)) >> 10)  & MASK_2BIT
        
        self.charge_oc_voltage = ((int(''.join(values[0x16:0x18][::-1]), 16)) >> 12)  & MASK_3BIT
        self.charge_oc_timeout = ((int(''.join(values[0x18:0x1A][::-1]), 16)) >> 0)  & MASK_10BIT
        self.charge_oc_timeout_unit = ((int(''.join(values[0x18:0x1A][::-1]), 16)) >> 10)  & MASK_2BIT

        self.disch_sc_voltage = ((int(''.join(values[0x1A:0x1C][::-1]), 16)) >> 12)  & MASK_3BIT
        self.disch_sc_timeout =   ((int(''.join(values[0x1A:0x1C][::-1]), 16)) >> 0)  & MASK_10BIT
        self.disch_sc_timeout_unit = ((int(''.join(values[0x1A:0x1C][::-1]), 16)) >> 10)  & MASK_2BIT      

        #Temperature Limits
        self.tl_charge_over_temp  =  self.apply_mask_and_multiplier_temp(int(''.join(values[0x30:0x32][::-1]), 16))
        self.tl_charge_ot_recover =  self.apply_mask_and_multiplier_temp(int(''.join(values[0x32:0x34][::-1]), 16))
        self.tl_charge_under_temp =  self.apply_mask_and_multiplier_temp(int(''.join(values[0x34:0x36][::-1]), 16)) 
        self.tl_charge_ut_recover =  self.apply_mask_and_multiplier_temp(int(''.join(values[0x36:0x38][::-1]), 16)) 

        self.tl_disch_over_temp  =   self.apply_mask_and_multiplier_temp(int(''.join(values[0x38:0x3A][::-1]), 16))
        self.tl_disch_ot_recover =   self.apply_mask_and_multiplier_temp(int(''.join(values[0x3A:0x3C][::-1]), 16))
        self.tl_disch_under_temp  =  self.apply_mask_and_multiplier_temp(int(''.join(values[0x3C:0x3E][::-1]), 16))
        self.tl_disch_ut_recover =   self.apply_mask_and_multiplier_temp(int(''.join(values[0x3E:0x40][::-1]), 16))

        self.tl_internal_over_temp = self.apply_mask_and_multiplier_temp(int(''.join(values[0x40:0x42][::-1]), 16))
        self.tl_internal_ot_recover = self.apply_mask_and_multiplier_temp(int(''.join(values[0x42:0x44][::-1]), 16))

        #RAM
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
    
    def apply_mask_and_multiplier(self, value):
        # Apply masking
        masked_value = value & MASK_12BIT
        # Apply multiplier
        result = masked_value * VOLTAGE_CELL_MULTIPLIER
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