from dataclasses import dataclass

from bms.isl94203_constants import ISL94203_MEMORY_SIZE, ISL94203_RAM_SIZE

ERROR_BYTE = 0x09
BOARD_TRIGGERED = 0x0A

# FMCW Commands
@dataclass
class Command:
    name: str
    code: int
    response_size: int
    description: str = ""

# Define all commands
COMMANDS = [
    Command(name="CMD_GET_DEVICE_STATUS", code=0x08, response_size=25, description="Get device status"),
    Command(name="CMD_START_CALIBRATION", code=0x0B, response_size=20, description="Start calibration"),
    Command(name="CMD_GET_BOOTLOADER_STATUS", code=0x0C, response_size=11, description="Get bootloader status"),
    Command(name="CMD_GET_SDCARD_STATUS", code=0x0D, response_size=20, description="Get SD card status"),
    Command(name="CMD_GET_REMOTE_STATUS", code=0x0E, response_size=26, description="Get remote status"),
    Command(name="CMD_START_FFT_MEAS_ANTENNA_1", code=0x10, response_size=483, description="Start FFT measurement on antenna 1"),
    Command(name="CMD_START_ADC_MEAS_ANTENNA_1", code=0x11, response_size=1027, description="Start ADC measurement on antenna 1"),
    Command(name="CMD_START_FFT_MEAS_ANTENNA_2", code=0x12, response_size=483, description="Start FFT measurement on antenna 2"),
    Command(name="CMD_START_ADC_MEAS_ANTENNA_2", code=0x13, response_size=1027, description="Start ADC measurement on antenna 2"),
    Command(name="CMD_START_FFT_MEAS_ANTENNA_3", code=0x14, response_size=483, description="Start FFT measurement on antenna 3"),
    Command(name="CMD_START_ADC_MEAS_ANTENNA_3", code=0x15, response_size=1027, description="Start ADC measurement on antenna 3"),
    Command(name="CMD_START_FFT_MEAS_ANTENNA_4", code=0x16, response_size=483, description="Start FFT measurement on antenna 4"),
    Command(name="CMD_START_ADC_MEAS_ANTENNA_4", code=0x17, response_size=1027, description="Start ADC measurement on antenna 4"),
    Command(name="CMD_SET_RTC_YEAR", code=0x18, response_size=0, description="Set RTC year"),
    Command(name="CMD_SET_RTC_MONTH", code=0x19, response_size=0, description="Set RTC month"),
    Command(name="CMD_SET_RTC_DAY", code=0x1A, response_size=0, description="Set RTC day"),
    Command(name="CMD_SET_RTC_DOW", code=0x1B, response_size=0, description="Set RTC day of week"),
    Command(name="CMD_SET_RTC_HOUR", code=0x1C, response_size=0, description="Set RTC hour"),
    Command(name="CMD_SET_RTC_MINUTE", code=0x1D, response_size=0, description="Set RTC minute"),
    Command(name="CMD_SET_RTC_SECOND", code=0x1E, response_size=0, description="Set RTC second"),
    Command(name="CMD_SET_RTC_CALIBRATION", code=0x1F, response_size=4, description="Set RTC calibration"),
    Command(name="CMD_DIGITAL_POTI_1", code=0x20, response_size=8, description="Set digital potentiometer 1"),
    Command(name="CMD_DIGITAL_POTI_2", code=0x21, response_size=8, description="Set digital potentiometer 2"),
    Command(name="CMD_DIGITAL_POTI_3", code=0x22, response_size=8, description="Set digital potentiometer 3"),
    Command(name="CMD_DIGITAL_POTI_4", code=0x23, response_size=8, description="Set digital potentiometer 4"),
    Command(name="CMD_FILTER_REQUEST", code=0x24, response_size=7, description="Request filter data"),
    Command(name="CMD_RESET_TUSB3410", code=0x28, response_size=2, description="Reset TUSB3410"),
    Command(name="CMD_RESET_ISM", code=0x29, response_size=2, description="Reset ISM module"),
    Command(name="CMD_RESET_RS485", code=0x2A, response_size=2, description="Reset RS485 module"),
    Command(name="CMD_RESET", code=0x2B, response_size=2, description="Reset system"),
    Command(name="CMD_TABLE_FIRST_ENTRY", code=0x30, response_size=32, description="Get first table entry"),
    Command(name="CMD_TABLE_ENTRY", code=0x31, response_size=32, description="Get table entry"),
    Command(name="CMD_TABLE_LAST_ENTRY", code=0x32, response_size=32, description="Get last table entry"),
    Command(name="CMD_MODEM_RSSI", code=0x38, response_size=0, description="Get modem RSSI"),
    Command(name="CMD_MODEM_TEMPERATURE", code=0x39, response_size=0, description="Get modem temperature"),
    Command(name="CMD_MODEM_BATTERY", code=0x3A, response_size=0, description="Get modem battery status"),
    Command(name="CMD_MODEM_AT_MONP", code=0x3B, response_size=0, description="Execute AT+MONP command"),
    Command(name="CMD_MODEM_AT_SMONC", code=0x3C, response_size=0, description="Execute AT+SMONC command"),
    Command(name="CMD_MODEM_TYPE", code=0x3D, response_size=0, description="Get modem type"),
    Command(name="CMD_MODEM_OPERATOR", code=0x3E, response_size=0, description="Get modem operator"),
    Command(name="CMD_VAR1_UINT32_1", code=0x40, response_size=0, description="Variable 1, uint32 part 1"),
    Command(name="CMD_VAR1_UINT32_2", code=0x41, response_size=0, description="Variable 1, uint32 part 2"),
    Command(name="CMD_VAR1_UINT32_3", code=0x42, response_size=0, description="Variable 1, uint32 part 3"),
    Command(name="CMD_VAR1_UINT32_4", code=0x43, response_size=0, description="Variable 1, uint32 part 4"),
    Command(name="CMD_VAR2_UINT32_1", code=0x44, response_size=0, description="Variable 2, uint32 part 1"),
    Command(name="CMD_VAR2_UINT32_2", code=0x45, response_size=0, description="Variable 2, uint32 part 2"),
    Command(name="CMD_VAR2_UINT32_3", code=0x46, response_size=0, description="Variable 2, uint32 part 3"),
    Command(name="CMD_VAR2_UINT32_4", code=0x47, response_size=0, description="Variable 2, uint32 part 4"),
    Command(name="CMD_LOG_OUT", code=0x48, response_size=2, description="Log out"),
    Command(name="CMD_LOG_IN", code=0x49, response_size=2, description="Log in"),
    Command(name="CMD_FW_UPGRADE", code=0x4A, response_size=64, description="Firmware upgrade"),
    Command(name="CMD_SDCARD_WRITE", code=0x4B, response_size=64, description="Write to SD card"),
    Command(name="CMD_SDCARD_READ", code=0x4C, response_size=64, description="Read from SD card"),
    Command(name="CMD_SDCARD_DELETE", code=0x4D, response_size=64, description="Delete from SD card"),
    Command(name="CMD_READ_ALL_MEMORY", code=0x51, response_size=ISL94203_MEMORY_SIZE+3, description="BMS - Read all memory ( EEPROM + RAM )"),
    Command(name="CMD_READ_EEPROM", code=0x52, response_size=ISL94203_RAM_SIZE + 3, description="BMS - Read EEPROM"),
    Command(name="CMD_WRITE_EEPROM", code=0x53, response_size=0, description="BMS - Write EEPROM"),
    Command(name="CMD_READ_RAM", code=0x54, response_size=ISL94203_RAM_SIZE + 3, description="BMS - Read RAM"),
    Command(name="CMD_WRITE_USER_EEPROM", code=0x55, response_size=64, description="BMS - Write user EEPROM"),
    Command(name="CMD_READ_USER_EEPROM", code=0x56, response_size=64, description="BMS - Read user EEPROM"),
    Command(name="CMD_WRITE_EEPROM_PERSISTENT", code=0x57, response_size=0, description="BMS - Write EEPROM Persistent"),
    Command(name="CMD_TEST", code=0xFF, response_size=1, description="Test command"),
]

def get_command_by_name(name: str) -> Command:
    """
    Retrieve a Command object by its name.
    """
    for command in COMMANDS:
        if command.name == name:
            return command
    raise ValueError(f"Command with name '{name}' not found")


def get_command_by_code(code: int) -> Command:
    """
    Retrieve a Command object by its code.
    """
    for command in COMMANDS:
        if command.code == code:
            return command
    raise ValueError(f"Command with code 0x{code:02X} not found")

if "__main__" == __name__:
    # Example usage
    for command in COMMANDS:
        print(f"Command Name: {command.name}, Code: {command.code}, Response Size: {command.response_size}, Description: {command.description}")