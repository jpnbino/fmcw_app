
from .register_types import TimeRegisterField
from bms.isl94203_constants import *

"""Voltage Timing Definitions"""
overvoltage_delay_timeout = TimeRegisterField(
    name="overvoltage_delay_timeout",
    address=0x10,
    bit_length=8,
    bit_position=0,
    unit_bit_length=2,
    unit_bit_position=10,
    mapping= UNIT_MAPPING,
    to_raw= lambda x: x,
    from_raw = lambda x: x,
)

undervoltage_delay_timeout = TimeRegisterField(
    name="undervoltage_delay_timeout",
    address=0x12,
    bit_length=8,
    bit_position=0,
    unit_bit_length=2,
    unit_bit_position=10,
    mapping= UNIT_MAPPING,
    to_raw= lambda x: x,
    from_raw = lambda x: x,
)

open_wire_timing = TimeRegisterField(
    name="open_wire_timing",
    address=0x14,
    bit_length=8,
    bit_position=0,
    unit_bit_length=1,
    unit_bit_position=10,
    mapping= UNIT_MAPPING,
    to_raw= lambda x: x,
    from_raw = lambda x: x,
)