from bms_constants import *

class BMSConfiguration:
    
    def __init__(self):

        #Default from datasheet:      1E2A  0DD4  18FF  09FF  0E7F  0600  0DFF  07AA  0801  0801  0214  44A0  44A0  60C8  0A55  0D70  0010  01AB  0802  0802  0BF2  0A93  04B6  053E  04B6  053E  0BF2  0A93  04B6  053E  0BF2  0A93  067C  0621  06AA  FC0F  83FF       |USER EEPROM  8bytes    |0000  2240  0000  0003  0000  0A8F  0ABE  0015  0A91  0ABE  0000  0000  0000  0000  0A8F  0A92  027B  04D2  04D2  0368  0B09  002A              
        self.configuration_default = "2A,1E,D4,0D,FF,18,FF,09,7F,0E,00,06,FF,0D,AA,07,01,08,01,08,14,02,A0,44,A0,44,C8,60,55,0A,70,0D,10,00,AB,01,02,08,02,08,F2,0B,93,0A,B6,04,3E,05,B6,04,3E,05,F2,0B,93,0A,B6,04,3E,05,F2,0B,93,0A,7C,06,21,06,AA,06,0F,FC,FF,83,00,00,00,00,00,00,00,00,00,00,40,22,00,00,03,00,00,00,8F,0A,BE,0A,15,00,91,0A,BE,0A,00,00,00,00,00,00,00,00,8F,0A,92,0A,7B,02,D2,04,D2,04,68,03,09,0B,2A,00,"

        # Mapping of codes to text values
        self.unit_mapping = {00: "μs", 1: "ms", 2: "s", 3: "min"}

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




    def get_default_config(self):
        return self.configuration_default

    def get_config(self):
        return self.config_values
    
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

        #Timers
        self.ov_delay_timeout =     ((int(''.join(values[0x10:0x12][::-1]), 16)) >> 0)  & MASK_10BIT
        self.ov_delay_timeout_unit= ((int(''.join(values[0x10:0x12][::-1]), 16)) >> 10)  & MASK_2BIT

        self.uv_delay_timeout =     ((int(''.join(values[0x12:0x14][::-1]), 16)) >> 0)  & MASK_10BIT
        self.uv_delay_timeout_unit = ((int(''.join(values[0x12:0x14][::-1]), 16)) >> 10)  & MASK_2BIT

        self.open_wire_timing =     ((int(''.join(values[0x14:0x16][::-1]), 16)) >> 0)  & 0x01ff
        self.open_wire_timing_unit = ((int(''.join(values[0x14:0x16][::-1]), 16)) >> 9)  & MASK_1BIT

        self.sleep_delay =          ((int(''.join(values[0x46:0x48][::-1]), 16)) >> 0)  & 0x01ff
        self.sleep_delay_unit =     ((int(''.join(values[0x46:0x48][::-1]), 16)) >> 9)  & MASK_2BIT
        
        self.timer_wdt = ((int(''.join(values[0x46:0x48][::-1]), 16)) >> 11)  & 0x001f
        self.timer_idle_doze = ((int(''.join(values[0x48:0x4A][::-1]), 16)) >> 0)  & 0x000f
        self.timer_sleep = ((int(''.join(values[0x48:0x4A][::-1]), 16)) >> 0)  & 0x00ff
        
        #Cell Configutarion
        self.cell_config = ((int(''.join(values[0x48:0x4A][::-1]), 16)) >> 8)  & 0x00ff

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
    
    def apply_mask_and_multiplier_temp(self, value):
        # Apply masking
        masked_value = value & MASK_12BIT
        # Apply multiplier
        result = masked_value * TEMPERATURE_MULTIPLIER
        return result