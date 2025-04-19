
from bms.cfg_current_limits_registers import unit_from_raw, unit_to_raw
from .register_types import TimeRegisterField, TimeUnitRegisterField
from bms.isl94203_constants import *

map = [
    ("overvoltage_delay_timeout", 0x10, 0, Mask.MASK_10BIT, 10, Mask.MASK_2BIT),
    ("undervoltage_delay_timeout", 0x12, 0, Mask.MASK_10BIT, 10, Mask.MASK_2BIT),
    ("open_wire_timeout", 0x14, 0, Mask.MASK_9BIT, 9, Mask.MASK_1BIT),
    ("sleep_delay", 0x46, 0, Mask.MASK_9BIT, 9, Mask.MASK_2BIT),
]

"""Voltage Timing Definitions"""
reg = {}
for name, address, bit_position, bit_mask, unit_bit_position, unit_bit_mask in map:
    reg[name] = TimeRegisterField(
        name=name,
        address=address,
        bit_mask=bit_mask,
        bit_position=bit_position,
        to_raw= lambda x: x,
        from_raw = lambda x: x,
        unit="ms"
    )
    reg[f"{name}_unit"] = TimeUnitRegisterField(
        name=name,
        address=address,
        bit_mask=unit_bit_mask,
        bit_position=unit_bit_position,
        to_raw= unit_to_raw,
        from_raw = unit_from_raw,
        unit_mapping= UNIT_MAPPING,
        unit = "ms"
    )

pulse_width_map = [
    ("charge_detect_pulse_width", 0x00, 12, Mask.MASK_4BIT),
    ("load_detect_pulse_width", 0x04,  12, Mask.MASK_2BIT),
]

for name, address, bit_position, bit_mask in pulse_width_map:
    reg[name] = TimeRegisterField(
        name=name,
        address=address,
        bit_mask=bit_mask,
        bit_position=bit_position,
        to_raw= lambda x: x,
        from_raw = lambda x: x,
        unit = "ms"
    )
    