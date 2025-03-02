from .register_types import VoltageRegisterField
from .isl94203_constants import *

# Voltage Definitions
def voltage_cell_from_raw(value: int) -> float:
    return (value * VOLTAGE_CELL_MULTIPLIER)

def voltage_cell_to_raw(value: float) -> int:
    return int((value / VOLTAGE_CELL_MULTIPLIER))

map = [
    ("overvoltage_threshold", 0x00),
    ("overvoltage_recovery", 0x02),
    ("undervoltage_threshold", 0x04),
    ("undervoltage_recovery", 0x06),
    ("overvoltage_lockout", 0x08),
    ("undervoltage_lockout", 0x0A),
    ("end_of_charge_voltage", 0x0C),
    ("low_voltage_charge", 0x0E),
    ("sleep_voltage", 0x44),
]

reg = {}
for name, address in map:
    reg[name] = VoltageRegisterField(
        name=name,
        address=address,
        bit_mask=Mask.MASK_12BIT,
        bit_position=0,
        to_raw=voltage_cell_to_raw,
        from_raw=voltage_cell_from_raw,
    )

