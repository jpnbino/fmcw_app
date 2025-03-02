
from .register_types import TimeRegisterField
from bms.isl94203_constants import *

map = [
    ("overvoltage_delay_timeout", 0x10, 0, Mask.MASK_8BIT , 10, Mask.MASK_2BIT),
    ("undervoltage_delay_timeout", 0x12,0, Mask.MASK_8BIT, 10, Mask.MASK_2BIT),
    ("open_wire_timeout", 0x14,0, Mask.MASK_8BIT, 10, Mask.MASK_1BIT),
    ("charge_detect_pulse_width", 0x00, 0, Mask.MASK_8BIT, 10, Mask.MASK_2BIT),
    ("load_detect_pulse_width", 0x04,  0, Mask.MASK_8BIT, 10, Mask.MASK_2BIT),
]


"""Voltage Timing Definitions"""
reg = {}
for name, address, bit_position, bit_mask, unit_bit_position, unit_bit_mask in map:
    reg[name] = TimeRegisterField(
        name=name,
        address=address,
        bit_mask=bit_mask,
        bit_position=bit_position,
        unit_bit_mask=unit_bit_mask,
        unit_bit_position=unit_bit_position,
        to_raw= lambda x: x,
        from_raw = lambda x: x,
        unit_mapping=UNIT_MAPPING
    )
