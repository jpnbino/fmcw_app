MASK_1BIT = 0x0001
MASK_2BIT = 0x0003
MASK_3BIT = 0x0007
MASK_4BIT = 0x000F
MASK_5BIT = 0x001F
MASK_8BIT = 0x00FF
MASK_9BIT = 0x01FF
MASK_10BIT = 0x03FF
MASK_11BIT = 0x07FF
MASK_12BIT = 0x0FFF
MASK_15BIT = 0x7FFF

VOLTAGE_CELL_MULTIPLIER = (1.8 * 8.0) / (4095.0 * 3.0) # 0,0011721611721612
VOLTAGE_PACK_MULTIPLIER = (1.8 * 32.0) / (4095.0)
VOLTAGE_VRGO_MULTIPLIER = (1.8 * 2.0) / (4095.0) 
CURRENT_CELL_MULTIPLIER = (1.8) / (4095.0)
TEMPERATURE_MULTIPLIER =  (1.8) / (4095.0)


ADDR_EEPROM_BEGIN = 0x00
ADDR_EEPROM_END = 0x4B

ADDR_RESERVED_EEPROM_BEGIN = 0x4C
ADDR_RESERVED_EEPROM_END = 0x4F

ADDR_USER_EEPROM_BEGIN = 0x50
ADDR_USER_EEPROM_END = 0x57

ADDR_RAM_BEGIN = 0x80
ADDR_RAM_END = 0xAB

#This constants allow api user to get_ram_16bits(0x80) as the array is in different index
#0x80 starts the RAM address of the ISL94203
#0x57 is the last address of reserved area
ADDR_RAM_OFFSET = ADDR_EEPROM_END + (ADDR_USER_EEPROM_END - ADDR_USER_EEPROM_BEGIN)


#Default from datasheet:      
# 1E2A  0DD4  18FF  09FF  0E7F 
# 0600  0DFF  07AA  0801  0801 
# 0214  44A0  44A0  60C8  0A55
# 0D70  0010  01AB  0802  0802
# 0BF2  0A93  04B6  053E  04B6 
# 053E  0BF2  0A93  04B6  053E 
# 0BF2  0A93  067C  0621  06AA 
# FC0F  83FF  
# |USER EEPROM  8bytes    |
# 0000  2240  0000  0003  0000
# 0A8F  0ABE  0015  0A91  0ABE 
# 0000  0000  0000  0000  0A8F
# 0A92  027B  04D2  04D2  0368
# 0B09  002A              
#self.configuration_default = "2A,1E,D4,0D,FF,18,FF,09,7F,0E,00,06,FF,0D,AA,07,01,08,01,08,14,02,A0,44,A0,44,C8,60,55,0A,70,0D,10,00,AB,01,02,08,02,08,F2,0B,93,0A,B6,04,3E,05,B6,04,3E,05,F2,0B,93,0A,B6,04,3E,05,F2,0B,93,0A,7C,06,21,06,AA,06,0F,FC,FF,83,00,00,00,00,00,00,00,00,00,00,40,22,00,00,03,00,00,00,8F,0A,BE,0A,15,00,91,0A,BE,0A,00,00,00,00,00,00,00,00,8F,0A,92,0A,7B,02,D2,04,D2,04,68,03,09,0B,2A,00,"
DEFAULT_CONFIG = [
    0x2A, 0x1E, 0xD4, 0x0D, 0xFF, 0x18, 0xFF, 0x09, 0x7F, 0x0E,
    0x00, 0x06, 0xFF, 0x0D, 0xAA, 0x07, 0x01, 0x08, 0x01, 0x08, 
    0x14, 0x02, 0xA0, 0x44, 0xA0, 0x44, 0xC8, 0x60, 0x55, 0x0A,
    0x70, 0x0D, 0x10, 0x00, 0xAB, 0x01, 0x02, 0x08, 0x02, 0x08,
    0xF2, 0x0B, 0x93, 0x0A, 0xB6, 0x04, 0x3E, 0x05, 0xB6, 0x04,
    0x3E, 0x05, 0xF2, 0x0B, 0x93, 0x0A, 0xB6, 0x04, 0x3E, 0x05,
    0xF2, 0x0B, 0x93, 0x0A, 0x7C, 0x06, 0x21, 0x06, 0xAA, 0x06,
    0x0F, 0xFC, 0xFF, 0x83, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x40, 0x22, 0x00, 0x00, 0x03, 0x00,
    0x00, 0x00, 0x8F, 0x0A, 0xBE, 0x0A, 0x15, 0x00, 0x91, 0x0A,
    0xBE, 0x0A, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x8F, 0x0A, 0x92, 0x0A, 0x7B, 0x02, 0xD2, 0x04, 0xD2, 0x04,
    0x68, 0x03, 0x09, 0x0B, 0x2A, 0x00
]

UNIT_MAPPING = {0: "μs", 1: "ms", 2: "s", 3: "min"}
DOC_MAPPING = {0: "4mV", 1: "8mV", 2: "16mV", 3: "24mV", 4: "32mV", 5: "48mV", 6: "64mV", 7: "96mV"}
COC_MAPPING = {0: "1mV", 1: "2mV", 2: "4mV", 3: "6mV", 4: "8mV", 5: "12mV", 6: "16mV", 7: "24mV"}
DSC_MAPPING = {0: "16mV", 1: "24mV", 2: "32mV", 3: "48mV", 4: "64mV", 5: "96mV", 6: "128mV", 7: "256mV"}

# Create a dictionary mapping binary patterns to connected cell counts
CELL_CONFIG_MAPPING = {
    0b10000011: 3, #3 cells
    0b11000011: 4, #4 cells
    0b11000111: 5, #5 cells
    0b11100111: 6, #6 cells
    0b11110111: 7, #7 cells
    0b11111111: 8  #8 cells
    }

#Create a dictionary mapping binary patterns current gains
CURRENT_GAIN_MAPPING = {
    0b00: 50,
    0b01: 5,
    0b10: 500,
    0b11: 500
    }