from .register_types import VoltageRegisterField
from .isl94203_constants import *

# Voltage Definitions
def voltage_cell_from_raw(value: int) -> float:
    return (value * VOLTAGE_CELL_MULTIPLIER)

def voltage_cell_to_raw(value: float) -> int:
    return int((value / VOLTAGE_CELL_MULTIPLIER))

overvoltage_threshold = VoltageRegisterField(
    name="overvoltage_threshold",
    address=0x00,
    bit_length=12,
    bit_position=0,
    to_raw= voltage_cell_to_raw,
    from_raw = voltage_cell_from_raw,
)

overvoltage_recovery = VoltageRegisterField(
    name="overvoltage_recovery",
    address=0x02,
    bit_length=12,
    bit_position=0,
    to_raw= voltage_cell_to_raw,
    from_raw = voltage_cell_from_raw,
)

undervoltage_threshold = VoltageRegisterField(
    name="undervoltage_threshold",
    address=0x04,
    bit_length=12,
    bit_position=0,
    to_raw= voltage_cell_to_raw,
    from_raw = voltage_cell_from_raw,
)

undervoltage_recovery = VoltageRegisterField(
    name="undervoltage_recovery",
    address=0x06,
    bit_length=12,
    bit_position=0,
    to_raw= voltage_cell_to_raw,
    from_raw = voltage_cell_from_raw,
)

overvoltage_lockout = VoltageRegisterField(
    name="overvoltage_lockout",
    address=0x08,
    bit_length=12,
    bit_position=0,
    to_raw= voltage_cell_to_raw,
    from_raw = voltage_cell_from_raw,
)

undervoltage_lockout = VoltageRegisterField(	
    name="undervoltage_lockout",
    address=0x0A,
    bit_length=12,
    bit_position=0,
    to_raw= voltage_cell_to_raw,
    from_raw = voltage_cell_from_raw,
)

eoc_voltage = VoltageRegisterField(
    name="end_of_charge_voltage",
    address=0x0C,
    bit_length=12,
    bit_position=0,
    to_raw= voltage_cell_to_raw,
    from_raw = voltage_cell_from_raw,
)

low_voltage_charge = VoltageRegisterField(
    name="low_voltage_charge",
    address=0x0E,
    bit_length=12,
    bit_position=0,
    to_raw= voltage_cell_to_raw,
    from_raw = voltage_cell_from_raw,
)

sleep_voltage = VoltageRegisterField(
    name="sleep_voltage",
    address=0x10,
    bit_length=12,
    bit_position=0,
    to_raw= voltage_cell_to_raw,
    from_raw = voltage_cell_from_raw,
)
